> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Scrapfly ile Web Sitesi Scrape Aracı

> `ScrapflyScrapeWebsiteTool`, web sitelerinden çeşitli biçimlerde içerik çıkarmak için Scrapfly'ın web scraping API'sini kullanır.

# `ScrapflyScrapeWebsiteTool`

## Açıklama

`ScrapflyScrapeWebsiteTool`, web sitelerinden içerik çıkarmak için [Scrapfly](https://scrapfly.io/) web scraping API'sinden yararlanmak üzere tasarlanmıştır. Bu araç; headless tarayıcı desteği, proxy'ler ve anti-bot aşma özellikleriyle gelişmiş web scraping yetenekleri sunar. Ham HTML, markdown ve düz metin dahil çeşitli biçimlerde web sayfası verisi çıkarmaya izin verir; bu da onu geniş bir web scraping görev yelpazesi için ideal hale getirir.

## Kurulum

Bu aracı kullanmak için Scrapfly SDK'sını kurmanız gerekir:

```shell  theme={null}
uv add scrapfly-sdk
```

Ayrıca [scrapfly.io/register](https://www.scrapfly.io/register/) üzerinden kaydolup bir Scrapfly API anahtarı edinmeniz gerekir.

## Başlamak İçin Adımlar

`ScrapflyScrapeWebsiteTool` aracını etkili şekilde kullanmak için şu adımları izleyin:

1. **Bağımlılıkları Kurun**: Yukarıdaki komutla Scrapfly SDK'sını kurun.
2. **API Anahtarı Edinin**: API anahtarınızı almak için Scrapfly'a kaydolun.
3. **Aracı Başlatın**: API anahtarınızla aracın bir örneğini oluşturun.
4. **Scraping Parametrelerini Yapılandırın**: İhtiyaçlarınıza göre scraping parametrelerini özelleştirin.

## Örnek

Aşağıdaki örnek, `ScrapflyScrapeWebsiteTool` aracının bir web sitesinden içerik çıkarmak için nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import ScrapflyScrapeWebsiteTool

# Aracı başlat
scrape_tool = ScrapflyScrapeWebsiteTool(api_key="your_scrapfly_api_key")

# Aracı kullanan bir ajan tanımla
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Web sitelerinden bilgi çıkar",
    backstory="Herhangi bir web sitesinden içerik çıkarabilen bir web scraping uzmanı.",
    tools=[scrape_tool],
    verbose=True,
)

# Bir web sitesinden içerik çıkarma örnek görevi
scrape_task = Task(
    description="https://web-scraping.dev/products adresindeki ürün sayfasından ana içeriği çıkar ve mevcut ürünleri özetle.",
    expected_output="Web sitesinde mevcut ürünlerin özeti.",
    agent=web_scraper_agent,
)

# Ekibi oluştur ve çalıştır
crew = Crew(agents=[web_scraper_agent], tasks=[scrape_task])
result = crew.kickoff()
```

Scraping parametrelerini ayrıca özelleştirebilirsiniz:

```python Code theme={null}
# Özel scraping parametreleriyle örnek
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Özel parametrelerle web sitelerinden bilgi çıkar",
    backstory="Herhangi bir web sitesinden içerik çıkarabilen bir web scraping uzmanı.",
    tools=[scrape_tool],
    verbose=True,
)

# Ajan aracı şu tür parametrelerle kullanacaktır:
# url="https://web-scraping.dev/products"
# scrape_format="markdown"
# ignore_scrape_failures=True
# scrape_config={
#     "asp": True,  # Cloudflare gibi scraping engelleme çözümlerini aş
#     "render_js": True,  # Bulut tabanlı headless tarayıcı ile JavaScript render özelliğini aç
#     "proxy_pool": "public_residential_pool",  # Bir proxy havuzu seç
#     "country": "us",  # Bir proxy konumu seç
#     "auto_scroll": True,  # Sayfayı otomatik kaydır
# }

scrape_task = Task(
    description="https://web-scraping.dev/products adresindeki ürün sayfasından, JavaScript render ve proxy ayarları dahil gelişmiş scraping seçeneklerini kullanarak ana içeriği çıkar.",
    expected_output="Tüm mevcut bilgileri içeren ayrıntılı ürün özeti.",
    agent=web_scraper_agent,
)
```

## Parametreler

`ScrapflyScrapeWebsiteTool` şu parametreleri kabul eder:

### Başlatma Parametreleri

* **api\_key**: Gerekli. Scrapfly API anahtarınız.

### Çalıştırma Parametreleri

* **url**: Gerekli. Scrape edilecek web sitesinin URL'si.
* **scrape\_format**: İsteğe bağlı. Web sayfası içeriğinin çıkarılacağı biçim. Seçenekler `"raw"` (HTML), `"markdown"` veya `"text"` şeklindedir. Varsayılan `"markdown"`dur.
* **scrape\_config**: İsteğe bağlı. Ek Scrapfly scraping yapılandırma seçeneklerini içeren sözlük.
* **ignore\_scrape\_failures**: İsteğe bağlı. Scraping sırasında oluşan hataların yok sayılıp sayılmayacağı. `True` olduğunda scraping başarısızsa araç istisna fırlatmak yerine `None` döndürür.

## Scrapfly Yapılandırma Seçenekleri

`scrape_config` parametresi, scraping davranışını şu seçeneklerle özelleştirmenize olanak tanır:

* **asp**: Anti-scraping korumasını aşmayı etkinleştirir.
* **render\_js**: Bulut headless tarayıcı ile JavaScript render özelliğini etkinleştirir.
* **proxy\_pool**: Bir proxy havuzu seçer (ör. `"public_residential_pool"`, `"datacenter"`).
* **country**: Bir proxy konumu seçer (ör. `"us"`, `"uk"`).
* **auto\_scroll**: Lazy-load edilen içeriği yüklemek için sayfayı otomatik olarak kaydırır.
* **js**: Headless tarayıcı tarafından özel JavaScript kodu çalıştırır.

Yapılandırma seçeneklerinin tam listesi için [Scrapfly API documentation](https://scrapfly.io/docs/scrape-api/getting-started) sayfasına bakın.

## Kullanım

`ScrapflyScrapeWebsiteTool` bir ajanla kullanıldığında, ajan scrape edilecek web sitesinin URL'sini sağlamalı ve isteğe bağlı olarak biçimi ve ek yapılandırma seçeneklerini belirtebilir:

```python Code theme={null}
# Aracın bir ajan ile kullanım örneği
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Web sitelerinden bilgi çıkar",
    backstory="Herhangi bir web sitesinden içerik çıkarabilen bir web scraping uzmanı.",
    tools=[scrape_tool],
    verbose=True,
)

# Ajan için bir görev oluştur
scrape_task = Task(
    description="example.com içeriğinin ana bölümünü markdown biçiminde çıkar.",
    expected_output="example.com ana içeriği markdown biçiminde.",
    agent=web_scraper_agent,
)

# Görevi çalıştır
crew = Crew(agents=[web_scraper_agent], tasks=[scrape_task])
result = crew.kickoff()
```

Özel yapılandırmayla daha gelişmiş kullanım için:

```python Code theme={null}
# Daha belirgin talimatlarla bir görev oluştur
advanced_scrape_task = Task(
    description="""
    example.com içeriğini şu gereksinimlerle çıkar:
    - İçeriği düz metin biçimine dönüştür
    - JavaScript render özelliğini etkinleştir
    - ABD tabanlı bir proxy kullan
    - Her türlü scraping hatasını zarif şekilde ele al
    """,
    expected_output="example.com üzerinden çıkarılan içerik",
    agent=web_scraper_agent,
)
```

## Hata Yönetimi

Varsayılan olarak `ScrapflyScrapeWebsiteTool`, scraping başarısız olursa bir istisna fırlatır. Ajanlara `ignore_scrape_failures` parametresini belirterek hataları zarif şekilde ele almaları söylenebilir:

```python Code theme={null}
# Ajanın hataları ele almasını söyleyen bir görev oluştur
error_handling_task = Task(
    description="""
    Sorun çıkarma ihtimali olan bir web sitesinden içerik çıkar ve
    ignore_scrape_failures değerini True yaparak her türlü scraping hatasını zarif biçimde ele aldığından emin ol.
    """,
    expected_output="Çıkarılan içerik veya zarif bir hata mesajı",
    agent=web_scraper_agent,
)
```

## Uygulama Ayrıntıları

`ScrapflyScrapeWebsiteTool`, Scrapfly API ile etkileşim kurmak için Scrapfly SDK'sını kullanır:

```python Code theme={null}
class ScrapflyScrapeWebsiteTool(BaseTool):
    name: str = "Scrapfly web scraping API tool"
    description: str = (
        "Bir web sayfası URL'sini Scrapfly ile scrape et ve içeriğini markdown veya metin olarak döndür"
    )
    
    # Implementation details...
    
    def _run(
        self,
        url: str,
        scrape_format: str = "markdown",
        scrape_config: Optional[Dict[str, Any]] = None,
        ignore_scrape_failures: Optional[bool] = None,
    ):
        from scrapfly import ScrapeApiResponse, ScrapeConfig

        scrape_config = scrape_config if scrape_config is not None else {}
        try:
            response: ScrapeApiResponse = self.scrapfly.scrape(
                ScrapeConfig(url, format=scrape_format, **scrape_config)
            )
            return response.scrape_result["content"]
        except Exception as e:
            if ignore_scrape_failures:
                logger.error(f"Error fetching data from {url}, exception: {e}")
                return None
            else:
                raise e
```

## Sonuç

`ScrapflyScrapeWebsiteTool`, Scrapfly'ın gelişmiş web scraping yeteneklerini kullanarak web sitelerinden içerik çıkarmak için güçlü bir yol sunar. Headless tarayıcı desteği, proxy'ler ve anti-bot aşma gibi özelliklerle karmaşık web sitelerini işleyebilir ve çeşitli biçimlerde içerik çıkarabilir. Bu araç, özellikle güvenilir web scraping gerektiren veri çıkarımı, içerik izleme ve araştırma görevlerinde kullanışlıdır.
