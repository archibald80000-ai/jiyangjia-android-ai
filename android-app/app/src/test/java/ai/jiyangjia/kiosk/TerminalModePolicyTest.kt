package ai.jiyangjia.kiosk

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class TerminalModePolicyTest {
    @Test
    fun phoneDemoKeepsSystemNavigationAvailable() {
        val policy = TerminalModePolicy(storeKiosk = false)

        assertFalse(policy.keepScreenOn)
        assertFalse(policy.immersive)
        assertFalse(policy.managedKiosk)
        assertFalse(policy.selfUpdate)
    }

    @Test
    fun storeKioskRetainsManagedTerminalCapabilities() {
        val policy = TerminalModePolicy(storeKiosk = true)

        assertTrue(policy.keepScreenOn)
        assertTrue(policy.immersive)
        assertTrue(policy.managedKiosk)
        assertTrue(policy.selfUpdate)
    }
}
