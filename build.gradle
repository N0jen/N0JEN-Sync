buildscript {
    repositories {
        google()
        mavenCentral()
        maven { 
            url 'https://jitpack.io' 
            metadataSources {
                artifact()
            }
        }
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.2'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.20'
        classpath 'com.github.recloudstream:gradle:master-SNAPSHOT'
    }
}

apply plugin: 'com.android.library'
apply plugin: 'kotlin-android'
apply plugin: 'com.lagradost.cloudstream3.gradle'

cloudstream {
    pluginName = "N0JEN Sync"
    pluginAuthor = "N0jen"
    pluginDescription = "AtomSpor canlı maç ve TV yayınları"
    pluginVersion = 1
    pluginTypes = ["tv"]
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
    maven { 
        url 'https://jitpack.io' 
        metadataSources {
            artifact()
        }
    }
}

dependencies {
    implementation 'com.github.recloudstream:Cloudstream:master-SNAPSHOT'
    implementation 'org.jsoup:jsoup:1.15.3'
    
    // POM bypass edildiği için Cloudstream'in arayabileceği temel kütüphaneler:
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4'
    implementation 'com.fasterxml.jackson.module:jackson-module-kotlin:2.13.1'
}
