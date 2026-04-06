> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Exa Arama Aracı

> Herhangi bir sorgu için en alakalı sonuçları bulmak için Exa Search API'sini kullanarak web araması yapın, tam sayfa içeriği, vurgular ve özetler için seçenekler ile.

`EXASearchTool`, CrewAI ajanlarının [Exa](https://exa.ai/) arama API'sini kullanarak web araması yapmasını sağlar. Herhangi bir sorgu için en alakalı sonuçları döndürür, tam sayfa içeriği ve yapay zeka tarafından oluşturulan özetler için seçenekler ile.

## Kurulum

CrewAI araçları paketini yükleyin:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Ortam Değişkenleri

Exa API anahtarınızı bir ortam değişkeni olarak ayarlayın:

```bash  theme={null}
export EXA_API_KEY='your_exa_api_key'
```

[Exa panosundan](https://dashboard.exa.ai/api-keys) bir API anahtarı alın.

## Örnek Kullanım

CrewAI ajanı içinde `EXASearchTool`'u nasıl kullanacağınız aşağıda açıklanmıştır:

```python  theme={null}
import os
from crewai import Agent, Task, Crew
from crewai_tools import EXASearchTool

# Aracı başlat
exa_tool = EXASearchTool()

# Aracı kullanan bir ajan oluştur
researcher = Agent(
    role='Research Analyst',
    goal='Find the latest information on any topic',
    backstory='An expert researcher who finds the most relevant and up-to-date information.',
    tools=[exa_tool],
    verbose=True
)

# Ajan için bir görev oluştur
research_task = Task(
    description='Find the top 3 recent breakthroughs in quantum computing.',
    expected_output='A summary of the top 3 breakthroughs with source URLs.',
    agent=researcher
)

# Crew'u oluştur ve başlat
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

## Yapılandırma Seçenekleri

`EXASearchTool` başlangıçta aşağıdaki parametreleri kabul eder:

* `type` (str, isteğe bağlı): Kullanılacak arama türü. Varsayılan: `"auto"`. Seçenekler: `"auto"`, `"instant"`, `"fast"`, `"deep"`.
* `content` (bool, isteğe bağlı): Sonuçlara tam sayfa içeriğini dahil edip etmeyeceği. Varsayılan: `False`.
* `summary` (bool, isteğe bağlı): Her bir sonucun yapay zeka tarafından oluşturulan özetlerini dahil edip etmeyeceği. `content=True` gerektirir. Varsayılan: `False`.
* `api_key` (str, isteğe bağlı): Exa API anahtarınız. Sağlanmazsa `EXA_API_KEY` ortam değişkenine geri döner.
* `base_url` (str, isteğe bağlı): Özel API sunucu URL'si. Sağlanmazsa `EXA_BASE_URL` ortam değişkenine geri döner.

Aracı çağırırken (veya bir ajan onu çalıştırdığında), aşağıdaki arama parametreleri kullanılabilir:

* `search_query` (str): **Gerekli**. Arama sorgusu dizesi.
* `start_published_date` (str, isteğe bağlı): Bu tarihten sonra yayınlanan sonuçları filtreleyin (ISO 8601 formatı, ör. `"2024-01-01"`).
* `end_published_date` (str, isteğe bağlı): Bu tarihten önce yayınlanan sonuçları filtreleyin (ISO 8601 formatı).
* `include_domains` (list\[str], isteğe bağlı): Aramayı sınırlandırmak için alan adlarının bir listesi.

## Gelişmiş Kullanım

Daha zengin sonuçlar için aracı özel parametrelerle yapılandırabilirsiniz:

```python  theme={null}
# Yapay zeka özetleriyle tam sayfa içeriğini al
exa_tool = EXASearchTool(
    content=True,
    summary=True,
    type="deep"
)

# Bunu bir ajanda kullan
agent = Agent(
    role="Deep Researcher",
    goal="Conduct thorough research with full content and summaries",
    tools=[exa_tool]
)
```

## Özellikler

* **Anlamsal Arama**: Yalnızca anahtar sözcüklere değil, anlama göre sonuçlar bulun
* **Tam İçerik Alma**: Arama sonuçları ile birlikte web sayfalarının tam metnini alın
* **Yapay Zeka Özetleri**: Her bir sonucun kısa, yapay zeka tarafından oluşturulan özetlerini alın
* **Tarih Filtreleme**: Yayınlanan tarih filtreleriyle sonuçları belirli zaman dönemlerine sınırlandırın
* **Domain Filtreleme**: Aramaları belirli domainlerle sınırlandırın

