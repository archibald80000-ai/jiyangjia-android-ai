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
import androidx.media3.common.util.UnstableApi

@androidx.annotation.OptIn(markerClass = [UnstableApi::class])
class KioskActivity : Activity() {
    private val terminalMode = TerminalModePolicy(BuildConfig.STORE_KIOSK)
    private lateinit var idleContainer: FrameLayout
    private lateinit var statusText: TextView
    private lateinit var diagnosticsText: TextView
    private lateinit var subtitleText: TextView
    private lateinit var startButton: Button
    private lateinit var diagnosticsButton: Button
    private lateinit var idleVideoController: IdleVideoController
    private lateinit var audioController: AudioLoopbackController
    private lateinit var contentSyncManager: ContentSyncManager
    private lateinit var managedKioskController: ManagedKioskController
    private lateinit var releaseUpdateManager: ReleaseUpdateManager
    private var state: ConsultationState = ConsultationState.BOOT
    private var config: ClientConfig = ClientConfig.fromValues(null, null, null, null, null)
    private var lastRecording: PcmAudio? = null
    private var lastDialogue: DialogueResult? = null
    private var gatewayThread: Thread? = null
    private var streamClient: StreamingDialogueClient? = null
    private var streamGeneration: Int = 0
    @Volatile private var streamError: String? = null
    private var streamFallbackGeneration: Int? = null
    private var bargeInMonitor = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        if (terminalMode.keepScreenOn) {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }
        config = loadConfig()
        buildLayout()
        if (terminalMode.immersive) {
            enterImmersiveMode()
        }
        idleVideoController = IdleVideoController(
            context = this,
            container = idleContainer,
            subtitle = subtitleText,
            consultButton = startButton,
            onPlaybackFailure = ::handleDisplayPlaybackFailure
        )
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
        managedKioskController = ManagedKioskController(this)
        releaseUpdateManager = ReleaseUpdateManager(this, { config.gatewayBaseUrl }) { message ->
            runOnUiThread { diagnosticsText.text = message }
        }
        audioController = AudioLoopbackController(this)
        audioController.startDeviceMonitoring { reason -> handleAudioDeviceChange(reason) }
        transitionTo(ConsultationState.IDLE_VIDEO)
        refreshAudioDiagnostics()
        if (intent.getBooleanExtra(BootReceiver.EXTRA_BOOT_RECOVERY, false)) {
            diagnosticsText.text = "Boot recovery: cached bundle restored; dialogue state cleared"
        }
    }

    override fun onStart() {
        super.onStart()
        contentSyncManager.startForeground()
        if (terminalMode.selfUpdate) {
            releaseUpdateManager.checkAndInstall()
        }
    }

    override fun onResume() {
        super.onResume()
        diagnosticsText.text = if (terminalMode.managedKiosk) {
            val kiosk = managedKioskController.configureAndEnter()
            "Kiosk=${kiosk.mode} owner=${kiosk.deviceOwner} permitted=${kiosk.lockTaskPermitted} locked=${kiosk.lockTaskLocked}" +
                (kiosk.error?.let { " error=$it" } ?: "")
        } else {
            "PhoneDemo=${managedKioskController.exitForPhoneDemo()} system_navigation=available"
        }
    }

    override fun onStop() {
        contentSyncManager.stopForeground()
        super.onStop()
    }

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus && terminalMode.immersive) {
            enterImmersiveMode()
        }
    }

    override fun onDestroy() {
        gatewayThread?.interrupt()
        gatewayThread = null
        streamClient?.cancel()
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
        }
        if (::idleVideoController.isInitialized && state == ConsultationState.IDLE_VIDEO) {
            idleVideoController.show(cached)
        }
    }

    private fun handleDisplayPlaybackFailure(bundleVersion: String, reason: String) {
        val restored = contentSyncManager.rollback(bundleVersion, reason)
        diagnosticsText.text = "Display rollback: ${bundleVersion.take(12)} / ${reason.take(80)}"
        if (restored != null) {
            applyCachedBundle(restored)
        } else {
            idleVideoController.show(config)
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
        root.addView(overlay, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
            gravity = Gravity.TOP
        })

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

        subtitleText = TextView(this).apply {
            setTextColor(Color.WHITE)
            textSize = 32f
            gravity = Gravity.CENTER
            setShadowLayer(4f, 0f, 2f, Color.BLACK)
            text = getString(R.string.fallback_subtitle)
        }
        root.addView(subtitleText, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
            gravity = Gravity.BOTTOM
            leftMargin = 48
            rightMargin = 48
            bottomMargin = 180
        })

        startButton = Button(this).apply {
            text = getString(R.string.record_start)
            textSize = 20f
            setOnClickListener { handleAudioButton() }
        }
        root.addView(startButton, FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
            gravity = Gravity.BOTTOM or Gravity.CENTER_HORIZONTAL
            bottomMargin = 48
        })

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
                val hasVideo = contentSyncManager.cachedBundle()?.let(idleVideoController::show) ?: idleVideoController.show(config)
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
            streamClient?.stop()
            audioController.stopRecording()
            startButton.isEnabled = false
            subtitleText.text = "正在停止录音"
            return
        }
        if (state == ConsultationState.UPLOADING || state == ConsultationState.WAITING_FOR_RESPONSE || state == ConsultationState.PLAYING_ANSWER) {
            val wasPlaying = state == ConsultationState.PLAYING_ANSWER
            cancelCurrentInteraction(if (wasPlaying) "已打断播报，请开始说话" else "已取消本次咨询")
            if (wasPlaying) ensureMicPermissionThenRecord()
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
        beginStreamingCapture(isBargeIn = false)
    }

    private fun beginStreamingCapture(isBargeIn: Boolean) {
        if (!isBargeIn) transitionTo(ConsultationState.RECORDING)
        bargeInMonitor = isBargeIn
        streamError = null
        val generation = ++streamGeneration
        if (!isBargeIn) {
            lastRecording = null
            streamFallbackGeneration = null
        }
        val requestId = GatewayClient.newRequestId()
        val sessionId = "sess-${config.deviceId}"
        lateinit var client: StreamingDialogueClient
        client = StreamingDialogueClient(config, requestId, sessionId, generation, object : StreamingDialogueListener {
            override fun onReady(requestId: String) {
                if (generation != streamGeneration) return
                runOnUiThread { startPcmCapture(client, generation, isBargeIn) }
            }

            override fun onSpeechStarted(requestId: String) {
                if (generation != streamGeneration) return
                runOnUiThread {
                    if (bargeInMonitor && state == ConsultationState.PLAYING_ANSWER) {
                        audioController.stopPlayback()
                        bargeInMonitor = false
                        transitionTo(ConsultationState.RECORDING)
                        diagnosticsText.text = "Automatic barge-in request_id=$requestId"
                    }
                    subtitleText.text = "检测到语音，正在识别"
                }
            }

            override fun onPartial(requestId: String, text: String) {
                if (generation == streamGeneration) runOnUiThread { subtitleText.text = text }
            }

            override fun onSpeechEnded(requestId: String) {
                if (generation != streamGeneration) return
                audioController.stopRecording()
                runOnUiThread {
                    transitionTo(ConsultationState.WAITING_FOR_RESPONSE)
                    subtitleText.text = "语音结束，正在生成回答"
                }
            }

            override fun onResult(result: DialogueResult) {
                if (generation != streamGeneration) return
                fetchAndPlayStreamResult(result, generation)
            }

            override fun onError(requestId: String, code: String, message: String) {
                if (generation != streamGeneration) return
                if (bargeInMonitor && code in setOf("NO_SPEECH_TIMEOUT", "NO_SPEECH")) {
                    audioController.stopRecording()
                    bargeInMonitor = false
                    runOnUiThread { diagnosticsText.text = "AEC monitor idle timeout; click interrupt remains available" }
                    return
                }
                streamError = "$code: $message"
                audioController.stopRecording()
                if (!isBargeIn) {
                    runOnUiThread {
                        lastRecording?.takeIf { it.isPlayable }?.let {
                            submitStreamFallback(it, generation, streamError.orEmpty())
                        } ?: run {
                            subtitleText.text = "流式识别中断，正在完成录音并切换上传"
                        }
                    }
                }
            }
        })
        streamClient?.cancel()
        streamClient = client
        client.connect()
    }

    private fun startPcmCapture(client: StreamingDialogueClient, generation: Int, isBargeIn: Boolean) {
        audioController.startRecording(
            maxSeconds = 30,
            useVoiceCommunicationSource = isBargeIn,
            onLevel = { level, elapsedMillis ->
                if (generation == streamGeneration && state == ConsultationState.RECORDING && (!isBargeIn || !bargeInMonitor)) {
                    subtitleText.text = "录音中 ${elapsedMillis / 1000}s  音量 $level%"
                }
            },
            onComplete = { pcm ->
                lastRecording = pcm
                if (!isBargeIn) {
                    diagnosticsText.text = "Recorded ${pcm.durationMillis}ms / ${pcm.bytes.size} bytes"
                }
                val failure = streamError
                if (failure != null && pcm.isPlayable && !isBargeIn && generation == streamGeneration) {
                    submitStreamFallback(pcm, generation, failure)
                } else if (!pcm.isPlayable && !isBargeIn) {
                    showAudioError("未录到可播放音频")
                } else if (!isBargeIn && generation == streamGeneration && state == ConsultationState.RECORDING) {
                    client.stop()
                    transitionTo(ConsultationState.WAITING_FOR_RESPONSE)
                    subtitleText.text = "录音已结束，正在识别"
                }
            },
            onError = { message ->
                showAudioError(message)
            },
            onFrame = { frame ->
                if (generation == streamGeneration && !client.sendPcm(frame)) {
                    streamError = "PCM_SEND_FAILED"
                    audioController.stopRecording()
                }
            },
            onEffects = { effects ->
                diagnosticsText.text = if (effects.automaticBargeInReady) {
                    "VOICE_COMMUNICATION AEC=${effects.aecEnabled} NS=${effects.noiseSuppressorEnabled}"
                } else {
                    "DEGRADED: AEC unavailable; automatic barge-in release gate blocked"
                }
            }
        )
    }

    private fun submitStreamFallback(pcm: PcmAudio, generation: Int, failure: String) {
        if (generation != streamGeneration || streamFallbackGeneration == generation) return
        streamFallbackGeneration = generation
        streamClient?.cancel()
        diagnosticsText.text = "WAV fallback ${pcm.durationMillis}ms / ${pcm.bytes.size} bytes: ${failure.take(48)}"
        submitRecording(pcm)
    }

    private fun fetchAndPlayStreamResult(dialogue: DialogueResult, generation: Int) {
        gatewayThread = Thread {
            try {
                val audio = GatewayClient(config).fetchAudio(dialogue.audioId, dialogue.requestId)
                if (generation != streamGeneration) return@Thread
                runOnUiThread {
                    lastDialogue = dialogue
                    showDialogueResult(dialogue)
                    playAnswerAudio(audio)
                }
            } catch (error: Throwable) {
                if (generation == streamGeneration) runOnUiThread { showServiceError(error.message ?: "audio fetch failed") }
            }
        }.apply { name = "kiosk-stream-result"; start() }
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
                streamClient?.cancel()
                audioController.stopRecording()
                bargeInMonitor = false
                transitionTo(ConsultationState.IDLE_VIDEO)
                lastDialogue?.let { dialogue ->
                    subtitleText.text = dialogue.preferredSubtitle
                    showDialogueResult(dialogue)
                } ?: refreshAudioDiagnostics("playback complete")
            },
            onError = { message ->
                showAudioError(message)
            }
        )
        if (
            checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED &&
            audioController.supportsAutomaticBargeIn()
        ) {
            beginStreamingCapture(isBargeIn = true)
        } else {
            diagnosticsText.text = if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                "DEGRADED: microphone permission missing; click interrupt only"
            } else {
                "Built-in microphone: click to interrupt; automatic barge-in requires USB input"
            }
        }
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
        streamGeneration += 1
        streamClient?.cancel()
        streamClient = null
        streamError = null
        bargeInMonitor = false
        audioController.stopRecording()
        audioController.stopPlayback()
        transitionTo(ConsultationState.IDLE_VIDEO)
        subtitleText.text = message
        refreshAudioDiagnostics("cancelled")
    }

    private fun enterImmersiveMode() {
        val decorView = window.decorView
        decorView.post {
            if (isFinishing || isDestroyed) return@post
            val modernApplied = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.R) {
                runCatching {
                    val controller = decorView.windowInsetsController ?: return@runCatching false
                    controller.hide(WindowInsets.Type.systemBars())
                    controller.systemBarsBehavior = WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                    true
                }.getOrDefault(false)
            } else {
                false
            }
            if (!modernApplied) applyLegacyImmersiveMode(decorView)
        }
    }

    @Suppress("DEPRECATION")
    private fun applyLegacyImmersiveMode(decorView: View) {
        decorView.systemUiVisibility =
            View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY or
                View.SYSTEM_UI_FLAG_FULLSCREEN or
                View.SYSTEM_UI_FLAG_HIDE_NAVIGATION or
                View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN or
                View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION or
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
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
