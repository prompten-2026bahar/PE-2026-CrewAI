> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Scrapegraph Scrape Aracı

> `ScrapegraphScrapeTool`, web sitelerinden akıllı şekilde içerik çıkarmak için Scrapegraph AI'nin SmartScraper API'sinden yararlanır.

# `ScrapegraphScrapeTool`

## Açıklama

`ScrapegraphScrapeTool`, web sitelerinden akıllı şekilde içerik çıkarmak için Scrapegraph AI'nin SmartScraper API'sinden yararlanmak üzere tasarlanmıştır. Bu araç, yapay zeka destekli içerik çıkarımı ile gelişmiş web scraping yetenekleri sunar ve hedefli veri toplama ile içerik analizi görevleri için idealdir. Geleneksel web scraper'lardan farklı olarak, doğal dil prompt'larına göre en ilgili bilgiyi çıkarmak için web sayfalarının bağlamını ve yapısını anlayabilir.

## Kurulum

Bu aracı kullanmak için Scrapegraph Python istemcisini kurmanız gerekir:

```shell  theme={null}
uv add scrapegraph-py
```

Ayrıca Scrapegraph API anahtarınızı bir ortam değişkeni olarak ayarlamanız gerekir:

```shell  theme={null}
export SCRAPEGRAPH_API_KEY="your_api_key"
```

[Scrapegraph AI](https://scrapegraphai.com) üzerinden bir API anahtarı alabilirsiniz.

## Başlamak İçin Adımlar

`ScrapegraphScrapeTool` aracını etkili şekilde kullanmak için şu adımları izleyin:

1. **Bağımlılıkları Kurun**: Yukarıdaki komutu kullanarak gerekli paketi kurun.
2. **API Anahtarını Ayarlayın**: Scrapegraph API anahtarınızı ortam değişkeni olarak ayarlayın veya başlatma sırasında verin.
3. **Aracı Başlatın**: Gerekli parametrelerle aracın bir örneğini oluşturun.
4. **Çıkarım Prompt'ları Tanımlayın**: Belirli içeriğin çıkarılmasını yönlendirmek için doğal dil prompt'ları hazırlayın.

## Örnek

Aşağıdaki örnek, `ScrapegraphScrapeTool` aracının bir web sitesinden içerik çıkarmak için nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import ScrapegraphScrapeTool

# Aracı başlat
scrape_tool = ScrapegraphScrapeTool(api_key="your_api_key")

# Aracı kullanan bir ajan tanımla
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Web sitelerinden belirli bilgileri çıkar",
    backstory="Web sayfalarından hedefli içerik çıkarabilen bir web scraping uzmanı.",
    tools=[scrape_tool],
    verbose=True,
)

# Bir e-ticaret sitesinden ürün bilgisi çıkarma örnek görevi
scrape_task = Task(
    description="example.com üzerindeki öne çıkan ürünler bölümünden ürün adlarını, fiyatları ve açıklamaları çıkar.",
    expected_output="Adlar, fiyatlar ve açıklamalar dahil ürün bilgilerinin yapılandırılmış bir listesi.",
    agent=web_scraper_agent,
)

# Ekibi oluştur ve çalıştır
crew = Crew(agents=[web_scraper_agent], tasks=[scrape_task])
result = crew.kickoff()
```

Aracı önceden tanımlanmış parametrelerle de başlatabilirsiniz:

```python Code theme={null}
# Aracı önceden tanımlanmış parametrelerle başlat
scrape_tool = ScrapegraphScrapeTool(
    website_url="https://www.example.com",
    user_prompt="Extract all product prices and descriptions",
    api_key="your_api_key"
)
```

## Parametreler

`ScrapegraphScrapeTool`, başlatma sırasında şu parametreleri kabul eder:

* **api\_key**: İsteğe bağlı. Scrapegraph API anahtarınız. Verilmezse `SCRAPEGRAPH_API_KEY` ortam değişkeni aranır.
* **website\_url**: İsteğe bağlı. Scrape edilecek web sitesinin URL'si. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz.
* **user\_prompt**: İsteğe bağlı. İçerik çıkarımı için özel talimatlar. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz.
* **enable\_logging**: İsteğe bağlı. Scrapegraph istemcisi için günlük kaydını etkinleştirip etkinleştirmeyeceği. Varsayılan `False`.

## Kullanım

`ScrapegraphScrapeTool` bir ajanla kullanıldığında, ajan aşağıdaki parametreleri sağlamalıdır (başlatma sırasında verilmedilerse):

* **website\_url**: Scrape edilecek web sitesinin URL'si.
* **user\_prompt**: İsteğe bağlı. İçerik çıkarımı için özel talimatlar. Varsayılan `"Extract the main content of the webpage"` değeridir.

Araç, verilen prompt'a göre çıkarılan içeriği döndürecektir.

```python Code theme={null}
# Aracın bir ajan ile kullanım örneği
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Web sitelerinden belirli bilgileri çıkar",
    backstory="Web sayfalarından hedefli içerik çıkarabilen bir web scraping uzmanı.",
    tools=[scrape_tool],
    verbose=True,
)

# Ajanın belirli içeriği çıkarması için bir görev oluştur
extract_task = Task(
    description="example.com üzerinden ana başlığı ve özeti çıkar",
    expected_output="Web sitesindeki ana başlık ve özet",
    agent=web_scraper_agent,
)

# Görevi çalıştır
crew = Crew(agents=[web_scraper_agent], tasks=[extract_task])
result = crew.kickoff()
```

## Hata Yönetimi

`ScrapegraphScrapeTool` aşağıdaki istisnaları fırlatabilir:

* **ValueError**: API anahtarı eksik olduğunda veya URL biçimi geçersiz olduğunda.
* **RateLimitError**: API oran limitleri aşıldığında.
* **RuntimeError**: Scraping işlemi başarısız olduğunda (ağ sorunları, API hataları).

Ajanlara olası hataları zarif biçimde ele almalarını söylemeniz önerilir:

```python Code theme={null}
# Hata yönetimi talimatları içeren bir görev oluştur
robust_extract_task = Task(
    description="""
    example.com üzerinden ana başlığı çıkar.
    Şu tür hatalarla karşılaşabileceğinin farkında ol:
    - Geçersiz URL biçimi
    - Eksik API anahtarı
    - Aşılan oran limiti
    - Ağ veya API hataları
    
    Herhangi bir hatayla karşılaşırsan, neyin yanlış gittiğini açıkça açıkla
    ve olası çözümler öner.
    """,
    expected_output="Çıkarılan başlık veya açık bir hata açıklaması",
    agent=web_scraper_agent,
)
```

## Oran Sınırlama

Scrapegraph API'nin, abonelik planınıza göre değişen oran limitleri vardır. Şu en iyi uygulamaları göz önünde bulundurun:

* Birden fazla URL işlerken istekler arasında uygun gecikmeler uygulayın.
* Uygulamanızda oran limiti hatalarını zarif şekilde ele alın.
* Scrapegraph panosunda API planı limitlerinizi kontrol edin.

## Uygulama Ayrıntıları

`ScrapegraphScrapeTool`, SmartScraper API ile etkileşim kurmak için Scrapegraph Python istemcisini kullanır:

```python Code theme={null}
class ScrapegraphScrapeTool(BaseTool):
    """
    Web sitesi içeriğini akıllı şekilde scrape etmek için Scrapegraph AI kullanan araç.
    """
    
    # Implementation details...
    
    def _run(self, **kwargs: Any) -> Any:
        website_url = kwargs.get("website_url", self.website_url)
        user_prompt = (
            kwargs.get("user_prompt", self.user_prompt)
            or "Extract the main content of the webpage"
        )

        if not website_url:
            raise ValueError("website_url is required")

        # URL biçimini doğrula
        self._validate_url(website_url)

        try:
            # SmartScraper isteğini yap
            response = self._client.smartscraper(
                website_url=website_url,
                user_prompt=user_prompt,
            )

            return response
        # Hata yönetimi...
```

## Sonuç

`ScrapegraphScrapeTool`, web sayfası yapısını yapay zeka destekli anlayışla kullanarak web sitelerinden içerik çıkarmak için güçlü bir yol sunar. Ajanların doğal dil prompt'larıyla belirli bilgileri hedeflemesini sağlayarak web scraping görevlerini daha verimli ve odaklı hale getirir. Bu araç, özellikle web sayfalarından belirli bilgilerin çıkarılması gereken veri çıkarımı, içerik izleme ve araştırma görevlerinde kullanışlıdır.
