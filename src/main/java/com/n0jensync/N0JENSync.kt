package com.n0jensync

import android.content.Context
import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*
import com.lagradost.cloudstream3.plugins.CloudstreamPlugin
import com.lagradost.cloudstream3.plugins.Plugin

@CloudstreamPlugin
class N0JENSyncPlugin : Plugin() {
    override fun load(context: Context) {
        registerMainAPI(AtomSporProvider())
    }
}

class AtomSporProvider : MainAPI() {
    override var mainUrl = "https://atomsportv492.top"
    override var name = "N0JEN Sync"
    override val hasMainPage = true
    override var lang = "tr"
    override val supportedTypes = setOf(TvType.Live)

    private val matchesUrl = "https://teletv3.top/load/matches.php"
    private val startUrl = "https://url24.link/AtomSporTV"
    private val logoBase = "https://im.mackolik.com/img/logo/buyuk"

    private fun normalizeLogo(src: String?): String {
        if (src.isNullOrEmpty()) return ""
        if (src.startsWith("http")) return src
        if (src.startsWith("//")) return "https:$src"
        return "$logoBase/${src.trimStart('/')}"
    }

    private suspend fun getBaseDomain(): String {
        return try {
            app.get(startUrl, allowRedirects = true).url.trimEnd('/')
        } catch (e: Exception) {
            mainUrl
        }
    }

    override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse {
        val items = mutableListOf<HomePageList>()
        val matchItems = mutableListOf<SearchResponse>()
        
        try {
            val doc = app.get(matchesUrl).document
            val skipWords = listOf("futbol", "futbol tr", "futboi", "günün maçı")

            doc.select("a[href*='matches?id=']").forEach { a ->
                val href = a.attr("href")
                val matchId = Regex("id=([a-f0-9]+)").find(href)?.groupValues?.get(1) ?: return@forEach
                
                val imgs = a.select("img")
                val homeLogo = if (imgs.size >= 1) normalizeLogo(imgs[0].attr("src")) else ""
                val awayLogo = if (imgs.size >= 2) normalizeLogo(imgs[1].attr("src")) else ""
                val displayLogo = homeLogo.ifEmpty { awayLogo }

                val textLines = a.wholeText().lines()
                    .map { it.trim() }
                    .filter { it.isNotEmpty() && !skipWords.contains(it.lowercase()) }
                
                val title = textLines.joinToString(" | ")

                matchItems.add(
                    LiveSearchResponse(
                        name = title,
                        url = matchId,
                        apiName = this.name,
                        type = TvType.Live,
                        posterUrl = displayLogo
                    )
                )
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        if (matchItems.isNotEmpty()) {
            items.add(HomePageList("🔥 Canlı Maçlar", matchItems))
        }

        val tvChannels = listOf(
            Triple("bein-sports-1", "BEIN SPORTS 1", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/BeIN_Sports_1_HD.svg/200px-BeIN_Sports_1_HD.svg.png"),
            Triple("bein-sports-2", "BEIN SPORTS 2", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/BeIN_Sports_2_HD.svg/200px-BeIN_Sports_2_HD.svg.png"),
            Triple("s-sport", "S SPORT", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/S_Sport_logo.svg/200px-S_Sport_logo.svg.png"),
            Triple("trt-spor", "TRT SPOR", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/TRT_Spor_logo.svg/200px-TRT_Spor_logo.svg.png")
        )

        val channelItems = tvChannels.map { (id, chName, logo) ->
            LiveSearchResponse(
                name = chName,
                url = id,
                apiName = this.name,
                type = TvType.Live,
                posterUrl = logo
            )
        }
        
        items.add(HomePageList("📺 TV Kanalları", channelItems))
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
        subtitleCallback: (SubtitleFile) -> Unit,
        callback: (ExtractorLink) -> Unit
    ): Boolean {
        val resourceId = data
        val baseDomain = getBaseDomain()

        try {
            val matchPage = app.get("$baseDomain/matches?id=$resourceId", referer = "$baseDomain/").text
            val fetchRegex = Regex("""fetch\(\s*["']([^"']+)["']""")
            var fetchUrl = fetchRegex.find(matchPage)?.groupValues?.get(1)?.trim() ?: return false
            if (!fetchUrl.endsWith(resourceId)) fetchUrl += resourceId

            val apiHeaders = mapOf("Origin" to baseDomain)
            val apiResp = app.get(fetchUrl, headers = apiHeaders).text

            val patterns = listOf(
                """"deismackanal":"(.*?)"""".toRegex(),
                """"stream":\s*"(.*?)"""".toRegex(),
                """"url":\s*"(.*?\.m3u8[^"]*)"""".toRegex(),
                """(https?://[^\s"']+\.m3u8[^\s"']*)""".toRegex()
            )

            var streamUrl = ""
            for (pat in patterns) {
                val match = pat.find(apiResp)
                if (match != null) {
                    streamUrl = match.groupValues[1].replace("\\/", "/").replace("\\", "")
                    break
                }
            }

            if (streamUrl.isNotEmpty()) {
                callback.invoke(
                    ExtractorLink(
                        source = this.name,
                        name = "Yayın 1",
                        url = streamUrl,
                        referer = "$baseDomain/",
                        quality = Qualities.Unknown.value,
                        isM3u8 = streamUrl.contains(".m3u8")
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
