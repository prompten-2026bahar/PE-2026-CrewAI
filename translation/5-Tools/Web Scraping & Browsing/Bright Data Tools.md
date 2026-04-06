> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Bright Data Araçları

> SERP araması, Web Unlocker scraping ve Dataset API için Bright Data entegrasyonları.

# Bright Data Araçları

Bu araç seti, web veri çıkarımı için Bright Data servislerini entegre eder.

## Kurulum

```shell  theme={null}
uv add crewai-tools requests aiohttp
```

## Ortam Değişkenleri

* `BRIGHT_DATA_API_KEY` (required)
* `BRIGHT_DATA_ZONE` (for SERP/Web Unlocker)

[https://brightdata.com/](https://brightdata.com/) üzerinden kimlik bilgilerinizi oluşturun (kaydolun, ardından bir API token'ı ve zone oluşturun).
Dokümantasyonları için: [https://developers.brightdata.com/](https://developers.brightdata.com/)

## Dahil Olan Araçlar

* `BrightDataSearchTool`: Coğrafya/dil/cihaz seçenekleriyle SERP araması (Google/Bing/Yandex).
* `BrightDataWebUnlockerTool`: Anti-bot aşma ve render desteğiyle sayfa scraping işlemi.
* `BrightDataDatasetTool`: Dataset API işlerini çalıştırma ve sonuçları alma.

## Örnekler

### SERP Araması

```python Code theme={null}
from crewai_tools import BrightDataSearchTool

tool = BrightDataSearchTool(
    query="CrewAI", 
    country="us",
)

print(tool.run())
```

### Web Unlocker

```python Code theme={null}
from crewai_tools import BrightDataWebUnlockerTool

tool = BrightDataWebUnlockerTool(
    url="https://example.com", 
    format="markdown",
)

print(tool.run(url="https://example.com"))
```

### Dataset API

```python Code theme={null}
from crewai_tools import BrightDataDatasetTool

tool = BrightDataDatasetTool(
    dataset_type="ecommerce", 
    url="https://example.com/product",
)

print(tool.run())
```

## Sorun Giderme

* 401/403: `BRIGHT_DATA_API_KEY` ve `BRIGHT_DATA_ZONE` değerlerini doğrulayın.
* Boş/engellenmiş içerik: render özelliğini etkinleştirin veya farklı bir zone deneyin.

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import BrightDataSearchTool

tool = BrightDataSearchTool(
    query="CrewAI", 
    country="us",
)

agent = Agent(
            role="Web Araştırmacısı",
            goal="Bright Data ile arama yap",
            backstory="Güvenilir sonuçlar bulur",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="CrewAI için arama yap ve en iyi sonuçları özetle",
    expected_output="Bağlantılarla birlikte kısa özet",
    agent=agent,
)

crew = Crew(
    agents=[agent], 
    tasks=[task],
    verbose=True,
)

result = crew.kickoff()
```
