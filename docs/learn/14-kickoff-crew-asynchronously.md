> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Ekibi Asenkron Olarak Başlatma

> Bir Ekibi Asenkron Olarak Başlatın

## Giriş

CrewAI, bir ekibi asenkron olarak başlatma yeteneği sunarak ekip yürütmesini bloklamayan bir şekilde başlatmanıza imkân tanır. Bu özellik, birden fazla ekibi eş zamanlı olarak çalıştırmak istediğinizde veya ekip yürütülürken diğer görevleri gerçekleştirmeniz gerektiğinde özellikle kullanışlıdır.

CrewAI, asenkron yürütme için iki yaklaşım sunar:

| Yöntem | Tür | Açıklama |
| --- | --- | --- |
| `akickoff()` | Yerel asenkron | Tüm yürütme zinciri boyunca gerçek async/await |
| `kickoff_async()` | İş parçacığı tabanlı | Senkron yürütmeyi `asyncio.to_thread` içine sarar |

> **Not:** Yüksek eşzamanlılık iş yükleri için görev yürütme, bellek işlemleri ve bilgi alımı için yerel asenkron kullanan `akickoff()` önerilir.

## `akickoff()` ile Yerel Asenkron Yürütme

`akickoff()` yöntemi, görev yürütme, bellek işlemleri ve bilgi sorguları dahil olmak üzere tüm yürütme zinciri boyunca async/await kullanan gerçek yerel asenkron yürütme sağlar.

### Yöntem İmzası

```python
async def akickoff(self, inputs: dict) -> CrewOutput:
```

### Parametreler

- `inputs` (dict): Görevler için gereken girdi verilerini içeren sözlük.

### Döndürür

- `CrewOutput`: Ekip yürütmesinin sonucunu temsil eden nesne.

### Örnek: Yerel Asenkron Ekip Yürütmesi

```python
import asyncio
from crewai import Crew, Agent, Task

# Bir ajan oluşturun
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Python kullanarak veri analizi yap ve içgörüler sun",
    backstory="Güçlü Python becerilerine sahip deneyimli bir veri analistisiniz.",
    allow_code_execution=True
)

# Bir görev oluşturun
data_analysis_task = Task(
    description="Verilen veri kümesini analiz edin ve katılımcıların ortalama yaşını hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Katılımcıların ortalama yaşı."
)

# Bir ekip oluşturun
analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

# Yerel asenkron yürütme
async def main():
    result = await analysis_crew.akickoff(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Ekip Sonucu:", result)

asyncio.run(main())
```

### Örnek: Birden Fazla Yerel Asenkron Ekip

Yerel asenkron ile `asyncio.gather()` kullanarak birden fazla ekibi eş zamanlı olarak çalıştırın:

```python
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Python kullanarak veri analizi yap ve içgörüler sun",
    backstory="Güçlü Python becerilerine sahip deneyimli bir veri analistisiniz.",
    allow_code_execution=True
)

task_1 = Task(
    description="İlk veri kümesini analiz edin ve ortalama yaşı hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Katılımcıların ortalama yaşı."
)

task_2 = Task(
    description="İkinci veri kümesini analiz edin ve ortalama yaşı hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Katılımcıların ortalama yaşı."
)

crew_1 = Crew(agents=[coding_agent], tasks=[task_1])
crew_2 = Crew(agents=[coding_agent], tasks=[task_2])

async def main():
    results = await asyncio.gather(
        crew_1.akickoff(inputs={"ages": [25, 30, 35, 40, 45]}),
        crew_2.akickoff(inputs={"ages": [20, 22, 24, 28, 30]})
    )

    for i, result in enumerate(results, 1):
        print(f"Ekip {i} Sonucu:", result)

asyncio.run(main())
```

### Örnek: Birden Fazla Girdi İçin Yerel Asenkron

Yerel asenkron ile birden fazla girdi için ekibinizi eş zamanlı olarak çalıştırmak amacıyla `akickoff_for_each()` kullanın:

```python
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Python kullanarak veri analizi yap ve içgörüler sun",
    backstory="Güçlü Python becerilerine sahip deneyimli bir veri analistisiniz.",
    allow_code_execution=True
)

data_analysis_task = Task(
    description="Veri kümesini analiz edin ve ortalama yaşı hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Katılımcıların ortalama yaşı."
)

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

async def main():
    datasets = [
        {"ages": [25, 30, 35, 40, 45]},
        {"ages": [20, 22, 24, 28, 30]},
        {"ages": [30, 35, 40, 45, 50]}
    ]

    results = await analysis_crew.akickoff_for_each(datasets)

    for i, result in enumerate(results, 1):
        print(f"Veri Kümesi {i} Sonucu:", result)

asyncio.run(main())
```

## `kickoff_async()` ile İş Parçacığı Tabanlı Asenkron

`kickoff_async()` yöntemi, senkron `kickoff()`'u bir iş parçacığına sararak asenkron yürütme sağlar. Bu, daha basit asenkron entegrasyon veya geriye dönük uyumluluk için kullanışlıdır.

### Yöntem İmzası

```python
async def kickoff_async(self, inputs: dict) -> CrewOutput:
```

### Parametreler

- `inputs` (dict): Görevler için gereken girdi verilerini içeren sözlük.

### Döndürür

- `CrewOutput`: Ekip yürütmesinin sonucunu temsil eden nesne.

### Örnek: İş Parçacığı Tabanlı Asenkron Yürütme

```python
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Python kullanarak veri analizi yap ve içgörüler sun",
    backstory="Güçlü Python becerilerine sahip deneyimli bir veri analistisiniz.",
    allow_code_execution=True
)

data_analysis_task = Task(
    description="Verilen veri kümesini analiz edin ve katılımcıların ortalama yaşını hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Katılımcıların ortalama yaşı."
)

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

async def async_crew_execution():
    result = await analysis_crew.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Ekip Sonucu:", result)

asyncio.run(async_crew_execution())
```

### Örnek: Birden Fazla İş Parçacığı Tabanlı Asenkron Ekip

```python
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Python kullanarak veri analizi yap ve içgörüler sun",
    backstory="Güçlü Python becerilerine sahip deneyimli bir veri analistisiniz.",
    allow_code_execution=True
)

task_1 = Task(
    description="İlk veri kümesini analiz edin ve katılımcıların ortalama yaşını hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Katılımcıların ortalama yaşı."
)

task_2 = Task(
    description="İkinci veri kümesini analiz edin ve katılımcıların ortalama yaşını hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Katılımcıların ortalama yaşı."
)

crew_1 = Crew(agents=[coding_agent], tasks=[task_1])
crew_2 = Crew(agents=[coding_agent], tasks=[task_2])

async def async_multiple_crews():
    result_1 = crew_1.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    result_2 = crew_2.kickoff_async(inputs={"ages": [20, 22, 24, 28, 30]})

    results = await asyncio.gather(result_1, result_2)

    for i, result in enumerate(results, 1):
        print(f"Ekip {i} Sonucu:", result)

asyncio.run(async_multiple_crews())
```

## Asenkron Akış

Her iki asenkron yöntem de ekipte `stream=True` ayarlandığında akışı destekler:

```python
import asyncio
from crewai import Crew, Agent, Task

agent = Agent(
    role="Researcher",
    goal="Konuları araştır ve özetle",
    backstory="Uzman bir araştırmacısınız."
)

task = Task(
    description="Konuyu araştırın: {topic}",
    agent=agent,
    expected_output="Konunun kapsamlı bir özeti."
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    stream=True  # Akışı etkinleştir
)

async def main():
    streaming_output = await crew.akickoff(inputs={"topic": "2024'te yapay zeka trendleri"})

    # Akış parçaları üzerinde asenkron yineleme
    async for chunk in streaming_output:
        print(f"Parça: {chunk.content}")

    # Akış tamamlandıktan sonra nihai sonuca erişin
    result = streaming_output.result
    print(f"Nihai sonuç: {result.raw}")

asyncio.run(main())
```

## Potansiyel Kullanım Durumları

- **Paralel İçerik Üretimi**: Birden fazla bağımsız ekibi asenkron olarak başlatın; her biri farklı konularda içerik üretmekten sorumlu olsun. Örneğin, bir ekip yapay zeka trendleri üzerine makale araştırıp taslak hazırlarken, diğer ekip yeni bir ürün lansmanı hakkında sosyal medya gönderileri oluşturabilir.

- **Eş Zamanlı Pazar Araştırması Görevleri**: Paralel pazar araştırması yürütmek için birden fazla ekibi asenkron olarak başlatın. Bir ekip sektör trendlerini analiz ederken, diğeri rakip stratejilerini inceleyebilir ve bir diğeri tüketici duyarlılığını değerlendirebilir.

- **Bağımsız Seyahat Planlama Modülleri**: Bir seyahatin farklı yönlerini bağımsız olarak planlamak için ayrı ekipleri yürütün. Bir ekip uçuş seçeneklerini, diğeri konaklama seçeneklerini yönetirken üçüncüsü aktiviteleri planlayabilir.

## `akickoff()` ve `kickoff_async()` Arasında Seçim

| Özellik | `akickoff()` | `kickoff_async()` |
| --- | --- | --- |
| Yürütme modeli | Yerel async/await | İş parçacığı tabanlı sarmalayıcı |
| Görev yürütme | `aexecute_sync()` ile asenkron | İş parçacığı havuzunda senkron |
| Bellek işlemleri | Asenkron | İş parçacığı havuzunda senkron |
| Bilgi alımı | Asenkron | İş parçacığı havuzunda senkron |
| En iyi kullanım | Yüksek eşzamanlılık, G/Ç bağlı iş yükleri | Basit asenkron entegrasyon |
| Akış desteği | Evet | Evet |
