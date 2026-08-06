package ai.jiyangjia.kiosk

enum class ConsultationState {
    BOOT,
    IDLE_VIDEO,
    READY_TO_RECORD,
    RECORDING,
    UPLOADING,
    WAITING_FOR_RESPONSE,
    PLAYING_ANSWER,
    ERROR
}

fun ConsultationState.canStartConsultation(): Boolean =
    this == ConsultationState.IDLE_VIDEO || this == ConsultationState.READY_TO_RECORD || this == ConsultationState.ERROR
