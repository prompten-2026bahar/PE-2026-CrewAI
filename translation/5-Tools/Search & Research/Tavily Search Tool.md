> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Tavily Arama Aracı

> Tavily Search API kullanarak kapsamlı web aramaları gerçekleştirin

`TavilySearchTool`, Tavily Search API için bir arayüz sağlar ve CrewAI ajanlarının kapsamlı web aramaları yapmasına olanak tanır. Arama derinliğini, konuları, zaman aralıklarını, dahil edilen/edilmeyen alan adlarını ve sonuçlara doğrudan yanıtlar, ham içerik veya görsellerin dahil edilip edilmeyeceğini belirlemeye izin verir.

## Kurulum

`TavilySearchTool` kullanmak için `tavily-python` kütüphanesini kurmanız gerekir:

```shell  theme={null}
pip install 'crewai[tools]' tavily-python
```

## Ortam Değişkenleri

Tavily API anahtarınızın bir ortam değişkeni olarak ayarlandığından emin olun:

```bash  theme={null}
export TAVILY_API_KEY='your_tavily_api_key'
```

API anahtarını [https://app.tavily.com/](https://app.tavily.com/) üzerinden alın (kaydolun, ardından bir anahtar oluşturun).

## Kullanım Örneği

`TavilySearchTool` aracını bir CrewAI ajanı içinde başlatmak ve kullanmak için şu örneği izleyebilirsiniz:

```python  theme={null}
import os
from crewai import Agent, Task, Crew
from crewai_tools import TavilySearchTool

# TAVILY_API_KEY ortam değişkeninin ayarlı olduğundan emin olun
# os.environ["TAVILY_API_KEY"] = "YOUR_TAVILY_API_KEY"

# Aracı başlat
tavily_tool = TavilySearchTool()

# Aracı kullanan bir ajan oluştur
researcher = Agent(
    role='Pazar Araştırmacısı',
    goal='En son yapay zeka trendleri hakkında bilgi bul',
    backstory='Teknoloji alanında uzman bir pazar araştırmacısı.',
    tools=[tavily_tool],
    verbose=True
)

# Ajan için bir görev oluştur
research_task = Task(
    description='2024 yılındaki en önemli 3 yapay zeka trendini ara.',
    expected_output='Bulunan en önemli 3 yapay zeka trendini özetleyen bir JSON raporu.',
    agent=researcher
)

# Ekibi oluştur ve başlat
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=2
)

result = crew.kickoff()
print(result)
```

## Yapılandırma Seçenekleri

`TavilySearchTool`, başlatma sırasında veya `run` metodu çağrılırken şu argümanları kabul eder:

* `query` (str): **Gerekli**. Arama sorgusu dizesi.
* `search_depth` (Literal\["basic", "advanced"], optional): Aramanın derinliği. Varsayılan `"basic"`.
* `topic` (Literal\["general", "news", "finance"], optional): Aramanın odaklanacağı konu. Varsayılan `"general"`.
* `time_range` (Literal\["day", "week", "month", "year"], optional): Arama için zaman aralığı. Varsayılan `None`.
* `days` (int, optional): Kaç gün geriye dönük aranacağı. `time_range` ayarlı değilse anlamlıdır. Varsayılan `7`.
* `max_results` (int, optional): Döndürülecek maksimum arama sonucu sayısı. Varsayılan `5`.
* `include_domains` (Sequence\[str], optional): Aramada öncelik verilecek alan adlarının listesi. Varsayılan `None`.
* `exclude_domains` (Sequence\[str], optional): Aramadan hariç tutulacak alan adlarının listesi. Varsayılan `None`.
* `include_answer` (Union\[bool, Literal\["basic", "advanced"]], optional): Arama sonuçlarından sentezlenmiş doğrudan bir yanıtın dahil edilip edilmeyeceği. Varsayılan `False`.
* `include_raw_content` (bool, optional): Aranan sayfaların ham HTML içeriğinin dahil edilip edilmeyeceği. Varsayılan `False`.
* `include_images` (bool, optional): Görsel sonuçlarının dahil edilip edilmeyeceği. Varsayılan `False`.
* `timeout` (int, optional): İstek zaman aşımı, saniye cinsinden. Varsayılan `60`.

## Gelişmiş Kullanım

Aracı özel parametrelerle yapılandırabilirsiniz:

```python  theme={null}
# Örnek: Belirli parametrelerle başlat
custom_tavily_tool = TavilySearchTool(
    search_depth='advanced',
    max_results=10,
    include_answer=True
)

# Ajan bu varsayılanları kullanacaktır
agent_with_custom_tool = Agent(
    role="Gelişmiş Araştırmacı",
    goal="Kapsamlı sonuçlarla ayrıntılı araştırma yürüt",
    tools=[custom_tavily_tool]
)
```

## Özellikler

* **Kapsamlı Arama**: Tavily’nin güçlü arama dizinine erişim
* **Yapılandırılabilir Derinlik**: Temel ve gelişmiş arama modları arasında seçim yapın
* **Konu Filtreleme**: Aramaları genel, haber veya finans konularına odaklayın
* **Zaman Aralığı Kontrolü**: Sonuçları belirli zaman dönemleriyle sınırlayın
* **Alan Adı Kontrolü**: Belirli alan adlarını dahil edin veya hariç tutun
* **Doğrudan Yanıtlar**: Arama sonuçlarından sentezlenmiş yanıtlar alın
* **İçerik Filtreleme**: Otomatik içerik kısaltma ile bağlam penceresi sorunlarını önleyin

## Yanıt Biçimi

Araç, şu öğeleri içeren bir JSON dizesi olarak arama sonuçlarını döndürür:

* Başlıklar, URL’ler ve içerik parçacıklarıyla arama sonuçları
* Sorgulara isteğe bağlı doğrudan yanıtlar
* İsteğe bağlı görsel sonuçları
* İsteğe bağlı ham HTML içeriği (etkinleştirildiğinde)

Her sonuç için içerik, en ilgili bilgiyi korurken bağlam penceresi sorunlarını önlemek amacıyla otomatik olarak kısaltılır.
