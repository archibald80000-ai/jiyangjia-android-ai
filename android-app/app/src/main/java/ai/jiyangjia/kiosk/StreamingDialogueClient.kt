package ai.jiyangjia.kiosk

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import okio.ByteString.Companion.toByteString
import org.json.JSONObject
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

interface StreamingDialogueListener {
    fun onReady(requestId: String) = Unit
    fun onSpeechStarted(requestId: String) = Unit
    fun onPartial(requestId: String, text: String) = Unit
    fun onSpeechEnded(requestId: String) = Unit
    fun onResult(result: DialogueResult) = Unit
    fun onError(requestId: String, code: String, message: String) = Unit
}

class StreamingDialogueClient(
    config: ClientConfig,
    private val requestId: String,
    private val sessionId: String,
    private val generation: Int,
    private val listener: StreamingDialogueListener
) {
    private val client = OkHttpClient.Builder().readTimeout(0, TimeUnit.MILLISECONDS).build()
    private val stopped = AtomicBoolean(false)
    private var socket: WebSocket? = null
    private var transcript = ""
    private var answer = JSONObject()

    private val streamUrl = config.gatewayBaseUrl.trimEnd('/')
        .replaceFirst("https://", "wss://")
        .replaceFirst("http://", "ws://") + "/api/v1/dialogue/stream"

    fun connect() {
        socket = client.newWebSocket(Request.Builder().url(streamUrl).build(), object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                webSocket.send(
                    JSONObject()
                        .put("type", "start")
                        .put("request_id", requestId)
                        .put("session_id", sessionId)
                        .put("generation", generation)
                        .toString()
                )
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                handleEvent(JSONObject(text))
            }

            override fun onFailure(webSocket: WebSocket, error: Throwable, response: Response?) {
                if (!stopped.get()) listener.onError(requestId, "WEBSOCKET_FAILED", error.message ?: "stream failed")
            }
        })
    }

    fun sendPcm(frame: ByteArray): Boolean {
        if (frame.size != PCM_FRAME_BYTES || stopped.get()) return false
        return socket?.send(frame.toByteString()) == true
    }

    fun stop() {
        if (stopped.compareAndSet(false, true)) {
            socket?.send(control("stop"))
        }
    }

    fun cancel() {
        if (stopped.compareAndSet(false, true)) {
            socket?.send(control("cancel"))
            socket?.close(1000, "cancelled")
            client.dispatcher.executorService.shutdown()
        }
    }

    private fun control(type: String): String = JSONObject()
        .put("type", type)
        .put("request_id", requestId)
        .put("generation", generation)
        .toString()

    private fun handleEvent(event: JSONObject) {
        if (event.optInt("generation", generation) != generation || event.optString("request_id") != requestId) return
        when (event.optString("type")) {
            "ready" -> listener.onReady(requestId)
            "speech_started" -> listener.onSpeechStarted(requestId)
            "partial_transcript" -> listener.onPartial(requestId, event.optString("text"))
            "speech_ended" -> listener.onSpeechEnded(requestId)
            "final_transcript" -> {
                transcript = event.optJSONObject("transcript")?.optString("text").orEmpty()
            }
            "answer" -> answer = event
            "tts_ready" -> {
                val answerPayload = answer.optJSONObject("answer") ?: JSONObject()
                val tts = event.optJSONObject("tts") ?: JSONObject()
                val sourcesJson = answer.optJSONArray("sources")
                val sources = (0 until (sourcesJson?.length() ?: 0)).mapNotNull { index ->
                    sourcesJson?.optJSONObject(index)?.let { it.optString("title").ifBlank { it.optString("uri") } }
                }
                listener.onResult(
                    DialogueResult(
                        requestId = requestId,
                        sessionId = sessionId,
                        transcriptText = transcript,
                        answerText = answerPayload.optString("text"),
                        subtitles = listOfNotNull(answerPayload.optJSONArray("subtitles")?.optString(0)?.takeIf(String::isNotBlank)),
                        audioId = tts.optString("audio_id"),
                        audioContentType = tts.optString("content_type"),
                        sources = sources
                    )
                )
                socket?.close(1000, "complete")
                client.dispatcher.executorService.shutdown()
            }
            "error" -> listener.onError(requestId, event.optString("code"), event.optString("message"))
        }
    }

    companion object {
        const val PCM_FRAME_BYTES = 640
    }
}
