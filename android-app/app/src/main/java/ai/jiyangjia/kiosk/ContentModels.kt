package ai.jiyangjia.kiosk

import org.json.JSONObject

data class AssetDescriptor(
    val id: String,
    val type: String,
    val url: String,
    val version: String,
    val contentType: String,
    val sizeBytes: Long,
    val sha256: String
) {
    init {
        require(type in setOf("video", "image"))
        require(url.isNotBlank())
        require(sizeBytes in 1..MAX_ASSET_BYTES)
        require(SHA256_REGEX.matches(sha256))
    }

    fun toJson(): JSONObject = JSONObject()
        .put("id", id)
        .put("type", type)
        .put("url", url)
        .put("version", version)
        .put("content_type", contentType)
        .put("size_bytes", sizeBytes)
        .put("sha256", sha256)

    companion object {
        const val MAX_ASSET_BYTES = 250L * 1024L * 1024L
        private val SHA256_REGEX = Regex("^[A-Fa-f0-9]{64}$")

        fun fromJson(type: String, payload: JSONObject?): AssetDescriptor? {
            if (payload == null) return null
            return AssetDescriptor(
                id = payload.optString("avatar_id", payload.optString("id")),
                type = type,
                url = payload.optString("url", payload.optString("uri")),
                version = payload.optString("version"),
                contentType = payload.optString("content_type"),
                sizeBytes = payload.optLong("size_bytes"),
                sha256 = payload.optString("sha256").uppercase()
            )
        }
    }
}

data class DisplayProfileConfig(
    val profileId: String,
    val widthPx: Int,
    val heightPx: Int,
    val orientation: String,
    val scaleMode: String,
    val characterAnchorX: Float,
    val characterAnchorY: Float,
    val characterScale: Float,
    val subtitleSafeLeft: Float,
    val subtitleSafeRight: Float,
    val subtitleSafeBottom: Float,
    val subtitleFontPx: Int,
    val consultButtonX: Float,
    val consultButtonY: Float
) {
    init {
        require(widthPx >= 320 && heightPx >= 320)
        require(orientation in setOf("portrait", "landscape"))
        require(scaleMode in setOf("fit", "fill", "crop"))
        require(characterAnchorX in 0f..1f && characterAnchorY in 0f..1f)
        require(characterScale in 0.1f..5f)
        require(subtitleSafeLeft in 0f..1f && subtitleSafeRight in 0f..1f && subtitleSafeBottom in 0f..1f)
        require(consultButtonX in 0f..1f && consultButtonY in 0f..1f)
    }

    fun toJson(): JSONObject = JSONObject()
        .put("profile_id", profileId)
        .put("width_px", widthPx)
        .put("height_px", heightPx)
        .put("orientation", orientation)
        .put("scale_mode", scaleMode)
        .put("character_anchor_x", characterAnchorX)
        .put("character_anchor_y", characterAnchorY)
        .put("character_scale", characterScale)
        .put("subtitle_safe_area", JSONObject().put("left", subtitleSafeLeft).put("right", subtitleSafeRight).put("bottom", subtitleSafeBottom))
        .put("subtitle_font_px", subtitleFontPx)
        .put("button_positions", JSONObject().put("consult", JSONObject().put("x", consultButtonX).put("y", consultButtonY)))

    companion object {
        fun fromJson(payload: JSONObject): DisplayProfileConfig {
            val safe = payload.optJSONObject("subtitle_safe_area") ?: JSONObject()
            val consult = payload.optJSONObject("button_positions")?.optJSONObject("consult") ?: JSONObject()
            return DisplayProfileConfig(
                profileId = payload.getString("profile_id"),
                widthPx = payload.getInt("width_px"),
                heightPx = payload.getInt("height_px"),
                orientation = payload.getString("orientation"),
                scaleMode = payload.optString("scale_mode", "fit"),
                characterAnchorX = payload.optDouble("character_anchor_x", 0.5).toFloat(),
                characterAnchorY = payload.optDouble("character_anchor_y", 0.5).toFloat(),
                characterScale = payload.optDouble("character_scale", 1.0).toFloat(),
                subtitleSafeLeft = safe.optDouble("left", 0.08).toFloat(),
                subtitleSafeRight = safe.optDouble("right", 0.08).toFloat(),
                subtitleSafeBottom = safe.optDouble("bottom", 0.08).toFloat(),
                subtitleFontPx = payload.optInt("subtitle_font_px", 36),
                consultButtonX = consult.optDouble("x", 0.5).toFloat(),
                consultButtonY = consult.optDouble("y", 0.88).toFloat()
            )
        }
    }
}

data class ContentBundle(
    val bundleVersion: String,
    val refreshIntervalSeconds: Long,
    val minimumVersionCode: Int,
    val profile: DisplayProfileConfig,
    val video: AssetDescriptor?,
    val background: AssetDescriptor?
) {
    init {
        require(Regex("^[A-Fa-f0-9]{64}$").matches(bundleVersion))
        require(refreshIntervalSeconds in 15..3600)
        require(minimumVersionCode >= 1)
    }

    fun toJson(): JSONObject = JSONObject()
        .put("bundle_version", bundleVersion)
        .put("refresh_interval_seconds", refreshIntervalSeconds)
        .put("minimum_version_code", minimumVersionCode)
        .put("display_profile", profile.toJson())
        .put("video", video?.toJson())
        .put("background", background?.toJson())

    companion object {
        fun fromBootstrap(payload: JSONObject): ContentBundle {
            val config = payload.getJSONObject("config")
            val manifest = payload.getJSONObject("assets_manifest")
            return ContentBundle(
                bundleVersion = payload.getString("bundle_version").uppercase(),
                refreshIntervalSeconds = config.optLong("refresh_interval_seconds", 60),
                minimumVersionCode = config.optInt("minimum_version_code", 1),
                profile = DisplayProfileConfig.fromJson(payload.getJSONObject("display_profile")),
                video = AssetDescriptor.fromJson("video", manifest.optJSONObject("video")),
                background = AssetDescriptor.fromJson("image", manifest.optJSONObject("background"))
            )
        }

        fun fromStored(payload: JSONObject): ContentBundle = ContentBundle(
            bundleVersion = payload.getString("bundle_version"),
            refreshIntervalSeconds = payload.getLong("refresh_interval_seconds"),
            minimumVersionCode = payload.getInt("minimum_version_code"),
            profile = DisplayProfileConfig.fromJson(payload.getJSONObject("display_profile")),
            video = AssetDescriptor.fromJson("video", payload.optJSONObject("video")),
            background = AssetDescriptor.fromJson("image", payload.optJSONObject("background"))
        )
    }
}

data class CachedContentBundle(
    val bundle: ContentBundle,
    val directory: java.io.File,
    val videoFile: java.io.File?,
    val backgroundFile: java.io.File?
)
