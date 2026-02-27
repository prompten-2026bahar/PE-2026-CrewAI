# Herhangi Bir LLM'e Bağlanma

> Desteklenen sağlayıcılar ve yapılandırma seçenekleri dahil olmak üzere LiteLLM kullanarak CrewAI'yi çeşitli Büyük Dil Modelleriyle (LLM) entegre etmeye yönelik kapsamlı kılavuz.

## CrewAI'yi LLM'lere Bağlama

CrewAI, geniş bir Dil Modelleri (LLM) yelpazesine bağlanmak için LiteLLM kullanır. Bu entegrasyon, basit ve birleşik bir arayüzle çok sayıda sağlayıcının modellerini kullanmanıza imkân tanıyarak kapsamlı bir esneklik sunar.

> **Not:** CrewAI varsayılan olarak `gpt-4o-mini` modelini kullanır. Bu, ayarlanmamışsa "gpt-4o-mini" değerini varsayılan olarak alan `OPENAI_MODEL_NAME` ortam değişkeni tarafından belirlenir. Bu kılavuzda açıklandığı şekilde ajanlarınızı farklı bir model veya sağlayıcı kullanacak şekilde kolayca yapılandırabilirsiniz.

## Desteklenen Sağlayıcılar

LiteLLM, aşağıdakiler dahil geniş bir sağlayıcı yelpazesini destekler:

- OpenAI
- Anthropic
- Google (Vertex AI, Gemini)
- Azure OpenAI
- AWS (Bedrock, SageMaker)
- Cohere
- VoyageAI
- Hugging Face
- Ollama
- Mistral AI
- Replicate
- Together AI
- AI21
- Cloudflare Workers AI
- DeepInfra
- Groq
- SambaNova
- Nebius AI Studio
- [NVIDIA NIMs](https://docs.api.nvidia.com/nim/reference/models-1)
- Ve çok daha fazlası!

Desteklenen sağlayıcıların güncel ve tam listesi için lütfen [LiteLLM Sağlayıcıları dokümantasyonuna](https://docs.litellm.ai/docs/providers) başvurun.

## LLM'i Değiştirme

CrewAI ajanlarınızla farklı bir LLM kullanmak için birkaç seçeneğiniz vardır:

### String Tanımlayıcı Kullanma

Ajanı başlatırken model adını string olarak iletin:

```python
from crewai import Agent

# OpenAI'nin GPT-4'ünü kullanma
openai_agent = Agent(
    role='OpenAI Expert',
    goal="GPT-4 kullanarak içgörüler sun",
    backstory="OpenAI'nin en güncel modeli tarafından desteklenen bir yapay zeka asistanı.",
    llm='gpt-4'
)

# Anthropic'in Claude'unu kullanma
claude_agent = Agent(
    role='Anthropic Expert',
    goal="Claude kullanarak veri analizi yap",
    backstory="Anthropic'in dil modelinden yararlanan bir yapay zeka asistanı.",
    llm='claude-2'
)
```

### LLM Sınıfını Kullanma

Daha ayrıntılı yapılandırma için LLM sınıfını kullanın:

```python
from crewai import Agent, LLM

llm = LLM(
    model="gpt-4",
    temperature=0.7,
    base_url="https://api.openai.com/v1",
    api_key="your-api-key-here"
)

agent = Agent(
    role='Customized LLM Expert',
    goal='Özelleştirilmiş yanıtlar sun',
    backstory="Özel LLM ayarlarına sahip bir yapay zeka asistanı.",
    llm=llm
)
```

## Yapılandırma Seçenekleri

Ajanınız için bir LLM yapılandırırken geniş bir parametre yelpazesine erişiminiz olur:

| Parametre | Tür | Açıklama |
| :--- | :---: | :--- |
| **model** | `str` | Kullanılacak modelin adı (ör. "gpt-4", "claude-2") |
| **temperature** | `float` | Çıktıdaki rastgeleliği kontrol eder (0.0 ile 1.0 arası) |
| **max\_tokens** | `int` | Üretilecek maksimum token sayısı |
| **top\_p** | `float` | Çıktının çeşitliliğini kontrol eder (0.0 ile 1.0 arası) |
| **frequency\_penalty** | `float` | Yeni tokenleri metinde şimdiye kadarki sıklıklarına göre cezalandırır |
| **presence\_penalty** | `float` | Yeni tokenleri metinde şimdiye kadarki varlıklarına göre cezalandırır |
| **stop** | `str`, `List[str]` | Üretimi durduracak dizi veya diziler |
| **base\_url** | `str` | API uç noktası için temel URL |
| **api\_key** | `str` | Kimlik doğrulama için API anahtarınız |

Parametrelerin ve açıklamalarının tam listesi için LLM sınıfı dokümantasyonuna başvurun.

## OpenAI Uyumlu LLM'lere Bağlanma

OpenAI uyumlu LLM'lere ortam değişkenleri kullanarak veya LLM sınıfında belirli nitelikler ayarlayarak bağlanabilirsiniz:

### Ortam Değişkenleri Kullanma

**Genel:**

```python
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["OPENAI_API_BASE"] = "https://api.your-provider.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "your-model-name"
```

**Google:**

```python
import os

# Gemini'nin OpenAI uyumlu API'sini kullanan örnek.
os.environ["OPENAI_API_KEY"] = "your-gemini-key"  # AIza... ile başlamalıdır
os.environ["OPENAI_API_BASE"] = "https://generativelanguage.googleapis.com/v1beta/openai/"
os.environ["OPENAI_MODEL_NAME"] = "openai/gemini-2.0-flash"  # Gemini modelinizi buraya, openai/ altına ekleyin
```

### LLM Sınıfı Nitelikleri Kullanma

**Genel:**

```python
llm = LLM(
    model="custom-model-name",
    api_key="your-api-key",
    base_url="https://api.your-provider.com/v1"
)
agent = Agent(llm=llm, ...)
```

**Google:**

```python
# Gemini'nin OpenAI uyumlu API'sini kullanan örnek
llm = LLM(
    model="openai/gemini-2.0-flash",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key="your-gemini-key",  # AIza... ile başlamalıdır
)
agent = Agent(llm=llm, ...)
```

## Ollama ile Yerel Modeller Kullanma

Ollama tarafından sağlananlar gibi yerel modeller için:

1. **Ollama'yı indirin ve yükleyin** — [İndirmek ve yüklemek için buraya tıklayın](https://ollama.com/download)

2. **İstediğiniz modeli çekin** — Örneğin modeli indirmek için `ollama pull llama3.2` komutunu çalıştırın.

3. **Ajanınızı yapılandırın:**

    ```python
    agent = Agent(
        role='Local AI Expert',
        goal='Yerel bir model kullanarak bilgi işle',
        backstory="Yerel donanım üzerinde çalışan bir yapay zeka asistanı.",
        llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
    )
    ```

## Temel API URL'sini Değiştirme

`base_url` parametresini ayarlayarak herhangi bir LLM sağlayıcısı için temel API URL'sini değiştirebilirsiniz:

```python
llm = LLM(
    model="custom-model-name",
    base_url="https://api.your-provider.com/v1",
    api_key="your-api-key"
)
agent = Agent(llm=llm, ...)
```

Bu özellik, OpenAI uyumlu API'lerle çalışırken veya seçtiğiniz sağlayıcı için farklı bir uç nokta belirtmeniz gerektiğinde özellikle kullanışlıdır.

## Sonuç

LiteLLM'den yararlanarak CrewAI, geniş bir LLM yelpazesiyle sorunsuz entegrasyon sunar. Bu esneklik, performansı, maliyet verimliliğini veya yerel dağıtımı öncelik olarak belirleyip belirlemediğinizden bağımsız olarak spesifik ihtiyaçlarınıza en uygun modeli seçmenize imkân tanır. Desteklenen modeller ve yapılandırma seçenekleri hakkında en güncel bilgi için [LiteLLM dokümantasyonuna](https://docs.litellm.ai/docs/) başvurmayı unutmayın.
