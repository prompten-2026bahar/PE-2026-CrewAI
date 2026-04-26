> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Selenium Scraper

> `SeleniumScrapingTool`, Selenium kullanarak belirtilen bir web sitesinin içeriğini çıkarmak ve okumak için tasarlanmıştır.

# `SeleniumScrapingTool`

<Note>
  Bu araç şu anda geliştirme aşamasındadır. Yeteneklerini iyileştirirken kullanıcılar beklenmeyen davranışlarla karşılaşabilir.
  Geri bildiriminiz iyileştirmeler yapabilmemiz için bizim için çok değerlidir.
</Note>

## Açıklama

`SeleniumScrapingTool`, yüksek verimli web scraping görevleri için tasarlanmıştır.
Belirli öğeleri hedeflemek için CSS seçicileri kullanarak web sayfalarından hassas içerik çıkarımı yapmayı sağlar.
Tasarımı, sağlanan herhangi bir web sitesi URL'siyle çalışabilecek esnekliği sunarak geniş bir scraping ihtiyacı yelpazesine hitap eder.

## Kurulum

Bu aracı kullanmak için CrewAI araç paketini ve Selenium'u kurmanız gerekir:

```shell  theme={null}
pip install 'crewai[tools]'
uv add selenium webdriver-manager
```

Ayrıca araç tarayıcı otomasyonu için Chrome WebDriver kullandığından sisteminizde Chrome kurulu olmalıdır.

## Örnek

Aşağıdaki örnek, `SeleniumScrapingTool` aracının bir CrewAI ajanı ile nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import SeleniumScrapingTool

# Aracı başlat
selenium_tool = SeleniumScrapingTool()

# Aracı kullanan bir ajan tanımla
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Selenium kullanarak web sitelerinden bilgi çıkar",
    backstory="Dinamik web sitelerinden içerik çıkarabilen bir web scraping uzmanı.",
    tools=[selenium_tool],
    verbose=True,
)

# Bir web sitesinden içerik scrape etme örnek görevi
scrape_task = Task(
    description="example.com ana sayfasından ana içeriği çıkar. Ana içerik alanını hedeflemek için 'main' CSS seçicisini kullan.",
    expected_output="example.com ana sayfasındaki ana içerik.",
    agent=web_scraper_agent,
)

# Ekibi oluştur ve çalıştır
crew = Crew(
    agents=[web_scraper_agent],
    tasks=[scrape_task],
    verbose=True,
    process=Process.sequential,
)
result = crew.kickoff()
```

Aracı önceden tanımlanmış parametrelerle de başlatabilirsiniz:

```python Code theme={null}
# Aracı önceden tanımlanmış parametrelerle başlat
selenium_tool = SeleniumScrapingTool(
    website_url='https://example.com',
    css_element='.main-content',
    wait_time=5
)

# Aracı kullanan bir ajan tanımla
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Selenium kullanarak web sitelerinden bilgi çıkar",
    backstory="Dinamik web sitelerinden içerik çıkarabilen bir web scraping uzmanı.",
    tools=[selenium_tool],
    verbose=True,
)
```

## Parametreler

`SeleniumScrapingTool`, başlatma sırasında şu parametreleri kabul eder:

* **website\_url**: İsteğe bağlı. Scrape edilecek web sitesinin URL'si. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz.
* **css\_element**: İsteğe bağlı. Çıkarılacak öğeler için CSS seçicisi. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz.
* **cookie**: İsteğe bağlı. Çerez bilgilerini içeren sözlük; kısıtlı içeriğe erişmek için giriş yapılmış bir oturumu simüle etmekte yararlıdır.
* **wait\_time**: İsteğe bağlı. Scraping öncesinde beklenecek süreyi (saniye cinsinden) belirtir; böylece web sitesinin ve dinamik içeriğin tamamen yüklenmesine izin verir. Varsayılan `3` saniyedir.
* **return\_html**: İsteğe bağlı. Yalnızca metin yerine HTML içeriğinin döndürülüp döndürülmeyeceği. Varsayılan `False`.

Araç bir ajan ile kullanıldığında, ajan aşağıdaki parametreleri sağlamalıdır (başlatma sırasında verilmedilerse):

* **website\_url**: Gerekli. Scrape edilecek web sitesinin URL'si.
* **css\_element**: Gerekli. Çıkarılacak öğeler için CSS seçicisi.

## Ajan Entegrasyonu Örneği

Burada `SeleniumScrapingTool` aracının bir CrewAI ajanı ile nasıl entegre edileceğine dair daha ayrıntılı bir örnek vardır:

```python Code theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import SeleniumScrapingTool

# Aracı başlat
selenium_tool = SeleniumScrapingTool()

# Aracı kullanan bir ajan tanımla
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Dinamik web sitelerinden bilgi çıkar ve analiz et",
    backstory="""You are an expert web scraper who specializes in extracting 
    content from dynamic websites that require browser automation. You have 
    extensive knowledge of CSS selectors and can identify the right selectors 
    to target specific content on any website.""",
    tools=[selenium_tool],
    verbose=True,
)

# Ajan için bir görev oluştur
scrape_task = Task(
    description="""
    Extract the following information from the news website at {website_url}:
    
    1. The headlines of all featured articles (CSS selector: '.headline')
    2. The publication dates of these articles (CSS selector: '.pub-date')
    3. The author names where available (CSS selector: '.author')
    
    Compile this information into a structured format with each article's details grouped together.
    """,
    expected_output="A structured list of articles with their headlines, publication dates, and authors.",
    agent=web_scraper_agent,
)

# Görevi çalıştır
crew = Crew(
    agents=[web_scraper_agent],
    tasks=[scrape_task],
    verbose=True,
    process=Process.sequential,
)
result = crew.kickoff(inputs={"website_url": "https://news-example.com"})
```

## Uygulama Ayrıntıları

`SeleniumScrapingTool`, tarayıcı etkileşimlerini otomatikleştirmek için Selenium WebDriver kullanır:

```python Code theme={null}
class SeleniumScrapingTool(BaseTool):
    name: str = "Read a website content"
    description: str = "A tool that can be used to read a website content."
    args_schema: Type[BaseModel] = SeleniumScrapingToolSchema
    
    def _run(self, **kwargs: Any) -> Any:
        website_url = kwargs.get("website_url", self.website_url)
        css_element = kwargs.get("css_element", self.css_element)
        return_html = kwargs.get("return_html", self.return_html)
        driver = self._create_driver(website_url, self.cookie, self.wait_time)

        content = self._get_content(driver, css_element, return_html)
        driver.close()

        return "\n".join(content)
```

Araç şu adımları gerçekleştirir:

1. Headless bir Chrome tarayıcı örneği oluşturur
2. Belirtilen URL'ye gider
3. Sayfanın yüklenmesi için belirtilen süre kadar bekler
4. Varsa çerezleri ekler
5. CSS seçicisine göre içeriği çıkarır
6. Çıkarılan içeriği metin veya HTML olarak döndürür
7. Tarayıcı örneğini kapatır

## Dinamik İçeriği Yönetme

`SeleniumScrapingTool`, özellikle JavaScript ile yüklenen dinamik içeriğe sahip web sitelerini scrape etmek için kullanışlıdır. Gerçek bir tarayıcı örneği kullandığı için şunları yapabilir:

1. Sayfada JavaScript çalıştırma
2. Dinamik içeriğin yüklenmesini bekleme
3. Gerekirse öğelerle etkileşime girme
4. Basit HTTP istekleriyle erişilemeyecek içeriği çıkarma

Çıkarım öncesinde tüm dinamik içeriğin yüklendiğinden emin olmak için `wait_time` parametresini ayarlayabilirsiniz.

## Sonuç

`SeleniumScrapingTool`, tarayıcı otomasyonu kullanarak web sitelerinden içerik çıkarmak için güçlü bir yol sunar. Ajanların gerçek bir kullanıcı gibi web siteleriyle etkileşime girmesini sağlayarak daha basit yöntemlerle çıkarılması zor veya imkansız olan dinamik içeriğin scrape edilmesini kolaylaştırır. Bu araç, özellikle JavaScript ile render edilen içerik içeren modern web uygulamalarında araştırma, veri toplama ve izleme görevleri için kullanışlıdır.
