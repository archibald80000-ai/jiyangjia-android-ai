package ai.jiyangjia.kiosk

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ConsultationStateTest {
    @Test
    fun onlyRecoverableIdleStatesCanStartConsultation() {
        assertTrue(ConsultationState.IDLE_VIDEO.canStartConsultation())
        assertTrue(ConsultationState.READY_TO_RECORD.canStartConsultation())
        assertTrue(ConsultationState.ERROR.canStartConsultation())

        assertFalse(ConsultationState.BOOT.canStartConsultation())
        assertFalse(ConsultationState.RECORDING.canStartConsultation())
        assertFalse(ConsultationState.UPLOADING.canStartConsultation())
        assertFalse(ConsultationState.WAITING_FOR_RESPONSE.canStartConsultation())
        assertFalse(ConsultationState.PLAYING_ANSWER.canStartConsultation())
    }
}
