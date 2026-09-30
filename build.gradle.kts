buildscript {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
    dependencies {
        classpath("com.android.tools.build:gradle:7.4.2")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.20")
        // DÜZELTME: JitPack'in metadata hatasını aşmak için master-master-SNAPSHOT kullanıyoruz
        classpath("com.github.recloudstream:gradle:master-master-SNAPSHOT")
    }
}

apply(plugin = "com.android.library")
apply(plugin = "kotlin-android")
apply(plugin = "com.lagradost.cloudstream3.gradle")

cloudstream {
    pluginName = "N0JEN Sync"
    pluginAuthor = "N0jen"
    pluginDescription = "AtomSpor canlı maç ve TV yayınları"
    pluginVersion = 1
    pluginTypes = listOf("tv")
}

android {
    namespace = "com.n0jensync"
    compileSdk = 33
    defaultConfig {
        minSdk = 21
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
}

repositories {
    google()
    mavenCentral()
    maven("https://jitpack.io")
}

dependencies {
    // DÜZELTME: Aynı sorunu burada da yaşamamak için burayı da güncelledik
    implementation("com.github.recloudstream:Cloudstream:master-master-SNAPSHOT")
    implementation("org.jsoup:jsoup:1.15.3")
}
