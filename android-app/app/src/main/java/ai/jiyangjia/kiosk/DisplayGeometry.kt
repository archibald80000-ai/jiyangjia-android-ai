package ai.jiyangjia.kiosk

import kotlin.math.roundToInt

data class ResolvedDisplayGeometry(
    val characterLeft: Int,
    val characterTop: Int,
    val characterWidth: Int,
    val characterHeight: Int,
    val subtitleLeft: Int,
    val subtitleRight: Int,
    val subtitleBottom: Int,
    val subtitleWidth: Int,
    val buttonCenterX: Float,
    val buttonCenterY: Float
)

object DisplayGeometry {
    fun compute(viewWidth: Int, viewHeight: Int, profile: DisplayProfileConfig): ResolvedDisplayGeometry {
        require(viewWidth > 0 && viewHeight > 0)
        val characterWidth = (viewWidth * profile.characterScale).roundToInt().coerceAtLeast(1)
        val characterHeight = (viewHeight * profile.characterScale).roundToInt().coerceAtLeast(1)
        val centerX = viewWidth * profile.characterAnchorX
        val centerY = viewHeight * profile.characterAnchorY
        val subtitleLeft = (viewWidth * profile.subtitleSafeLeft).roundToInt()
        val subtitleRight = (viewWidth * profile.subtitleSafeRight).roundToInt()
        return ResolvedDisplayGeometry(
            characterLeft = (centerX - characterWidth / 2f).roundToInt(),
            characterTop = (centerY - characterHeight / 2f).roundToInt(),
            characterWidth = characterWidth,
            characterHeight = characterHeight,
            subtitleLeft = subtitleLeft,
            subtitleRight = subtitleRight,
            subtitleBottom = (viewHeight * profile.subtitleSafeBottom).roundToInt(),
            subtitleWidth = (viewWidth - subtitleLeft - subtitleRight).coerceAtLeast(1),
            buttonCenterX = viewWidth * profile.consultButtonX,
            buttonCenterY = viewHeight * profile.consultButtonY
        )
    }
}
