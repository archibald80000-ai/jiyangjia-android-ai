package ai.jiyangjia.kiosk

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
}
