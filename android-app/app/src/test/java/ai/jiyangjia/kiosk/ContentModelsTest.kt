package ai.jiyangjia.kiosk

import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class ContentModelsTest {
    @Test
    fun parsesVersionedBootstrapAndProfileGeometry() {
        val hash = "A".repeat(64)
        val payload = JSONObject(
            """
            {
              "bundle_version":"$hash",
              "config":{"refresh_interval_seconds":60,"minimum_version_code":1},
              "display_profile":{
                "profile_id":"display-1080x1920","width_px":1080,"height_px":1920,
                "orientation":"portrait","scale_mode":"crop","character_anchor_x":0.62,
                "character_anchor_y":0.48,"character_scale":1.1,
                "subtitle_safe_area":{"left":0.1,"right":0.1,"bottom":0.12},
                "subtitle_font_px":44,"button_positions":{"consult":{"x":0.5,"y":0.9}}
              },
              "assets_manifest":{
                "video":{"avatar_id":"asset_1","url":"/api/v1/assets/asset_1","version":"v1","content_type":"video/mp4","size_bytes":12,"sha256":"$hash"},
                "background":null
              }
            }
            """.trimIndent()
        )

        val bundle = ContentBundle.fromBootstrap(payload)

        assertEquals(60, bundle.refreshIntervalSeconds)
        assertEquals("crop", bundle.profile.scaleMode)
        assertEquals(0.62f, bundle.profile.characterAnchorX)
        assertEquals("asset_1", bundle.video?.id)
        assertNull(bundle.background)
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejectsInvalidAssetHash() {
        AssetDescriptor("asset", "video", "/asset", "v1", "video/mp4", 12, "bad")
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejectsPartialAssetAfterDownload() {
        val hash = "A".repeat(64)
        val asset = AssetDescriptor("asset", "video", "/asset", "v1", "video/mp4", 12, hash)
        ContentSyncManager.verifyAssetIntegrity(11, hash, asset)
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejectsBadHashAfterDownload() {
        val hash = "A".repeat(64)
        val asset = AssetDescriptor("asset", "video", "/asset", "v1", "video/mp4", 12, hash)
        ContentSyncManager.verifyAssetIntegrity(12, "B".repeat(64), asset)
    }
}
