package ai.jiyangjia.kiosk

import android.media.AudioDeviceInfo

data class AudioDeviceDescriptor(
    val id: Int,
    val type: Int,
    val productName: String,
    val isInput: Boolean,
    val isOutput: Boolean
) {
    val typeName: String = audioDeviceTypeName(type)
    val isUsbInput: Boolean =
        isInput && type in setOf(
            AudioDeviceInfo.TYPE_USB_ACCESSORY,
            AudioDeviceInfo.TYPE_USB_DEVICE,
            AudioDeviceInfo.TYPE_USB_HEADSET
        )

    val isPreferredOutput: Boolean =
        isOutput && type in setOf(
            AudioDeviceInfo.TYPE_BUILTIN_SPEAKER,
            AudioDeviceInfo.TYPE_USB_DEVICE,
            AudioDeviceInfo.TYPE_USB_HEADSET,
            AudioDeviceInfo.TYPE_WIRED_HEADPHONES,
            AudioDeviceInfo.TYPE_WIRED_HEADSET
        )

    fun shortLine(): String {
        val roles = listOfNotNull(
            if (isInput) "input" else null,
            if (isOutput) "output" else null
        ).joinToString("+")
        return "#$id $roles $typeName $productName"
    }

    companion object {
        fun from(info: AudioDeviceInfo): AudioDeviceDescriptor =
            AudioDeviceDescriptor(
                id = info.id,
                type = info.type,
                productName = info.productName?.toString().orEmpty().ifBlank { "unknown" },
                isInput = info.isSource,
                isOutput = info.isSink
            )
    }
}

fun audioDeviceTypeName(type: Int): String =
    when (type) {
        AudioDeviceInfo.TYPE_BUILTIN_EARPIECE -> "BUILTIN_EARPIECE"
        AudioDeviceInfo.TYPE_BUILTIN_SPEAKER -> "BUILTIN_SPEAKER"
        AudioDeviceInfo.TYPE_WIRED_HEADSET -> "WIRED_HEADSET"
        AudioDeviceInfo.TYPE_WIRED_HEADPHONES -> "WIRED_HEADPHONES"
        AudioDeviceInfo.TYPE_LINE_ANALOG -> "LINE_ANALOG"
        AudioDeviceInfo.TYPE_LINE_DIGITAL -> "LINE_DIGITAL"
        AudioDeviceInfo.TYPE_BLUETOOTH_SCO -> "BLUETOOTH_SCO"
        AudioDeviceInfo.TYPE_BLUETOOTH_A2DP -> "BLUETOOTH_A2DP"
        AudioDeviceInfo.TYPE_HDMI -> "HDMI"
        AudioDeviceInfo.TYPE_HDMI_ARC -> "HDMI_ARC"
        AudioDeviceInfo.TYPE_USB_ACCESSORY -> "USB_ACCESSORY"
        AudioDeviceInfo.TYPE_USB_DEVICE -> "USB_DEVICE"
        AudioDeviceInfo.TYPE_USB_HEADSET -> "USB_HEADSET"
        AudioDeviceInfo.TYPE_BUILTIN_MIC -> "BUILTIN_MIC"
        AudioDeviceInfo.TYPE_TELEPHONY -> "TELEPHONY"
        AudioDeviceInfo.TYPE_AUX_LINE -> "AUX_LINE"
        AudioDeviceInfo.TYPE_IP -> "IP"
        AudioDeviceInfo.TYPE_BUS -> "BUS"
        AudioDeviceInfo.TYPE_HEARING_AID -> "HEARING_AID"
        else -> "TYPE_$type"
    }
