package ai.jiyangjia.kiosk

import android.content.Context
import android.graphics.BitmapFactory
import android.net.Uri
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.TextView
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.PlayerView
import java.io.File

@UnstableApi
class IdleVideoController(
    private val context: Context,
    private val container: FrameLayout,
    private val subtitle: TextView,
    private val consultButton: Button,
    private val onPlaybackFailure: (String, String) -> Unit
) {
    private var player: ExoPlayer? = null
    private var mediaLayer: FrameLayout? = null

    fun show(config: ClientConfig): Boolean {
        val configured = config.idleVideoPath.takeIf(String::isNotBlank)?.let(::File)?.takeIf(File::isFile)
            ?: return showFallback()
        val profile = defaultProfile(container.width.coerceAtLeast(1080), container.height.coerceAtLeast(1920))
        return showMedia(configured, null, profile, "local")
    }

    fun show(cached: CachedContentBundle): Boolean {
        applyOverlayGeometry(cached.bundle.profile)
        val video = cached.videoFile ?: return showFallback()
        return showMedia(video, cached.backgroundFile, cached.bundle.profile, cached.bundle.bundleVersion)
    }

    fun stop() {
        player?.release()
        player = null
        mediaLayer = null
        container.removeAllViews()
    }

    private fun showMedia(video: File, background: File?, profile: DisplayProfileConfig, bundleVersion: String): Boolean {
        val nextLayer = FrameLayout(context).apply {
            setBackgroundColor(android.graphics.Color.BLACK)
            alpha = 0f
        }
        background?.takeIf(File::isFile)?.let { imageFile ->
            val bitmap = BitmapFactory.decodeFile(imageFile.absolutePath)
            if (bitmap != null) {
                nextLayer.addView(
                    ImageView(context).apply {
                        setImageBitmap(bitmap)
                        scaleType = imageScaleType(profile.scaleMode)
                    },
                    FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
                )
            }
        }
        val nextPlayerView = PlayerView(context).apply {
            useController = false
            resizeMode = videoResizeMode(profile.scaleMode)
        }
        nextLayer.addView(nextPlayerView)
        container.addView(nextLayer, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
        applyCharacterGeometry(nextPlayerView, profile)

        val previousLayer = mediaLayer
        val previousPlayer = player
        val nextPlayer = ExoPlayer.Builder(context).build()
        nextPlayer.repeatMode = Player.REPEAT_MODE_ONE
        nextPlayer.volume = 0f
        nextPlayer.setMediaItem(MediaItem.fromUri(Uri.fromFile(video)))
        nextPlayer.addListener(object : Player.Listener {
                override fun onRenderedFirstFrame() {
                    nextLayer.animate().alpha(1f).setDuration(120).withEndAction {
                        previousPlayer?.release()
                        if (previousLayer !== nextLayer) container.removeView(previousLayer)
                    }.start()
                }

                override fun onPlayerError(error: PlaybackException) {
                    nextPlayerView.player = null
                    nextPlayer.release()
                    container.removeView(nextLayer)
                    mediaLayer = previousLayer
                    player = previousPlayer
                    if (previousLayer == null) showFallback()
                    onPlaybackFailure(bundleVersion, error.errorCodeName)
                }
            })
        nextPlayer.prepare()
        nextPlayer.playWhenReady = true
        nextPlayerView.player = nextPlayer
        mediaLayer = nextLayer
        player = nextPlayer
        return true
    }

    private fun applyOverlayGeometry(profile: DisplayProfileConfig) {
        val width = container.width.takeIf { it > 0 } ?: profile.widthPx
        val height = container.height.takeIf { it > 0 } ?: profile.heightPx
        val geometry = DisplayGeometry.compute(width, height, profile)
        subtitle.setTextSize(android.util.TypedValue.COMPLEX_UNIT_PX, profile.subtitleFontPx.toFloat())
        subtitle.layoutParams = FrameLayout.LayoutParams(geometry.subtitleWidth, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
            leftMargin = geometry.subtitleLeft
            rightMargin = geometry.subtitleRight
            bottomMargin = geometry.subtitleBottom
            gravity = android.view.Gravity.BOTTOM
        }
        consultButton.post {
            consultButton.x = geometry.buttonCenterX - consultButton.width / 2f
            consultButton.y = geometry.buttonCenterY - consultButton.height / 2f
        }
    }

    private fun applyCharacterGeometry(view: PlayerView, profile: DisplayProfileConfig) {
        val apply = {
            val width = container.width.takeIf { it > 0 } ?: profile.widthPx
            val height = container.height.takeIf { it > 0 } ?: profile.heightPx
            val geometry = DisplayGeometry.compute(width, height, profile)
            view.layoutParams = FrameLayout.LayoutParams(geometry.characterWidth, geometry.characterHeight).apply {
                leftMargin = geometry.characterLeft
                topMargin = geometry.characterTop
            }
        }
        if (container.width > 0 && container.height > 0) apply() else container.post { apply() }
    }

    private fun showFallback(): Boolean {
        player?.release()
        player = null
        container.removeAllViews()
        mediaLayer = FrameLayout(context).apply {
            addView(IdleFallbackView(context), ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        }
        container.addView(mediaLayer, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        return false
    }

    private fun imageScaleType(mode: String): ImageView.ScaleType = when (mode) {
        "fill" -> ImageView.ScaleType.FIT_XY
        "crop" -> ImageView.ScaleType.CENTER_CROP
        else -> ImageView.ScaleType.FIT_CENTER
    }

    private fun videoResizeMode(mode: String): Int = when (mode) {
        "fill" -> AspectRatioFrameLayout.RESIZE_MODE_FILL
        "crop" -> AspectRatioFrameLayout.RESIZE_MODE_ZOOM
        else -> AspectRatioFrameLayout.RESIZE_MODE_FIT
    }

    private fun defaultProfile(width: Int, height: Int) = DisplayProfileConfig(
        profileId = "local-default",
        widthPx = width,
        heightPx = height,
        orientation = if (width >= height) "landscape" else "portrait",
        scaleMode = "fit",
        characterAnchorX = 0.5f,
        characterAnchorY = 0.5f,
        characterScale = 1f,
        subtitleSafeLeft = 0.08f,
        subtitleSafeRight = 0.08f,
        subtitleSafeBottom = 0.08f,
        subtitleFontPx = 36,
        consultButtonX = 0.5f,
        consultButtonY = 0.88f
    )
}
