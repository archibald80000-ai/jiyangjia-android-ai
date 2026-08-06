package ai.jiyangjia.kiosk

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class ClientConfigTest {
    @Test
    fun defaultsAreNonSecretAndBounded() {
        val config = ClientConfig.fromValues(null, null, null, null, null)

        assertEquals(ClientConfig.DEFAULT_GATEWAY, config.gatewayBaseUrl)
        assertEquals(ClientConfig.DEFAULT_DEVICE_ID, config.deviceId)
        assertEquals(ClientConfig.DISPLAY_MODE_IDLE_VIDEO_VOICE, config.displayMode)
        assertEquals(20, config.maxRecordSeconds)
        assertFalse(config.sanitizedSummary().contains("key", ignoreCase = true))
    }

    @Test
    fun recordSecondsAreClamped() {
        assertEquals(3, ClientConfig.fromValues(null, null, null, -1, null).maxRecordSeconds)
        assertEquals(60, ClientConfig.fromValues(null, null, null, 1000, null).maxRecordSeconds)
    }
}
