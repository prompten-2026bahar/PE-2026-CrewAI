> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# SerpApi Google Alışveriş Aracı

> `SerpApiGoogleShoppingTool`, SerpApi kullanarak Google Alışveriş sonuçlarını arar.

# `SerpApiGoogleShoppingTool`

## Açıklama

SerpApi üzerinden Google Alışveriş'i sorgulamak ve ürün odaklı sonuçları almak için `SerpApiGoogleShoppingTool`'u kullanın.

## Kurulum

```shell  theme={null}
uv add crewai-tools[serpapi]
```

## Ortam Değişkenleri

* `SERPAPI_API_KEY` (gerekli): SerpApi için API anahtarı. [https://serpapi.com/](https://serpapi.com/) adresinde bir tane oluşturun (ücretsiz katman mevcut).

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import SerpApiGoogleShoppingTool

tool = SerpApiGoogleShoppingTool()

agent = Agent(
    role="Shopping Researcher",
    goal="Find relevant products",
    backstory="Expert in product search",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="Search Google Shopping for 'wireless noise-canceling headphones'",
    expected_output="Top relevant products with titles and links",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

## Notlar

* Ortamda `SERPAPI_API_KEY` belirleyin. [https://serpapi.com/](https://serpapi.com/) adresinde bir anahtar oluşturun
* Ayrıca bkz. SerpApi üzerinden Google Web Araması: `/en/tools/search-research/serpapi-googlesearchtool`

## Parametreler

### Çalıştırma Parametreleri

* `search_query` (str, gerekli): Ürün arama sorgusu.
* `location` (str, isteğe bağlı): Coğrafi konum parametresi.

