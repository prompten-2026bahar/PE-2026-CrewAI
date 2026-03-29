# CrewAI ile Langfuse Entegrasyonu

Bu not defteri, OpenTelemetry aracılığıyla **OpenLit** SDK'sı kullanarak **CrewAI** ile **Langfuse** entegrasyonunu göstermektedir. Bu not defterinin sonunda, geliştirilmiş gözlemlenebilirlik ve hata ayıklama için CrewAI uygulamalarınızı Langfuse ile izleyebileceksiniz.

> **Langfuse Nedir?** [Langfuse](https://langfuse.com), açık kaynaklı bir LLM mühendisliği platformudur. Geliştiricilerin AI sistemlerini hata ayıklamasına, analiz etmesine ve optimize etmesine yardımcı olarak LLM uygulamaları için izleme ve izleme yetenekleri sağlar. Langfuse, yerel entegrasyonlar, OpenTelemetry ve API'ler/SDK'lar aracılığıyla çeşitli araçlar ve çerçevelerle entegre olur.

[![Langfuse Genel Bakış Videosu](https://github.com/user-attachments/assets/3926b288-ff61-4b95-8aa1-45d041c70866)](https://langfuse.com/watch-demo)

## Başlangıç

CrewAI'yi kullanarak basit bir örneği inceleyeceğiz ve OpenTelemetry aracılığıyla OpenLit ile entegre edeceğiz.

### 1. Adım: Bağımlılıkları Yükleyin

```python
%pip install langfuse openlit crewai crewai_tools
```

### 2. Adım: Ortam Değişkenlerini Ayarlayın

Langfuse API anahtarlarınızı ayarlayın ve izleri Langfuse'a göndermek için OpenTelemetry dışa aktarma ayarlarını yapılandırın. Langfuse OpenTelemetry uç noktası `/api/public/otel` ve kimlik doğrulama hakkında daha fazla bilgi için [Langfuse OpenTelemetry Belgeleri](https://langfuse.com/docs/opentelemetry/get-started) adresine bakın.

```python
 
# Proje ayarları sayfasından proje anahtarlarınızı alın: https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..." 
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com" # 🇪🇺 AB bölgesi
# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 ABD bölgesi
 
 
# OpenAI anahtarınız
os.environ["OPENAI_API_KEY"] = "sk-proj-..."
```
Ortam değişkenlerini ayarladıktan sonra, Langfuse istemcisini başlatabiliriz. `get_client()` fonksiyonu, ortam değişkenlerinde sağlanan kimlik bilgilerini kullanarak Langfuse istemcisini başlatır.

```python
from langfuse import get_client
 
langfuse = get_client()
 
# Bağlantıyı doğrulayın
if langfuse.auth_check():
    print("Langfuse istemcisi kimliği doğrulanmış ve kullanıma hazır!")
else:
    print("Kimlik doğrulama başarısız oldu. Lütfen kimlik bilgilerinizi ve ana makinenizi kontrol edin.")
```

### 3. Adım: OpenLit'i Başlatın

OpenTelemetry izlerini yakalamaya başlamak için OpenLit OpenTelemetry ölçüm SDK'sını başlatın.

```python

openlit.init()
```

### 4. Adım: Basit Bir CrewAI Uygulaması Oluşturun

Çoklu ajanların bir kullanıcının sorusunu yanıtlamak için işbirliği yaptığı basit bir CrewAI uygulaması oluşturacağız.

```python
from crewai import Agent, Task, Crew

from crewai_tools import (
    WebsiteSearchTool
)

web_rag_tool = WebsiteSearchTool()

writer = Agent(
        role="Yazar",
        goal="Matematik eğitimini genç çocuklar için şiir yoluyla ilgi çekici ve anlaşılır kılarsınız",
        backstory="Haiku yazma konusunda uzmansınız ancak matematikle hiçbir şey bilmezsiniz.",
        tools=[web_rag_tool],  
    )

task = Task(description=("Çarpma nedir?"),
            expected_output=("Cevabı içeren bir haiku bestele."),
            agent=writer)

crew = Crew(
  agents=[writer],
  tasks=[task],
  share_crew=False
)
```

### 5. Adım: Langfuse'ta İzlemeyi Görüntüleyin

Ajanı çalıştırdıktan sonra, CrewAI uygulamanız tarafından oluşturulan izlemeleri [Langfuse](https://cloud.langfuse.com) adresinde görüntüleyebilirsiniz. LLM etkileşimlerinin ayrıntılı adımlarını göreceksiniz ki bu, AI ajanınızı hata ayıklamanıza ve optimize etmenize yardımcı olabilir.

![Langfuse'taki CrewAI örnek izi](https://langfuse.com/images/cookbook/integration_crewai/crewai-example-trace.png)

_[Langfuse'taki genel örnek izi](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/e2cf380ffc8d47d28da98f136140642b?timestamp=2025-02-05T15%3A12%3A02.717Z&observation=3b32338ee6a5d9af)_

## Referanslar

- [Langfuse OpenTelemetry Belgeleri](https://langfuse.com/docs/opentelemetry/get-started)