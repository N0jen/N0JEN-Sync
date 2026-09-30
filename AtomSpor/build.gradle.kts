import com.lagradost.cloudstream3.plugins.CloudstreamPluginConfiguration

apply(plugin = "com.lagradost.cloudstream3.plugins")

configure<CloudstreamPluginConfiguration> {
    name = "AtomSporTV"
    description = "AtomSporTV Canlı Maç ve TV Kanalları"
    authors = listOf("N0jen")
    version = 1
    tvTypes = listOf("Live")
}
