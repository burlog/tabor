
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

// Release signing is configured from environment variables so no secrets
// are ever written to disk or committed. Set these when building a release:
//   MPS_STORE_FILE      path to the upload keystore (default: mps-upload.jks)
//   MPS_STORE_PASSWORD  keystore password (required to enable signing)
//   MPS_KEY_ALIAS       key alias (default: mps)
//   MPS_KEY_PASSWORD    key password (default: same as MPS_STORE_PASSWORD)
val storePasswordEnv: String? = System.getenv("MPS_STORE_PASSWORD")
val hasReleaseSigning = !storePasswordEnv.isNullOrBlank()

android {
    namespace = "cz.burlog.tabor.mps"
    compileSdk = 36

    defaultConfig {
        applicationId = "cz.burlog.tabor.mps"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }

    signingConfigs {
        if (hasReleaseSigning) {
            create("release") {
                storeFile = rootProject.file(
                    System.getenv("MPS_STORE_FILE") ?: "mps-upload.jks"
                )
                storePassword = storePasswordEnv
                keyAlias = System.getenv("MPS_KEY_ALIAS") ?: "mps"
                keyPassword = System.getenv("MPS_KEY_PASSWORD") ?: storePasswordEnv
            }
        }
    }

    buildTypes {
        release {
            if (hasReleaseSigning) {
                signingConfig = signingConfigs.getByName("release")
            }
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    buildFeatures {
        viewBinding = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.constraintlayout:constraintlayout:2.2.0")

    testImplementation("junit:junit:4.13.2")
}
