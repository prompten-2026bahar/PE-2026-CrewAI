## Etkinlik Dinleyicileri

### Genel Bakış

CrewAI, yürütme yaşam döngüsü boyunca çeşitli olaylara tepki vermenizi sağlayan güçlü bir olay sistemi sağlar. Bu özellik, özel entegrasyonlar, izleme çözümleri, günlükleme sistemleri veya CrewAI'nin iç olaylarına göre tetiklenmesi gereken diğer işlevleri oluşturmanızı sağlar.

### Nasıl Çalışır

CrewAI, yürütme yaşam döngüsü boyunca olayları yaymak için bir olay otobüsü mimarisi kullanır. Olay sistemi aşağıdaki bileşenlere dayanır:

1. **CrewAIEventsBus**: Olay kaydını ve yayımını yöneten tekil bir olay otobüsü.
2. **BaseEvent**: Sistemdeki tüm olaylar için temel sınıf.
3. **BaseEventListener**: Özel olay dinleyicileri oluşturmak için soyut temel sınıf.

CrewAI'de belirli eylemler meydana geldiğinde (Crew yürütmesinin başlaması, bir Aracının bir görevi tamamlaması veya bir aracın kullanılması gibi), ilgili olaylar yayımlanır. Bunlar meydana geldiğinde özel kod yürütmek için bu olaylar için işleyiciler kaydedebilirsiniz.

CrewAI AMP, tüm istemleri, tamamlamaları ve ilgili meta verileri izlemek, depolamak ve görselleştirmek için olay sistemini kullanan yerleşik bir İstek İzleme özelliğine sahiptir. Bu, güçlü hata ayıklama yetenekleri ve Aracınızın operasyonları hakkında şeffaflık sağlar.

![İstek İzleme Panosu](../images/traces-overview.png)

İstek İzleme ile şunları yapabilirsiniz:

- LLM'nize gönderilen tüm istemlerin tam geçmişini görüntüleyin
- Belge kullanımını ve maliyetleri izleyin
- Aracın akıl yürütme hatalarını ayıklayın
- İstek dizilerini ekibinizle paylaşın
- Farklı istem stratejilerini karşılaştırın
- Uyumluluk ve denetim için izleri dışa aktarın

### Özel Bir Etkinlik Dinleyicisi Oluşturma

Özel bir etkinlik dinleyicisi oluşturmak için şunları yapmanız gerekir:

1. `BaseEventListener`'dan devralan bir sınıf oluşturun
2. `setup_listeners` yöntemini uygulayın
3. İlgili olaylar için işleyiciler kaydedin
4. İşleyicinizin bir örneğini uygun dosyada oluşturun

İşte özel bir etkinlik dinleyicisi sınıfının basit bir örneği:

```python
from crewai.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
)
from crewai.events import BaseEventListener

class MyCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            print(f"Crew '{event.crew_name}' yürütme başladı!")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            print(f"Crew '{event.crew_name}' yürütme tamamlandı!")
            print(f"Çıktı: {event.output}")

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print(f"Aracı '{event.agent.role}' görevi tamamladı")
            print(f"Çıktı: {event.output}")
```

### İşleyicinizi Düzgün Bir Şekilde Kaydetme

Sadece dinleyici sınıfınızı tanımlamak yeterli değildir. Bir örneğini oluşturmanız ve uygulamanızda içe aktarmayı sağlamanız gerekir. Bu, şunları sağlar:

1. Olay işleyicileri olay otobüsüyle kayıtlıdır
2. Dinleyici örneği bellekte kalır (çöp toplama olmaz)
3. Olaylar yayımlanırken dinleyici aktiftir

### Seçenek 1: Ekip veya Akış Uygulamanızda İçe Aktarın ve Örneklendirin

Yapmanız gereken en önemli şey, dinleyicinizin örneğini Ekip veya Akışınızın tanımlandığı ve yürütüldüğü dosyada oluşturmaktır:

#### Ekip Tabanlı Uygulamalar için

Dinleyicinizin örneğini Ekip uygulamanız dosyasının en üstüne oluşturun ve aktarın:

```python
# crew.py dosyanızda
from crewai import Agent, Crew, Task
from my_listeners import MyCustomListener

# Dinleyicinizin bir örneğini oluşturun
my_listener = MyCustomListener()

class MyCustomCrew:
    # Ekip uygulamanız...

    def crew(self):
        return Crew(
            agents=[...],
            tasks=[...],
            # ...
        )
```

#### Akış Tabanlı Uygulamalar için

Dinleyicinizin örneğini Akış uygulamanız dosyasının en üstüne oluşturun ve aktarın:

```python
# main.py veya flow.py dosyanızda
from crewai.flow import Flow, listen, start
from my_listeners import MyCustomListener

# Dinleyicinizin bir örneğini oluşturun
my_listener = MyCustomListener()

class MyCustomFlow(Flow):
    # Akış uygulamanız...

    @start()
    def first_step(self):
        # ...
```

Bu, dinleyicinizin yüklü ve aktif olduğundan emin olurken Ekip veya Akışınız yürütülür.

### Seçenek 2: Dinleyicileriniz için Bir Paket Oluşturun

Özellikle birden fazla dinleyiciniz varsa, daha yapılandırılmış bir yaklaşım için:

1. Dinleyicileriniz için bir paket oluşturun:

```
my_project/
  ├── listeners/
  │   ├── __init__.py
  │   ├── my_custom_listener.py
  │   └── another_listener.py
```

2. `my_custom_listener.py` içinde dinleyici sınıfınızı tanımlayın ve bir örnek oluşturun:

```python
# my_custom_listener.py
from crewai.events import BaseEventListener
# ... olayları içe aktar ...

class MyCustomListener(BaseEventListener):
    # ... uygulama ...

# Dinleyicinizin bir örneğini oluşturun
my_custom_listener = MyCustomListener()
```

3. `__init__.py`'de işleyicilerinizi yüklenmelerini sağlamak için aktarın:

```python
# __init__.py
from .my_custom_listener import my_custom_listener
from .another_listener import another_listener

# İhtiyacınız varsa bunları dışa aktarmayı seçin
__all__ = ['my_custom_listener', 'another_listener']
```

4. Ekip veya Akış dosyanızda dinleyiciler paketinizin içe aktarın:

```python
# crew.py veya flow.py dosyanızda

class MyCustomCrew:
    # Ekip uygulamanız...
```

Bu, üçüncü taraf etkinlik dinleyicilerinin CrewAI kodu tabanında nasıl kaydedildiğinin yoludur.

### Mevcut Olay Türleri

CrewAI, dinleyebileceğiniz çok çeşitli olaylar sağlar:

### Ekip Olayları

- **CrewKickoffStartedEvent**: Bir Ekip yürütmeye başladığında yayımlanır
- **CrewKickoffCompletedEvent**: Bir Ekip yürütmeyi tamamladığında yayımlanır
- **CrewKickoffFailedEvent**: Bir Ekip yürütmeyi tamamlayamadığında yayımlanır
- **CrewTestStartedEvent**: Bir Ekip testi başlatırken yayımlanır
- **CrewTestCompletedEvent**: Bir Ekip testi tamamladığında yayımlanır
- **CrewTestFailedEvent**: Bir Ekip testi tamamlayamadığında yayımlanır
- **CrewTrainStartedEvent**: Bir Ekip eğitimi başlatırken yayımlanır
- **CrewTrainCompletedEvent**: Bir Ekip eğitimi tamamladığında yayımlanır
- **CrewTrainFailedEvent**: Bir Ekip eğitimi tamamlayamadığında yayımlanır

### Aracı Olayları

- **AgentExecutionStartedEvent**: Bir Aracının bir görevi yürütmeye başladığında yayımlanır
- **AgentExecutionCompletedEvent**: Bir Aracının bir görevi yürütmeyi tamamladığında yayımlanır
- **AgentExecutionErrorEvent**: Bir Aracı yürütme sırasında bir hatayla karşılaştığında yayımlanır

### Görev Olayları

- **TaskStartedEvent**: Bir Görev yürütmeye başladığında yayımlanır
- **TaskCompletedEvent**: Bir Görev yürütmeyi tamamladığında yayımlanır
- **TaskFailedEvent**: Bir Görev yürütmeyi tamamlayamadığında yayımlanır
- **TaskEvaluationEvent**: Bir Görev değerlendirildiğinde yayımlanır

### Araç Kullanımı Olayları

- **ToolUsageStartedEvent**: Bir araç yürütmesinin başlatıldığında yayımlanır
- **ToolUsageFinishedEvent**: Bir araç yürütmesinin tamamlandığında yayımlanır
- **ToolUsageErrorEvent**: Bir araç yürütmesi bir hatayla karşılaştığında yayımlanır
- **ToolValidateInputErrorEvent**: Bir araç giriş doğrulaması bir hatayla karşılaştığında yayımlanır
- **ToolExecutionErrorEvent**: Bir araç yürütmesi bir hatayla karşılaştığında yayımlanır
- **ToolSelectionErrorEvent**: Bir araç seçerken bir hata olduğunda yayımlanır

### Bilgi Olayları

- **KnowledgeRetrievalStartedEvent**: Bir bilgi alma işlemi başlatıldığında yayımlanır
- **KnowledgeRetrievalCompletedEvent**: Bir bilgi alma işlemi tamamlandığında yayımlanır
- **KnowledgeQueryStartedEvent**: Bir bilgi sorgusu başlatıldığında yayımlanır
- **KnowledgeQueryCompletedEvent**: Bir bilgi sorgusu tamamlandığında yayımlanır
- **KnowledgeQueryFailedEvent**: Bir bilgi sorgusu başarısız olduğunda yayımlanır
- **KnowledgeSearchQueryFailedEvent**: Bir bilgi arama sorgusu başarısız olduğunda yayımlanır

### LLM Koruyucu Olayları

- **LLMGuardrailStartedEvent**: Bir koruyucu doğrulama başladığında yayımlanır. Uygulanan koruyucu ve tekrar sayısı hakkında ayrıntıları içerir.
- **LLMGuardrailCompletedEvent**: Bir koruyucu doğrulama tamamlandığında yayımlanır. Doğrulama başarısı/başarısızlığı, sonuçlar ve varsa hata mesajları hakkında ayrıntıları içerir.

### Akış Olayları

- **FlowCreatedEvent**: Bir Akış oluşturulduğunda yayımlanır
- **FlowStartedEvent**: Bir Akış yürütmeye başladığında yayımlanır
- **FlowFinishedEvent**: Bir Akış tamamlandığında yayımlanır
- **FlowPlotEvent**: Bir Akış çizildiğinde yayımlanır
- **MethodExecutionStartedEvent**: Bir Akış yöntemi yürütmeye başladığında yayımlanır
- **MethodExecutionFinishedEvent**: Bir Akış yöntemi yürütmeyi tamamladığında yayımlanır
- **MethodExecutionFailedEvent**: Bir Akış yöntemi yürütmeyi tamamlayamadığında yayımlanır

### LLM Olayları

- **LLMCallStartedEvent**: Bir LLM çağrısı başladığında yayımlanır
- **LLMCallCompletedEvent**: Bir LLM çağrısı tamamlandığında yayımlanır
- **LLMCallFailedEvent**: Bir LLM çağrısı başarısız olduğunda yayımlanır
- **LLMStreamChunkEvent**: Akış LLM yanıtları sırasında her parça alındığında yayımlanır

### Bellek Olayları

- **MemoryQueryStartedEvent**: Bir bellek sorgusu başlatıldığında yayımlanır. Sorguyu, limiti ve isteğe bağlı puan eşiğini içerir.
- **MemoryQueryCompletedEvent**: Bir bellek sorgusu başarıyla tamamlandığında yayımlanır. Sorguyu, sonuçları, limiti, puan eşiğini ve sorgu yürütme süresini içerir.
- **MemoryQueryFailedEvent**: Bir bellek sorgusu başarısız olduğunda yayımlanır. Sorguyu, limiti, puan eşiğini ve hata mesajını içerir.
- **MemorySaveStartedEvent**: Bir bellek kaydetme işlemi başlatıldığında yayımlanır. Kaydedilecek değeri, meta verileri ve isteğe bağlı araç rolünü içerir.
- **MemorySaveCompletedEvent**: Bir bellek kaydetme işlemi başarıyla tamamlandığında yayımlanır. Kaydedilen değeri, meta verileri, araç rolünü ve kaydetme yürütme süresini içerir.
- **MemorySaveFailedEvent**: Bir bellek kaydetme işlemi başarısız olduğunda yayımlanır. Değeri, meta verileri, araç rolünü ve hata mesajını içerir.
- **MemoryRetrievalStartedEvent**: Bir görev istemi için bellek alma başlatıldığında yayımlanır. İsteğe bağlı görev kimliğini içerir.
- **MemoryRetrievalCompletedEvent**: Bir görev istemi için bellek alma başarıyla tamamlandığında yayımlanır. Görev kimliğini, bellek içeriğini ve alma yürütme süresini içerir.

### İşleyici Yapısı

Her olay işleyicisi iki parametre alır:

1. **kaynak**: Olayı yayan nesne
2. **olay**: Olay tipine özgü veriler içeren olay örneği

Olay nesnesinin yapısı olay tipine bağlıdır, ancak tüm olaylar `BaseEvent`'tan türetilir ve şunları içerir:

- **damga**: Olayın yayımlandığı zaman
- **tür**: Olay tipini tanımlayan bir dize kimlik

Ek alanlar olay tipine göre değişir. Örneğin, `CrewKickoffCompletedEvent`, `crew_name` ve `output` alanlarını içerir.

### Gelişmiş Kullanım: Kapsamlı İşleyiciler

Geçici olay işleme için (test etme veya belirli işlemler için kullanışlı):

```python
from crewai.events import crewai_event_bus, CrewKickoffStartedEvent

with crewai_event_bus.scoped_handlers():
    @crewai_event_bus.on(CrewKickoffStartedEvent)
    def temp_handler(source, event):
        print("Bu işleyici bu bağlam içinde yalnızca var")

    # Olayları yayan bir şey yapın

# Bağlamın dışında, geçici işleyici kaldırılır
```

### Kullanım Alanları

Olay dinleyicileri çeşitli amaçlarla kullanılabilir:

1. **Günlükleme ve İzleme**: Ekip yürütmesinin yürütülmesini izleyin ve önemli olayları günlüğe kaydedin
2. **Analitik**: Ekip performansının ve davranışının verilerini toplayın
3. **Hata Ayıklama**: Belirli sorunları ayıklamak için geçici dinleyiciler ayarlayın
4. **Entegrasyon**: CrewAI'yı izleme platformları, veritabanları veya bildirim hizmetleri gibi harici sistemlerle entegre edin
5. **Özel Davranış**: Belirli olaylara göre özel eylemleri tetikleyin

CrewAI'nin olay sistemini kullanarak işlevselliğini genişletebilir ve mevcut altyapınızla sorunsuz bir şekilde entegre edebilirsiniz.