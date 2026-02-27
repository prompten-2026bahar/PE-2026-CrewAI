# Her Öğe İçin Ekibi Başlat

> Listedeki Her Öğe İçin Ekibi Başlatın

## Giriş

CrewAI, bir listedeki her öğe için ekibi başlatma yeteneği sunarak ekibin listedeki her öğe için yürütülmesine imkân tanır. Bu özellik, birden fazla öğe için aynı görev kümesini gerçekleştirmeniz gerektiğinde özellikle kullanışlıdır.

## Her Öğe İçin Ekibi Başlatma

Bir listedeki her öğe için ekibi başlatmak amacıyla `kickoff_for_each()` yöntemini kullanın. Bu yöntem, listedeki her öğe için ekibi yürüterek birden fazla öğeyi verimli biçimde işlemenize olanak tanır.

Bir listedeki her öğe için ekibi nasıl başlatacağınıza dair bir örnek:

```python
from crewai import Crew, Agent, Task

# Kod çalıştırma etkinleştirilmiş bir ajan oluşturun
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Python kullanarak veri analizi yap ve içgörüler sun",
    backstory="Güçlü Python becerilerine sahip deneyimli bir veri analistisiniz.",
    allow_code_execution=True
)

# Kod çalıştırma gerektiren bir görev oluşturun
data_analysis_task = Task(
    description="Verilen veri kümesini analiz edin ve katılımcıların ortalama yaşını hesaplayın. Yaşlar: {ages}",
    agent=coding_agent,
    expected_output="Veri kümesinden hesaplanan ortalama yaş"
)

# Bir ekip oluşturun ve görevi ekleyin
analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task],
    verbose=True,
    memory=False
)

datasets = [
  { "ages": [25, 30, 35, 40, 45] },
  { "ages": [20, 25, 30, 35, 40] },
  { "ages": [30, 35, 40, 45, 50] }
]

# Ekibi çalıştırın
result = analysis_crew.kickoff_for_each(inputs=datasets)
```
