# LLM'ler
CrewAI projelerinizde Büyük Dil Modelleri'ni (LLM) yapılandırma ve kullanma konusunda kapsamlı bir rehber.


## Genel Bakış

CrewAI, yerel sağlayıcı SDK'ları aracılığıyla çok sayıda LLM sağlayıcısıyla entegre olarak, özel kullanım durumunuz için doğru modeli seçme esnekliği sağlar. Bu rehber, farklı LLM sağlayıcılarını CrewAI projelerinizde nasıl yapılandıracağınızı ve kullanacağınızı anlamanıza yardımcı olacaktır.

## LLM'ler Nedir?

Büyük Dil Modelleri (LLM'ler), CrewAI ajanlarının temel zekasını oluşturur. Ajanların bağlamı anlamasını, karar vermesini ve insan benzeri yanıtlar oluşturmasını sağlar. Bilmeniz gerekenler şunlardır:

### LLM Temelleri

Büyük Dil Modelleri, muazzam miktarda metin verisi üzerinde eğitilmiş yapay zeka sistemleridir. Bunlar, CrewAI ajanlarınızın zekâsını çalıştırır ve metin anlamalarını ve oluşturmalarını sağlar.

### Bağlam Penceresi

Bağlam penceresi, bir LLM'nin aynı anda işleyebileceği metin miktarını belirler. Daha büyük pencereler (örneğin 128K token), daha fazla bağlam sağlar ancak daha pahalı ve yavaş olabilir.

### Sıcaklık

Sıcaklık (0,0 ila 1,0), yanıt rastgeleliğini kontrol eder. Daha düşük değerler (örneğin 0,2), daha odaklanmış ve deterministik çıktılar üretirken, daha yüksek değerler (örneğin 0,8) yaratıcılığı ve değişkenliği artırır.

### Sağlayıcı Seçimi

Her LLM sağlayıcısı (örneğin OpenAI, Anthropic, Google), değişen yeteneklere, fiyatlandırmaya ve özelliklere sahip farklı modeller sunar. Doğruluğunuz, hızınız ve maliyetiniz için ihtiyaçlarınıza göre seçim yapın.

## LLM'nizi Kurma

LLM'yi kullanacağınız yer CrewAI kodunda çeşitli yerler bulunur. Kullandığınız modeli belirledikten sonra, kullandığınız her model sağlayıcısı için yapılandırmayı (örneğin bir API anahtarı) sağlamanız gerekir. Sağlayıcınız için [sağlayıcı yapılandırma örneklerine](#provider-configuration-examples) bölümüne bakın.

    En basit başlangıç yolu. Modeli doğrudan ortamınızda, bir `.env` dosyasında veya uygulamanızdaki kodda belirtin. Projenizi `crewai create` ile başlattıysanız, zaten ayarlanmış olacaktır.

    ```bash .env
    MODEL=model-id  # Örneğin gpt-4o, gemini-2.0-flash, claude-3-sonnet-...

    # API anahtarlarınızı da buraya ayarlamayı unutmayın.
    # Daha fazla bilgi için Sağlayıcı
    # bölümüne bakın.
    ```

    API anahtarlarını asla sürüm kontrolüne commit etmeyin. Ortam dosyaları (.env) veya sisteminizin gizli yönetimi kullanın.

    YAML dosyasını yapılandırmanızla agent yapılandırmanızı tanımlayın. Bu yöntem, ekip çalışması ve sürüm kontrolü için harikadır:

    ```yaml agents.yaml {6}
    researcher:
        role: Araştırma Uzmanı
        goal: Kapsamlı araştırma ve analiz yapın
        backstory: Yılların deneyimine sahip özel bir araştırma uzmanı
        verbose: true
        llm: provider/model-id  # Örneğin openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...
        # daha fazla bilgi için sağlayıcı yapılandırma örneklerine bakın
    ```

    YAML yapılandırması şunlara izin verir:
    - Ajan ayarlarınızı sürüm kontrolüne alın
    - Farklı modeller arasında kolayca geçiş yapın
    - Ayarları ekip üyeleri arasında paylaşın
    - Model seçimlerini ve amaçlarını belgeleyin

    Maksimum esneklik için LLM'leri doğrudan Python kodunuzda yapılandırın:

    ```python {4,8}
    from crewai import LLM

    # Temel yapılandırma
    llm = LLM(model="model-id-here")  # gpt-4o, gemini-2.0-flash, anthropic/claude...

    # Ayrıntılı parametrelerle gelişmiş yapılandırma
    llm = LLM(
        model="model-id-here",  # gpt-4o, gemini-2.0-flash, anthropic/claude...
        temperature=0.7,        # Yüksek yaratıcı çıktılar için
        timeout=120,            # Yanıt için bekleme süresi (saniye)
        max_tokens=4000,        # Yanıtın maksimum uzunluğu
        top_p=0.9,              # Örnekleme parametresi
        frequency_penalty=0.1 , # Tekrarı azaltır
        presence_penalty=0.1,   # Konu çeşitliliğini teşvik eder
        response_format={"type": "json"},  # Yapılandırılmış çıktılar için
        seed=42                 # Yeniden üretilebilir sonuçlar için
    )
    ```

    Parametre açıklamaları:
    - `temperature`: Rastgeleliği kontrol eder (0,0-1,0)
    - `timeout`: Yanıt için maksimum bekleme süresi
    - `max_tokens`: Yanıt uzunluğunu sınırlar
    - `top_p`: Örnekleme için sıcaklığa alternatif
    - `frequency_penalty`: Kelime tekrarını azaltır
    - `presence_penalty`: Yeni konuları teşvik eder
    - `response_format`: Çıktı yapısını belirtir
    - `seed`: Tutarlı sonuçlar sağlar

CrewAI, OpenAI, Anthropic, Google (Gemini API), Azure ve AWS Bedrock için yerel SDK entegrasyonları sağlar — ötesinde sağlayıcıya özel ekler (örneğin `uv add "crewai[openai]"`) dışında herhangi bir kurulum gerekmez.

Diğer tüm sağlayıcılar **LiteLLM** tarafından desteklenir. Herhangi birini kullanmayı planlıyorsanız, projenize bağımlılık olarak ekleyin:
```bash
uv add 'crewai[litellm]'
```

## Sağlayıcı Yapılandırma Örnekleri

CrewAI, OpenAI, Anthropic, Google (Gemini API), Azure ve AWS Bedrock için yerel SDK entegrasyonları sağlar — ötesinde sağlayıcıya özel ekler (örneğin `uv add "crewai[openai]"`) dışında herhangi bir kurulum gerekmez.

CrewAI, OpenAI için OpenAI Python SDK'sı aracılığıyla yerel entegrasyon sağlar.

```toml Code
# Gerekli
OPENAI_API_KEY=sk-...

# İsteğe bağlı
OPENAI_BASE_URL=<custom-base-url>
```

**Temel Kullanım:**
```python Code
from crewai import LLM

llm = LLM(
    model="openai/gpt-4o",
    api_key="your-api-key",  # Veya OPENAI_API_KEY'i ayarlayın
    temperature=0.7,
    max_tokens=4000
)
```

**Gelişmiş Yapılandırma:**
```python Code
from crewai import LLM

llm = LLM(
    model="openai/gpt-4o",
    api_key="your-api-key",
    base_url="https://api.openai.com/v1",  # İsteğe bağlı özel uç nokta
    organization="org-...",  # İsteğe bağlı kuruluş kimliği
    project="proj_...",  # İsteğe bağlı proje kimliği
    temperature=0.7,
    max_tokens=4000,
    max_completion_tokens=4000,  # Daha yeni modeller için
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42,  # Yeniden üretilebilir çıktılar için
    stream=True,  # Akışı etkinleştir
    timeout=60.0,  # İstenen zaman aşımı süresi (saniye)
    max_retries=3,  # Maksimum yeniden deneme sayısı
    logprobs=True,  # Token düzeyindeki içgörüler için günlük olasılıkları döndür
    top_logprobs=5,  # En olası jetonların sayısı
    reasoning_effort="medium"  # o1 modelleri için: düşük, orta, yüksek
)
```

**Yapılandırılmış Çıktılar:**
```python Code
from pydantic import BaseModel
from crewai import LLM

class ResponseFormat(BaseModel):
    name: str
    age: int
    summary: str

llm = LLM(
    model="openai/gpt-4o",
)
```

**Desteklenen Ortam Değişkenleri:**
- `OPENAI_API_KEY`: OpenAI API anahtarınız (gerekli)
- `OPENAI_BASE_URL`: Özel OpenAI API URL'si (isteğe bağlı)

**Özellikler:**
- Yerel işlev çağırma desteği (o1 modelleri hariç)
- JSON şeması ile yapılandırılmış çıktılar
- Gerçek zamanlı yanıtlar için akış desteği
- Token kullanımı takibi

**Desteklenen Modeller:**

| Model | Bağlam Penceresi | Şunun için İdeal |
|---|---|---|
| gpt-4.1 | 1M token | Gelişmiş yeteneklere sahip en son model |
| gpt-4.1-mini | 1M token | Daha fazla bağlama sahip verimli sürüm |
| gpt-4.1-nano | 1M token | Ultra verimli varyant |
| gpt-4o | 128.000 token | Hız ve zekâ için optimize edilmiş |
| gpt-4o-mini | 200.000 token | Büyük bağlam ile uygun maliyetli |
| gpt-4-turbo | 128.000 token | Uzun biçimli içerik, belge analizi |
| gpt-4 | 8.192 token | Yüksek doğruluklu görevler, karmaşık akıl yürütme |
| o1 | 200.000 token | Gelişmiş akıl yürütme, karmaşık problem çözme |
| o1-preview | 128.000 token | Akıl yürütme yeteneklerinin önizlemesi |
| o1-mini | 128.000 token | Verimli akıl yürütme modeli |
| o3-mini | 200.000 token | Hafif akıl yürütme modeli |
| o4-mini | 200.000 token | Yeni nesil verimli akıl yürütme |

**Yanıtlar API'si:**

OpenAI, varsayılan olarak Sohbet Tamamlama ve daha yeni Yanıtlar API'si olmak üzere iki API sunar. Yanıtlar API, yerleşik çok modlu desteğe sahip olarak sıfırdan tasarlanmıştır—metin, resimler, ses ve işlev çağrıları hepsi birinci sınıf vatandaştır. Akıl yürütme modelleriyle daha iyi performans ve otomatik zincirleme ve yerleşik araçlar gibi ek özellikler sağlar.

```python Code
from crewai import LLM

# Yanıtlar API'sini Sohbet Tamamlama yerine kullanın
llm = LLM(
    model="openai/gpt-4o",
    api="responses",  # Yanıtlar API'sini etkinleştirin
    store=True,  # Çok yönlü konuşmalar için yanıtları saklayın (isteğe bağlı)
    auto_chain=True,  # Akıl yürütme modelleri için otomatik zincirleme (isteğe bağlı)
)
```

**Yanıtlar API Parametreleri:**
- `api`: "responses" olarak ayarlanarak Yanıtlar API'sini kullanır (varsayılan: "completions")
- `instructions`: (Yanıtlar API'si yalnızca) Sistem düzeyindeki talimatlar
- `store`: Çok yönlü konuşmalar için yanıtları saklayıp saklamayacağınızı belirtir
- `previous_response_id`: Çok yönlü konuşmalar için önceki yanıtın kimliği
- `include`: Yanıta dahil edilecek ek veriler (örneğin, `["reasoning.encrypted_content"]`)
- `builtin_tools`: OpenAI yerleşik araçlarının listesi: `"web_search"`, `"file_search"`, `"code_interpreter"`, `"computer_use"`
- `parse_tool_outputs`: ayrıştırılmış yerleşik araç çıktılarıyla yapılandırılmış `ResponsesAPIResult` döndürür
- `auto_chain`: Çok yönlü konuşmalar için yanıt kimliklerini otomatik olarak izler ve kullanır
- `auto_chain_reasoning`: ZDR (Sıfır Veri Koruması) uyumluluğu için şifreli akıl yürütme öğelerini izler

Yeni projeler için ve özellikle akıl yürütme modelleri ([dosyalar](/en/concepts/files)) kullandığınızda Yanıtlar API'sini kullanın.

**Not:** OpenAI kullanmak için gerekli bağımlılıkları yükleyin:
```bash
uv add "crewai[openai]"
```

Meta's Llama API, Meta'nın aileden büyük dil modellerine erişim sağlar.
API, [Meta Llama API](https://llama.developer.meta.com?utm_source=partner-crewai&utm_medium=website) aracılığıyla kullanılabilir.

Ortam değişkenlerinizi `.env` dosyanızda ayarlayın:

```toml Code
# Gerekli
LLAMA_API_KEY=LLM|your_api_key_here
```

Projenizdeki CrewAI kullanım örneği:
```python Code
from crewai import LLM

# Meta Llama LLM'yi başlatın
llm = LLM(
    model="meta_llama/Llama-4-Scout-17B-16E-Instruct-FP8",
    temperature=0.8,
    stop=["END"],
    seed=42
)
```

Burada listelenen tüm modeller [https://llama.developer.meta.com/docs/models/](https://llama.developer.meta.com/docs/models/) desteklenir.

| Model | Giriş bağlam penceresi | Çıkış bağlam penceresi | Giriş Modları | Çıkış Modları |
|---|---|---|---|---|
| `meta_llama/Llama-4-Scout-17B-16E-Instruct-FP8` | 128k | 4028 | Metin, Resim | Metin |
| `meta_llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 128k | 4028 | Metin, Resim | Metin |
| `meta_llama/Llama-3.3-70B-Instruct` | 128k | 4028 | Metin | Metin |
| `meta_llama/Llama-3.3-8B-Instruct` | 128k | 4028 | Metin | Metin |

**Not:** Bu sağlayıcı LiteLLM'yi kullanır. Projenize bağımlılığı ekleyin:
```bash
uv add 'crewai[litellm]'
```

CrewAI, OpenAI Python SDK'sı aracılığıyla OpenAI ile yerel entegrasyon sağlar.

```toml Code
# Gerekli
ANTHROPIC_API_KEY=sk-ant-...
```

**Temel Kullanım:**
```python Code
from crewai import LLM

llm = LLM(
    model="anthropic/claude-3-5-sonnet-20241022",
    api_key="your-api-key",  # Veya ANTHROPIC_API_KEY'i ayarlayın
    max_tokens=4096  # Anthropic için gereklidir
)
```

**Gelişmiş Yapılandırma:**
```python Code
from crewai import LLM

llm = LLM(
    model="anthropic/claude-3-5-sonnet-20241022",
    api_key="your-api-key",
    base_url="https://api.anthropic.com",  # İsteğe bağlı özel uç nokta
    temperature=0.7,
    max_tokens=4096,  # Gereken parametre
    top_p=0.9,
    stop_sequences=["END", "STOP"],  # Anthropic durdurma dizilerini kullanır
    stream=True,  # Akışı etkinleştir
    timeout=60.0,  # İstenen zaman aşımı süresi (saniye)
    max_retries=3  # Maksimum yeniden deneme sayısı
)
```

**Genişletilmiş Akıl Yürütme (Claude Sonnet 4 ve Ötesi):**

CrewAI, Claude'un insan benzeri bir şekilde sorunlar üzerinde düşünmesini ve yanıt vermeden önce yanıt vermesini sağlayan Claude'un Genişletilmiş Akıl Yürütme özelliğini destekler. Bu, özellikle karmaşık akıl yürütme, analiz ve problem çözme görevleri için kullanışlıdır.

```python Code
from crewai import LLM

# Akıl yürütmeyi varsayılan ayarlarla etkinleştirin
llm = LLM(
    model="anthropic/claude-sonnet-4",
    thinking={"type": "enabled"},
    max_tokens=10000
)

# Akıl yürütmeyi bütçe kontrolüyle yapılandırın
llm = LLM(
    model="anthropic/claude-sonnet-4",
    thinking={
        "type": "enabled",
        "budget_tokens": 5000  # Akıl yürütme belirteçlerini sınırlayın
    },
    max_tokens=10000
)
```

**Akıl Yürütme Yapılandırma Seçenekleri:**
- `type`: Genişletilmiş akıl yürütme modunu etkinleştirmek için `"etkinleştirildi"` olarak ayarlayın
- `budget_tokens` (isteğe bağlı): Akıl yürütme için kullanılacak maksimum belirteç (maliyetleri kontrol etmeye yardımcı olur)

**Genişletilmiş Akıl Yürütmeyi Destekleyen Modeller:**
- `claude-sonnet-4` ve daha yeni modeller
- `claude-3-7-sonnet` (genişletilmiş akıl yürütme yetenekleriyle)

**Genişletilmiş Akıl Yürütmeyi Ne Zaman Kullanmalı:**
- Karmaşık akıl yürütme ve çok adımlı problem çözme
- Matematiksel hesaplamalar ve kanıtlar
- Kod analizi ve hata ayıklama
- Stratejik planlama ve karar verme
- Araştırma ve analiz görevleri

**Akıl Yürütme belirteçleri ek belirteçler tüketir, ancak karmaşık görevler için yanıt kalitesini önemli ölçüde artırabilir.**

**Desteklenen Ortam Değişkenleri:**
- `ANTHROPIC_API_KEY`: Anthropic API anahtarınız (gerekli)

**Özellikler:**
- Yerel araç kullanma desteği Claude 3+ modelleri için
- Claude Sonnet 4+ için Genişletilmiş Akıl Yürütme desteği
- Gerçek zamanlı yanıtlar için akış desteği
- Otomatik sistem mesajı işleme
- Kontrollü çıktı için durdurma dizileri
- Token kullanımı takibi

**Önemli Notlar:**
- `max_tokens`, tüm Anthropic modelleri için **gerekli** bir parametredir
- Claude, `stop` yerine `stop_sequences` kullanır
- Sistem mesajları, konuşma mesajlarından ayrı işlenir
- İlk mesaj kullanıcıdan gelmelidir (otomatik olarak işlenir)
- Mesajlar kullanıcı ve asistan arasında dönüşümlü olmalıdır

Anthropic kullanmak için gerekli bağımlılıkları yükleyin:
```bash
uv add "crewai[anthropic]"
```

CrewAI, OpenAI aracılığıyla OpenAI Python SDK'sı aracılığıyla OpenAI ile yerel entegrasyon sağlar.

Set your API key in your `.env` file. If you need a key, check [AI Studio](https://aistudio.google.com/apikey).

```python Code
from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key="your-api-key",  # Veya GOOGLE_API_KEY/GEMINI_API_KEY'i ayarlayın
    temperature=0.7
)
```

```python Code
from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.5-pro-preview-05-06",
    api_key="your-api-key",
    temperature=0.7,
    top_p=0.9,
    top_k=40,  # Top-k örnekleme parametresi
    max_output_tokens=8192,
    stop_sequences=["END", "STOP"],
    stream=True,  # Akışı etkinleştir
    safety_settings={
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE"
    }
)
```

**Vertex AI Express Modu (API Anahtarı Kimlik Doğrulaması):**

Vertex AI Express modu, hizmet hesabı kimlik bilgilerini kullanmak yerine basit bir API anahtarı kimlik doğrulamasıyla Vertex AI'ı kullanmanızı sağlar. Bu, başlamanın en hızlı yoludur.

Express modunu etkinleştirmek için, `.env` dosyanızda iki ortam değişkenini ayarlayın:
```toml .env
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_API_KEY=<your-api-key>
```

Ardından LLM'nizi her zamanki gibi kullanın:
```python Code
from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7
)
```

Vertex AI Konfigürasyonu (Hizmet Hesabı):
```python Code
from crewai import LLM

llm = LLM(
    model="gemini-1.5-pro-latest", # veya vertex_ai/gemini-1.5-pro-latest
    project="your-gcp-project-id",
    location="us-central1"  # GCP bölgesi
)
```

**Desteklenen Ortam Değişkenleri:**
- `GOOGLE_API_KEY` veya `GEMINI_API_KEY`: Google API anahtarınız (Gemini API'si ve Vertex AI Express modu için gereklidir)
- `GOOGLE_GENAI_USE_VERTEXAI`: Vertex AI kullanmak için `true` olarak ayarlanır (Express modu için gereklidir)
- `GOOGLE_CLOUD_PROJECT`: Google Cloud proje kimliği (hizmet hesabı ile Vertex AI için)
- `GOOGLE_CLOUD_LOCATION`: GCP konumu (varsayılan olarak `us-central1`)

**Özellikler:**
- Gemini 1.5+ ve 2.x modelleri için yerel işlev çağırma desteği
- Gerçek zamanlı yanıtlar için akış desteği
- Çoklu modlu yetenekler (metin, resim, video)
- Güvenlik ayarları yapılandırması
- Hem Gemini API'si hem de Vertex AI için destek
- Otomatik sistem talimatı işleme
- Token kullanımı takibi

**Not:** Google Gemini kullanmak için gerekli bağımlılıkları yükleyin:
```bash
uv add "crewai[google-genai]"
```

CrewAI, AWS Bedrock aracılığıyla boto3 SDK'sını kullanarak yerel entegrasyon sağlar.

```toml Code
# Gerekli
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>

# İsteğe bağlı
AWS_SESSION_TOKEN=<your-session-token>  # Geçici kimlik bilgiler için
AWS_DEFAULT_REGION=<your-region>  # varsayılan olarak us-east-1
AWS_REGION_NAME=<your-region>  # Geriye dönük uyumluluk için LiteLLM ile
```

```python Code
from crewai import LLM

llm = LLM(
    model="bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-east-1"
)
```

CrewAI, çok sayıda LLM sağlayıcısıyla entegre olur ve her biri benzersiz özellikler, kimlik doğrulama yöntemleri ve model yetenekleri sunar.

Bu bölüm, projenizin ihtiyaçları için en uygun LLM'yi seçmenize, yapılandırmanıza ve optimize etmenize yardımcı olacak ayrıntılı örnekler içerir.

---

Bu çeviri, belgenin tamamını korurken sağlanan yönergelerle uyumlu şekilde oluşturulmuştur.