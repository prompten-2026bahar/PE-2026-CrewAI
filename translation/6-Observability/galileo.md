# Galileo
Galileo entegrasyonu, CrewAI takibi ve değerlendirmesi için

## Genel Bakış

Bu kılavuz, kapsamlı takip ve Değerlendirme Mühendisliği için **Galileo**'yu **CrewAI** ile nasıl entegre edeceğinizi göstermektedir.
Bu kılavuzun sonunda, CrewAI ajanlarınızı izleyebilecek, performanslarını izleyebilecek ve Galileo'nun güçlü gözlemlenebilirlik platformuyla davranışlarını değerlendirebileceksiniz.

> **Galileo Nedir?** [Galileo](https://galileo.ai), uçtan uca izleme, değerlendirme ve izleme sağlayan bir yapay zeka değerlendirme ve gözlemlenebilirlik platformudur. AI uygulamaları için gerçek verileri yakalamayı, sağlam güvenlik duvarları oluşturmayı ve yerleşik deneyim izleme ve performans analitiği ile sistematik deneyler çalıştırmayı mümkün kılar; bu da yapay zeka yaşam döngüsü boyunca güvenilirliği, şeffaflığı ve sürekli iyileştirmeyi sağlar.

## Başlangıç

Bu eğitim, [CrewAI hızlı başlangıç](/en/quickstart) eğitimini takip eder ve Galileo'nun [CrewAIEventListener](https://v2docs.galileo.ai/sdk-api/python/reference/handlers/crewai/handler) olay işleyicisinin nasıl ekleneceğini gösterir.
Daha fazla bilgi için Galileo'nun [CrewAI Uygulamasına Galileo Ekleme](https://v2docs.galileo.ai/how-to-guides/third-party-integrations/add-galileo-to-crewai/add-galileo-to-crewai) kılavızına bakın.

> **Not** Bu eğitim, [CrewAI hızlı başlangıç](/en/quickstart) eğitimini tamamladığınızı varsayar. Kapsamlı bir örnek için, Galileo'nun [CrewAI sdk-example repo](https://github.com/rungalileo/sdk-examples/tree/main/python/agent/crew-ai) deposuna bakın.

### 1. Adım: Bağımlılıkları yükleyin

Uygulamanız için gerekli bağımlılıkları yükleyin.
Tercih ettiğiniz yöntemle bir sanal ortam oluşturun ve ardından tercih ettiğiniz araçla bu ortam içinde bağımlılıkları yükleyin:

```bash
uv add galileo 
```

### 2. Adım: Çevrimdışı [CrewAI hızlı başlangıç](/en/quickstart) dosyasından `.env` dosyasına ekleyin

```bash
# Galileo API anahtarınız
GALILEO_API_KEY="your-galileo-api-key"

# Galileo proje adınız
GALILEO_PROJECT="your-galileo-project-name"

# Günlük kaydı için kullanmak istediğiniz Log akışı adı
GALILEO_LOG_STREAM="your-galileo-log-stream "
```

### 3. Adım: Galileo olay dinleyicisini ekleyin

Galileo ile günlük kaydını etkinleştirmek için, `CrewAIEventListener` örneğini oluşturmanız gerekir.
Aşağıdaki kodu main.py dosyanızın en üstüne ekleyerek Galileo CrewAI işleyici paketini içe aktarın:

```python
from galileo.handlers.crewai.handler import CrewAIEventListener
```

Çalıştırma fonksiyonunuzun başında olay dinleyicisini oluşturun:

```python
def run():
    # Olay dinleyicisini oluşturun
    CrewAIEventListener()
    # Mevcut kodunuzun geri kalanı buraya gelir
```

Dinleyici örneğini oluşturduğunuzda, otomatik olarak CrewAI ile kayıtlı olur.

### 4. Adım: Ekibinizi çalıştırın

CrewAI CLI ile ekibinizi çalıştırın:

```bash
crewai run
```

### 5. Adım: İzlemeleri Galileo'da görüntüleyin

Ekibiniz bitirdikten sonra izlemeler akışa verilecek ve Galileo'da görünecektir.

![Galileo izleme görünümü](../images/galileo-trace-veiw.png)
  
## Galileo Entegrasyonunu Anlamak

Galileo, Crew yürütme olaylarını (örneğin, aracı eylemleri, araç çağrıları, model yanıtları) yakalayan ve gözlemlenebilirlik ve değerlendirme için Galileo'ya ileten bir olay dinleyicisi kaydederek CrewAI ile entegre olur.

### Olay dinleyicisini anlamak

`CrewAIEventListener()` örneği oluşturmak, Galileo'yu bir CrewAI çalıştırması için etkinleştirmek için gereken tüm işlemlerdir. Dinleyici örneklenirken:

- Otomatik olarak CrewAI ile kayıtlı olur
- Çevrimdışı değişkenlerden Galileo yapılandırmasını okur
- `GALILEO_PROJECT` ve `GALILEO_LOG_STREAM` tarafından belirtilen Galileo projesine ve günlük akışına tüm çalıştırma verilerini kaydeder

Ek yapılandırma veya kod değişikliği gerektirmez.
Tüm veriler, çevrimdışı yapılandırmanız (örneğin, GALILEO_PROJECT ve GALILEO_LOG_STREAM) tarafından belirtilen Galileo projesine ve günlük akışına kaydedilir.