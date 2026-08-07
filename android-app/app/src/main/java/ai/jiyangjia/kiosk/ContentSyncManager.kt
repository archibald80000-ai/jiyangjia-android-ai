package ai.jiyangjia.kiosk

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.os.Handler
import android.os.Looper
import androidx.work.BackoffPolicy
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.File
import java.io.FileOutputStream
import java.security.MessageDigest
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledFuture
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

sealed class ContentSyncResult {
    data class Activated(val bundle: CachedContentBundle) : ContentSyncResult()
    data class Unchanged(val bundle: CachedContentBundle?) : ContentSyncResult()
    data class Failed(val reason: String, val cached: CachedContentBundle?) : ContentSyncResult()
}

class ContentSyncManager(
    context: Context,
    private val baseUrl: () -> String,
    private val metrics: () -> Triple<Int, Int, String>,
    private val onResult: (ContentSyncResult) -> Unit,
    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(5, TimeUnit.SECONDS)
        .readTimeout(45, TimeUnit.SECONDS)
        .build()
) {
    private val appContext = context.applicationContext
    private val store = ContentBundleStore(appContext)
    private val preferences = appContext.getSharedPreferences("content_sync_http", Context.MODE_PRIVATE)
    private val executor = Executors.newSingleThreadScheduledExecutor { runnable ->
        Thread(runnable, "kiosk-content-sync").apply { isDaemon = true }
    }
    private val mainHandler = Handler(Looper.getMainLooper())
    private val running = AtomicBoolean(false)
    private val syncInFlight = AtomicBoolean(false)
    private var polling: ScheduledFuture<*>? = null
    private var networkCallback: ConnectivityManager.NetworkCallback? = null

    fun cachedBundle(): CachedContentBundle? = store.active()

    fun startForeground() {
        if (!running.compareAndSet(false, true)) return
        syncAsync()
        polling = executor.scheduleWithFixedDelay(::syncAsync, 60, 60, TimeUnit.SECONDS)
        val manager = appContext.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val callback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                syncAsync()
            }
        }
        networkCallback = callback
        val request = NetworkRequest.Builder()
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .build()
        runCatching { manager.registerNetworkCallback(request, callback) }
    }

    fun stopForeground() {
        running.set(false)
        polling?.cancel(false)
        polling = null
        val manager = appContext.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        networkCallback?.let { runCatching { manager.unregisterNetworkCallback(it) } }
        networkCallback = null
    }

    fun rollback(failedVersion: String, reason: String): CachedContentBundle? = store.rollback(failedVersion, reason)

    fun syncAsync() {
        if (!syncInFlight.compareAndSet(false, true)) return
        executor.execute {
            val result = try {
                syncOnce()
            } catch (error: Throwable) {
                scheduleRecovery()
                ContentSyncResult.Failed(error.message ?: error.javaClass.simpleName, store.active())
            } finally {
                syncInFlight.set(false)
            }
            mainHandler.post { onResult(result) }
        }
    }

    internal fun syncOnce(): ContentSyncResult {
        val root = baseUrl().trim().trimEnd('/')
        if (root.isBlank()) return ContentSyncResult.Failed("Gateway bootstrap URL is not configured", store.active())
        if (!BuildConfig.ALLOW_CLEARTEXT_GATEWAY && !root.startsWith("https://")) {
            return ContentSyncResult.Failed("Release gateway URL must use HTTPS", store.active())
        }
        val parsed = root.toHttpUrlOrNull() ?: return ContentSyncResult.Failed("Invalid gateway URL", store.active())
        val (width, height, orientation) = metrics()
        val bootstrapUrl = parsed.newBuilder()
            .addPathSegments("api/v1/client/bootstrap")
            .addQueryParameter("width", width.toString())
            .addQueryParameter("height", height.toString())
            .addQueryParameter("orientation", orientation)
            .addQueryParameter("version_code", BuildConfig.VERSION_CODE.toString())
            .build()
        val request = Request.Builder().url(bootstrapUrl).apply {
            preferences.getString(KEY_ETAG, null)?.let { header("If-None-Match", it) }
        }.build()
        client.newCall(request).execute().use { response ->
            if (response.code == 304) return ContentSyncResult.Unchanged(store.active())
            if (!response.isSuccessful) error("Bootstrap HTTP ${response.code}")
            val body = response.body?.string() ?: error("Bootstrap response is empty")
            if (body.length > MAX_BOOTSTRAP_CHARS) error("Bootstrap response is too large")
            val bundle = ContentBundle.fromBootstrap(JSONObject(body))
            if (bundle.minimumVersionCode > BuildConfig.VERSION_CODE) error("Client update is required")
            val active = store.active()
            if (active?.bundle?.bundleVersion == bundle.bundleVersion) {
                response.header("ETag")?.let { preferences.edit().putString(KEY_ETAG, it).apply() }
                return ContentSyncResult.Unchanged(active)
            }
            val staging = store.prepare(bundle)
            try {
                bundle.video?.let { downloadAsset(root, it, store.assetFile(staging, it)) }
                bundle.background?.let { downloadAsset(root, it, store.assetFile(staging, it)) }
                val activated = store.activate(bundle, staging)
                response.header("ETag")?.let { preferences.edit().putString(KEY_ETAG, it).commit() }
                return ContentSyncResult.Activated(activated)
            } catch (error: Throwable) {
                staging.deleteRecursively()
                throw error
            }
        }
    }

    private fun downloadAsset(root: String, descriptor: AssetDescriptor, target: File) {
        val resolved = root.toHttpUrlOrNull()?.resolve(descriptor.url) ?: error("Invalid asset URL")
        if (!BuildConfig.ALLOW_CLEARTEXT_GATEWAY && !resolved.isHttps) error("Release asset URL must use HTTPS")
        val request = Request.Builder().url(resolved).build()
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) error("Asset HTTP ${response.code}")
            val contentType = response.header("Content-Type").orEmpty().substringBefore(';').lowercase()
            if (contentType != descriptor.contentType.lowercase()) error("Asset content type mismatch")
            val advertised = response.body?.contentLength() ?: -1
            if (advertised > descriptor.sizeBytes || advertised > AssetDescriptor.MAX_ASSET_BYTES) error("Asset exceeds declared size")
            val digest = MessageDigest.getInstance("SHA-256")
            var total = 0L
            FileOutputStream(target).use { output ->
                val input = response.body?.byteStream() ?: error("Asset response is empty")
                val buffer = ByteArray(8192)
                while (true) {
                    val count = input.read(buffer)
                    if (count < 0) break
                    total += count
                    if (total > descriptor.sizeBytes || total > AssetDescriptor.MAX_ASSET_BYTES) error("Asset download exceeded limit")
                    digest.update(buffer, 0, count)
                    output.write(buffer, 0, count)
                }
                output.fd.sync()
            }
            val actual = digest.digest().joinToString("") { "%02X".format(it) }
            verifyAssetIntegrity(total, actual, descriptor)
        }
    }

    private fun scheduleRecovery() {
        val request = OneTimeWorkRequestBuilder<ContentSyncWorker>()
            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
            .build()
        WorkManager.getInstance(appContext).enqueueUniqueWork(WORK_NAME, ExistingWorkPolicy.KEEP, request)
    }

    companion object {
        private const val KEY_ETAG = "bootstrap_etag"
        private const val WORK_NAME = "jiyangjia-content-sync-recovery"
        private const val MAX_BOOTSTRAP_CHARS = 1024 * 1024

        internal fun verifyAssetIntegrity(total: Long, actualSha256: String, descriptor: AssetDescriptor) {
            require(total == descriptor.sizeBytes) { "Asset size mismatch" }
            require(actualSha256.equals(descriptor.sha256, ignoreCase = true)) { "Asset SHA-256 mismatch" }
        }
    }
}
