> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Ajanları Özelleştirme

> CrewAI çerçevesinde ajanları belirli roller, görevler ve gelişmiş özelleştirmeler için uyarlamaya yönelik kapsamlı kılavuz.

## Özelleştirilebilir Nitelikler

Verimli bir CrewAI ekibi oluşturmanın temeli, yapay zeka ajanlarını herhangi bir projenin benzersiz gereksinimlerini karşılayacak şekilde dinamik olarak uyarlayabilme yeteneğine dayanır. Bu bölüm, özelleştirebileceğiniz temel nitelikleri kapsamaktadır.

### Özelleştirme İçin Temel Nitelikler

| Nitelik | Açıklama |
| :--- | :--- |
| **Role** | Ajanın ekip içindeki işini belirtir; örneğin 'Analist' veya 'Müşteri Hizmetleri Temsilcisi'. |
| **Goal** | Ajanın hedeflerini, rolüyle ve ekibin genel misyonuyla uyumlu biçimde tanımlar. |
| **Backstory** | Ajanın kişiliğine derinlik katarak ekip içindeki motivasyonları ve etkileşimleri güçlendirir. |
| **Tools** *(İsteğe Bağlı)* | Ajanın görevler için kullandığı yetenekleri veya yöntemleri temsil eder; basit fonksiyonlardan karmaşık entegrasyonlara kadar uzanır. |
| **Cache** *(İsteğe Bağlı)* | Ajanın araç kullanımı için önbellek kullanıp kullanmaması gerektiğini belirler. |
| **Max RPM** | Dakika başına maksimum istek sayısını (`max_rpm`) ayarlar. Harici servislere sınırsız istek için `None` olarak ayarlanabilir. |
| **Verbose** *(İsteğe Bağlı)* | Hata ayıklama ve optimizasyon için ayrıntılı günlüklemeyi etkinleştirir; yürütme süreçlerine ilişkin içgörüler sağlar. |
| **Allow Delegation** *(İsteğe Bağlı)* | Görev delegasyonunu diğer ajanlara kontrol eder; varsayılan `False`'tur. |
| **Max Iter** *(İsteğe Bağlı)* | Sonsuz döngüleri önlemek için bir görev için maksimum yineleme sayısını (`max_iter`) sınırlar; varsayılan 25'tir. |
| **Max Execution Time** *(İsteğe Bağlı)* | Bir ajanın görevi tamamlaması için izin verilen maksimum süreyi ayarlar. |
| **System Template** *(İsteğe Bağlı)* | Ajan için sistem formatını tanımlar. |
| **Prompt Template** *(İsteğe Bağlı)* | Ajan için istem formatını tanımlar. |
| **Response Template** *(İsteğe Bağlı)* | Ajan için yanıt formatını tanımlar. |
| **Use System Prompt** *(İsteğe Bağlı)* | Ajanın görev yürütme sırasında sistem istemi kullanıp kullanmayacağını kontrol eder. |
| **Respect Context Window** | Bağlam boyutunu koruyan kayan bağlam penceresini varsayılan olarak etkinleştirir. |
| **Max Retry Limit** | Hata durumunda bir ajan için maksimum yeniden deneme sayısını (`max_retry_limit`) ayarlar. |

## Gelişmiş Özelleştirme Seçenekleri

Temel niteliklerin ötesinde CrewAI, bir ajanın davranışını ve yeteneklerini önemli ölçüde geliştirmek için daha derin özelleştirmeye imkân tanır.

### Dil Modeli Özelleştirme

Ajanlar, özel dil modelleri (`llm`) ve fonksiyon çağırma dil modelleri (`function_calling_llm`) ile özelleştirilebilir; bu da işleme ve karar verme yetenekleri üzerinde gelişmiş kontrol sunar. `function_calling_llm` ayarlanmasının varsayılan ekip fonksiyon çağırma dil modelini geçersiz kılarak daha yüksek düzeyde özelleştirme sağladığına dikkat etmek önemlidir.

## Performans ve Hata Ayıklama Ayarları

Bir ajanın performansını ayarlamak ve operasyonlarını izlemek, verimli görev yürütme için kritik öneme sahiptir.

### Ayrıntılı Mod ve RPM Sınırı

- **Ayrıntılı Mod**: Hata ayıklama ve optimizasyon için kullanışlı olan ajanın eylemlerinin ayrıntılı günlüklenmesini etkinleştirir. Özellikle ajan yürütme süreçlerine ilişkin içgörüler sağlayarak performans optimizasyonuna yardımcı olur.
- **RPM Sınırı**: Dakika başına maksimum istek sayısını (`max_rpm`) ayarlar. Bu nitelik isteğe bağlıdır; gerektiğinde harici servislere sınırsız sorguya izin vermek için `None` olarak ayarlanabilir.

### Görev Yürütme İçin Maksimum Yineleme

`max_iter` niteliği, kullanıcıların bir ajanın tek bir görev için gerçekleştirebileceği maksimum yineleme sayısını tanımlamasına imkân tanır; sonsuz döngüleri veya aşırı uzun yürütmeleri önler. Varsayılan değer, kapsamlılık ile verimlilik arasında denge sağlayan 25 olarak ayarlanmıştır. Ajan bu sayıya yaklaştığında mümkün olan en iyi yanıtı vermeye çalışır.

## Ajanları ve Araçları Özelleştirme

Ajanlar, başlatma sırasında nitelikleri ve araçları tanımlanarak özelleştirilir. Araçlar, ajanların özel görevler gerçekleştirmesini sağlayarak işlevselliğin kritik bileşenidir. `tools` niteliği, ajanın kullanabileceği araçlardan oluşan bir dizi olmalıdır ve varsayılan olarak boş liste olarak başlatılır. Araçlar, yeni gereksinimlere uyum sağlamak amacıyla ajan başlatıldıktan sonra eklenebilir veya değiştirilebilir.

```shell
pip install 'crewai[tools]'
```

### Örnek: Bir Ajana Araç Atama

```python
import os
from crewai import Agent
from crewai_tools import SerperDevTool

# Araç başlatma için API anahtarlarını ayarlayın
os.environ["OPENAI_API_KEY"] = "Your Key"
os.environ["SERPER_API_KEY"] = "Your Key"

# Bir arama aracı başlatın
search_tool = SerperDevTool()

# Ajanı gelişmiş seçeneklerle başlatın
agent = Agent(
  role='Research Analyst',
  goal='Güncel pazar analizi sağla',
  backstory='Pazar trendlerini keskin bir gözle takip eden uzman bir analist.',
  tools=[search_tool],
  memory=True, # Belleği etkinleştir
  verbose=True,
  max_rpm=None, # Dakika başına istek sınırı yok
  max_iter=25, # Maksimum yineleme için varsayılan değer
)
```

## Delegasyon ve Özerklik

Bir ajanın görev devretme veya soru sorma yeteneğini kontrol etmek, CrewAI çerçevesi içindeki özerkliğini ve iş birliği dinamiklerini şekillendirmek açısından hayati önem taşır. Varsayılan olarak `allow_delegation` niteliği `False` olarak ayarlanmıştır; bu da ajanların gerektiğinde yardım aramasını veya görev devretmesini devre dışı bırakır. Bu varsayılan davranış, CrewAI ekosistemi içinde iş birlikçi problem çözmeyi ve verimliliği teşvik edecek şekilde değiştirilebilir. Gerektiğinde, belirli operasyonel gereksinimlere uyacak şekilde delegasyon etkinleştirilebilir.

### Örnek: Bir Ajan İçin Delegasyonu Etkinleştirme

```python
agent = Agent(
  role='Content Writer',
  goal='Pazar trendleri hakkında ilgi çekici içerikler yaz',
  backstory='Pazar analizi konusunda uzmanlığa sahip deneyimli bir yazar.',
  allow_delegation=True # Delegasyonu etkinleştir
)
```

## Sonuç

CrewAI'de ajanları rolleri, hedefleri, geçmiş hikayeleri ve araçlarıyla birlikte; dil modeli özelleştirme, bellek, performans ayarları ve delegasyon tercihleri gibi gelişmiş seçeneklerle özelleştirmek, karmaşık zorluklara hazır nüanslı ve yetenekli bir yapay zeka ekibi oluşturur.
