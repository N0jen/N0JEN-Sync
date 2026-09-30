import com.lagradost.cloudstream3.gradle.CloudstreamExtension

// Güncel Cloudstream kütüphane kimliği
apply(plugin = "com.lagradost.cloudstream3.gradle")

// Sistemin cloudstream ayarlarını hatasız tanıması için zorunlu yapılandırma
configure<CloudstreamExtension> {
    name = "AtomSporTV"
    description = "AtomSporTV Canlı Maç ve TV Kanalları"
    authors = listOf("N0jen")
    version = 1
    tvTypes = listOf("Live")
}
