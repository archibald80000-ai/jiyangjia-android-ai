package ai.jiyangjia.kiosk

import org.junit.Assert.assertThrows
import org.junit.Test

class ReleasePolicyTest {
    private val release = ReleaseDescriptor("ai.jiyangjia.kiosk", 2, "1.1", "https://updates.example/app.apk", 100, "AA", "BB", "")
    private val apk = ApkIdentity("ai.jiyangjia.kiosk", 2, "BB")

    @Test
    fun acceptsMatchingNewerRelease() {
        ReleasePolicy.validate(release, 100, "aa", apk, 1, "bb")
    }

    @Test fun rejectsWrongHash() = rejects { ReleasePolicy.validate(release, 100, "CC", apk, 1, "BB") }
    @Test fun rejectsWrongPackage() = rejects { ReleasePolicy.validate(release, 100, "AA", apk.copy(packageName = "bad.package"), 1, "BB") }
    @Test fun rejectsLowerVersion() = rejects { ReleasePolicy.validate(release, 100, "AA", apk.copy(versionCode = 1), 1, "BB") }
    @Test fun rejectsWrongCertificate() = rejects { ReleasePolicy.validate(release, 100, "AA", apk.copy(certificateSha256 = "CC"), 1, "BB") }

    private fun rejects(block: () -> Unit) {
        assertThrows(IllegalArgumentException::class.java, block)
    }
}
