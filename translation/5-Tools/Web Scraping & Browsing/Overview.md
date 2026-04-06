> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Genel Bakış

> Güçlü scraping araçlarıyla web sitelerinden veri çıkarın ve tarayıcı etkileşimlerini otomatikleştirin

Bu araçlar, ajanlarınızın web ile etkileşime girmesini, web sitelerinden veri çıkarmasını ve tarayıcı tabanlı görevleri otomatikleştirmesini sağlar. Basit web scraping'den karmaşık tarayıcı otomasyonuna kadar, web etkileşimiyle ilgili tüm ihtiyaçlarınızı kapsar.

## **Kullanılabilir Araçlar**

<CardGroup cols={2}>
  <Card title="Scrape Website Tool" icon="globe" href="/en/tools/web-scraping/scrapewebsitetool">
    Herhangi bir web sitesinden içerik çıkarmak için genel amaçlı web scraping aracı.
  </Card>

  <Card title="Scrape Element Tool" icon="crosshairs" href="/en/tools/web-scraping/scrapeelementfromwebsitetool">
    Hassas scraping yetenekleriyle web sayfalarındaki belirli öğeleri hedefleyin.
  </Card>

  <Card title="Firecrawl Crawl Tool" icon="spider" href="/en/tools/web-scraping/firecrawlcrawlwebsitetool">
    Firecrawl'ın güçlü motoruyla tüm web sitelerini sistematik biçimde tarayın.
  </Card>

  <Card title="Firecrawl Scrape Tool" icon="fire" href="/en/tools/web-scraping/firecrawlscrapewebsitetool">
    Firecrawl'ın gelişmiş yetenekleriyle yüksek performanslı web scraping.
  </Card>

  <Card title="Firecrawl Search Tool" icon="magnifying-glass" href="/en/tools/web-scraping/firecrawlsearchtool">
    Firecrawl'ın arama özelliklerini kullanarak belirli içerikleri arayın ve çıkarın.
  </Card>

  <Card title="Selenium Scraping Tool" icon="robot" href="/en/tools/web-scraping/seleniumscrapingtool">
    Selenium WebDriver yetenekleriyle tarayıcı otomasyonu ve scraping.
  </Card>

  <Card title="ScrapFly Tool" icon="plane" href="/en/tools/web-scraping/scrapflyscrapetool">
    ScrapFly'ın premium scraping servisiyle profesyonel web scraping.
  </Card>

  <Card title="ScrapGraph Tool" icon="network-wired" href="/en/tools/web-scraping/scrapegraphscrapetool">
    Karmaşık veri ilişkileri için grafik tabanlı web scraping.
  </Card>

  <Card title="Spider Tool" icon="spider" href="/en/tools/web-scraping/spidertool">
    Kapsamlı web tarama ve veri çıkarma yetenekleri.
  </Card>

  <Card title="BrowserBase Tool" icon="browser" href="/en/tools/web-scraping/browserbaseloadtool">
    BrowserBase altyapısıyla bulut tabanlı tarayıcı otomasyonu.
  </Card>

  <Card title="HyperBrowser Tool" icon="window-maximize" href="/en/tools/web-scraping/hyperbrowserloadtool">
    HyperBrowser'ın optimize motoruyla hızlı tarayıcı etkileşimleri.
  </Card>

  <Card title="Stagehand Tool" icon="hand" href="/en/tools/web-scraping/stagehandtool">
    Doğal dil komutlarıyla akıllı tarayıcı otomasyonu.
  </Card>

  <Card title="Oxylabs Scraper Tool" icon="globe" href="/en/tools/web-scraping/oxylabsscraperstool">
    Oxylabs ile büyük ölçekte web verisine erişin.
  </Card>

  <Card title="Bright Data Tools" icon="spider" href="/en/tools/web-scraping/brightdata-tools">
    SERP araması, Web Unlocker ve Dataset API entegrasyonları.
  </Card>
</CardGroup>

## **Yaygın Kullanım Senaryoları**

* **Veri Çıkarımı**: Ürün bilgilerini, fiyatları ve yorumları scrape edin
* **İçerik İzleme**: Web siteleri ve haber kaynaklarındaki değişimleri takip edin
* **Lead Üretimi**: İletişim bilgilerini ve işletme verilerini çıkarın
* **Pazar Araştırması**: Rekabet istihbaratı ve pazar verileri toplayın
* **Test ve QA**: Tarayıcı testlerini ve doğrulama iş akışlarını otomatikleştirin
* **Sosyal Medya**: Gönderileri, yorumları ve sosyal medya analizlerini çıkarın

## **Hızlı Başlangıç Örneği**

```python  theme={null}
from crewai_tools import ScrapeWebsiteTool, FirecrawlScrapeWebsiteTool, SeleniumScrapingTool

# Scraping araçlarını oluştur
simple_scraper = ScrapeWebsiteTool()
advanced_scraper = FirecrawlScrapeWebsiteTool()
browser_automation = SeleniumScrapingTool()

# Ajanınıza ekleyin
agent = Agent(
    role="Web Araştırma Uzmanı",
    tools=[simple_scraper, advanced_scraper, browser_automation],
    goal="Web verisini verimli şekilde çıkar ve analiz et"
)
```

## **Scraping İçin En İyi Uygulamalar**

* **robots.txt'ye Saygı Gösterin**: Web sitesi scraping politikalarını her zaman kontrol edin ve uygulayın
* **Oran Sınırlama**: Sunucuları aşırı yüklememek için istekler arasına gecikmeler koyun
* **User Agent'lar**: Botunuzu tanımlamak için uygun user agent dizeleri kullanın
* **Yasal Uyum**: Scraping faaliyetlerinizin hizmet şartlarına uygun olduğundan emin olun
* **Hata Yönetimi**: Ağ sorunları ve engellenmiş istekler için sağlam hata yönetimi uygulayın
* **Veri Kalitesi**: Çıkarılan veriyi işlemeden önce doğrulayın ve temizleyin

## **Araç Seçim Rehberi**

* **Basit Görevler**: Temel içerik çıkarımı için `ScrapeWebsiteTool` kullanın
* **JavaScript Yoğun Siteler**: Dinamik içerik için `SeleniumScrapingTool` kullanın
* **Ölçek ve Performans**: Yüksek hacimli scraping için `FirecrawlScrapeWebsiteTool` kullanın
* **Bulut Altyapısı**: Ölçeklenebilir tarayıcı otomasyonu için `BrowserBaseLoadTool` kullanın
* **Karmaşık İş Akışları**: Akıllı tarayıcı etkileşimleri için `StagehandTool` kullanın
