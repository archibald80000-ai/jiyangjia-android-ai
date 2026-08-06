package ai.jiyangjia.kiosk

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertArrayEquals
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

    @Test
    fun wrapsPcmBytesAsWavForGatewayUpload() {
        val pcm = PcmAudio(byteArrayOf(1, 0, 2, 0), 16000, 1, 16)

        val wav = pcm.toWavBytes()

        assertEquals(PcmAudio.WAV_HEADER_BYTES + 4, wav.size)
        assertEquals("RIFF", wav.copyOfRange(0, 4).toString(Charsets.US_ASCII))
        assertEquals("WAVE", wav.copyOfRange(8, 12).toString(Charsets.US_ASCII))
        assertEquals("data", wav.copyOfRange(36, 40).toString(Charsets.US_ASCII))
        assertArrayEquals(byteArrayOf(1, 0, 2, 0), wav.copyOfRange(44, 48))
    }
}
