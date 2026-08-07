package ai.jiyangjia.kiosk

import android.app.Activity
import android.app.ActivityManager
import android.app.admin.DevicePolicyManager
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Build

data class ManagedKioskStatus(
    val deviceOwner: Boolean,
    val lockTaskPermitted: Boolean,
    val lockTaskLocked: Boolean,
    val persistentHomeConfigured: Boolean,
    val error: String? = null
) {
    val mode: String = if (deviceOwner && lockTaskPermitted && lockTaskLocked) "managed_locked" else "limited_unmanaged"
}

class ManagedKioskController(private val activity: Activity) {
    private val policy = activity.getSystemService(Context.DEVICE_POLICY_SERVICE) as DevicePolicyManager
    private val activityManager = activity.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
    private val admin = ComponentName(activity, KioskDeviceAdminReceiver::class.java)
    private val kioskActivity = ComponentName(activity, KioskActivity::class.java)

    fun configureAndEnter(): ManagedKioskStatus {
        val isOwner = policy.isDeviceOwnerApp(activity.packageName)
        var homeConfigured = false
        var failure: String? = null
        runCatching {
            if (isOwner) {
                policy.setLockTaskPackages(admin, arrayOf(activity.packageName))
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                    policy.setLockTaskFeatures(admin, DevicePolicyManager.LOCK_TASK_FEATURE_NONE)
                }
                policy.setStatusBarDisabled(admin, true)
                val homeFilter = IntentFilter(Intent.ACTION_MAIN).apply {
                    addCategory(Intent.CATEGORY_HOME)
                    addCategory(Intent.CATEGORY_DEFAULT)
                }
                policy.addPersistentPreferredActivity(admin, homeFilter, kioskActivity)
                homeConfigured = true
            }
        }.onFailure { failure = it.javaClass.simpleName }
        val permitted = policy.isLockTaskPermitted(activity.packageName)
        runCatching {
            if (permitted && activityManager.lockTaskModeState != ActivityManager.LOCK_TASK_MODE_LOCKED) activity.startLockTask()
        }.onFailure { failure = it.javaClass.simpleName }
        return ManagedKioskStatus(
            deviceOwner = isOwner,
            lockTaskPermitted = permitted,
            lockTaskLocked = activityManager.lockTaskModeState == ActivityManager.LOCK_TASK_MODE_LOCKED,
            persistentHomeConfigured = homeConfigured,
            error = failure
        )
    }
}
