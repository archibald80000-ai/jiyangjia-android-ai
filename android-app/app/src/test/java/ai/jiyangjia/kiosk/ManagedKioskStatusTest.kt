package ai.jiyangjia.kiosk

import org.junit.Assert.assertEquals
import org.junit.Test

class ManagedKioskStatusTest {
    @Test
    fun onlyConfirmedLockedDeviceOwnerReportsManagedMode() {
        assertEquals("managed_locked", ManagedKioskStatus(true, true, true, true).mode)
        assertEquals("limited_unmanaged", ManagedKioskStatus(true, true, false, true).mode)
        assertEquals("limited_unmanaged", ManagedKioskStatus(false, false, false, false).mode)
    }
}
