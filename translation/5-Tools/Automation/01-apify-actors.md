# Apify Aktörleri

> `ApifyActorsTool`, CrewAI iş akışlarınıza web kazıma, tarama (crawling), veri ayıklama ve web otomasyonu yetenekleri kazandırmak için Apify Aktörlerini çağırmanıza olanak tanır.

# `ApifyActorsTool`

[Apify Aktörlerini](https://apify.com/actors) CrewAI iş akışlarınıza entegre edin.

## Açıklama

`ApifyActorsTool`, bulut tabanlı web kazıma ve otomasyon programları olan [Apify Aktörlerini](https://apify.com/actors), CrewAI iş akışlarınıza bağlar. Sosyal medya, arama motorları, çevrimiçi haritalar, e-ticaret siteleri, seyahat portalları veya genel web sitelerinden veri ayıklamak gibi durumlar için [Apify Store](https://apify.com/store) üzerindeki 4.000'den fazla Aktörden herhangi birini kullanın.

Ayrıntılar için Apify dökümantasyonundaki [Apify CrewAI entegrasyonu](https://docs.apify.com/platform/integrations/crewai) sayfasına bakın.

## Başlangıç Adımları

1. **Bağımlılıkları Kurun**: `pip install 'crewai[tools]' langchain-apify` komutunu kullanarak `crewai[tools]` ve `langchain-apify` paketlerini yükleyin.
2. **Apify API Anahtarı Edinin**: [Apify Console](https://console.apify.com/) üzerinden kaydolun ve [Apify API anahtarınızı](https://console.apify.com/settings/integrations) alın.
3. **Ortamı Yapılandırın**: Aracın işlevselliğini etkinleştirmek için Apify API anahtarınızı `APIFY_API_TOKEN` ortam değişkeni (environment variable) olarak ayarlayın.

## Kullanım Örneği

Bir web araması yapmak amacıyla [RAG Web Browser Actor](https://apify.com/apify/rag-web-browser)'ü manuel olarak çalıştırmak için `ApifyActorsTool`'u kullanın:

```python  theme={null}
from crewai_tools import ApifyActorsTool

# Aracı bir Apify Aktörü ile başlatın
tool = ApifyActorsTool(actor_name="apify/rag-web-browser")

# Aracı giriş parametreleriyle çalıştırın
results = tool.run(run_input={"query": "CrewAI nedir?", "maxResults": 5})

# Sonuçları işleyin
for result in results:
    print(f"URL: {result['metadata']['url']}")
    print(f"İçerik: {result.get('markdown', 'N/A')[:100]}...")
```

### Beklenen Çıktı

Yukarıdaki kodu çalıştırmanın çıktısı şöyledir:

```text  theme={null}
URL: https://www.example.com/crewai-giris
İçerik: CrewAI, yapay zeka destekli iş akışları oluşturmak için bir çerçevedir...
URL: https://docs.crewai.com/
İçerik: CrewAI için resmi dökümantasyon...
```

`ApifyActorsTool`, sağlanan `actor_name`'i kullanarak Aktör tanımını ve giriş şemasını Apify'dan otomatik olarak çeker, ardından araç açıklamasını ve argüman şemasını oluşturur. Bu, ajanlarla kullanıldığında sadece geçerli bir `actor_name` belirtmenizin yeterli olduğu ve `run_input` belirtmenize gerek kalmadığı anlamına gelir. İşte nasıl çalıştığı:

```python  theme={null}
from crewai import Agent
from crewai_tools import ApifyActorsTool

rag_browser = ApifyActorsTool(actor_name="apify/rag-web-browser")

agent = Agent(
    role="Araştırma Analisti",
    goal="Belirli konular hakkında bilgi bul ve özetle",
    backstory="Detaylara önem veren deneyimli bir araştırmacısınız",
    tools=[rag_browser],
)
```

[Apify Store](https://apify.com/store) üzerindeki diğer Aktörleri sadece `actor_name`'i değiştirerek ve manuel kullanımda `run_input`'u Aktörün giriş şemasına göre ayarlayarak çalıştırabilirsiniz.

Ajanlarla kullanım örneği için [CrewAI Aktör şablonuna](https://apify.com/templates/python-crewai) bakın.

## Yapılandırma

`ApifyActorsTool`'un çalışması için şu girişler gereklidir:

* **`actor_name`**: Çalıştırılacak Apify Aktörünün ID'si, örn. `"apify/rag-web-browser"`. Tüm Aktörlere [Apify Store](https://apify.com/store) üzerinden göz atın.
* **`run_input`**: Aracı manuel olarak çalıştırırken Aktör için giriş parametrelerini içeren sözlük.
  * Örneğin, `apify/rag-web-browser` Aktörü için: `{"query": "arama terimi", "maxResults": 5}`
  * Giriş parametrelerinin listesi için Aktörün [giriş şemasına](https://apify.com/apify/rag-web-browser/input-schema) bakın.

## Kaynaklar

* **[Apify](https://apify.com/)**: Apify platformunu keşfedin.
* **[Apify'da yapay zeka ajanı nasıl oluşturulur?](https://blog.apify.com/how-to-build-an-ai-agent/)** - Apify platformunda yapay zeka ajanları oluşturma, yayınlama ve paraya dönüştürme konusunda eksiksiz bir rehber.
* **[RAG Web Browser Actor](https://apify.com/apify/rag-web-browser)**: LLM'ler için popüler bir web arama Aktörü.
* **[CrewAI Entegrasyon Rehberi](https://docs.apify.com/platform/integrations/crewai)**: Apify ve CrewAI'yi entegre etmek için resmi rehberi takip edin.
