package ai.jiyangjia.kiosk

import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class GatewayClientTest {
    @Test
    fun parsesDialogueResponseForSubtitleAudioAndSources() {
        val payload = JSONObject(
            """
            {
              "request_id": "req-123",
              "session_id": "sess-1",
              "transcript": {"text": "服务时间是什么？"},
              "answer": {"text": "以现场公告为准。", "subtitles": ["以现场公告为准。"]},
              "tts": {"audio_id": "aud_123", "content_type": "audio/mpeg"},
              "sources": [{"title": "服务时间", "uri": "manual://faq"}]
            }
            """.trimIndent()
        )

        val result = GatewayClient.parseDialogue(payload)

        assertEquals("req-123", result.requestId)
        assertEquals("服务时间是什么？", result.transcriptText)
        assertEquals("以现场公告为准。", result.preferredSubtitle)
        assertEquals("aud_123", result.audioId)
        assertEquals("audio/mpeg", result.audioContentType)
        assertEquals(listOf("服务时间"), result.sources)
    }

    @Test
    fun extractsUserFacingErrorMessage() {
        val message = GatewayClient.messageForError(
            """{"detail":{"code":"AUDIO_TOO_LARGE","message_for_user":"录音太长，请缩短后重试。"}}""",
            "fallback"
        )

        assertEquals("录音太长，请缩短后重试。", message)
    }

    @Test
    fun generatedRequestIdsAreAndroidScoped() {
        assertTrue(GatewayClient.newRequestId().startsWith("android-"))
    }
}
