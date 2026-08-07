package ai.jiyangjia.kiosk

data class ClientConfig(
    val gatewayBaseUrl: String,
    val deviceId: String,
    val displayMode: String,
    val maxRecordSeconds: Int,
    val idleVideoPath: String
) {
    fun sanitizedSummary(): String =
        "gateway=$gatewayBaseUrl device=$deviceId mode=$displayMode maxRecordSeconds=$maxRecordSeconds"

    companion object {
        val DEFAULT_GATEWAY: String = BuildConfig.GATEWAY_BOOTSTRAP_URL
        const val DEFAULT_DEVICE_ID = "android-kiosk-dev"
        const val DISPLAY_MODE_IDLE_VIDEO_VOICE = "idle_video_voice"

        fun fromValues(
            gatewayBaseUrl: String?,
            deviceId: String?,
            displayMode: String?,
            maxRecordSeconds: Int?,
            idleVideoPath: String?
        ): ClientConfig {
            val normalizedGateway = gatewayBaseUrl?.trim()?.trimEnd('/').orEmpty()
                .ifBlank { DEFAULT_GATEWAY }
            require(
                normalizedGateway.isBlank() ||
                    BuildConfig.ALLOW_CLEARTEXT_GATEWAY ||
                    normalizedGateway.startsWith("https://")
            ) { "Release gateway URL must use HTTPS" }
            val normalizedDeviceId = deviceId?.trim().orEmpty()
                .ifBlank { DEFAULT_DEVICE_ID }
            val normalizedMode = displayMode?.trim().orEmpty()
                .ifBlank { DISPLAY_MODE_IDLE_VIDEO_VOICE }
            val boundedRecordSeconds = (maxRecordSeconds ?: 20).coerceIn(3, 60)

            return ClientConfig(
                gatewayBaseUrl = normalizedGateway,
                deviceId = normalizedDeviceId,
                displayMode = normalizedMode,
                maxRecordSeconds = boundedRecordSeconds,
                idleVideoPath = idleVideoPath?.trim().orEmpty()
            )
        }
    }
}
