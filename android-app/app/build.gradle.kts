plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

fun secretValue(property: String, environment: String = property): String? =
    providers.gradleProperty(property).orNull ?: System.getenv(environment)

fun quotedBuildConfig(value: String): String =
    "\"${value.replace("\\", "\\\\").replace("\"", "\\\"")}\""

val releaseRequested = gradle.startParameter.taskNames.any { it.contains("release", ignoreCase = true) }
val controlledVersionCode = secretValue("JIYANGJIA_VERSION_CODE")?.toIntOrNull()
val controlledVersionName = secretValue("JIYANGJIA_VERSION_NAME")
val signingStoreFile = secretValue("JIYANGJIA_SIGNING_STORE_FILE")
val signingStorePassword = secretValue("JIYANGJIA_SIGNING_STORE_PASSWORD")
val signingKeyAlias = secretValue("JIYANGJIA_SIGNING_KEY_ALIAS")
val signingKeyPassword = secretValue("JIYANGJIA_SIGNING_KEY_PASSWORD")
val signingReady = listOf(signingStoreFile, signingStorePassword, signingKeyAlias, signingKeyPassword).all { !it.isNullOrBlank() }
val productionGatewayBaseUrl = "https://ai-jiyangjia.cloud"
val developmentGatewayBaseUrl = secretValue("JIYANGJIA_GATEWAY_BASE_URL")
    ?.trim()
    ?.trimEnd('/')
    ?.takeIf { it.isNotEmpty() }
    ?: productionGatewayBaseUrl
val developmentAllowsCleartext = secretValue("JIYANGJIA_ALLOW_CLEARTEXT_GATEWAY")
    ?.equals("true", ignoreCase = true)
    ?: false

if (releaseRequested) {
    require(controlledVersionCode != null && controlledVersionCode > 0) { "Release requires positive JIYANGJIA_VERSION_CODE" }
    require(!controlledVersionName.isNullOrBlank()) { "Release requires JIYANGJIA_VERSION_NAME" }
    require(signingReady) { "Release requires JIYANGJIA_SIGNING_STORE_FILE/PASSWORD and KEY_ALIAS/PASSWORD" }
}

android {
    namespace = "ai.jiyangjia.kiosk"
    compileSdk = 35

    defaultConfig {
        applicationId = "ai.jiyangjia.kiosk"
        minSdk = 23
        targetSdk = 35
        versionCode = controlledVersionCode ?: 9
        versionName = controlledVersionName ?: "0.1.8"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        buildConfigField("String", "GATEWAY_BOOTSTRAP_URL", quotedBuildConfig(productionGatewayBaseUrl))
        buildConfigField("boolean", "ALLOW_CLEARTEXT_GATEWAY", "false")
        manifestPlaceholders["usesCleartextTraffic"] = "false"
    }

    flavorDimensions += "terminalMode"
    productFlavors {
        create("phoneDemo") {
            dimension = "terminalMode"
            applicationIdSuffix = ".debug"
            buildConfigField("boolean", "STORE_KIOSK", "false")
        }
        create("storeKiosk") {
            dimension = "terminalMode"
            applicationIdSuffix = ".store"
            buildConfigField("boolean", "STORE_KIOSK", "true")
        }
    }

    signingConfigs {
        if (signingReady) {
            create("controlledRelease") {
                storeFile = file(requireNotNull(signingStoreFile))
                storePassword = signingStorePassword
                keyAlias = signingKeyAlias
                keyPassword = signingKeyPassword
                enableV1Signing = true
                enableV2Signing = true
                enableV3Signing = true
            }
        }
    }

    buildTypes {
        debug {
            buildConfigField("String", "GATEWAY_BOOTSTRAP_URL", quotedBuildConfig(developmentGatewayBaseUrl))
            buildConfigField("boolean", "ALLOW_CLEARTEXT_GATEWAY", developmentAllowsCleartext.toString())
            manifestPlaceholders["usesCleartextTraffic"] = developmentAllowsCleartext.toString()
        }
        release {
            isMinifyEnabled = false
            buildConfigField("String", "GATEWAY_BOOTSTRAP_URL", quotedBuildConfig(productionGatewayBaseUrl))
            buildConfigField("boolean", "ALLOW_CLEARTEXT_GATEWAY", "false")
            manifestPlaceholders["usesCleartextTraffic"] = "false"
            signingConfig = signingConfigs.findByName("controlledRelease")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    buildFeatures {
        buildConfig = true
    }
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    implementation("androidx.media3:media3-exoplayer:1.5.1")
    implementation("androidx.media3:media3-ui:1.5.1")
    implementation("androidx.work:work-runtime:2.9.1")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.json:json:20240303")
    testImplementation("com.squareup.okhttp3:mockwebserver:4.12.0")
    androidTestImplementation("androidx.test:core:1.6.1")
    androidTestImplementation("androidx.test:runner:1.6.2")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
}
