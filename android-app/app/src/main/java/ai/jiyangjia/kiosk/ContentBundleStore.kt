package ai.jiyangjia.kiosk

import android.content.Context
import java.io.File
import java.io.FileOutputStream

class ContentBundleStore(context: Context) {
    private val root = File(context.filesDir, "content-bundles").apply { mkdirs() }
    private val preferences = context.getSharedPreferences("content_bundle_state", Context.MODE_PRIVATE)

    fun prepare(bundle: ContentBundle): File {
        val staging = File(root, "${safeVersion(bundle.bundleVersion)}.staging")
        staging.deleteRecursively()
        check(staging.mkdirs()) { "Unable to create staging directory" }
        return staging
    }

    fun assetFile(staging: File, descriptor: AssetDescriptor): File {
        val suffix = when (descriptor.type) {
            "video" -> ".mp4"
            else -> if (descriptor.contentType.contains("png", ignoreCase = true)) ".png" else ".jpg"
        }
        return File(staging, "${descriptor.type}$suffix")
    }

    fun activate(bundle: ContentBundle, staging: File): CachedContentBundle {
        writeDurable(File(staging, METADATA_FILE), bundle.toJson().toString().toByteArray(Charsets.UTF_8))
        val finalDirectory = File(root, safeVersion(bundle.bundleVersion))
        if (!finalDirectory.exists()) {
            check(staging.renameTo(finalDirectory)) { "Unable to activate staged bundle" }
        } else {
            staging.deleteRecursively()
        }
        val prior = preferences.getString(KEY_ACTIVE, null)
        check(preferences.edit().putString(KEY_PREVIOUS, prior).putString(KEY_ACTIVE, bundle.bundleVersion).commit()) {
            "Unable to persist active bundle pointer"
        }
        removeExpiredBundles(bundle.bundleVersion, prior)
        return read(bundle.bundleVersion) ?: error("Activated bundle is unreadable")
    }

    fun active(): CachedContentBundle? = preferences.getString(KEY_ACTIVE, null)?.let(::read)

    fun rollback(failedVersion: String, reason: String): CachedContentBundle? {
        val previous = preferences.getString(KEY_PREVIOUS, null) ?: return null
        val current = preferences.getString(KEY_ACTIVE, null)
        File(root, "rollback-${System.currentTimeMillis()}.txt").writeText(
            "failed_version=${safeVersion(failedVersion)}\nreason=${reason.take(200)}\n",
            Charsets.UTF_8
        )
        preferences.edit().putString(KEY_ACTIVE, previous).remove(KEY_PREVIOUS).commit()
        if (current != null && current != previous) {
            File(root, safeVersion(current)).renameTo(File(root, "${safeVersion(current)}.failed"))
        }
        return read(previous)
    }

    private fun read(version: String): CachedContentBundle? {
        val directory = File(root, safeVersion(version))
        val metadata = File(directory, METADATA_FILE)
        if (!metadata.isFile) return null
        return runCatching {
            val bundle = ContentBundle.fromStored(org.json.JSONObject(metadata.readText(Charsets.UTF_8)))
            CachedContentBundle(
                bundle = bundle,
                directory = directory,
                videoFile = bundle.video?.let { assetFile(directory, it).takeIf(File::isFile) },
                backgroundFile = bundle.background?.let { assetFile(directory, it).takeIf(File::isFile) }
            )
        }.getOrNull()
    }

    private fun removeExpiredBundles(active: String, previous: String?) {
        root.listFiles()?.filter { it.isDirectory && !it.name.endsWith(".staging") }
            ?.filterNot { it.name == safeVersion(active) || it.name == previous?.let(::safeVersion) }
            ?.forEach { it.deleteRecursively() }
    }

    private fun safeVersion(value: String): String = value.uppercase().replace(Regex("[^A-F0-9]"), "").take(64)

    companion object {
        private const val METADATA_FILE = "bundle.json"
        private const val KEY_ACTIVE = "active_version"
        private const val KEY_PREVIOUS = "previous_version"

        fun writeDurable(target: File, bytes: ByteArray) {
            FileOutputStream(target).use { output ->
                output.write(bytes)
                output.fd.sync()
            }
        }
    }
}
