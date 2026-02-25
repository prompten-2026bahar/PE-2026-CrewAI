# Koşullu Görevler

> crewAI başlatmasında koşullu görevlerin nasıl kullanılacağını öğrenin

## Giriş

crewAI'deki Koşullu Görevler, önceki görevlerin sonuçlarına göre dinamik iş akışı uyarlamasına imkân tanır.
Bu güçlü özellik, ekiplerin kararlar almasını ve görevleri seçici biçimde yürütmesini sağlayarak yapay zeka destekli süreçlerinizin esnekliğini ve verimliliğini artırır.

## Kullanım Örneği

```python
from typing import List
from pydantic import BaseModel
from crewai import Agent, Crew
from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput
from crewai.task import Task
from crewai_tools import SerperDevTool

# Koşullu görev için bir koşul fonksiyonu tanımlayın
# False döndürürse görev atlanır, True döndürürse görev yürütülür.
def is_data_missing(output: TaskOutput) -> bool:
    return len(output.pydantic.events) < 10  # bu görev atlanacak

# Ajanları tanımlayın
data_fetcher_agent = Agent(
    role="Data Fetcher",
    goal="Serper aracını kullanarak çevrimiçi veri çek",
    backstory="Backstory 1",
    verbose=True,
    tools=[SerperDevTool()]
)

data_processor_agent = Agent(
    role="Data Processor",
    goal="Çekilen veriyi işle",
    backstory="Backstory 2",
    verbose=True
)

summary_generator_agent = Agent(
    role="Summary Generator",
    goal="Çekilen veriden özet oluştur",
    backstory="Backstory 3",
    verbose=True
)

class EventOutput(BaseModel):
    events: List[str]

task1 = Task(
    description="Serper aracını kullanarak San Francisco'daki etkinlikler hakkında veri çek",
    expected_output="Bu hafta SF'de yapılacak 10 şeyin listesi",
    agent=data_fetcher_agent,
    output_pydantic=EventOutput,
)

conditional_task = ConditionalTask(
    description="""
        Verinin eksik olup olmadığını kontrol edin. 10'dan az etkinliğimiz varsa,
        bu hafta SF'de toplam 10 etkinliğimiz olacak şekilde
        Serper aracını kullanarak daha fazla etkinlik çekin.
        """,
    expected_output="Bu hafta SF'de yapılacak 10 şeyin listesi",
    condition=is_data_missing,
    agent=data_processor_agent,
)

task3 = Task(
    description="Çekilen veriden San Francisco'daki etkinliklerin özetini oluştur",
    expected_output="Müşteri ve onların müşterileri ile rakipleri hakkında demografik bilgiler, tercihler, pazar konumlandırması ve hedef kitle etkileşimi dahil eksiksiz bir rapor.",
    agent=summary_generator_agent,
)

# Görevlerle bir ekip oluşturun
crew = Crew(
    agents=[data_fetcher_agent, data_processor_agent, summary_generator_agent],
    tasks=[task1, conditional_task, task3],
    verbose=True,
    planning=True
)

# Ekibi çalıştırın
result = crew.kickoff()
print("sonuçlar", result)
```
