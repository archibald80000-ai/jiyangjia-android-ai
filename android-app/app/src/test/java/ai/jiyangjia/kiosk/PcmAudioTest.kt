package ai.jiyangjia.kiosk

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class PcmAudioTest {
    @Test
    fun calculatesDurationForMono16BitPcm() {
        val oneSecond = ByteArray(16000 * 2)

        assertEquals(1000, PcmAudio(oneSecond, 16000, 1, 16).durationMillis)
    }

    @Test
    fun rejectsEmptyAudioForPlayback() {
        assertFalse(PcmAudio(ByteArray(0), 16000, 1, 16).isPlayable)
        assertTrue(PcmAudio(ByteArray(2), 16000, 1, 16).isPlayable)
    }
}
