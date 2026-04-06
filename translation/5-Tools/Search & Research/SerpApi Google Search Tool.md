> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# SerpApi Google Arama Aracı

> `SerpApiGoogleSearchTool`, SerpApi hizmetini kullanarak Google aramaları gerçekleştirir.

# `SerpApiGoogleSearchTool`

## Açıklama

SerpApi ile Google aramaları çalıştırmak ve yapılandırılmış sonuçları almak için `SerpApiGoogleSearchTool`'u kullanın. Bir SerpApi API anahtarı gereklidir.

## Kurulum

```shell  theme={null}
uv add crewai-tools[serpapi]
```

## Ortam Değişkenleri

* `SERPAPI_API_KEY` (gerekli): SerpApi için API anahtarı. [https://serpapi.com/](https://serpapi.com/) adresinde bir tane oluşturun (ücretsiz katman mevcut).

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import SerpApiGoogleSearchTool

tool = SerpApiGoogleSearchTool()

agent = Agent(
    role="Researcher",
    goal="Answer questions using Google search",
    backstory="Search specialist",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="Search for the latest CrewAI releases",
    expected_output="A concise list of relevant results with titles and links",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

## Notlar

* Ortamda `SERPAPI_API_KEY` belirleyin. [https://serpapi.com/](https://serpapi.com/) adresinde bir anahtar oluşturun
* Ayrıca bkz. SerpApi üzerinden Google Alışveriş: `/en/tools/search-research/serpapi-googleshoppingtool`

## Parametreler

### Çalıştırma Parametreleri

* `search_query` (str, gerekli): Google sorgusu.
* `location` (str, isteğe bağlı): Coğrafi konum parametresi.

## Notlar

* Bu araç SerpApi'yi sarmallar ve yapılandırılmış arama sonuçları döndürür.

