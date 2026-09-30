buildscript {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
    dependencies {
        // Jitpack hatasını atlamak için doğrudan hatasız sürümün kodunu kullanıyoruz
        classpath("com.github.recloudstream:gradle:32895aedb6")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.22")
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
}
