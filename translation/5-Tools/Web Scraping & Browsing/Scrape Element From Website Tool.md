> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Web Sitesinden Öğe Scrape Etme Aracı

> `ScrapeElementFromWebsiteTool`, CrewAI ajanlarının CSS seçicileri kullanarak web sitelerinden belirli öğeleri çıkarmasını sağlar.

# `ScrapeElementFromWebsiteTool`

## Açıklama

`ScrapeElementFromWebsiteTool`, CSS seçicileri kullanarak web sitelerinden belirli öğeleri çıkarmak için tasarlanmıştır. Bu araç, CrewAI ajanlarının web sayfalarından hedefli içerik scrape etmesini sağlar; böylece yalnızca belirli bölümlerin gerektiği veri çıkarma görevlerinde kullanışlı olur.

## Kurulum

Bu aracı kullanmak için gerekli bağımlılıkları kurmanız gerekir:

```shell  theme={null}
uv add requests beautifulsoup4
```

## Başlamak İçin Adımlar

`ScrapeElementFromWebsiteTool` aracını etkili şekilde kullanmak için şu adımları izleyin:

1. **Bağımlılıkları Kurun**: Yukarıdaki komutla gerekli paketleri kurun.
2. **CSS Seçicilerini Belirleyin**: Web sitesinden çıkarmak istediğiniz öğeler için CSS seçicilerini belirleyin.
3. **Aracı Başlatın**: Gerekli parametrelerle aracın bir örneğini oluşturun.

## Örnek

Aşağıdaki örnek, `ScrapeElementFromWebsiteTool` aracının bir web sitesinden belirli öğeleri çıkarmak için nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeElementFromWebsiteTool

# Aracı başlat
scrape_tool = ScrapeElementFromWebsiteTool()

# Aracı kullanan bir ajan tanımla
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Web sitelerinden belirli bilgileri çıkar",
    backstory="Web sayfalarından hedefli içerik çıkarabilen bir web scraping uzmanı.",
    tools=[scrape_tool],
    verbose=True,
)

# Bir haber sitesinden manşetleri çıkarma örnek görevi
scrape_task = Task(
    description="CNN ana sayfasındaki ana manşetleri çıkar. Manşet öğelerini hedeflemek için '.headline' CSS seçicisini kullan.",
    expected_output="CNN'deki ana manşetlerin listesi.",
    agent=web_scraper_agent,
)

# Ekibi oluştur ve çalıştır
crew = Crew(agents=[web_scraper_agent], tasks=[scrape_task])
result = crew.kickoff()
```

Aracı önceden tanımlanmış parametrelerle de başlatabilirsiniz:

```python Code theme={null}
# Aracı önceden tanımlanmış parametrelerle başlat
scrape_tool = ScrapeElementFromWebsiteTool(
    website_url="https://www.example.com",
    css_element=".main-content"
)
```

## Parametreler

`ScrapeElementFromWebsiteTool`, başlatma sırasında şu parametreleri kabul eder:

* **website\_url**: İsteğe bağlı. Scrape edilecek web sitesinin URL'si. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz.
* **css\_element**: İsteğe bağlı. Çıkarılacak öğeler için CSS seçicisi. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz.
* **cookies**: İsteğe bağlı. İstek ile gönderilecek çerezleri içeren sözlük. Kimlik doğrulama gerektiren siteler için yararlı olabilir.

## Kullanım

`ScrapeElementFromWebsiteTool` bir ajanla kullanıldığında, ajan aşağıdaki parametreleri sağlamalıdır (başlatma sırasında verilmedilerse):

* **website\_url**: Scrape edilecek web sitesinin URL'si.
* **css\_element**: Çıkarılacak öğeler için CSS seçicisi.

Araç, CSS seçicisi ile eşleşen tüm öğelerin metin içeriğini satır sonlarıyla birleştirerek döndürür.

```python Code theme={null}
# Aracın bir ajan ile kullanım örneği
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Web sitelerinden belirli öğeleri çıkar",
    backstory="CSS seçicileri kullanarak hedefli içerik çıkarabilen bir web scraping uzmanı.",
    tools=[scrape_tool],
    verbose=True,
)

# Ajanın belirli öğeleri çıkarması için bir görev oluştur
extract_task = Task(
    description="""
    example.com üzerindeki öne çıkan ürünler bölümündeki tüm ürün başlıklarını çıkar.
    Başlık öğelerini hedeflemek için '.product-title' CSS seçicisini kullan.
    """,
    expected_output="Web sitesindeki ürün başlıklarının listesi",
    agent=web_scraper_agent,
)

# Görevi ekip üzerinden çalıştır
crew = Crew(agents=[web_scraper_agent], tasks=[extract_task])
result = crew.kickoff()
```

## Uygulama Ayrıntıları

`ScrapeElementFromWebsiteTool`, web sayfasını almak için `requests` kütüphanesini ve HTML'i ayrıştırıp belirtilen öğeleri çıkarmak için `BeautifulSoup` kullanır:

```python Code theme={null}
class ScrapeElementFromWebsiteTool(BaseTool):
    name: str = "Read a website content"
    description: str = "A tool that can be used to read a website content."
    
    # Implementation details...
    
    def _run(self, **kwargs: Any) -> Any:
        website_url = kwargs.get("website_url", self.website_url)
        css_element = kwargs.get("css_element", self.css_element)
        page = requests.get(
            website_url,
            headers=self.headers,
            cookies=self.cookies if self.cookies else {},
        )
        parsed = BeautifulSoup(page.content, "html.parser")
        elements = parsed.select(css_element)
        return "\n".join([element.get_text() for element in elements])
```

## Sonuç

`ScrapeElementFromWebsiteTool`, CSS seçicileri kullanarak web sitelerinden belirli öğeleri çıkarmak için güçlü bir yol sunar. Ajanların yalnızca ihtiyaç duydukları içeriği hedeflemesini sağlayarak web scraping görevlerini daha verimli ve odaklı hale getirir. Bu araç, özellikle web sayfalarından belirli bilgilerin çıkarılması gereken veri çıkarımı, içerik izleme ve araştırma görevlerinde kullanışlıdır.
