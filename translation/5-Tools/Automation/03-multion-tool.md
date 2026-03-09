# MultiOn Aracı

> `MultiOnTool`, CrewAI ajanlarına doğal dil talimatları aracılığıyla web üzerinde gezinme ve etkileşim kurma yeteneği kazandırır.

## Genel Bakış

`MultiOnTool`, [MultiOn'un](https://docs.multion.ai/welcome) web tarama yeteneklerini sarmalamak için tasarlanmıştır ve CrewAI ajanlarının doğal dil talimatlarını kullanarak web tarayıcılarını kontrol etmelerini sağlar. Bu araç, web tabanlı görevlerin otomasyonu ve dinamik web verisi etkileşimi gerektiren projeler için temel bir varlık haline gelerek sorunsuz web taramasını kolaylaştırır.

## Kurulum

Bu aracı kullanmak için MultiOn paketini yüklemeniz gerekir:

```shell  theme={null}
uv add multion
```

Ayrıca MultiOn tarayıcı uzantısını yüklemeniz ve API kullanımını etkinleştirmeniz gerekecektir.

## Başlangıç Adımları

`MultiOnTool`'u etkili bir şekilde kullanmak için şu adımları izleyin:

1. **CrewAI'yi Kurun**: `crewai[tools]` paketinin Python ortamınızda kurulu olduğundan emin olun.
2. **MultiOn'u Kurun ve Kullanın**: MultiOn Tarayıcı Uzantısını yüklemek için [MultiOn dökümantasyonunu](https://docs.multion.ai/learn/browser-extension) takip edin.
3. **API Kullanımını Etkinleştirin**: Tarayıcınızın uzantılar klasöründeki MultiOn uzantısına tıklayarak (web sayfasındaki yüzen MultiOn simgesine değil) uzantı yapılandırmalarını açın. API'yi etkinleştirmek için "API Enabled" düğmesine tıklayın.

## Örnek

Aşağıdaki örnek, aracın nasıl başlatılacağını ve bir web tarama görevinin nasıl yürütüleceğini gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MultiOnTool

# Aracı başlatın
multion_tool = MultiOnTool(api_key="MULTION_API_KEY_NIZ", local=False)

# Aracı kullanan bir ajan tanımlayın
browser_agent = Agent(
    role="Tarayıcı Ajanı",
    goal="Doğal dili kullanarak web tarayıcılarını kontrol et",
    backstory="Uzman bir tarama ajanı.",
    tools=[multion_tool],
    verbose=True,
)

# Haberleri arama ve özetleme görevi örneği
browse_task = Task(
    description="Trend olan ilk 3 yapay zeka haber başlığını özetle",
    expected_output="Trend olan ilk 3 yapay zeka haber başlığının özeti",
    agent=browser_agent,
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(agents=[browser_agent], tasks=[browse_task])
result = crew.kickoff()
```

## Parametreler

`MultiOnTool`, başlatma sırasında aşağıdaki parametreleri kabul eder:

* **api\_key**: Opsiyonel. MultiOn API anahtarını belirtir. Sağlanmazsa `MULTION_API_KEY` ortam değişkenine bakar.
* **local**: Opsiyonel. Ajanı yerel tarayıcınızda çalıştırmak için `True` olarak ayarlayın. MultiOn tarayıcı uzantısının kurulu olduğundan ve "API Enabled" seçeneğinin işaretli olduğundan emin olun. Varsayılan: `False`.
* **max\_steps**: Opsiyonel. MultiOn ajanının bir komut için atabileceği maksimum adım sayısını belirler. Varsayılan: `3`.

## Kullanım

`MultiOnTool` kullanıldığında, ajan aracın web tarama eylemlerine çevirdiği doğal dil talimatları sağlayacaktır. Araç, tarama oturumunun sonuçlarını bir durumla birlikte döndürür.

```python Code theme={null}
# Aracın bir ajanla kullanım örneği
browser_agent = Agent(
    role="Web Tarayıcı Ajanı",
    goal="Web'de bilgi ara ve özetle",
    backstory="Web sitelerinden bilgi bulma ve ayıklama konusunda uzman.",
    tools=[multion_tool],
    verbose=True,
)

# Ajan için bir görev oluşturun
search_task = Task(
    description="TechCrunch'ta en son yapay zeka haberlerini ara ve ilk 3 başlığı özetle",
    expected_output="TechCrunch'tan alınan ilk 3 yapay zeka haber başlığının özeti",
    agent=browser_agent,
)

# Görevi çalıştırın
crew = Crew(agents=[browser_agent], tasks=[search_task])
result = crew.kickoff()
```

Döndürülen durum `CONTINUE` ise, ajana yürütmeye devam etmek için aynı talimatı yeniden vermesi söylenmelidir.

## Uygulama Detayları

`MultiOnTool`, CrewAI'den `BaseTool` sınıfının bir alt sınıfı olarak uygulanmıştır. Web tarama yetenekleri sağlamak için MultiOn istemcisini (client) sarmalar:

```python Code theme={null}
class MultiOnTool(BaseTool):
    """MultiOn Tarama Yeteneklerini sarmalayan araç."""

    name: str = "Multion Browse Tool"
    description: str = """MultiOn, LLM'lerin doğal dil talimatlarını kullanarak web tarayıcılarını kontrol etmesini sağlar.
            Durum 'CONTINUE' ise yürütmeye devam etmek için aynı talimatı yeniden verin.
        """
    
    # Uygulama detayları...
    
    def _run(self, cmd: str, *args: Any, **kwargs: Any) -> str:
        """
        Multion istemcisini verilen komutla çalıştırır.
        
        Argümanlar:
            cmd (str): Web taraması için ayrıntılı ve spesifik doğal dil talimatı
            *args (Any): MultiOn istemcisine iletilecek ek argümanlar
            **kwargs (Any): MultiOn istemcisine iletilecek ek anahtar kelime argümanları
        """
        # Uygulama detayları...
```

## Sonuç

`MultiOnTool`, web tarama yeteneklerini CrewAI ajanlarına entegre etmenin güçlü bir yolunu sunar. Ajanların doğal dil talimatları yoluyla web siteleriyle etkileşim kurmasını sağlayarak; veri toplama ve araştırmadan, web servisleriyle otomatik etkileşimlere kadar web tabanlı görevler için geniş bir olasılık yelpazesi açar.
