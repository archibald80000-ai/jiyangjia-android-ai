package ai.jiyangjia.kiosk

import android.content.Context
import android.net.Uri
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import android.widget.VideoView
import java.io.File

class IdleVideoController(
    private val context: Context,
    private val container: FrameLayout
) {
    private var videoView: VideoView? = null
    private var fallbackView: View? = null

    fun show(config: ClientConfig): Boolean {
        container.removeAllViews()

        val videoUri = resolveVideoUri(config)
        if (videoUri == null) {
            showFallback()
            return false
        }

        val player = VideoView(context).apply {
            setVideoURI(videoUri)
            setOnPreparedListener {
                it.isLooping = true
                start()
            }
            setOnErrorListener { _, _, _ ->
                showFallback()
                true
            }
        }
        videoView = player
        container.addView(player, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        return true
    }

    fun stop() {
        videoView?.stopPlayback()
        videoView = null
    }

    private fun resolveVideoUri(config: ClientConfig): Uri? {
        val configured = config.idleVideoPath
        if (configured.isNotBlank()) {
            val file = File(configured)
            if (file.exists() && file.isFile) {
                return Uri.fromFile(file)
            }
        }

        val rawId = context.resources.getIdentifier("idle_placeholder", "raw", context.packageName)
        if (rawId != 0) {
            return Uri.parse("android.resource://${context.packageName}/$rawId")
        }
        return null
    }

    private fun showFallback() {
        videoView?.stopPlayback()
        videoView = null
        container.removeAllViews()
        fallbackView = IdleFallbackView(context)
        container.addView(fallbackView, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
    }
}
