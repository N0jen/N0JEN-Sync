// DÜZELTME 1: Kotlin'in bu kelimeleri tanıması için yollarını içe aktarıyoruz
import com.android.build.gradle.LibraryExtension
import com.lagradost.cloudstream3.gradle.CloudstreamExtension

buildscript {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io") {
            metadataSources {
                artifact()
            }
        }
    }
    dependencies {
        classpath("com.android.tools.build:gradle:7.4.2")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.20")
        classpath("com.github.recloudstream:gradle:master-SNAPSHOT")
    }
}

apply(plugin = "com.android.library")
apply(plugin = "kotlin-android")
apply(plugin = "com.lagradost.cloudstream3.gradle")

// DÜZELTME 2: Kotlin'e cloudstream bloğunu açıkça yapılandırıyoruz
configure<CloudstreamExtension> {
    pluginName = "N0JEN Sync"
    pluginAuthor = "N0jen"
    pluginDescription = "AtomSpor canlı maç ve TV yayınları"
    pluginVersion = 1
    pluginTypes = listOf("tv")
}

// DÜZELTME 3: Kotlin'e android bloğunu açıkça yapılandırıyoruz
configure<LibraryExtension> {
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
    maven("https://jitpack.io") {
        metadataSources {
            artifact()
        }
    }
}

// DÜZELTME 4: Kotlin DSL'de apply kullanıldığında implementation yerine add() komutu kullanılır
dependencies {
    add("implementation", "com.github.recloudstream:Cloudstream:master-SNAPSHOT")
    add("implementation", "org.jsoup:jsoup:1.15.3")
    
    add("implementation", "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4")
    add("implementation", "com.fasterxml.jackson.module:jackson-module-kotlin:2.13.1")
}
