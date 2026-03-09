# CrewAI Otomasyon Çalıştırma Aracı (CrewAI Run Automation Tool)

> CrewAI ajanlarının CrewAI Platformu otomasyonlarını çağırmasına ve iş akışlarınızda harici ekip (crew) servislerinden yararlanmasına olanak tanır.

# `InvokeCrewAIAutomationTool`

`InvokeCrewAIAutomationTool`, harici ekip servisleriyle CrewAI Platformu API entegrasyonu sağlar. Bu araç, CrewAI ajanlarınızın içinden CrewAI Platformu otomasyonlarını çağırmanıza ve onlarla etkileşim kurmanıza olanak tanıyarak farklı ekip iş akışları arasında sorunsuz entegrasyon sağlar.

## Kurulum

```bash  theme={null}
uv pip install 'crewai[tools]'
```

## Gereksinimler

* CrewAI Platformu API erişimi
* Kimlik doğrulama için geçerli bir taşıyıcı belirteç (bearer token)
* CrewAI Platformu otomasyon uç noktalarına (endpoints) ağ erişimi

## Kullanım

Aracın bir CrewAI ajanıyla nasıl kullanılacağı aşağıda açıklanmıştır:

```python {2, 4-9} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import InvokeCrewAIAutomationTool

# Aracı başlatın
automation_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://data-analysis-crew-[...].crewai.com",
    crew_bearer_token="bearer_tokeninizi_buraya_yazin",
    crew_name="Veri Analiz Ekibi",
    crew_description="Verileri analiz eder ve içgörüler oluşturur"
)

# Aracı kullanan bir CrewAI ajanı oluşturun
automation_coordinator = Agent(
    role='Otomasyon Koordinatörü',
    goal='Otomatik ekip görevlerini koordine et ve yürüt',
    backstory='Karmaşık iş akışlarını yürütmek için otomasyon araçlarını kullanma konusunda uzmanım.',
    tools=[automation_tool],
    verbose=True
)

# Ajan için bir görev oluşturun
analysis_task = Task(
    description="Veri analizi otomasyonunu yürüt ve içgörüler sağla",
    agent=automation_coordinator,
    expected_output="Kapsamlı veri analizi raporu"
)

# Ajanla bir ekip oluşturun
crew = Crew(
    agents=[automation_coordinator],
    tasks=[analysis_task],
    verbose=2
)

# Ekibi çalıştırın
result = crew.kickoff()
print(result)
```

## Araç Argümanları

| Argüman                 | Tip    | Zorunlu | Varsayılan | Açıklama                                            |
| :---------------------- | :----- | :------ | :--------- | :-------------------------------------------------- |
| **crew\_api\_url**      | `str`  | Evet    | Yok        | CrewAI Platformu otomasyon API'sinin temel URL'si    |
| **crew\_bearer\_token** | `str`  | Evet    | Yok        | API kimlik doğrulaması için taşıyıcı belirteç       |
| **crew\_name**          | `str`  | Evet    | Yok        | Ekip otomasyonunun adı                              |
| **crew\_description**   | `str`  | Evet    | Yok        | Ekip otomasyonunun ne yaptığına dair açıklama       |
| **max\_polling\_time**  | `int`  | Hayır   | 600        | Görev tamamlanması için beklenecek saniye cinsinden süre |
| **crew\_inputs**        | `dict` | Hayır   | Yok        | Özel giriş şeması alanlarını tanımlayan sözlük      |

## Ortam Değişkenleri

```bash  theme={null}
CREWAI_API_URL=https://ekip-otomasyonunuz.crewai.com  # crew_api_url geçirmeye alternatif
CREWAI_BEARER_TOKEN=bearer_tokeninizi_buraya_yazin   # crew_bearer_token geçirmeye alternatif
```

## Gelişmiş Kullanım

### Dinamik Parametrelerle Özel Giriş Şeması

```python {2, 4-15} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import InvokeCrewAIAutomationTool
from pydantic import Field

# Özel giriş şemasını tanımlayın
custom_inputs = {
    "year": Field(..., description="Raporun isteneceği yıl (tam sayı)"),
    "region": Field(default="global", description="Analiz için coğrafi bölge"),
    "format": Field(default="summary", description="Rapor formatı (summary, detailed, raw)")
}

# Özel girişlerle aracı oluşturun
market_research_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://state-of-ai-report-crew-[...].crewai.com",
    crew_bearer_token="bearer_tokeninizi_buraya_yazin",
    crew_name="Yapay Zekanın Durumu Raporu",
    crew_description="Belirli bir yıl ve bölge için yapay zekanın durumuna dair kapsamlı bir rapor getirir",
    crew_inputs=custom_inputs,
    max_polling_time=15 * 60  # 15 dakika zaman aşımı
)

# Aracı kullanan bir ajan oluşturun
research_agent = Agent(
    role="Araştırma Koordinatörü",
    goal="Pazar araştırması görevlerini koordine et ve yürüt",
    backstory="Araştırma görevlerini koordine etme ve otomasyon araçlarını kullanma konusunda uzmansınız.",
    tools=[market_research_tool],
    verbose=True
)

# Özel parametrelerle bir görev oluşturun ve yürütün
research_task = Task(
    description="Kuzey Amerika'da 2024 yılı için Yapay Zeka Araçları pazarında detaylı formatta pazar araştırması yap",
    agent=research_agent,
    expected_output="Kapsamlı pazar araştırması raporu"
)

crew = Crew(
    agents=[research_agent],
    tasks=[research_task]
)

result = crew.kickoff()
```

### Çok Aşamalı Otomasyon İş Akışı

```python {2, 4-35} theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import InvokeCrewAIAutomationTool

# Farklı otomasyon araçlarını başlatın
data_collection_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://data-collection-crew-[...].crewai.com",
    crew_bearer_token="bearer_tokeninizi_buraya_yazin",
    crew_name="Veri Toplama Otomasyonu",
    crew_description="Ham verileri toplar ve ön işlemeden geçirir"
)

analysis_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://analysis-crew-[...].crewai.com",
    crew_bearer_token="bearer_tokeninizi_buraya_yazin",
    crew_name="Analiz Otomasyonu",
    crew_description="Gelişmiş veri analizi ve modelleme yapar"
)

reporting_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://reporting-crew-[...].crewai.com",
    crew_bearer_token="bearer_tokeninizi_buraya_yazin",
    crew_name="Raporlama Otomasyonu",
    crew_description="Kapsamlı raporlar ve görselleştirmeler oluşturur"
)

# Uzman ajanlar oluşturun
data_collector = Agent(
    role='Veri Toplama Uzmanı',
    goal='Çeşitli kaynaklardan veri topla ve ön işlemeden geçir',
    backstory='Çoklu kaynaklardan veri toplama ve temizleme konusunda uzmanım.',
    tools=[data_collection_tool]
)

data_analyst = Agent(
    role='Veri Analizi Uzmanı',
    goal='Toplanan veriler üzerinde gelişmiş analiz yap',
    backstory='İstatistiksel analiz ve makine öğrenimi konularında uzmanım.',
    tools=[analysis_tool]
)

report_generator = Agent(
    role='Rapor Oluşturma Uzmanı',
    goal='Kapsamlı raporlar ve görselleştirmeler oluştur',
    backstory='Karmaşık verilerden net, eyleme dönüştürülebilir raporlar oluşturma konusunda başarılıyım.',
    tools=[reporting_tool]
)

# Ardışık görevler oluşturun
collection_task = Task(
    description="2024 4. çeyrek analizi için pazar verilerini topla",
    agent=data_collector
)

analysis_task = Task(
    description="Trendleri ve kalıpları belirlemek için toplanan verileri analiz et",
    agent=data_analyst
)

reporting_task = Task(
    description="Temel içgörüler ve öneriler içeren yönetici özeti raporu oluştur",
    agent=report_generator
)

# Ardışık işlemeli bir ekip oluşturun
crew = Crew(
    agents=[data_collector, data_analyst, report_generator],
    tasks=[collection_task, analysis_task, reporting_task],
    process=Process.sequential,
    verbose=2
)

result = crew.kickoff()
```

## Kullanım Durumları

### Dağıtılmış Ekip Orkestrasyonu

* Karmaşık, çok aşamalı iş akışlarını yönetmek için birden fazla uzman ekip otomasyonunu koordine edin.
* Kapsamlı görev yürütme için farklı otomasyon servisleri arasında sorunsuz devirler sağlayın.
* İş yüklerini birden fazla CrewAI Platformu otomasyonuna dağıtarak işlemeyi ölçeklendirin.

### Platformlar Arası Entegrasyon

* Hibrit yerel-bulut iş akışları için CrewAI ajanları ile CrewAI Platformu otomasyonları arasında köprü kurun.
* Yerel kontrolü ve orkestrasyonu korurken uzmanlaşmış otomasyonlardan yararlanın.
* Yerel ajanlar ile bulut tabanlı otomasyon servisleri arasında güvenli işbirliği sağlayın.

### Kurumsal Otomasyon Hatları

* Yerel zekayı bulutun işlem gücüyle birleştiren kurumsal düzeyde otomasyon hatları oluşturun.
* Birden fazla otomasyon servisini kapsayan karmaşık iş akışlarını uygulayın.
* Veri analizi, raporlama ve karar verme için ölçeklenebilir, tekrarlanabilir süreçler oluşturun.

### Dinamik İş Akışı Bileşimi

* Görev gereksinimlerine göre farklı otomasyon servislerini zincirleyerek iş akışlarını dinamik olarak oluşturun.
* Otomasyon seçiminin veri özelliklerine veya iş kurallarına bağlı olduğu uyarlanabilir işlemeyi etkinleştirin.
* Çeşitli şekillerde birleştirilebilen esnek, yeniden kullanılabilir otomasyon bileşenleri oluşturun.

### Uzmanlaşmış Alan İşlemesi

* Genel amaçlı ajanlardan alana özgü otomasyonlara (finansal analiz, hukuk araştırması, teknik dokümantasyon) erişin.
* Karmaşık alan mantığını yeniden oluşturmadan önceden oluşturulmuş, uzmanlaşmış ekip otomasyonlarından yararlanın.
* Ajanların hedeflenmiş otomasyon servisleri aracılığıyla uzman düzeyindeki yeteneklere erişmesini sağlayın.

## Özel Giriş Şeması

`crew_inputs` tanımı yaparken, giriş parametrelerini belirtmek için Pydantic Field nesnelerini kullanın:

```python  theme={null}
from pydantic import Field

crew_inputs = {
    "zorunlu_parametre": Field(..., description="Bu parametre zorunludur"),
    "opsiyonel_parametre": Field(default="varsayilan_deger", description="Bu parametre opsiyoneldir"),
    "tipli_parametre": Field(..., description="Tam sayı parametresi", ge=1, le=100)  # Doğrulama ile birlikte
}
```

## Hata Yönetimi

Araç, yaygın senaryolar için kapsamlı hata yönetimi sağlar:

* **API Bağlantı Hataları**: CrewAI Platformu ile ağ bağlantı sorunları.
* **Kimlik Doğrulama Hataları**: Geçersiz veya süresi dolmuş taşıyıcı belirteçler.
* **Zaman Aşımı Hataları**: Maksimum yoklama (polling) süresini aşan görevler.
* **Görev Hataları**: Yürütme sırasında başarısız olan ekip otomasyonları.
* **Giriş Doğrulama Hataları**: Otomasyon uç noktalarına iletilen geçersiz parametreler.

## API Uç Noktaları

Araç, iki ana API uç noktasıyla etkileşim kurar:

* `POST {crew_api_url}/kickoff`: Yeni bir ekip otomasyon görevi başlatır.
* `GET {crew_api_url}/status/{crew_id}`: Çalışan bir görevin durumunu kontrol eder.

## Notlar

* Araç, tamamlanana veya zaman aşımına uğrayana kadar her saniye durum uç noktasını otomatik olarak denetler.
* Başarılı görevler sonucu doğrudan döndürürken, başarısız görevler hata bilgisini döndürür.
* Taşıyıcı belirteçler (bearer tokens) güvenli tutulmalı ve üretim ortamlarında kodun içine doğrudan yazılmamalıdır.
* Taşıyıcı belirteçler gibi hassas yapılandırmalar için ortam değişkenlerini kullanmayı düşünün.
* Özel giriş şemaları, hedef ekip otomasyonunun beklediği parametrelerle uyumlu olmalıdır.
