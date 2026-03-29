# Patronus AI Değerlendirmesi

## Genel Bakış

[Patronus AI](https://patronus.ai), CrewAI ajanları için kapsamlı değerlendirme ve izleme yetenekleri sağlar, model çıktılarını, ajan davranışlarını ve genel sistem performansını değerlendirmenize olanak tanır. Bu entegrasyon, üretim ortamlarında kalite ve güvenilirliği korumaya yardımcı olan sürekli değerlendirme iş akışlarını uygulamanıza olanak sağlar.

## Temel Özellikler

- **Otomatik Değerlendirme**: Ajan çıktıları ve davranışlarının gerçek zamanlı değerlendirmesi
- **Özel Kriterler**: Kullanım durumlarınıza göre özel değerlendirme kriterleri tanımlayın
- **Performans İzleme**: Ajan performans metriklerini zaman içinde takip edin
- **Kalite Güvencesi**: Farklı senaryolarda tutarlı çıktı kalitesini sağlayın
- **Güvenlik ve Uyumluluk**: Olası sorunları ve politika ihlallerini izleyin

## Değerlendirme Araçları

Patronus, farklı kullanım durumları için üç ana değerlendirme aracı sağlar:

1. **PatronusEvalTool**: Ajanların, değerlendirme görevinde en uygun değerlendiriciyi ve kriterleri seçmesini sağlar.
2. **PatronusPredefinedCriteriaEvalTool**: Kullanıcı tarafından belirtilen önceden tanımlanmış değerlendirici ve kriterleri kullanır.
3. **PatronusLocalEvaluatorTool**: Kullanıcı tarafından tanımlanan özel fonksiyon değerlendiricilerini kullanır.

## Kurulum

Bu araçları kullanmak için Patronus paketini kurmanız gerekir:

```shell
uv add patronus
```

Ayrıca Patronus API anahtarınızı bir ortam değişkeni olarak ayarlamanız gerekecektir:

```shell
export PATRONUS_API_KEY="your_patronus_api_key"
```

## Başlangıç Adımları

Patronus değerlendirme araçlarını etkili bir şekilde kullanmak için aşağıdaki adımları izleyin:

1. **Patronus'u Kurun**: Yukarıdaki komutu kullanarak Patronus paketini kurun.
2. **API Anahtarını Ayarlayın**: Patronus API anahtarınızı bir ortam değişkeni olarak ayarlayın.
3. **Doğru Aracı Seçin**: İhtiyaçlarınıza göre uygun Patronus değerlendirme aracını seçin.
4. **Aracı Yapılandırın**: Aracı gerekli parametrelerle yapılandırın.

## Örnekler

### PatronusEvalTool Kullanımı

Aşağıdaki örnek, ajanların en uygun değerlendiriciyi ve kriterleri seçmesini sağlayan `PatronusEvalTool`'u nasıl kullanacağınızı göstermektedir:

```python Code
from crewai import Agent, Task, Crew
from crewai_tools import PatronusEvalTool

# Aracı başlatın
patronus_eval_tool = PatronusEvalTool()

# Aracı kullanan bir ajan tanımlayın
coding_agent = Agent(
    role="Kodlama Ajanı",
    goal="Yüksek kaliteli kod üretin ve çıktının kod olduğunu doğrulayın",
    backstory="Deneyimli bir kodlayıcıdır ve yüksek kaliteli python kodu üretebilir.",
    tools=[patronus_eval_tool],
    verbose=True,
)

# Kodu üretip değerlendirmek için örnek bir görev
generate_code_task = Task(
    description="Fibonacci dizisinin ilk N sayısını üreten basit bir program oluşturun. Çıktınızı değerlendirmek için en uygun değerlendiriciyi ve kriterleri seçin.",
    expected_output="Fibonacci dizisinin ilk N sayısını üreten program.",
    agent=coding_agent,
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(agents=[coding_agent], tasks=[generate_code_task])
result = crew.kickoff()
```

### PatronusPredefinedCriteriaEvalTool Kullanımı

Aşağıdaki örnek, önceden tanımlanmış değerlendirici ve kriterleri kullanan `PatronusPredefinedCriteriaEvalTool`'u nasıl kullanacağınızı göstermektedir:

```python Code
from crewai import Agent, Task, Crew
from crewai_tools import PatronusPredefinedCriteriaEvalTool

# Önceden tanımlanmış kriterlerle aracı başlatın
patronus_eval_tool = PatronusPredefinedCriteriaEvalTool(
    evaluators=[{"evaluator": "judge", "criteria": "contains-code"}]
)

# Aracı kullanan bir ajan tanımlayın
coding_agent = Agent(
    role="Kodlama Ajanı",
    goal="Yüksek kaliteli kod üretin",
    backstory="Deneyimli bir kodlayıcıdır ve yüksek kaliteli python kodu üretebilir.",
    tools=[patronus_eval_tool],
    verbose=True,
)

# Kod üretmek için örnek bir görev
generate_code_task = Task(
    description="Fibonacci dizisinin ilk N sayısını üreten basit bir program oluşturun.",
    expected_output="Fibonacci dizisinin ilk N sayısını üreten program.",
    agent=coding_agent,
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(agents=[coding_agent], tasks=[generate_code_task])
result = crew.kickoff()
```

### PatronusLocalEvaluatorTool Kullanımı

Aşağıdaki örnek, özel fonksiyon değerlendiricilerini kullanan `PatronusLocalEvaluatorTool`'u nasıl kullanacağınızı göstermektedir:

```python Code
from crewai import Agent, Task, Crew
from crewai_tools import PatronusLocalEvaluatorTool
from patronus import Client, EvaluationResult
import random

# Patronus istemcisini başlatın
client = Client()

# Özel bir değerlendirici kaydetti
@client.register_local_evaluator("random_evaluator")
def random_evaluator(**kwargs):
    score = random.random()
    return EvaluationResult(
        score_raw=score,
        pass_=score >= 0.5,
        explanation="örnek açıklama",
    )

# Özel değerlendiriciyle aracı başlatın
patronus_eval_tool = PatronusLocalEvaluatorTool(
    patronus_client=client,
    evaluator="random_evaluator",
    evaluated_model_gold_answer="örnek etiket",
)

# Aracı kullanan bir ajan tanımlayın
coding_agent = Agent(
    role="Kodlama Ajanı",
    goal="Yüksek kaliteli kod üretin",
    backstory="Deneyimli bir kodlayıcıdır ve yüksek kaliteli python kodu üretebilir.",
    tools=[patronus_eval_tool],
    verbose=True,
)

# Kod üretmek için örnek bir görev
generate_code_task = Task(
    description="Fibonacci dizisinin ilk N sayısını üreten basit bir program oluşturun.",
    expected_output="Fibonacci dizisinin ilk N sayısını üreten program.",
    agent=coding_agent,
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(agents=[coding_agent], tasks=[generate_code_task])
result = crew.kickoff()
```

## Parametreler

### PatronusEvalTool

`PatronusEvalTool`, başlatma sırasında herhangi bir parametre gerektirmez. Patronus API'sinden mevcut değerlendiricileri ve kriterleri otomatik olarak çeker.

### PatronusPredefinedCriteriaEvalTool

`PatronusPredefinedCriteriaEvalTool`, başlatma sırasında aşağıdaki parametreleri kabul eder:

- **evaluators**: Gerekli. Kullanılacak değerlendirici ve kriterleri içeren bir liste. Örneğin: `[{"evaluator": "judge", "criteria": "contains-code"}]`.

### PatronusLocalEvaluatorTool

`PatronusLocalEvaluatorTool`, başlatma sırasında aşağıdaki parametreleri kabul eder:

- **patronus_client**: Gerekli. Patronus istemcisi örneği.
- **evaluator**: İsteğe bağlı. Kullanılacak kaydedilmiş yerel değerlendiricinin adı. Varsayılan olarak boş bir dizedir.
- **evaluated_model_gold_answer**: İsteğe bağlı. Değerlendirme için kullanılacak altın cevap. Varsayılan olarak boş bir dizedir.

## Kullanım

Patronus değerlendirme araçlarını kullanırken, model girdisini, çıktıyı ve bağlamı sağlarsınız ve araç, Patronus API'sinden değerlendirme sonuçlarını döndürür.

`PatronusEvalTool` ve `PatronusPredefinedCriteriaEvalTool` için, aracı çağırdığınızda aşağıdaki parametreler gereklidir:

- **evaluated_model_input**: Ajanın görevin basit metin açıklaması.
- **evaluated_model_output**: Ajanın görevin çıktısı.
- **evaluated_model_retrieved_context**: Ajanın bağlamı.

`PatronusLocalEvaluatorTool` için aynı parametreler gereklidir, ancak değerlendirici ve altın cevap başlatma sırasında belirtilir.

## Sonuç

Patronus değerlendirme araçları, Patronus AI platformunu kullanarak model girdilerini ve çıktılarını değerlendirmek ve puanlamak için güçlü bir yol sunar. Ajanların kendi çıktılarını veya diğer ajanların çıktılarını değerlendirmesini sağlayarak, bu araçlar CrewAI iş akışlarının kalitesini ve güvenilirliğini artırmaya yardımcı olabilir.