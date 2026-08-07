package ai.jiyangjia.kiosk

import org.junit.Assert.assertThrows
import org.junit.Test

class ReleasePolicyTest {
    private val fileHash = "A".repeat(64)
    private val certificateHash = "B".repeat(64)
    private val release = ReleaseDescriptor("ai.jiyangjia.kiosk", 2, "1.1", "https://updates.example/app.apk", 100, fileHash, certificateHash, "")
    private val apk = ApkIdentity("ai.jiyangjia.kiosk", 2, certificateHash)

    @Test
    fun acceptsMatchingNewerRelease() {
        ReleasePolicy.validate(release, 100, fileHash.lowercase(), apk, 1, certificateHash.lowercase())
    }

    @Test fun rejectsWrongHash() = rejects { ReleasePolicy.validate(release, 100, "C".repeat(64), apk, 1, certificateHash) }
    @Test fun rejectsWrongPackage() = rejects { ReleasePolicy.validate(release, 100, fileHash, apk.copy(packageName = "bad.package"), 1, certificateHash) }
    @Test fun rejectsLowerVersion() = rejects { ReleasePolicy.validate(release, 100, fileHash, apk.copy(versionCode = 1), 1, certificateHash) }
    @Test fun rejectsWrongCertificate() = rejects { ReleasePolicy.validate(release, 100, fileHash, apk.copy(certificateSha256 = "C".repeat(64)), 1, certificateHash) }

    @Test fun rejectsCleartextBeforeDownload() = rejects { ReleasePolicy.validateDescriptor(release.copy(apkUrl = "http://updates.example/app.apk")) }

    private fun rejects(block: () -> Unit) {
        assertThrows(IllegalArgumentException::class.java, block)
    }
}
