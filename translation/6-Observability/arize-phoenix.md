# Arize Phoenix Entegrasyonu

Bu kılavuz, **CrewAI**'ı OpenTelemetry aracılığıyla [OpenInference](https://github.com/openinference/openinference) SDK'sı ile **Arize Phoenix** ile nasıl entegre edeceğinizi göstermektedir. Bu kılavuzun sonunda, CrewAI ajanlarınızı izleyebilecek ve kolayca hata ayıklayabileceksiniz.

> **Arize Phoenix Nedir?** [Arize Phoenix](https://phoenix.arize.com), AI uygulamaları için izleme ve değerlendirme sağlayan bir LLM gözlemlenebilirlik platformudur.

[![Entegrasyonumuzun Phoenix ile Video Demosunu İzleyin](https://storage.googleapis.com/arize-assets/fixtures/setup_crewai.png)](https://www.youtube.com/watch?v=Yc5q3l6F7Ww)

## Başlangıç

CrewAI'ı kullanarak ve OpenTelemetry aracılığıyla Arize Phoenix ile entegre etmenin basit bir örneğini inceleyeceğiz.

Bu kılavuz aynı zamanda [Google Colab](https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/tracing/crewai_tracing_tutorial.ipynb) adresinden de erişilebilir.

### 1. Adım: Bağımlılıkları Yükleyin

```bash
pip install openinference-instrumentation-crewai crewai crewai-tools arize-phoenix-otel
```

### 2. Adım: Ortam Değişkenlerini Ayarlayın

Phoenix Cloud API anahtarlarını alın ve OpenTelemetry'in izlemeleri Phoenix'e göndermesi için yapılandırın. Phoenix Cloud, Arize Phoenix'in barındırılan bir sürümüdür, ancak bu entegrasyonu kullanmak için gerekli değildir.

Ücretsiz Serper API anahtarınızı [buradan](https://serper.dev/) alabilirsiniz.

```python
from getpass import getpass

# Phoenix Cloud kimlik bilgilerinizi alın
PHOENIX_API_KEY = getpass("🔑 Phoenix Cloud API Anahtarınızı girin: ")

# API anahtarlarını alın servisler için
OPENAI_API_KEY = getpass("🔑 OpenAI API anahtarınızı girin: ")
SERPER_API_KEY = getpass("🔑 Serper API anahtarınızı girin: ")

# Ortam değişkenlerini ayarlayın
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com" # Phoenix Cloud, kendi uç noktanızı kullanıyorsanız bunu değiştirin
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY
```

### 3. Adım: Phoenix ile OpenTelemetry'i Başlatın

İzlemeleri yakalamaya başlamak ve bunları Phoenix'e göndermek için OpenInference OpenTelemetry SDK'sını başlatın.

```python
from phoenix.otel import register

tracer_provider = register(
    project_name="crewai-tracing-demo",
    auto_instrument=True,
)
```

### 4. Adım: Bir CrewAI Uygulaması Oluşturun

İki aracının işbirliği yaptığı ve bir blog yazısı araştırıp yazdığı bir CrewAI uygulaması oluşturacağız.

```python
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from openinference.instrumentation.crewai import CrewAIInstrumentor
from phoenix.otel import register

# crew'unuz için izleme ayarlayın
tracer_provider = register(
    endpoint="http://localhost:6006/v1/traces")
CrewAIInstrumentor().instrument(skip_dep_check=True, tracer_provider=tracer_provider)
search_tool = SerperDevTool()

# Ajanlarınızı roller ve hedeflerle tanımlayın
researcher = Agent(
    role="Kıdemli Araştırma Analisti"
    goal="AI ve veri bilimindeki en son gelişmeleri ortaya çıkarma",
    backstory="""Ön planlı bir teknoloji düşünce kuruluşunda çalışıyorsunuz.
    Uzmanlığınız, ortaya çıkan eğilimleri belirlemektir.
    Karmaşık verileri kesme ve eyleme geçirilebilir bilgiler sunma konusunda bir yeteneğiniz var.""",
    verbose=True,
    allow_delegation=False,
    # İsteğe bağlı olarak kullanmak istediğiniz modeli belirten bir llm özniteliği geçirebilirsiniz.
    # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7),
    tools=[search_tool],
)
writer = Agent(
    role="Tek İçerik Stratejisti",
    goal="Teknoloji gelişmelerine ilişkin ilgi çekici içerik oluşturma",
    backstory="""Tanınmış bir İçerik Stratejistisiniz, anlayışlı ve ilgi çekici makaleleriyle tanınırsınız.
    Karmaşık kavramları ilgi çekici anlatılara dönüştürüyorsunuz.""",
    verbose=True,
    allow_delegation=True,
)

# Ajanlarınız için görevler oluşturun
task1 = Task(
    description="""2024'teki yapay zeka gelişmelerinin kapsamlı bir analizini yapın.
    Kilit trendleri, çığır açan teknolojileri ve olası sektör etkilerini belirleyin.""",
    expected_output="Madde işaretli tam analiz raporu",
    agent=researcher,
)

task2 = Task(
    description="""Sağlanan bilgilerle, yapay zeka gelişmelerini vurgulayan ilgi çekici bir blog yazısı geliştirin.
    Yazınız bilgilendirici olmalı ancak teknik bilgisi olan bir kitleye hitap edecek şekilde erişilebilir olmalıdır.
    Havalı bir ses tonu kullanın, karmaşık kelimelerden kaçının, böylece yapay zeka gibi ses getirmez.""",
    expected_output="En az 4 paragraf içeren tam bir blog yazısı",
    agent=writer,
)

# Ajanlarınızı sıralı bir işlemle bir araya getirin
crew = Crew(
    agents=[researcher, writer], tasks=[task1, task2], verbose=1, process=Process.sequential
)

# Ekibinizi çalışmaya yönlendirin!
result = crew.kickoff()

print("######################")
print(result)
```

### 5. Adım: Phoenix'te İzlemeleri Görüntüleyin

Ajanı çalıştırdıktan sonra, CrewAI uygulamanız tarafından oluşturulan izlemeleri Phoenix'te görüntüleyebilirsiniz. Ajan etkileşimlerinin, araç kullanımlarının ve LLM çağrılarının ayrıntılı adımlarını görebilir ve bu da ajanlarınızı hata ayıklamanıza ve optimize etmenize yardımcı olabilir.

Phoenix Cloud hesabınıza giriş yapın ve `project_name` parametresinde belirttiğiniz projeye gidin. İzlemenin ajan etkileşimlerinin, araç kullanımlarının ve LLM çağrılarının tümünü gösteren bir zaman çizelgesi görünümünü göreceksiniz.

![Ajan etkileşimlerini gösteren Phoenix'teki örnek izleme](https://storage.googleapis.com/arize-assets/fixtures/crewai_traces.png)


### Uyumluluk Bilgileri
- Python 3.8+
- CrewAI >= 0.86.0
- Arize Phoenix >= 7.0.1
- OpenTelemetry SDK >= 1.31.0


### Referanslar
- [Phoenix Belgeleri](https://docs.arize.com/phoenix/) - Phoenix platformunun genel bakışı.
- [CrewAI Belgeleri](https://docs.crewai.com/) - CrewAI framework'ünün genel bakışı.
- [OpenTelemetry Belgeleri](https://opentelemetry.io/docs/) - OpenTelemetry rehberi
- [OpenInference GitHub](https://github.com/openinference/openinference) - OpenInference SDK kaynağı.