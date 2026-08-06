package ai.jiyangjia.kiosk

import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder

data class PcmAudio(
    val bytes: ByteArray,
    val sampleRate: Int,
    val channelCount: Int,
    val bitsPerSample: Int
) {
    val durationMillis: Long
        get() {
            val bytesPerFrame = channelCount * (bitsPerSample / 8)
            if (bytesPerFrame <= 0 || sampleRate <= 0) {
                return 0
            }
            return (bytes.size.toLong() * 1000L) / (sampleRate.toLong() * bytesPerFrame.toLong())
        }

    val isPlayable: Boolean = bytes.isNotEmpty() && sampleRate > 0 && channelCount > 0 && bitsPerSample > 0

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false
        other as PcmAudio
        return bytes.contentEquals(other.bytes) &&
            sampleRate == other.sampleRate &&
            channelCount == other.channelCount &&
            bitsPerSample == other.bitsPerSample
    }

    override fun hashCode(): Int {
        var result = bytes.contentHashCode()
        result = 31 * result + sampleRate
        result = 31 * result + channelCount
        result = 31 * result + bitsPerSample
        return result
    }

    fun toWavBytes(): ByteArray {
        require(bitsPerSample == 16) { "only 16-bit PCM is supported" }
        require(channelCount in 1..2) { "only mono/stereo PCM is supported" }
        require(sampleRate > 0) { "invalid sample rate" }
        val header = ByteBuffer.allocate(WAV_HEADER_BYTES).order(ByteOrder.LITTLE_ENDIAN)
        header.put("RIFF".toByteArray(Charsets.US_ASCII))
        header.putInt(36 + bytes.size)
        header.put("WAVE".toByteArray(Charsets.US_ASCII))
        header.put("fmt ".toByteArray(Charsets.US_ASCII))
        header.putInt(16)
        header.putShort(1)
        header.putShort(channelCount.toShort())
        header.putInt(sampleRate)
        header.putInt(sampleRate * channelCount * (bitsPerSample / 8))
        header.putShort((channelCount * (bitsPerSample / 8)).toShort())
        header.putShort(bitsPerSample.toShort())
        header.put("data".toByteArray(Charsets.US_ASCII))
        header.putInt(bytes.size)
        return ByteArrayOutputStream(WAV_HEADER_BYTES + bytes.size).apply {
            write(header.array())
            write(bytes)
        }.toByteArray()
    }

    companion object {
        const val WAV_HEADER_BYTES = 44
    }
}
