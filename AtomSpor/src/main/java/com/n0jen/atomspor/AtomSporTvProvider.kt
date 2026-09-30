package com.n0jen.atomspor

import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.ExtractorLink
import com.lagradost.cloudstream3.utils.Qualities

class AtomSporTvProvider : MainAPI() {
    override var mainUrl = "https://atomsportv492.top"
    override var name = "AtomSporTV"
    override val hasMainPage = true
    override var lang = "tr"
    override val hasDownloadSupport = false
    override val supportedTypes = setOf(TvType.Live)

    private val startUrl = "https://url24.link/AtomSporTV"
    private val matchesUrl = "https://teletv3.top/load/matches.php"
    private val logoBase = "https://im.mackolik.com/img/logo/buyuk"

    private val skipWords = setOf("futbol", "futbol tr", "futboi", "günün maçı")

    private val tvChannels = listOf(
        Triple("bein-sports-1", "BEIN SPORTS 1", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/BeIN_Sports_1_HD.svg/200px-BeIN_Sports_1_HD.svg.png"),
        Triple("bein-sports-2", "BEIN SPORTS 2", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/BeIN_Sports_2_HD.svg/200px-BeIN_Sports_2_HD.svg.png"),
        Triple("bein-sports-3", "BEIN SPORTS 3", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/BeIN_Sports_3_HD.svg/200px-BeIN_Sports_3_HD.svg.png"),
        Triple("bein-sports-4", "BEIN SPORTS 4", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/BeIN_Sports_4_HD.svg/200px-BeIN_Sports_4_HD.svg.png"),
        Triple("s-sport", "S SPORT", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/S_Sport_logo.svg/200px-S_Sport_logo.svg.png"),
        Triple("s-sport-2", "S SPORT 2", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/S_Sport_logo.svg/200px-S_Sport_logo.svg.png"),
        Triple("trt-spor", "TRT SPOR", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/TRT_Spor_logo.svg/200px-TRT_Spor_logo.svg.png"),
        Triple("aspor", "ASPOR", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/A_Spor_logo.svg/200px-A_Spor_logo.svg.png")
    )

    private suspend fun getDynamicDomain(): String {
        try {
            val r1 = app.get(startUrl, allowRedirects = false)
            val loc1 = r1.headers["location"] ?: return mainUrl
            val r2 = app.get(loc1, allowRedirects = false)
            val loc2 = r2.headers["location"] ?: return mainUrl
            mainUrl = loc2.trim().removeSuffix("/")
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return mainUrl
    }

    private fun normalizeLogo(src: String): String {
        if (src.isEmpty()) return ""
        if (src.startsWith("http")) return src
        if (src.startsWith("//")) return "https:$src"
        return "$logoBase/${src.trimStart('/')}"
    }

    override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse {
        val domain = getDynamicDomain()
        val items = mutableListOf<HomePageList>()

        try {
            val doc = app.get(matchesUrl).document
            val matchElements = doc.select("a[href*=matches?id=]")
            
            val matchesList = matchElements.mapNotNull { a ->
                val href = a.attr("href")
                val idMatch = """matches\?id=([a-f0-9]+)""".toRegex().find(href)
                val id = idMatch?.groupValues?.get(1) ?: return@mapNotNull null

                val imgs = a.select("img")
                val homeLogo = if (imgs.isNotEmpty()) normalizeLogo(imgs[0].attr("src")) else ""
                val awayLogo = if (imgs.size > 1) normalizeLogo(imgs[1].attr("src")) else ""
                val poster = homeLogo.ifEmpty { awayLogo }

                val lines = a.wholeText().lines()
                    .map { it.trim() }
                    .filter { it.isNotEmpty() && !skipWords.contains(it.lowercase()) }

                var saat = ""
                var lig = ""
                var homeTeam = ""
                var awayTeam = ""

                for (line in lines) {
                    if (line.contains("|") && saat.isEmpty()) {
                        val parts = line.split("|", limit = 2)
                        saat = parts[0].trim()
                        lig = parts.getOrNull(1)?.trim() ?: ""
                    } else if (saat.isNotEmpty() && homeTeam.isEmpty()) {
                        homeTeam = line
                    } else if (saat.isNotEmpty() && homeTeam.isNotEmpty() && awayTeam.isEmpty()) {
                        awayTeam = line
                    }
                }

                val fallbackHome = homeTeam.ifEmpty { "Ev Sahibi" }
                val fallbackAway = awayTeam.ifEmpty { "Deplasman" }
                val title = "$fallbackHome - $fallbackAway [$saat]"
                
                LiveSearchResponse(
                    name = title,
                    url = "$domain/matches?id=$id",
                    apiName = this@AtomSporTvProvider.name,
                    type = TvType.Live,
                    posterUrl = poster,
                    lang = "tr"
                )
            }
            
            if (matchesList.isNotEmpty()) {
                items.add(HomePageList("Canlı Maçlar", matchesList))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        val channelsList = tvChannels.map { (id, name, logo) ->
            LiveSearchResponse(
                name = name,
                url = "$domain/matches?id=$id",
                apiName = this@AtomSporTvProvider.name,
                type = TvType.Live,
                posterUrl = logo,
                lang = "tr"
            )
        }
        items.add(HomePageList("TV Kanalları", channelsList))

        return HomePageResponse(items)
    }

    override suspend fun load(url: String): LoadResponse {
        return LiveStreamLoadResponse(
            name = "Canlı Yayın",
            url = url,
            apiName = this.name,
            dataUrl = url
        )
    }

    override suspend fun loadLinks(
        data: String,
        isCasting: Boolean,
        callback: (ExtractorLink) -> Unit
    ): Boolean {
        val domain = getDynamicDomain()
        val idMatch = """id=([a-f0-9\-a-z]+)""".toRegex().find(data)
        val id = idMatch?.groupValues?.get(1) ?: return false

        try {
            val pageHtml = app.get(data, headers = mapOf("Referer" to "$domain/")).text
            
            val fetchRegex = """fetch\(\s*["']([^"']+)["']""".toRegex()
            val fetchMatch = fetchRegex.find(pageHtml) ?: return false
            var fetchUrl = fetchMatch.groupValues[1].trim()
            
            if (!fetchUrl.endsWith(id)) {
                fetchUrl += id
            }

            val apiData = app.get(fetchUrl, headers = mapOf("Origin" to domain)).text

            val patterns = listOf(
                """"deismackanal"\s*:\s*"(.*?)"""".toRegex(),
                """"stream"\s*:\s*"(.*?)"""".toRegex(),
                """"url"\s*:\s*"(.*?\.m3u8[^"]*)"""".toRegex(),
                """(https?://[^\s"']+\.m3u8[^\s"']*)""".toRegex()
            )

            var m3u8Link: String? = null
            for (pattern in patterns) {
                val match = pattern.find(apiData)
                if (match != null) {
                    m3u8Link = match.groupValues[1].replace("\\/", "/").replace("\\", "")
                    break
                }
            }

            if (!m3u8Link.isNullOrEmpty()) {
                callback.invoke(
                    ExtractorLink(
                        source = this.name,
                        name = "AtomSpor Stream",
                        url = m3u8Link,
                        referer = "$domain/",
                        quality = Qualities.Unknown.value,
                        isM3u8 = true
                    )
                )
                return true
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        return false
    }
}