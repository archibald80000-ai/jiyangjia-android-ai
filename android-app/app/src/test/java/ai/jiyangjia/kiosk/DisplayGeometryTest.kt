package ai.jiyangjia.kiosk

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.math.roundToInt

class DisplayGeometryTest {
    @Test
    fun resolvesPortraitLandscapeAndCustomProfiles() {
        val cases = listOf(
            Triple(1080, 1920, profile(1080, 1920, "portrait")),
            Triple(1920, 1080, profile(1920, 1080, "landscape")),
            Triple(1280, 720, profile(1280, 720, "landscape")),
            Triple(1600, 900, profile(1600, 900, "landscape", scale = 1.1f, anchorX = 0.62f))
        )

        cases.forEach { (width, height, profile) ->
            val resolved = DisplayGeometry.compute(width, height, profile)
            assertEquals((width * profile.characterScale).roundToInt(), resolved.characterWidth)
            assertEquals((height * 0.12f).roundToInt(), resolved.subtitleBottom)
            assertEquals(width * 0.5f, resolved.buttonCenterX)
            assertTrue(resolved.subtitleWidth > 0)
        }
    }

    @Test
    fun normalizedAnchorControlsCharacterCenter() {
        val profile = profile(1000, 500, "landscape", scale = 0.5f, anchorX = 0.75f)
        val resolved = DisplayGeometry.compute(1000, 500, profile)

        assertEquals(500, resolved.characterWidth)
        assertEquals(500, resolved.characterLeft)
        assertEquals(250, resolved.characterHeight)
    }

    private fun profile(
        width: Int,
        height: Int,
        orientation: String,
        scale: Float = 1f,
        anchorX: Float = 0.5f
    ) = DisplayProfileConfig(
        profileId = "$width-$height",
        widthPx = width,
        heightPx = height,
        orientation = orientation,
        scaleMode = "fit",
        characterAnchorX = anchorX,
        characterAnchorY = 0.5f,
        characterScale = scale,
        subtitleSafeLeft = 0.1f,
        subtitleSafeRight = 0.1f,
        subtitleSafeBottom = 0.12f,
        subtitleFontPx = 44,
        consultButtonX = 0.5f,
        consultButtonY = 0.9f
    )
}
