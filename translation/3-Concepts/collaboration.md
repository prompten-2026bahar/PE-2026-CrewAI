## İşbirliği

**Açıklama:** `CrewAI` ekiplerinde, acentelerin birbirleriyle görevleri devretmesi, etkili bir şekilde iletişim kurması ve birbirlerinin uzmanlığından yararlanması için nasıl birlikte çalışabileceklerini öğrenin. `allow_delegation=True` olduğunda, acenteler otomatik olarak güçlü işbirliği araçlarına erişim kazanır.

## Hızlı Başlangıç: İşbirliğini Etkinleştirme

```python
from crewai import Agent, Crew, Task

# Acenteler için işbirliğini etkinleştirin
researcher = Agent(
    role="Araştırma Uzmanı",
    goal="Herhangi bir konu hakkında kapsamlı araştırma yap",
    backstory="Çeşitli kaynaklara erişimi olan uzman araştırmacı",
    allow_delegation=True,  # 🔑 İşbirliği için temel ayar
    verbose=True
)

writer = Agent(
    role="İçerik Yazarı", 
    goal="Araştırmaya dayalı ilgi çekici içerik oluştur",
    backstory="Araştırmayı ilgi çekici içeriklere dönüştürme konusunda yetenekli yazar",
    allow_delegation=True,  # 🔑 İşbirliği için, diğer acentelere soru sormayı sağlar
    verbose=True
)

# Acenteler artık otomatik olarak işbirliği yapabilir
crew = Crew(
    agents=[researcher, writer],
    tasks=[...],
    verbose=True
)
```

## Acentelerin İşbirliği Nasıl Çalışır

`allow_delegation=True` olduğunda, `CrewAI` acentelere otomatik olarak iki güçlü araç sağlar:

### 1. **Görev Devretme Aracı**
Acentelerin, belirli bir uzmanlığa sahip takım arkadaşlarına görev atamasına olanak tanır.

```python
# Acente otomatik olarak bu araca sahip olur:
# Görevi iş arkadaşına devret(görev: str, bağlam: str, iş arkadaşı: str)
```

### 2. **Soru Sorma Aracı** 
Acentelerin, meslektaşlarından bilgi toplamak için belirli sorular sormasına olanak tanır.

```python
# Acente otomatik olarak bu araca sahip olur:
# Soru sorma iş arkadaşına(soru: str, bağlam: str, iş arkadaşı: str)
```

## İşbirliği Harekete Geçiyor

İçerik oluşturma görevinde işbirliği yapan acenteleri gösteren eksiksiz bir örnek:

```python
from crewai import Agent, Crew, Task, Process

# İşbirliği yapan acenteler oluşturun
researcher = Agent(
    role="Araştırma Uzmanı",
    goal="Herhangi bir konuda doğru ve güncel bilgi bulun",
    backstory="""Güvenilir kaynaklar bulma ve çeşitli alanlarda bilgileri doğrulama konusunda uzmanlığa sahip titiz bir araştırmacısınız.""",
    allow_delegation=True,
    verbose=True
)

writer = Agent(
    role="İçerik Yazarı",
    goal="İlgi çekici ve yapılandırılmış içerik oluştur",
    backstory=""""Araştırmayı farklı kitleler için ilgi çekici ve okunabilir içeriklere dönüştürmede mükemmel olan yetenekli bir içerik yazarıdırsınız.""",
    allow_delegation=True,
    verbose=True
)

editor = Agent(
    role="İçerik Editörü",
    goal="İçeriğin kalitesini ve tutarlılığını sağlamak",
    backstory=""""Detaylara dikkat eden ve içeriğin netlik ve doğruluk için yüksek standartları karşılamasını sağlayan deneyimli bir editörsünüz.""",
    allow_delegation=True,
    verbose=True
)

# İşbirliğini teşvik eden bir görev oluşturun
article_task = Task(
    description="""'Yapay Zekanın Sağlık Hizmetlerindeki Geleceği' hakkında kapsamlı 1000 kelimelik bir makale yazın.
    
    Makalede şunlar yer almalıdır:
    - Sağlık hizmetlerinde mevcut yapay zeka uygulamaları
    - Çıkan trendler ve teknolojiler  
    - Olası zorluklar ve etik hususlar
    - Önümüzdeki 5 yıl için uzman tahminleri
    
    Doğruluğu ve kaliteyi sağlamak için takım arkadaşlarınızla işbirliği yapın.""",
    expected_output="Yapılan araştırmayla ve uygun kaynaklarla desteklenen iyi yapılandırılmış ve ilgi çekici 1000 kelimelik bir makale",
    agent=writer  # Yazar liderlik eder, ancak araştırma görevini araştırmacıya devredebilir
)

# İşbirliği odaklı ekip oluşturun
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[article_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
```

## İşbirliği Modelleri

### Model 1: Araştırma → Yaz → Düzenle
```python
research_task = Task(
    description="Kuantum bilişimindeki en son gelişmeleri araştır",
    expected_output="Önemli bulguları ve kaynakları içeren kapsamlı araştırma özeti",
    agent=researcher
)

writing_task = Task(
    description="Araştırma bulgularına dayanarak bir makale yaz",
    expected_output="Kuantum bilişim hakkında ilgi çekici 800 kelimelik bir makale",
    agent=writer,
    context=[research_task]  # Araştırma çıktısını bağlam olarak alır
)

editing_task = Task(
    description="Makaleyi yayın için düzenleyin ve parlatın",
    expected_output="Yayın için hazır makale, geliştirilmiş netlik ve akışa sahip",
    agent=editor,
    context=[writing_task]  # Makale taslağını bağlam olarak alır
)
```

### Model 2: İşbirliği Odaklı Tek Görev
```python
collaborative_task = Task(
    description=""""Yeni bir yapay zeka ürünü için bir pazarlama stratejisi oluşturun.
    
    Yazar: Mesajlaşmaya ve içerik stratejisine odaklanın
    Araştırmacı: Pazar analizi ve rekabet istihbaratı sağlayın
    
    Kapsamlı bir strateji oluşturmak için birlikte çalışın.""",
    expected_output="Araştırmayla desteklenen tam bir pazarlama stratejisi",
    agent=writer  # Yönlendirici acente, ancak araştırmacıya devredebilir
)
```

## Hiyerarşik İşbirliği

Karmaşık projeler için, yönetici acente ile hiyerarşik bir süreç kullanın:

```python
from crewai import Agent, Crew, Task, Process

# Yönetici acente ekibi koordine eder
manager = Agent(
    role="Proje Yöneticisi",
    goal="Ekip çabalarını koordine edin ve proje başarısını sağlayın",
    backstory="Delege etme ve kalite kontrol konusunda yetenekli deneyimli proje yöneticisi",
    allow_delegation=True,
    verbose=True
)

# Uzman acenteler
researcher = Agent(
    role="Araştırmacı",
    goal="Doğru araştırma ve analiz sağlayın",
    backstory="Derin analitik becerilere sahip uzman araştırmacı",
    allow_delegation=False,  # Uzmanlar uzmanlıklarına odaklanır
    verbose=True
)

writer = Agent(
    role="Yazar", 
    goal="İlgi çekici içerik oluşturun",
    backstory="İlgi çekici içerik oluşturma konusunda yetenekli yazar",
    allow_delegation=False,
    verbose=True
)

# Yöneticinin yönettiği görev
project_task = Task(
    description="Önerilerle birlikte kapsamlı bir pazar analizi raporu oluşturun",
    expected_output="Yönetici özeti, ayrıntılı analiz ve stratejik öneriler",
    agent=manager  # Yönetici uzmanlara devredecek
)

# Hiyerarşik ekip
crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[project_task],
    process=Process.hierarchical,  # Yönetici her şeyi koordine eder
    manager_llm="gpt-4o",  # Yöneticisi için LLM'yi belirtin
    verbose=True
)
```

## İşbirliği İçin En İyi Uygulamalar

### 1. **Açık Rol Tanımı**
```python
# ✅ İyi: Belirli, tamamlayıcı roller
researcher = Agent(role="Pazar Araştırması Analisti", ...)
writer = Agent(role="Teknik İçerik Yazarı", ...)

# ❌ Kaçının: Üst üste binen veya belirsiz roller  
agent1 = Agent(role="Genel Yardımcı", ...)
agent2 = Agent(role="Yardımcı", ...)
```

### 2. **Stratejik Devretme Etkinleştirme**
```python
# ✅ Koordinatörler ve genelciler için devretmeyi etkinleştirin
lead_agent = Agent(
    role="İçerik Lideri",
    allow_delegation=True,  # Uzmanlara devredebilir
    ...
)

# ✅ Odaklanmış uzmanlar için devre dışı bırakın (isteğe bağlı)
specialist_agent = Agent(
    role="Veri Analisti", 
    allow_delegation=False,  # Temel uzmanlığına odaklanır
    ...
)
```

### 3. **Bağlam Paylaşımı**
```python
# ✅ Görev bağımlılıkları için bağlam parametresini kullanın
writing_task = Task(
    description="Araştırmaya dayalı bir makale yaz",
    agent=writer,
    context=[research_task],  # Araştırma sonuçlarını paylaşır
    ...
)
```

### 4. **Açık Görev Açıklamaları**
```python
# ✅ Belirli, eyleme geçirilebilir açıklamalar
Task(
    description=""""Yapay zeka sohbet robotu alanındaki rekabeti araştırın.
    Fiyatlandırma modelleri, temel özellikler, hedef pazarlar üzerine odaklanın.
    Verileri yapılandırılmış bir biçimde sağlayın.""",
    ...
)

# ❌ İşbirliği rehberlik etmeyen belirsiz açıklamalar
Task(description="Sohbet robotları hakkında biraz araştırma yapın", ...)
```

## İşbirliği Sorunlarını Giderme

### Sorun: Acenteler İşbirliği Yapmıyor
**Belirtiler:** Acenteler izole çalışıyor, devretme meydana gelmiyor
```python
# ✅ Çözüm: Devretmenin etkinleştirildiğinden emin olun
agent = Agent(
    role="...",
    allow_delegation=True,  # Bu gereklidir!
    ...
)
```

### Sorun: Çok Fazla Gidiş Dönüş
**Belirtiler:** Acenteler çok fazla soru soruyor, ilerleme yavaş
```python
# ✅ Çözüm: Daha iyi bağlam ve belirli roller sağlayın
Task(
    description="""Makine öğrenimi hakkında teknik bir blog yazısı yazın.
    
    Bağlam: Temel ML bilgisi olan yazılım geliştiricileri hedef kitle.
    Uzunluk: 1200 kelime
    Şunları içirin: kod örnekleri, pratik uygulamalar, en iyi uygulamalar
    
    Gerekli belirli teknik ayrıntılar için araştırmacıya devredin.""",
    ...
)
```

### Sorun: Devretme Döngüleri
**Belirtiler:** Acenteler sürekli olarak birbirlerine devretme
```python
# ✅ Çözüm: Açık hiyerarşi ve sorumluluklar
manager = Agent(role="Yönetici", allow_delegation=True)
specialist1 = Agent(role="Uzman A", allow_delegation=False)  # Tekrar devretme yok
specialist2 = Agent(role="Uzman B", allow_delegation=False)
```

## Gelişmiş İşbirliği Özellikleri

### Özel İşbirliği Kuralları
```python
# Acente geçmişini işbirliği yönergelerini belirleyin
agent = Agent(
    role="Kıdemli Geliştirici",
    backstory=""""Geliştirme projelerini koordine edin ve ekip üyeleriyle iletişim kurun.
    
    İşbirliği yönergeleri:
    - Araştırma görevlerini Araştırma Analisti'ne devredin
    - UI/UX rehberliği için Tasarımcı'ya danışın  
    - Test stratejileri için QA Mühendisi'ne danışın
    - Engelleme sorunlarını yalnızca Proje Yöneticisi'ne iletin""",
    allow_delegation=True
)
```

### İşbirliğini İzleme
```python
def track_collaboration(output):
    """İşbirliği kalıplarını izleyin"""
    if "Görevi iş arkadaşına devret" in output.raw:
        print("🤝 Devretme gerçekleşti")
    if "İş arkadaşına soru sor" in output.raw:
        print("❓ Soru soruldu")

crew = Crew(
    agents=[...],
    tasks=[...],
    step_callback=track_collaboration,  # İşbirliğini izleyin
    verbose=True
)
```

## Bellek ve Öğrenme

Acentelerin geçmiş işbirliklerini hatırlamasını sağlayın:

```python
agent = Agent(
    role="İçerik Lideri",
    memory=True,  # Geçmiş etkileşimleri hatırlayın
    allow_delegation=True,
    verbose=True
)
```

Bellek etkinleştirildiğinde, acenteler önceki işbirliklerinden öğrenir ve zamanla devretme kararlarını geliştirir.

## Sonraki Adımlar

- **Örnekleri deneyin**: Temel işbirliği örneği ile başlayın
- **Rolleri deneyin**: Farklı acente rolü kombinasyonlarını test edin
- **Etkileşimleri izleyin**: İşbirliği eylemde görmek için `verbose=True` kullanın
- **Görev açıklamalarını optimize edin**: Açık görevler daha iyi işbirliğine yol açar
- **Ölçeklendirin**: Karmaşık projeler için hiyerarşik süreçleri deneyin

İşbirliği, bireysel yapay zeka ajanlarını, karmaşık, çok yönlü zorlukları birlikte ele alabilen güçlü ekiplere dönüştürür.