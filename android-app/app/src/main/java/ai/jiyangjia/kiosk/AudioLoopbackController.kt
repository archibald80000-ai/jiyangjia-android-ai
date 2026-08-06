package ai.jiyangjia.kiosk

import android.annotation.SuppressLint
import android.content.Context
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioManager
import android.media.AudioRecord
import android.media.AudioTrack
import android.media.MediaRecorder
import android.os.Handler
import android.os.Looper
import java.io.ByteArrayOutputStream
import java.util.concurrent.atomic.AtomicBoolean
import kotlin.math.abs
import kotlin.math.min

class AudioLoopbackController(context: Context) {
    private val appContext = context.applicationContext
    private val audioManager = appContext.getSystemService(Context.AUDIO_SERVICE) as AudioManager
    private val mainHandler = Handler(Looper.getMainLooper())
    private val recording = AtomicBoolean(false)
    private val playing = AtomicBoolean(false)
    private var recorder: AudioRecord? = null
    private var player: AudioTrack? = null

    fun refreshDiagnostics(): AudioDiagnostics {
        val inputs = audioManager.getDevices(AudioManager.GET_DEVICES_INPUTS)
            .map { AudioDeviceDescriptor.from(it) }
        val outputs = audioManager.getDevices(AudioManager.GET_DEVICES_OUTPUTS)
            .map { AudioDeviceDescriptor.from(it) }
        return AudioDiagnostics(
            inputs = inputs,
            outputs = outputs,
            preferredInput = AudioRoutePolicy.choosePreferredInput(inputs),
            preferredOutput = AudioRoutePolicy.choosePreferredOutput(outputs)
        )
    }

    @SuppressLint("MissingPermission")
    fun startRecording(
        maxSeconds: Int,
        onLevel: (Int, Long) -> Unit,
        onComplete: (PcmAudio) -> Unit,
        onError: (String) -> Unit
    ) {
        if (!recording.compareAndSet(false, true)) {
            onError("recording already active")
            return
        }

        Thread {
            val sampleRate = SAMPLE_RATE
            val channelConfig = AudioFormat.CHANNEL_IN_MONO
            val audioFormat = AudioFormat.ENCODING_PCM_16BIT
            val minBuffer = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat)
            if (minBuffer <= 0) {
                recording.set(false)
                postError(onError, "invalid recorder buffer: $minBuffer")
                return@Thread
            }

            val bufferSize = minBuffer.coerceAtLeast(sampleRate / 2)
            val maxBytes = sampleRate * BYTES_PER_SAMPLE * maxSeconds.coerceIn(1, MAX_RECORD_SECONDS)
            val buffer = ByteArray(bufferSize)
            val output = ByteArrayOutputStream(maxBytes)
            var record: AudioRecord? = null

            try {
                val input = refreshDiagnostics().preferredInput
                record = AudioRecord.Builder()
                    .setAudioSource(MediaRecorder.AudioSource.VOICE_RECOGNITION)
                    .setAudioFormat(
                        AudioFormat.Builder()
                            .setEncoding(audioFormat)
                            .setSampleRate(sampleRate)
                            .setChannelMask(channelConfig)
                            .build()
                    )
                    .setBufferSizeInBytes(bufferSize)
                    .build()

                input?.let { preferred ->
                    val device = audioManager.getDevices(AudioManager.GET_DEVICES_INPUTS)
                        .firstOrNull { it.id == preferred.id }
                    if (device != null) {
                        record.preferredDevice = device
                    }
                }

                if (record.state != AudioRecord.STATE_INITIALIZED) {
                    throw IllegalStateException("AudioRecord is not initialized")
                }
                recorder = record
                record.startRecording()

                while (recording.get() && output.size() < maxBytes) {
                    val remaining = maxBytes - output.size()
                    val read = record.read(buffer, 0, min(buffer.size, remaining))
                    if (read > 0) {
                        output.write(buffer, 0, read)
                        postLevel(onLevel, peakLevel(buffer, read), output.size().toLong() * 1000L / (sampleRate * BYTES_PER_SAMPLE))
                    } else if (read < 0) {
                        throw IllegalStateException("AudioRecord read failed: $read")
                    }
                }

                val pcm = PcmAudio(output.toByteArray(), sampleRate, 1, 16)
                mainHandler.post { onComplete(pcm) }
            } catch (error: Throwable) {
                postError(onError, error.message ?: error.javaClass.simpleName)
            } finally {
                recording.set(false)
                try {
                    record?.stop()
                } catch (_: IllegalStateException) {
                }
                record?.release()
                if (recorder === record) {
                    recorder = null
                }
            }
        }.apply {
            name = "kiosk-audio-recorder"
            start()
        }
    }

    fun stopRecording() {
        recording.set(false)
    }

    fun play(
        pcm: PcmAudio,
        onComplete: () -> Unit,
        onError: (String) -> Unit
    ) {
        if (!pcm.isPlayable) {
            onError("no playable recording")
            return
        }
        if (!playing.compareAndSet(false, true)) {
            onError("playback already active")
            return
        }

        Thread {
            var track: AudioTrack? = null
            try {
                val minBuffer = AudioTrack.getMinBufferSize(
                    pcm.sampleRate,
                    AudioFormat.CHANNEL_OUT_MONO,
                    AudioFormat.ENCODING_PCM_16BIT
                )
                val bufferSize = minBuffer.coerceAtLeast(pcm.bytes.size)
                track = AudioTrack.Builder()
                    .setAudioAttributes(
                        AudioAttributes.Builder()
                            .setUsage(AudioAttributes.USAGE_MEDIA)
                            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                            .build()
                    )
                    .setAudioFormat(
                        AudioFormat.Builder()
                            .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                            .setSampleRate(pcm.sampleRate)
                            .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                            .build()
                    )
                    .setBufferSizeInBytes(bufferSize)
                    .setTransferMode(AudioTrack.MODE_STREAM)
                    .build()

                refreshDiagnostics().preferredOutput?.let { preferred ->
                    val device = audioManager.getDevices(AudioManager.GET_DEVICES_OUTPUTS)
                        .firstOrNull { it.id == preferred.id }
                    if (device != null) {
                        track.preferredDevice = device
                    }
                }

                player = track
                track.play()
                var offset = 0
                while (offset < pcm.bytes.size && playing.get()) {
                    val written = track.write(pcm.bytes, offset, pcm.bytes.size - offset)
                    if (written < 0) {
                        throw IllegalStateException("AudioTrack write failed: $written")
                    }
                    offset += written
                }
                track.stop()
                mainHandler.post { onComplete() }
            } catch (error: Throwable) {
                postError(onError, error.message ?: error.javaClass.simpleName)
            } finally {
                playing.set(false)
                track?.release()
                if (player === track) {
                    player = null
                }
            }
        }.apply {
            name = "kiosk-audio-player"
            start()
        }
    }

    fun shutdown() {
        recording.set(false)
        playing.set(false)
        try {
            recorder?.stop()
        } catch (_: IllegalStateException) {
        }
        recorder?.release()
        recorder = null
        try {
            player?.stop()
        } catch (_: IllegalStateException) {
        }
        player?.release()
        player = null
    }

    private fun postLevel(callback: (Int, Long) -> Unit, level: Int, elapsedMillis: Long) {
        mainHandler.post { callback(level, elapsedMillis) }
    }

    private fun postError(callback: (String) -> Unit, message: String) {
        mainHandler.post { callback(message) }
    }

    private fun peakLevel(buffer: ByteArray, read: Int): Int {
        var peak = 0
        var i = 0
        while (i + 1 < read) {
            val sample = (buffer[i].toInt() and 0xff) or (buffer[i + 1].toInt() shl 8)
            peak = maxOf(peak, abs(sample))
            i += 2
        }
        return ((peak / 32767f) * 100).toInt().coerceIn(0, 100)
    }

    companion object {
        const val SAMPLE_RATE = 16000
        const val BYTES_PER_SAMPLE = 2
        const val MAX_RECORD_SECONDS = 10
    }
}
