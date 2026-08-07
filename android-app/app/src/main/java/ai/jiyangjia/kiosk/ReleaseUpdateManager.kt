package ai.jiyangjia.kiosk

import android.app.PendingIntent
import android.app.admin.DevicePolicyManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInstaller
import android.content.pm.PackageManager
import android.os.Build
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.File
import java.io.FileInputStream
import java.security.MessageDigest
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicBoolean

data class ReleaseDescriptor(
    val packageName: String,
    val versionCode: Long,
    val versionName: String,
    val apkUrl: String,
    val sizeBytes: Long,
    val sha256: String,
    val certificateSha256: String,
    val releaseNotes: String
) {
    companion object {
        fun parse(json: JSONObject): ReleaseDescriptor = ReleaseDescriptor(
            packageName = json.getString("package"),
            versionCode = json.getLong("version_code"),
            versionName = json.getString("version_name"),
            apkUrl = json.getString("apk_url"),
            sizeBytes = json.getLong("size_bytes"),
            sha256 = normalizeDigest(json.getString("sha256")),
            certificateSha256 = normalizeDigest(json.getString("signing_certificate_sha256")),
            releaseNotes = json.optString("release_notes")
        )
    }
}

data class ApkIdentity(val packageName: String, val versionCode: Long, val certificateSha256: String)

object ReleasePolicy {
    fun validateDescriptor(release: ReleaseDescriptor) {
        require(release.apkUrl.startsWith("https://")) { "release APK must use HTTPS" }
        require(release.packageName == "ai.jiyangjia.kiosk") { "release package mismatch" }
        require(release.versionCode > 0) { "invalid release versionCode" }
        require(release.sizeBytes in 1..MAX_APK_BYTES) { "invalid release APK size" }
        require(release.sha256.matches(Regex("[A-F0-9]{64}"))) { "invalid APK SHA-256" }
        require(release.certificateSha256.matches(Regex("[A-F0-9]{64}"))) { "invalid certificate SHA-256" }
    }

    fun validate(
        release: ReleaseDescriptor,
        downloadedSize: Long,
        downloadedSha256: String,
        apk: ApkIdentity,
        installedVersionCode: Long,
        installedCertificateSha256: String
    ) {
        validateDescriptor(release)
        require(downloadedSize == release.sizeBytes) { "APK size mismatch" }
        require(normalizeDigest(downloadedSha256) == release.sha256) { "APK SHA-256 mismatch" }
        require(apk.packageName == "ai.jiyangjia.kiosk" && apk.packageName == release.packageName) { "APK package mismatch" }
        require(apk.versionCode == release.versionCode && apk.versionCode > installedVersionCode) { "APK versionCode is not newer" }
        require(normalizeDigest(apk.certificateSha256) == release.certificateSha256) { "release certificate mismatch" }
        require(normalizeDigest(apk.certificateSha256) == normalizeDigest(installedCertificateSha256)) { "installed certificate mismatch" }
    }

    private const val MAX_APK_BYTES = 250L * 1024L * 1024L
}

class ReleaseUpdateManager(
    private val context: Context,
    private val baseUrl: () -> String,
    private val onStatus: (String) -> Unit
) {
    private val executor = Executors.newSingleThreadExecutor()
    private val running = AtomicBoolean(false)
    private val client = OkHttpClient()

    fun checkAndInstall() {
        if (BuildConfig.DEBUG || !running.compareAndSet(false, true)) return
        executor.execute {
            try {
                val release = fetchManifest()
                ReleasePolicy.validateDescriptor(release)
                val installed = installedIdentity()
                if (release.versionCode <= installed.versionCode) {
                    onStatus("Release current: ${installed.versionCode}")
                    return@execute
                }
                val apk = download(release)
                try {
                    val candidate = inspectApk(apk)
                    ReleasePolicy.validate(
                        release, apk.length(), sha256(apk), candidate, installed.versionCode, installed.certificateSha256
                    )
                    install(apk, release.packageName)
                    onStatus("Verified update submitted: ${release.versionCode}")
                } finally {
                    apk.delete()
                }
            } catch (error: Throwable) {
                onStatus("Update retained current version: ${error.message?.take(100)}")
            } finally {
                running.set(false)
            }
        }
    }

    private fun fetchManifest(): ReleaseDescriptor {
        val url = baseUrl().trimEnd('/') + "/api/v1/client/release"
        val response = client.newCall(Request.Builder().url(url).build()).execute()
        response.use {
            check(it.isSuccessful) { "release manifest HTTP ${it.code}" }
            return ReleaseDescriptor.parse(JSONObject(it.body?.string().orEmpty()))
        }
    }

    private fun download(release: ReleaseDescriptor): File {
        val target = File(context.cacheDir, "release-${release.versionCode}.apk.tmp")
        try {
            val response = client.newCall(Request.Builder().url(release.apkUrl).build()).execute()
            response.use {
                check(it.isSuccessful) { "APK download HTTP ${it.code}" }
                val body = checkNotNull(it.body) { "empty APK response" }
                if (body.contentLength() >= 0) check(body.contentLength() == release.sizeBytes) { "APK content length mismatch" }
                body.byteStream().use { input ->
                    target.outputStream().use { output ->
                        val buffer = ByteArray(8192)
                        var total = 0L
                        while (true) {
                            val read = input.read(buffer)
                            if (read < 0) break
                            total += read
                            check(total <= release.sizeBytes) { "APK exceeds declared size" }
                            output.write(buffer, 0, read)
                        }
                    }
                }
            }
            return target
        } catch (error: Throwable) {
            target.delete()
            throw error
        }
    }

    @Suppress("DEPRECATION")
    private fun inspectApk(file: File): ApkIdentity {
        val flags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) PackageManager.GET_SIGNING_CERTIFICATES else PackageManager.GET_SIGNATURES
        val info = checkNotNull(context.packageManager.getPackageArchiveInfo(file.absolutePath, flags)) { "invalid APK" }
        val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) info.signingInfo?.apkContentsSigners else info.signatures
        val certificate = checkNotNull(signatures?.firstOrNull()) { "APK has no signing certificate" }
        return ApkIdentity(info.packageName, packageVersionCode(info), digest(certificate.toByteArray()))
    }

    @Suppress("DEPRECATION")
    private fun installedIdentity(): ApkIdentity {
        val flags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) PackageManager.GET_SIGNING_CERTIFICATES else PackageManager.GET_SIGNATURES
        val info = context.packageManager.getPackageInfo(context.packageName, flags)
        val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) info.signingInfo?.apkContentsSigners else info.signatures
        check(!signatures.isNullOrEmpty()) { "installed package has no signing certificate" }
        return ApkIdentity(info.packageName, packageVersionCode(info), digest(signatures.first().toByteArray()))
    }

    private fun install(apk: File, packageName: String) {
        val installer = context.packageManager.packageInstaller
        val params = PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL).apply {
            setAppPackageName(packageName)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val policy = context.getSystemService(Context.DEVICE_POLICY_SERVICE) as DevicePolicyManager
                if (policy.isDeviceOwnerApp(context.packageName)) setRequireUserAction(PackageInstaller.SessionParams.USER_ACTION_NOT_REQUIRED)
            }
        }
        val sessionId = installer.createSession(params)
        installer.openSession(sessionId).use { session ->
            FileInputStream(apk).use { input ->
                session.openWrite("base.apk", 0, apk.length()).use { output -> input.copyTo(output); session.fsync(output) }
            }
            val callback = PendingIntent.getBroadcast(
                context,
                sessionId,
                Intent(context, UpdateInstallReceiver::class.java),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_MUTABLE
            )
            session.commit(callback.intentSender)
        }
    }
}

private fun normalizeDigest(value: String): String = value.replace(":", "").trim().uppercase()
@Suppress("DEPRECATION")
private fun packageVersionCode(info: android.content.pm.PackageInfo): Long =
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) info.longVersionCode else info.versionCode.toLong()
private fun digest(bytes: ByteArray): String = MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02X".format(it) }
private fun sha256(file: File): String = file.inputStream().use { input ->
    val hash = MessageDigest.getInstance("SHA-256")
    val buffer = ByteArray(8192)
    while (true) {
        val read = input.read(buffer)
        if (read < 0) break
        hash.update(buffer, 0, read)
    }
    hash.digest().joinToString("") { "%02X".format(it) }
}
