package ai.jiyangjia.kiosk

import android.content.Context
import androidx.work.Worker
import androidx.work.WorkerParameters

class ContentSyncWorker(appContext: Context, workerParameters: WorkerParameters) : Worker(appContext, workerParameters) {
    override fun doWork(): Result {
        val config = loadConfig(applicationContext)
        var result: ContentSyncResult? = null
        val metrics = applicationContext.resources.displayMetrics
        val manager = ContentSyncManager(
            context = applicationContext,
            baseUrl = { config.gatewayBaseUrl },
            metrics = {
                Triple(metrics.widthPixels, metrics.heightPixels, if (metrics.widthPixels >= metrics.heightPixels) "landscape" else "portrait")
            },
            onResult = { result = it }
        )
        result = manager.syncOnce()
        return if (result is ContentSyncResult.Failed) Result.retry() else Result.success()
    }

    private fun loadConfig(context: Context): ClientConfig {
        val preferences = context.getSharedPreferences("kiosk_config", Context.MODE_PRIVATE)
        return ClientConfig.fromValues(
            gatewayBaseUrl = preferences.getString("gateway", null),
            deviceId = preferences.getString("device_id", null),
            displayMode = preferences.getString("display_mode", null),
            maxRecordSeconds = preferences.getInt("max_record_seconds", 20),
            idleVideoPath = preferences.getString("idle_video_path", null)
        )
    }
}
