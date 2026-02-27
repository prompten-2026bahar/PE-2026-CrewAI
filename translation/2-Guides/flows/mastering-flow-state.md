## Akış Durumu Yönetimini Mükemmelleştirme
CrewAI Akışları'nda sağlam yapay zeka uygulamaları oluşturmak için durumu yönetme, sürdürme ve kullanma konusunda kapsamlı bir rehber.


## Akışlarda Durumun Gücünü Anlama

Durum yönetimi, her türlü gelişmiş yapay zeka iş akışının temelini oluşturur. CrewAI Akışları'nda durum sistemi, bağlamı korumanıza, adımlar arasında veri paylaşmanıza ve karmaşık uygulama mantığı oluşturmanıza olanak tanır. Durum yönetimini ustalaşmak, güvenilir, bakımı kolay ve güçlü yapay zeka uygulamaları oluşturmak için esastır.

Bu rehber, temel kavramlardan gelişmiş tekniklere ve pratik kod örneklerine kadar, CrewAI Akışları'nda durumu yönetme konusunda bilmeniz gereken her şeyi adım adım açıklayacaktır.

### Neden Durum Yönetimi Önemlidir

Etkili durum yönetimi şunları sağlar:

1. **Çalışma adımları arasında bağlamı koruma** - İş akışınızın farklı aşamaları arasında bilgiyi sorunsuz bir şekilde iletin
2. **Karmaşık koşullu mantık oluşturma** - Birikmiş verilere göre karar alın
3. **Sürekli uygulamalar oluşturma** - İş akışı ilerlemesini kaydedin ve geri yükleyin
4. **Hataları zararsız bir şekilde ele alma** - Daha sağlam uygulamalar için kurtarma kalıplarını uygulayın
5. **Uygulamalarınızı ölçeklendirme** - Uygun veri organizasyonu ile karmaşık iş akışlarını destekleme
6. **Sohbet uygulamalarını etkinleştirme** - Bağlam duyarlı yapay zeka etkileşimleri için konuşma geçmişini depolayın ve erişin

Şimdi bu yetenekleri nasıl kullanacağımızı inceleyelim.

## Durum Yönetimi Temelleri

### Akış Durumu Yaşam Döngüsü

CrewAI Akışları'nda durum, öngörülebilir bir yaşam döngüsünü takip eder:

1. **Başlatma** - Bir akış oluşturulduğunda, durumu başlatılır (boş bir sözlük veya Pydantic model örneği olarak)
2. **Değiştirme** - Akış yöntemleri çalıştıkça durumu erişir ve değiştirir
3. **İletim** - Durum, otomatik olarak akış yöntemleri arasında iletilir
4. **Sürdürme** (isteğe bağlı) - Durum depolamaya kaydedilebilir ve daha sonra geri alınabilir
5. **Tamamlama** - Son durum, yürütülmüş tüm yöntemlerden elde edilen toplam değişiklikleri yansıtır

Bu yaşam döngüsünü anlamak, etkili akışlar tasarlamak için çok önemlidir.

### İki Yaklaşım Durum Yönetimi

CrewAI, akışlarınızda durumu yönetmek için iki yol sunar:

1. **Yapısız Durum** - Esneklik için sözlük benzeri nesneler kullanma
2. **Yapılandırılmış Durum** - Tip güvenliği ve doğrulama için Pydantic modelleri kullanma

Her iki yaklaşımı da ayrıntılı olarak inceleyelim.

## Yapısız Durum Yönetimi

Yapısız durum, basit uygulamalar için esneklik ve basitlik sunan bir sözlük yaklaşımı kullanır.

### Nasıl Çalışır

Yapısız durum ile:
- `self.state` aracılığıyla duruma erişirsiniz, bu bir sözlük gibi davranır
- Herhangi bir zamanda serbestçe anahtarlar ekleyebilir, değiştirebilir veya kaldırabilirsiniz
- Tüm durum, otomatik olarak tüm akış yöntemlerine erişilebilir

### Temel Örnek

Yapısız durum yönetiminin basit bir örneği:

```python
from crewai.flow.flow import Flow, listen, start

class UnstructuredStateFlow(Flow):
    @start()
    def initialize_data(self):
        print("Akış verilerini başlatıyor")
        # Durumdaki anahtar-değer çiftlerini ekleyin
        self.state["user_name"] = "Alex"
        self.state["preferences"] = {
            "theme": "dark",
            "language": "English"
        }
        self.state["items"] = []

        # Akış durumu otomatik olarak benzersiz bir kimlik alır
        print(f"Akış Kimliği: {self.state['id']}")

        return "Başlatıldı"

    @listen(initialize_data)
    def process_data(self, previous_result):
        print(f"Önceki adım şunları döndürdü: {previous_result}")

        # Duruma erişin ve değiştirin
        user = self.state["user_name"]
        print(f"Veriyi {user} için işleme")

        # Durumdaki bir listeye öğeler ekleyin
        self.state["items"].append("item1")
        self.state["items"].append("item2")

        # Yeni bir anahtar-değer çifti ekleyin
        self.state["processed"] = True

        return "İşlendi"

    @listen(process_data)
    def generate_summary(self, previous_result):
        # Birden fazla durum değerine erişin
        user = self.state["user_name"]
        theme = self.state["preferences"]["theme"]
        items = self.state["items"]
        processed = self.state.get("processed", False)

        summary = f"Kullanıcı {user} {len(items)} öğe ile {theme} temasına sahip. "
        summary += "Veri işlendi." if processed else "Veri işlenmedi."

        return summary

# Akışı çalıştır
flow = UnstructuredStateFlow()
result = flow.kickoff()
print(f"Sonuç: {result}")
print(f"Son durum: {flow.state}")
```

### Yapısız Durum Kullanma Zamanı

Yapısız durum aşağıdaki durumlar için idealdir:
- Hızlı prototip oluşturma ve basit akışlar
- Dinamik olarak değişen durum ihtiyaçları
- Yapının önceden bilinmediği durumlar
- Basit durum gereksinimleri olan akışlar

Yapısız durum, tip denetimi ve şema doğrulamasının olmaması nedeniyle karmaşık uygulamalarda hatalara yol açabilecekken, esnekliktir.

## Yapılandırılmış Durum Yönetimi

Yapılandırılmış durum, akışınızın durumu için bir şema tanımlamak üzere Pydantic modellerini kullanarak, tip güvenliği, doğrulama ve daha iyi geliştirici deneyimi sağlamak için kullanılır.

### Nasıl Çalışır

Yapılandırılmış durum ile:
- Durum yapınızı temsil eden bir Pydantic modeli tanımlarsınız
- Bu model türünü, akış sınıfınızdaki bir tür parametresi olarak geçirirsiniz
- `self.state` aracılığıyla duruma erişirsiniz, bu bir Pydantic model örneği gibi davranır
- Tüm alanlar, tanımlanmış türlerine göre doğrulanır
- IDE tamamlama ve tür denetimi desteği alırsınız

### Temel Örnek

Yapılandırılmış durum yönetimini nasıl uygulayacağınıza dair bir örnek:

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# Durum modelinizi tanımlayın
class UserPreferences(BaseModel):
    theme: str = "light"
    language: str = "English"

class AppState(BaseModel):
    user_name: str = ""
    preferences: UserPreferences = UserPreferences()
    items: List[str] = []
    processed: bool = False
    completion_percentage: float = 0.0

# Tip durumuna sahip bir akış oluşturun
class StructuredStateFlow(Flow[AppState]):
    @start()
    def initialize_data(self):
        print("Akış verilerini başlatıyor")
        # Durum değerlerini ayarlayın (tür denetimli)
        self.state.user_name = "Taylor"
        self.state.preferences.theme = "dark"

        # Kimlik alanı otomatik olarak kullanılabilir
        print(f"Akış Kimliği: {self.state.id}")

        return "Başlatıldı"

    @listen(initialize_data)
    def process_data(self, previous_result):
        print(f"{self.state.user_name} için veriyi işleme")

        # Durumu değiştirin (tür denetimleriyle)
        self.state.items.append("item1")
        self.state.items.append("item2")
        self.state.processed = True
        self.state.completion_percentage = 50.0

        return "İşlendi"

    @listen(process_data)
    def generate_summary(self, previous_result):
        # Duruma erişin (otamamlama ile)
        summary = f"Kullanıcı {self.state.user_name} {len(self.state.items)} öğe "
        summary += f"ile {self.state.preferences.theme} temasına sahip. "
        summary += "Veri işlendi." if self.state.processed else "Veri işlenmedi."
        summary += f" Tamamlama: {self.state.completion_percentage}%"

        return summary

# Akışı çalıştır
flow = StructuredStateFlow()
result = flow.kickoff()
print(f"Sonuç: {result}")
print(f"Son durum: {flow.state}")
```

### Yapılandırılmış Durumun Faydaları

Yapılandırılmış durum kullanmanın birçok avantajı vardır:

1. **Tip Güvenliği** - Tür hatalarını geliştirme zamanında yakalayın
2. **Kendi Kendine Belgeleme** - Durum modeli, mevcut verilerin ne olduğunu açıkça belge eder
3. **Doğrulama** - Veri türlerinin ve kısıtlamalarının otomatik doğrulaması
4. **IDE Desteği** - Otamamlama ve satır içi belgelendirme alın
5. **Varsayılan Değerler** - Eksik veriler için geri dönüşleri kolayca tanımlayın

### Yapılandırılmış Durum Kullanma Zamanı

Yapılandırılmış durum aşağıdaki durumlar için önerilir:
- İyi tanımlanmış veri şemalarına sahip karmaşık akışlar
- Birden fazla geliştiricinin aynı kod üzerinde çalıştığı ekip projeleri
- Veri doğrulamasının önemli olduğu uygulamalar
- Belirli veri türlerini ve kısıtlamalarını uygulaması gereken akışlar

## Otomatik Durum Kimliği

Hem yapılandırılmamış hem de yapılandırılmış durumların otomatik olarak benzersiz bir tanımlayıcı (UUID) alması, durum örneklerini izlemeye ve yönetmeye yardımcı olur.

### Nasıl Çalışır

- Yapısız durum için, kimlik `self.state["id"]` olarak erişilebilir
- Yapılandırılmış durum için, kimlik `self.state.id` olarak erişilebilir
- Bu kimlik, akış oluşturulduğunda otomatik olarak oluşturulur
- Kimlik, akışın yaşam döngüsü boyunca aynı kalır
- Kimlik, izleme, günlüğe kaydetme ve kalıcı durumları alma için kullanılabilir

Bu UUID, özellikle kalıcılık uygulamak veya birden çok akış yürütmesini izlemek için özellikle değerlidir.

## Dinamik Durum Güncellemeleri

Yapılandırılmış veya yapılandırılmamış durumu kullanıp kullanmadığınıza bakılmaksızın, akışınızın yürütülmesi boyunca durumu dinamik olarak güncelleyebilirsiniz.

### Adımlar Arası Veri Aktarımı

Akış yöntemleri, dinleme yöntemlerine argüman olarak geçirilecek değerleri döndürebilir:

```python
from crewai.flow.flow import Flow, listen, start

class DataPassingFlow(Flow):
    @start()
    def generate_data(self):
        # Bu döndürülen değer, dinleme yöntemlerine geçirilecektir
        return "Oluşturulan veri"

    @listen(generate_data)
    def process_data(self, data_from_previous_step):
        print(f"Alındı: {data_from_previous_step}")
        # Veriyi değiştirebilir ve iletebilirsiniz
        processed_data = f"{data_from_previous_step} - işlendi"
        # Ayrıca durumu güncelleyin
        self.state["last_processed"] = processed_data
        return processed_data

    @listen(process_data)
    def finalize_data(self, processed_data):
        print(f"İşlenmiş veri alındı: {processed_data}")
        # Hem geçirilen hem de durum verilerine erişin
        last_processed = self.state.get("last_processed", "")
        return f"Son: {processed_data} (durumdan: {last_processed})"
```

Bu kalıp, veri geçişini durum güncellemeleriyle birleştirerek maksimum esneklik sağlar.

## Akış Durumunu Sürdürme

CrewAI'nin en güçlü özelliklerinden biri, akış durumunu yürütmeler arasında sürdürebilmektir. Bu, duraklatılabilen, devam ettirilebilen ve hatta hatalardan sonra kurtarılabilen iş akışlarını etkinleştirir.

### @sürdür() Dekoratörü

@sürdür() dekoratörü, durum sürdürmeyi otomatikleştirerek akışınızın durumunu önemli noktada yürütme noktalarında kaydeder.

#### Sınıf Seviyesi Sürdürme

Sınıf seviyesinde uygulanan @sürdür(), her yöntem yürütülmesinden sonra durumu kaydeder:

```python
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist
from pydantic import BaseModel

class CounterState(BaseModel):
    value: int = 0

@persist()  # Tüm akış sınıfına uygulama
class PersistentCounterFlow(Flow[CounterState]):
    @start()
    def increment(self):
        self.state.value += 1
        print(f"Şuna artırıldı: {self.state.value}")
        return self.state.value

    @listen(increment)
    def double(self, value):
        self.state.value = value * 2
        print(f"İkiye katlandı: {self.state.value}")
        return self.state.value

# İlk çalıştırma
flow1 = PersistentCounterFlow()
result1 = flow1.kickoff()
print(f"İlk çalıştırma sonucu: {result1}")

# İkinci çalıştırma - durum otomatik olarak yüklenir
flow2 = PersistentCounterFlow()
result2 = flow2.kickoff()
print(f"İkinci çalıştırma sonucu: {result2}")  # Kalıcı durum nedeniyle daha yüksek olacaktır
```

#### Yöntem Seviyesi Sürdürme

Daha granüler kontrol için, @sürdür()'ü belirli yöntemlere uygulayabilirsiniz:

```python
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist

class SelectivePersistFlow(Flow):
    @start()
    def first_step(self):
        self.state["count"] = 1
        return "İlk adım"

    @persist()  # Yalnızca bu yöntemden sonra sürdürün
    @listen(first_step)
    def important_step(self, prev_result):
        self.state["count"] += 1
        self.state["important_data"] = "Bu sürdürülecek"
        return "Önemli adım tamamlandı"

    @listen(important_step)
    def final_step(self, prev_result):
        self.state["count"] += 1
        return f"Tamamlandı, sayım {self.state['count']} ile"
```

## Durum Yönetimi ile Kruvaziyer

CrewAI'daki en güçlü kalıplardan biri, akış durum yönetimi ile kruvaziyer yürütmesini birleştirmektir.

### Kruvaziyerlere Durum Geçirme

Akış durumunuzu kruvaziyerleri parametrelendirmek için kullanabilirsiniz:

```python
from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel

class ResearchState(BaseModel):
    topic: str = ""
    depth: str = "medium"
    results: str = ""

class ResearchFlow(Flow[ResearchState]):
    @start()
    def get_parameters(self):
        # Gerçek bir uygulamada bu kullanıcı girdisinden gelebilir
        self.state.topic = "Yapay Zeka Etiği"
        self.state.depth = "derin"
        return "Parametreler ayarlandı"

    @listen(get_parameters)
    def execute_research(self, _):
        # Aracılar oluşturun
        researcher = Agent(
            role="Araştırma Uzmanı",
            goal=f"{self.state.topic} hakkında {self.state.depth} ayrıntısıyla araştırma",
            backstory="Uzman bir araştırmacısınız ve doğru bilgi bulma konusunda yeteneklisiniz."
        )

        writer = Agent(
            role="İçerik Yazarı",
            goal="Araştırmayı açık ve ilgi çekici içeriklere dönüştürün",
            backstory="Karmaşık fikirleri açık ve öz bir şekilde iletmekte mükemmelsiniz."
        )

        # Görevleri oluşturun
        research_task = Task(
            description=f"{self.state.topic} hakkında {self.state.depth} analiz ile araştırma",
            expected_output="Markdown formatında kapsamlı araştırma notları",
            agent=researcher
        )

        writing_task = Task(
            description=f"{self.state.topic} hakkında araştırma sonuçlarına göre bir özet oluşturun",
            expected_output="Markdown formatında iyi yazılmış bir makale",
            agent=writer,
            context=[research_task]
        )

        # Kruvaziyer oluşturun ve çalıştırın
        research_crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process=Process.sequential,
            verbose=True
        )

        # Kruvaziyeri çalıştırın ve sonucu duruma kaydedin
        result = research_crew.kickoff()
        self.state.results = result.raw

        return "Araştırma tamamlandı"

    @listen(execute_research)
    def summarize_results(self, _):
        # Saklanan sonuçlara erişin
        result_length = len(self.state.results)
        return f"{self.state.topic} hakkında araştırma {result_length} karakter sonuçla tamamlandı."
```

### Durumdan Kruvaziyer Çıktılarını İşleme

Bir kruvaziyer tamamlandığında, çıktısını işleyebilir ve akış durumunuzda saklayabilirsiniz:

```python
@listen(execute_crew)
def process_crew_results(self, _):
    # Ham sonuçları ayrıştırın (JSON çıktısı varsayılarak)
    import json
    try:
        results_dict = json.loads(self.state.raw_results)
        self.state.processed_results = {
            "title": results_dict.get("title", ""),
            "main_points": results_dict.get("main_points", []),
            "conclusion": results_dict.get("conclusion", "")
        }
        return "Sonuçlar başarıyla işlendi"
    except json.JSONDecodeError:
        self.state.error = "Kruvaziyer sonuçlarını JSON olarak ayrıştırmada başarısız"
        return "Sonuçları işlerken hata oluştu"
```

## Durum Yönetimi İçin En İyi Uygulamalar

### 1. Durumu Odaklı Tutun

Durum tasarımınızda yalnızca gerekli olan şeyleri içirin:

```python
# Çok geniş
class BloatedState(BaseModel):
    user_data: Dict = {}
    system_settings: Dict = {}
    temporary_calculations: List = []
    debug_info: Dict = {}
    # ...daha fazla alan

# Daha iyi: Odaklı durum
class FocusedState(BaseModel):
    user_id: str
    preferences: Dict[str, str]
    completion_status: Dict[str, bool]
```

### 2. Karmaşık Akışlar İçin Yapılandırılmış Durum Kullanın

Akışlarınız karmaşıklaştıkça, yapılandırılmış durum giderek daha değerli hale gelir:

```python
# Basit akış yapılandırılmamış durumu kullanabilir
class SimpleGreetingFlow(Flow):
    @start()
    def greet(self):
        self.state["name"] = "World"
        return f"Merhaba, {self.state['name']}!"

# Karmaşık akış yapılandırılmış durumdan yararlanır
class UserRegistrationState(BaseModel):
    username: str
    email: str
    verification_status: bool = False
    registration_date: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

class RegistrationFlow(Flow[UserRegistrationState]):
    # Güçlü tipte durum erişimi olan yöntemler
```

### 3. Durum Geçişlerini Belgeleyin

Karmaşık akışlar için, durumun yürütme boyunca nasıl değiştiğini belgeleyin:

```python
@start()
def initialize_order(self):
    """
    Boş değerlerle sipariş durumunu başlatır.

    Durum öncesi: {}
    Durum sonrası: {order_id: str, items: [], status: 'new'}
    """
    self.state.order_id = str(uuid.uuid4())
    self.state.items = []
    self.state.status = "new"
    return "Sipariş başlatıldı"
```

### 4. Durum Hatalarını Zararsız Bir Şekilde İşleyin

Durum erişimi için hata işleme uygulayın:

```python
@listen(previous_step)
def process_data(self, _):
    try:
        # Mevcut olmayabilecek bir değere erişmeye çalışın
        user_preference = self.state.preferences.get("theme", "default")
    except (AttributeError, KeyError):
        # Hatayı zararsız bir şekilde işleyin
        self.state.errors = self.state.get("errors", [])
        self.state.errors.append("Tercihleri alma başarısız")
        user_preference = "default"

    return f"Tercih kullanıldı: {user_preference}"
```

### 5. İlerleme Takibi İçin Durumu Kullanın

Uzun süren akışlarda ilerlemeyi izlemek için durumu kullanın:

```python
class ProgressTrackingFlow(Flow):
    @start()
    def initialize(self):
        self.state["total_steps"] = 3
        self.state["current_step"] = 0
        self.state["progress"] = 0.0
        self.update_progress()
        return "Başlatıldı"

    def update_progress(self):
        """İlerlemeyi hesaplayıp güncelleyen yardımcı yöntem"""
        if self.state.get("total_steps", 0) > 0:
            self.state["progress"] = (self.state.get("current_step", 0) /
                                    self.state["total_steps"]) * 100
            print(f"İlerleme: {self.state['progress']:.1f}%")

    @listen(initialize)
    def step_one(self, _):
        # Çalışma yapın...
        self.state["current_step"] = 1
        self.update_progress()
        return "Adım 1 tamamlandı"

    # Ekstra adımlar...
```

### 6. Mümkün Olduğunda Değişmez İşlemler Kullanın

Özellikle yapılandırılmış durumla, açıklık için değiştirilmez işlemlere öncelik verin:

```python
# Yerinde liste değiştirmek yerine:
self.state.items.append(new_item)  # Değişken işlem

# Yeni bir durum oluşturmayı düşünün:
from pydantic import BaseModel
from typing import List

class ItemState(BaseModel):
    items: List[str] = []

class ImmutableFlow(Flow[ItemState]):
    @start()
    def add_item(self):
        # Eklenen öğem ile yeni bir liste oluşturun
        self.state.items = [*self.state.items, "yeni öğe"]
        return "Öğe eklendi"
```

## Akış Durumunu Hata Ayıklama

### Durum Değişikliklerini Günlüğe Kaydetme

Geliştirme yaparken, durum değişikliklerini izlemek için günlüğe kaydetmeyi ekleyin:

```python
import logging
logging.basicConfig(level=logging.INFO)

class LoggingFlow(Flow):
    def log_state(self, step_name):
        logging.info(f"Durum {step_name} sonrasında: {self.state}")

    @start()
    def initialize(self):
        self.state["counter"] = 0
        self.log_state("initialize")
        return "Başlatıldı"

    @listen(initialize)
    def increment(self, _):
        self.state["counter"] += 1
        self.log_state("increment")
        return f"Şuna artırıldı: {self.state['counter']}"
```

### Durum Görselleştirme

Hata ayıklama için durumunuzu görselleştirmek için bir yöntem ekleyebilirsiniz:

```python
def visualize_state(self):
    """Mevcut durumun basit bir görselleştirme oluşturun"""
    import json
    from rich.console import Console
    from rich.panel import Panel

    console = Console()

    if hasattr(self.state, "model_dump"):
        # Pydantic v2
        state_dict = self.state.model_dump()
    elif hasattr(self.state, "dict"):
        # Pydantic v1
        state_dict = self.state.dict()
    else:
        # Yapılandırılmamış durum
        state_dict = dict(self.state)

    # Temiz çıktı için kimliği kaldırın
    if "id" in state_dict:
        state_dict.pop("id")

    state_json = json.dumps(state_dict, indent=2, default=str)
    console.print(Panel(state_json, title="Mevcut Akış Durumu"))
```

## Sonuç

CrewAI Akışları'ndaki durum yönetimini ustalaşmak, sağlam yapay zeka uygulamaları oluşturmak için gereken güce sahip olmanızı sağlar, bağlamı korur, karmaşık kararlar alır ve tutarlı sonuçlar sağlar.

Hem yapılandırılmamış hem de yapılandırılmış durumu seçip, uygun durum yönetimi uygulamalarına uyarak hem güçlü hem de kolayca anlaşılabilir akışlar oluşturabilirsiniz.

## Sonraki Adımlar

- Akışlarınızda hem yapılandırılmış hem de yapılandırılmamış durumlarla deney yapın
- Uzun süren iş akışları için durum kalıcılığını uygulamayı deneyin
- [İlk kruvaziyerinizi oluşturma](/en/guides/crews/first-crew) bölümüne göz atarak kruvaziyerlerin ve akışların nasıl çalışabileceğini görün
- Daha gelişmiş özellikler için [Akış referans belgelerine](/en/concepts/flows) bakın