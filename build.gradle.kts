buildscript {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
    dependencies {
        classpath("com.android.tools.build:gradle:7.4.2")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.20")
        
        // DÜZELTME 1: Sonuna @jar ekleyerek JitPack'in hatalı metadata dosyasını (%100) es geçiyoruz.
        classpath("com.github.recloudstream:gradle:master-SNAPSHOT@jar")
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
    // DÜZELTME 2: Sonuna @aar ekleyerek Cloudstream ana kütüphanesini doğrudan çekiyoruz.
    implementation("com.github.recloudstream:Cloudstream:master-SNAPSHOT@aar")
    implementation("org.jsoup:jsoup:1.15.3")
    
    // NOT: Metadata (POM) dosyasını atladığımız için, Cloudstream'in ihtiyaç duyduğu
    // temel Kotlin kütüphanelerini eklentinin çökmemesi için manuel olarak ekliyoruz.
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.13.1")
}
