package ai.jiyangjia.kiosk

data class AudioDiagnostics(
    val inputs: List<AudioDeviceDescriptor>,
    val outputs: List<AudioDeviceDescriptor>,
    val preferredInput: AudioDeviceDescriptor?,
    val preferredOutput: AudioDeviceDescriptor?
) {
    fun summary(): String {
        val input = preferredInput?.shortLine() ?: "no input"
        val output = preferredOutput?.shortLine() ?: "no output"
        return "Audio input: $input\nAudio output: $output\nInputs: ${inputs.size} Outputs: ${outputs.size}"
    }

    fun detailedLines(): List<String> =
        buildList {
            add(summary())
            inputs.forEach { add("IN  ${it.shortLine()}") }
            outputs.forEach { add("OUT ${it.shortLine()}") }
        }
}

object AudioRoutePolicy {
    fun buildDiagnostics(devices: List<AudioDeviceDescriptor>): AudioDiagnostics {
        val inputs = devices.filter { it.isInput }
        val outputs = devices.filter { it.isOutput }
        return AudioDiagnostics(
            inputs = inputs,
            outputs = outputs,
            preferredInput = choosePreferredInput(inputs),
            preferredOutput = choosePreferredOutput(outputs)
        )
    }

    fun choosePreferredInput(inputs: List<AudioDeviceDescriptor>): AudioDeviceDescriptor? =
        inputs.firstOrNull { it.isUsbInput } ?: inputs.firstOrNull()

    fun choosePreferredOutput(outputs: List<AudioDeviceDescriptor>): AudioDeviceDescriptor? =
        outputs.firstOrNull { it.isPreferredOutput } ?: outputs.firstOrNull()

    fun supportsAutomaticBargeIn(inputs: List<AudioDeviceDescriptor>): Boolean =
        choosePreferredInput(inputs)?.isUsbInput == true
}
