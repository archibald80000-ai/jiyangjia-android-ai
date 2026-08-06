package ai.jiyangjia.kiosk

import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL
import java.util.UUID

data class DialogueResult(
    val requestId: String,
    val sessionId: String,
    val transcriptText: String,
    val answerText: String,
    val subtitles: List<String>,
    val audioId: String,
    val audioContentType: String,
    val sources: List<String>
) {
    val preferredSubtitle: String
        get() = subtitles.firstOrNull().orEmpty().ifBlank { answerText }
}

data class GatewayAudio(
    val bytes: ByteArray,
    val contentType: String,
    val requestId: String?
)

class GatewayException(
    message: String,
    val statusCode: Int? = null,
    cause: Throwable? = null
) : IOException(message, cause)

class GatewayClient(
    private val config: ClientConfig,
    private val connectTimeoutMillis: Int = DEFAULT_CONNECT_TIMEOUT_MS,
    private val readTimeoutMillis: Int = DEFAULT_READ_TIMEOUT_MS
) {
    fun submitAudio(pcm: PcmAudio, sessionId: String, requestId: String = newRequestId()): DialogueResult {
        val wav = pcm.toWavBytes()
        val boundary = "jiyangjia-${UUID.randomUUID().toString().replace("-", "")}"
        val connection = openConnection("/api/v1/dialogue/audio")
        connection.requestMethod = "POST"
        connection.doOutput = true
        connection.setRequestProperty("X-Request-Id", requestId)
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=$boundary")

        connection.outputStream.use { output ->
            writeFormField(output, boundary, "session_id", sessionId)
            writeFormField(output, boundary, "request_id", requestId)
            writeFormField(output, boundary, "duration_ms", pcm.durationMillis.toString())
            writeFormField(output, boundary, "sample_rate", pcm.sampleRate.toString())
            writeFormField(output, boundary, "input_device", "android-kiosk")
            writeFileField(output, boundary, "audio", "question.wav", "audio/wav", wav)
            output.write("--$boundary--\r\n".toByteArray(Charsets.UTF_8))
        }

        val body = readResponse(connection)
        if (connection.responseCode !in 200..299) {
            throw GatewayException(messageForError(body, "咨询服务暂时不可用，请稍后再试。"), connection.responseCode)
        }
        return parseDialogue(JSONObject(body))
    }

    fun fetchAudio(audioId: String, requestId: String): GatewayAudio {
        val connection = openConnection("/api/v1/audio/${urlPathSegment(audioId)}")
        connection.requestMethod = "GET"
        connection.setRequestProperty("X-Request-Id", requestId)
        val body = readBytes(connection)
        if (connection.responseCode !in 200..299) {
            val message = body.toString(Charsets.UTF_8).ifBlank { "语音文件不可用，请重新咨询。" }
            throw GatewayException(messageForError(message, "语音文件不可用，请重新咨询。"), connection.responseCode)
        }
        return GatewayAudio(
            bytes = body,
            contentType = connection.contentType ?: "application/octet-stream",
            requestId = connection.getHeaderField("X-Request-Id")
        )
    }

    private fun openConnection(path: String): HttpURLConnection {
        val base = config.gatewayBaseUrl.trimEnd('/')
        val connection = URL("$base$path").openConnection() as HttpURLConnection
        connection.connectTimeout = connectTimeoutMillis
        connection.readTimeout = readTimeoutMillis
        connection.useCaches = false
        return connection
    }

    companion object {
        const val DEFAULT_CONNECT_TIMEOUT_MS = 5000
        const val DEFAULT_READ_TIMEOUT_MS = 45000

        fun newRequestId(): String = "android-${UUID.randomUUID()}"

        fun parseDialogue(payload: JSONObject): DialogueResult {
            val answer = payload.optJSONObject("answer") ?: JSONObject()
            val tts = payload.optJSONObject("tts") ?: JSONObject()
            val transcript = payload.optJSONObject("transcript") ?: JSONObject()
            return DialogueResult(
                requestId = payload.optString("request_id"),
                sessionId = payload.optString("session_id"),
                transcriptText = transcript.optString("text"),
                answerText = answer.optString("text"),
                subtitles = toStringList(answer.optJSONArray("subtitles")),
                audioId = tts.optString("audio_id"),
                audioContentType = tts.optString("content_type", "application/octet-stream"),
                sources = sources(payload.optJSONArray("sources"))
            )
        }

        fun messageForError(body: String, fallback: String): String {
            return try {
                val detail = JSONObject(body).optJSONObject("detail")
                detail?.optString("message_for_user")?.ifBlank { fallback } ?: fallback
            } catch (_: Throwable) {
                fallback
            }
        }

        private fun toStringList(array: JSONArray?): List<String> {
            if (array == null) return emptyList()
            return (0 until array.length()).mapNotNull { index ->
                array.optString(index).takeIf { it.isNotBlank() }
            }
        }

        private fun sources(array: JSONArray?): List<String> {
            if (array == null) return emptyList()
            return (0 until array.length()).mapNotNull { index ->
                val item = array.optJSONObject(index) ?: return@mapNotNull null
                item.optString("title").ifBlank { item.optString("uri") }.ifBlank { null }
            }
        }
    }
}

private fun writeFormField(output: java.io.OutputStream, boundary: String, name: String, value: String) {
    output.write("--$boundary\r\n".toByteArray(Charsets.UTF_8))
    output.write("Content-Disposition: form-data; name=\"$name\"\r\n\r\n".toByteArray(Charsets.UTF_8))
    output.write(value.toByteArray(Charsets.UTF_8))
    output.write("\r\n".toByteArray(Charsets.UTF_8))
}

private fun writeFileField(
    output: java.io.OutputStream,
    boundary: String,
    name: String,
    filename: String,
    contentType: String,
    bytes: ByteArray
) {
    output.write("--$boundary\r\n".toByteArray(Charsets.UTF_8))
    output.write("Content-Disposition: form-data; name=\"$name\"; filename=\"$filename\"\r\n".toByteArray(Charsets.UTF_8))
    output.write("Content-Type: $contentType\r\n\r\n".toByteArray(Charsets.UTF_8))
    output.write(bytes)
    output.write("\r\n".toByteArray(Charsets.UTF_8))
}

private fun readResponse(connection: HttpURLConnection): String =
    readBytes(connection).toString(Charsets.UTF_8)

private fun readBytes(connection: HttpURLConnection): ByteArray {
    val stream = if (connection.responseCode in 200..299) connection.inputStream else connection.errorStream
    if (stream == null) {
        return ByteArray(0)
    }
    return stream.use { input ->
        val buffer = ByteArray(8192)
        val output = ByteArrayOutputStream()
        while (true) {
            val read = input.read(buffer)
            if (read < 0) break
            output.write(buffer, 0, read)
        }
        output.toByteArray()
    }
}

private fun urlPathSegment(value: String): String =
    value.replace(Regex("[^A-Za-z0-9_.-]"), "")
