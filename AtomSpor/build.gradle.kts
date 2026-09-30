plugins {
    id("com.lagradost.cloudstream3.gradle")
}

cloudstream {
    // name = "AtomSporTV" satırını SİLDİK
    description = "AtomSporTV Canlı Maç ve TV Kanalları"
    authors = listOf("N0jen")
    version = 1
    tvTypes = listOf("Live")
}
