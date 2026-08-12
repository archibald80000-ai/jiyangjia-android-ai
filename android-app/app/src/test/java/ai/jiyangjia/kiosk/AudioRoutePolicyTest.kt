package ai.jiyangjia.kiosk

import android.media.AudioDeviceInfo
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class AudioRoutePolicyTest {
    @Test
    fun usbInputIsPreferredOverBuiltInMic() {
        val builtIn = AudioDeviceDescriptor(1, AudioDeviceInfo.TYPE_BUILTIN_MIC, "built-in", isInput = true, isOutput = false)
        val usb = AudioDeviceDescriptor(2, AudioDeviceInfo.TYPE_USB_DEVICE, "usb mic", isInput = true, isOutput = false)

        assertEquals(usb, AudioRoutePolicy.choosePreferredInput(listOf(builtIn, usb)))
    }

    @Test
    fun fallsBackToFirstInputWhenUsbIsAbsent() {
        val builtIn = AudioDeviceDescriptor(1, AudioDeviceInfo.TYPE_BUILTIN_MIC, "built-in", isInput = true, isOutput = false)

        assertEquals(builtIn, AudioRoutePolicy.choosePreferredInput(listOf(builtIn)))
        assertNull(AudioRoutePolicy.choosePreferredInput(emptyList()))
    }

    @Test
    fun diagnosticsSummarizeInputsAndOutputs() {
        val devices = listOf(
            AudioDeviceDescriptor(1, AudioDeviceInfo.TYPE_BUILTIN_MIC, "built-in", isInput = true, isOutput = false),
            AudioDeviceDescriptor(2, AudioDeviceInfo.TYPE_BUILTIN_SPEAKER, "speaker", isInput = false, isOutput = true)
        )

        val diagnostics = AudioRoutePolicy.buildDiagnostics(devices)

        assertEquals(1, diagnostics.inputs.size)
        assertEquals(1, diagnostics.outputs.size)
        assertTrue(diagnostics.summary().contains("Inputs: 1 Outputs: 1"))
    }

    @Test
    fun automaticBargeInRequiresUsbInput() {
        val builtIn = AudioDeviceDescriptor(1, AudioDeviceInfo.TYPE_BUILTIN_MIC, "built-in", isInput = true, isOutput = false)
        val usb = AudioDeviceDescriptor(2, AudioDeviceInfo.TYPE_USB_DEVICE, "usb mic", isInput = true, isOutput = false)

        assertTrue(AudioRoutePolicy.supportsAutomaticBargeIn(listOf(builtIn, usb)))
        assertEquals(false, AudioRoutePolicy.supportsAutomaticBargeIn(listOf(builtIn)))
    }
}
