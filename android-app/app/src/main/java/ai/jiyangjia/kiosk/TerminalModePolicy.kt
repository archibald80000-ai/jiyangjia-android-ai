package ai.jiyangjia.kiosk

data class TerminalModePolicy(val storeKiosk: Boolean) {
    val keepScreenOn: Boolean = storeKiosk
    val immersive: Boolean = storeKiosk
    val managedKiosk: Boolean = storeKiosk
    val selfUpdate: Boolean = storeKiosk
}
