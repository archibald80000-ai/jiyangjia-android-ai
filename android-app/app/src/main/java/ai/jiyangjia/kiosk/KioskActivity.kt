package ai.jiyangjia.kiosk

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.pm.ActivityInfo
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.WindowInsets
import android.view.WindowInsetsController
import android.view.WindowManager
import android.widget.Button
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.TextView

class KioskActivity : Activity() {
    private lateinit var idleContainer: FrameLayout
    private lateinit var statusText: TextView
    private lateinit var diagnosticsText: TextView
    private lateinit var subtitleText: TextView
    private lateinit var startButton: Button
    private lateinit var diagnosticsButton: Button
    private lateinit var idleVideoController: IdleVideoController
    private lateinit var audioController: AudioLoopbackController
    private lateinit var contentSyncManager: ContentSyncManager
    private var state: ConsultationState = ConsultationState.BOOT
    private var config: ClientConfig = ClientConfig.fromValues(null, null, null, null, null)
    private var lastRecording: PcmAudio? = null
    private var lastDialogue: DialogueResult? = null
    private var gatewayThread: Thread? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        enterImmersiveMode()
        config = loadConfig()
        buildLayout()
        idleVideoController = IdleVideoController(this, idleContainer)
        contentSyncManager = ContentSyncManager(
            context = this,
            baseUrl = { config.gatewayBaseUrl },
            metrics = {
                val display = resources.displayMetrics
                Triple(
                    display.widthPixels,
                    display.heightPixels,
                    if (display.widthPixels >= display.heightPixels) "landscape" else "portrait"
                )
            },
            onResult = ::handleContentSyncResult
        )
        contentSyncManager.cachedBundle()?.let(::applyCachedBundle)
        audioController = AudioLoopbackController(this)
        audioController.startDeviceMonitoring { reason -> handleAudioDeviceChange(reason) }
        transitionTo(ConsultationState.IDLE_VIDEO)
        refreshAudioDiagnostics()
    }

    override fun onStart() {
        super.onStart()
        contentSyncManager.startForeground()
    }

    override fun onStop() {
        contentSyncManager.stopForeground()
        super.onStop()
    }

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus) {
            enterImmersiveMode()
        }
    }

    override fun onDestroy() {
        gatewayThread?.interrupt()
        gatewayThread = null
        contentSyncManager.stopForeground()
        audioController.shutdown()
        idleVideoController.stop()
        super.onDestroy()
    }

    private fun handleContentSyncResult(result: ContentSyncResult) {
        when (result) {
            is ContentSyncResult.Activated -> {
                applyCachedBundle(result.bundle)
                diagnosticsText.text = "Content bundle activated: ${result.bundle.bundle.bundleVersion.take(12)}"
            }
            is ContentSyncResult.Unchanged -> {
                result.bundle?.let(::applyCachedBundle)
            }
            is ContentSyncResult.Failed -> {
                result.cached?.let(::applyCachedBundle)
                diagnosticsText.text = "Content sync retained cache: ${result.reason.take(120)}"
            }
        }
    }

    private fun applyCachedBundle(cached: CachedContentBundle) {
        val videoPath = cached.videoFile?.absolutePath.orEmpty()
        if (videoPath.isNotBlank() && config.idleVideoPath != videoPath) {
            config = config.copy(idleVideoPath = videoPath)
            if (::idleVideoController.isInitialized && state == ConsultationState.IDLE_VIDEO) {
                idleVideoController.show(config)
            }
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_RECORD_AUDIO) {
            if (grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED) {
                beginRecording()
            } else {
                showAudioError("麦克风权限未授权，无法录音")
            }
        }
    }

    private fun buildLayout() {
        val root = FrameLayout(this).apply {
            setBackgroundColor(Color.rgb(20, 32, 36))
        }
        idleContainer = FrameLayout(this)
        root.addView(idleContainer, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)

        val overlay = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(32, 28, 32, 32)
        }
        root.addView(overlay, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)

        statusText = TextView(this).apply {
            setTextColor(Color.WHITE)
            textSize = 18f
            gravity = Gravity.CENTER
            setOnLongClickListener {
                showConfigDialog()
                true
            }
        }
        overlay.addView(statusText, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)

        diagnosticsText = TextView(this).apply {
            setTextColor(Color.rgb(224, 235, 231))
            textSize = 14f
            gravity = Gravity.CENTER
            setPadding(0, 10, 0, 0)
            text = "Audio diagnostics pending"
        }
        overlay.addView(diagnosticsText, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)

        val spacer = View(this)
        overlay.addView(spacer, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))

        subtitleText = TextView(this).apply {
            setTextColor(Color.WHITE)
            textSize = 32f
            gravity = Gravity.CENTER
            setShadowLayer(4f, 0f, 2f, Color.BLACK)
            text = getString(R.string.fallback_subtitle)
        }
        overlay.addView(subtitleText, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)

        startButton = Button(this).apply {
            text = getString(R.string.record_start)
            textSize = 20f
            setOnClickListener { handleAudioButton() }
        }
        val buttonParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
            topMargin = 28
            bottomMargin = 10
        }
        overlay.addView(startButton, buttonParams)

        diagnosticsButton = Button(this).apply {
            text = getString(R.string.refresh_audio)
            textSize = 16f
            setOnClickListener { refreshAudioDiagnostics("manual refresh") }
        }
        overlay.addView(diagnosticsButton, LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT))

        setContentView(root)
    }

    private fun transitionTo(next: ConsultationState) {
        state = next
        when (next) {
            ConsultationState.IDLE_VIDEO -> {
                val hasVideo = idleVideoController.show(config)
                statusText.text = if (hasVideo) "IDLE_VIDEO local_video" else "IDLE_VIDEO fallback"
                subtitleText.text = getString(R.string.fallback_subtitle)
                startButton.text = getString(R.string.consult_start)
                startButton.isEnabled = true
                diagnosticsButton.isEnabled = true
            }
            ConsultationState.READY_TO_RECORD -> {
                statusText.text = "READY_TO_RECORD"
                subtitleText.text = "准备录音"
                startButton.text = getString(R.string.record_start)
                startButton.isEnabled = true
                diagnosticsButton.isEnabled = true
            }
            ConsultationState.RECORDING -> {
                statusText.text = "RECORDING"
                subtitleText.text = "正在录音"
                startButton.text = getString(R.string.record_stop_send)
                startButton.isEnabled = true
                diagnosticsButton.isEnabled = false
            }
            ConsultationState.UPLOADING -> {
                statusText.text = "UPLOADING"
                subtitleText.text = "正在上传咨询录音"
                startButton.text = getString(R.string.cancel_consultation)
                startButton.isEnabled = true
                diagnosticsButton.isEnabled = false
            }
            ConsultationState.WAITING_FOR_RESPONSE -> {
                statusText.text = "WAITING_FOR_RESPONSE"
                subtitleText.text = "正在生成回答"
                startButton.text = getString(R.string.cancel_consultation)
                startButton.isEnabled = true
                diagnosticsButton.isEnabled = false
            }
            ConsultationState.PLAYING_ANSWER -> {
                statusText.text = "PLAYING_ANSWER"
                subtitleText.text = lastDialogue?.preferredSubtitle ?: "正在播放回答"
                startButton.text = getString(R.string.cancel_consultation)
                startButton.isEnabled = true
                diagnosticsButton.isEnabled = false
            }
            ConsultationState.ERROR -> {
                statusText.text = "ERROR"
                startButton.text = getString(R.string.consult_start)
                startButton.isEnabled = true
                diagnosticsButton.isEnabled = true
            }
            else -> {
                statusText.text = next.name
                startButton.isEnabled = false
            }
        }
    }

    private fun handleAudioButton() {
        if (state == ConsultationState.RECORDING) {
            audioController.stopRecording()
            startButton.isEnabled = false
            subtitleText.text = "正在停止录音"
            return
        }
        if (state == ConsultationState.UPLOADING || state == ConsultationState.WAITING_FOR_RESPONSE || state == ConsultationState.PLAYING_ANSWER) {
            cancelCurrentInteraction("已取消本次咨询")
            return
        }
        if (state.canStartConsultation()) {
            transitionTo(ConsultationState.READY_TO_RECORD)
            refreshAudioDiagnostics("before recording")
            ensureMicPermissionThenRecord()
        }
    }

    private fun ensureMicPermissionThenRecord() {
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            beginRecording()
            return
        }
        requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), REQUEST_RECORD_AUDIO)
        statusText.text = "REQUEST_RECORD_AUDIO_PERMISSION"
        subtitleText.text = "请授权麦克风权限"
    }

    private fun beginRecording() {
        transitionTo(ConsultationState.RECORDING)
        audioController.startRecording(
            maxSeconds = config.maxRecordSeconds,
            onLevel = { level, elapsedMillis ->
                subtitleText.text = "录音中 ${elapsedMillis / 1000}s  音量 $level%"
            },
            onComplete = { pcm ->
                lastRecording = pcm
                if (pcm.isPlayable) {
                    subtitleText.text = "录音 ${pcm.durationMillis}ms，开始上传"
                    submitRecording(pcm)
                } else {
                    showAudioError("未录到可播放音频")
                }
            },
            onError = { message ->
                showAudioError(message)
            }
        )
    }

    private fun submitRecording(pcm: PcmAudio) {
        transitionTo(ConsultationState.UPLOADING)
        val requestId = GatewayClient.newRequestId()
        val sessionId = "sess-${config.deviceId}"
        gatewayThread = Thread {
            try {
                val client = GatewayClient(config)
                runOnUiThread {
                    transitionTo(ConsultationState.WAITING_FOR_RESPONSE)
                    statusText.text = "WAITING_FOR_RESPONSE request_id=$requestId"
                    subtitleText.text = "正在识别并生成回答"
                }
                val dialogue = client.submitAudio(pcm, sessionId, requestId)
                if (Thread.currentThread().isInterrupted) {
                    return@Thread
                }
                val answerAudio = client.fetchAudio(dialogue.audioId, dialogue.requestId)
                runOnUiThread {
                    lastDialogue = dialogue
                    subtitleText.text = dialogue.preferredSubtitle
                    showDialogueResult(dialogue)
                    playAnswerAudio(answerAudio)
                }
            } catch (error: Throwable) {
                if (!Thread.currentThread().isInterrupted) {
                    runOnUiThread { showServiceError(error.message ?: error.javaClass.simpleName) }
                }
            }
        }.apply {
            name = "kiosk-gateway-dialogue"
            start()
        }
    }

    private fun playAnswerAudio(audio: GatewayAudio) {
        transitionTo(ConsultationState.PLAYING_ANSWER)
        audioController.playEncoded(
            bytes = audio.bytes,
            contentType = audio.contentType,
            onComplete = {
                transitionTo(ConsultationState.IDLE_VIDEO)
                subtitleText.text = "回答播放完成"
                refreshAudioDiagnostics("playback complete")
            },
            onError = { message ->
                showAudioError(message)
            }
        )
    }

    private fun showDialogueResult(dialogue: DialogueResult) {
        val sourceText = if (dialogue.sources.isEmpty()) "无来源命中" else "来源：${dialogue.sources.take(2).joinToString(" / ")}"
        diagnosticsText.text = listOf(
            "request_id=${dialogue.requestId}",
            "ASR=${dialogue.transcriptText.take(32)}",
            sourceText
        ).joinToString("\n")
    }

    private fun refreshAudioDiagnostics(reason: String = "initial") {
        if (!::audioController.isInitialized || !::diagnosticsText.isInitialized) {
            return
        }
        val diagnostics = audioController.refreshDiagnostics()
        diagnosticsText.text = listOf("Audio event: $reason")
            .plus(diagnostics.detailedLines())
            .take(6)
            .joinToString("\n")
    }

    private fun handleAudioDeviceChange(reason: String) {
        refreshAudioDiagnostics(reason)
        if (state == ConsultationState.RECORDING) {
            audioController.stopRecording()
            transitionTo(ConsultationState.ERROR)
            subtitleText.text = "检测到音频设备变化，已停止录音，请重新开始"
        }
    }

    private fun showAudioError(message: String) {
        transitionTo(ConsultationState.ERROR)
        subtitleText.text = "音频错误：$message"
        refreshAudioDiagnostics("error")
    }

    private fun showServiceError(message: String) {
        transitionTo(ConsultationState.ERROR)
        subtitleText.text = "服务错误：$message"
        refreshAudioDiagnostics("service error")
    }

    private fun cancelCurrentInteraction(message: String) {
        gatewayThread?.interrupt()
        gatewayThread = null
        audioController.stopRecording()
        audioController.stopPlayback()
        transitionTo(ConsultationState.IDLE_VIDEO)
        subtitleText.text = message
        refreshAudioDiagnostics("cancelled")
    }

    private fun enterImmersiveMode() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.R) {
            window.insetsController?.let {
                it.hide(WindowInsets.Type.systemBars())
                it.systemBarsBehavior = WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            }
        } else {
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility =
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY or
                    View.SYSTEM_UI_FLAG_FULLSCREEN or
                    View.SYSTEM_UI_FLAG_HIDE_NAVIGATION or
                    View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN or
                    View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION or
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        }
    }

    private fun loadConfig(): ClientConfig {
        val prefs = getSharedPreferences("kiosk_config", Context.MODE_PRIVATE)
        return ClientConfig.fromValues(
            gatewayBaseUrl = prefs.getString("gateway", null),
            deviceId = prefs.getString("device_id", null),
            displayMode = prefs.getString("display_mode", null),
            maxRecordSeconds = prefs.getInt("max_record_seconds", 20),
            idleVideoPath = prefs.getString("idle_video_path", null)
        )
    }

    private fun showConfigDialog() {
        val gatewayInput = EditText(this).apply {
            hint = "Gateway URL"
            setText(config.gatewayBaseUrl)
        }
        val deviceInput = EditText(this).apply {
            hint = "Device ID"
            setText(config.deviceId)
        }
        val videoInput = EditText(this).apply {
            hint = "Idle video local path"
            setText(config.idleVideoPath)
        }
        val form = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 12, 32, 0)
            addView(gatewayInput)
            addView(deviceInput)
            addView(videoInput)
        }
        AlertDialog.Builder(this)
            .setTitle("开发配置")
            .setView(form)
            .setNegativeButton("取消", null)
            .setPositiveButton("保存") { _, _ ->
                config = ClientConfig.fromValues(
                    gatewayBaseUrl = gatewayInput.text.toString(),
                    deviceId = deviceInput.text.toString(),
                    displayMode = ClientConfig.DISPLAY_MODE_IDLE_VIDEO_VOICE,
                    maxRecordSeconds = 20,
                    idleVideoPath = videoInput.text.toString()
                )
                getSharedPreferences("kiosk_config", Context.MODE_PRIVATE)
                    .edit()
                    .putString("gateway", config.gatewayBaseUrl)
                    .putString("device_id", config.deviceId)
                    .putString("display_mode", config.displayMode)
                    .putInt("max_record_seconds", config.maxRecordSeconds)
                    .putString("idle_video_path", config.idleVideoPath)
                    .apply()
                transitionTo(ConsultationState.IDLE_VIDEO)
            }
            .show()
    }

    companion object {
        private const val REQUEST_RECORD_AUDIO = 701
    }
}
