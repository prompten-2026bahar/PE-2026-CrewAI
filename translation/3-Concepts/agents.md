# Agents
CrewAI framework’ü içinde agent oluşturma ve yönetmeye yönelik detaylı rehber.


## Bir Agent’a Genel Bakış

CrewAI framework’ünde bir `Agent`, aşağıdakileri yapabilen otonom bir birimdir:

- Belirli task’leri gerçekleştirmek
- Rolü ve hedefi doğrultusunda kararlar almak
- Hedeflere ulaşmak için tool kullanmak
- Diğer agent’larla iletişim kurmak ve iş birliği yapmak
- Etkileşimlerin hafızasını tutmak
- İzin verildiğinde task devretmek


  Bir agent’ı, belirli beceri, uzmanlık ve sorumluluklara sahip
  uzmanlaşmış bir ekip üyesi gibi düşünün. Örneğin, bir `Researcher` agent
  bilgi toplama ve analiz etmede başarılı olabilirken, bir `Writer` agent
  içerik üretme konusunda daha iyi olabilir.



CrewAI AMP, kod yazmadan agent oluşturmayı ve yapılandırmayı kolaylaştıran bir Visual Agent Builder içerir. Agent’larınızı görsel olarak tasarlayın ve gerçek zamanlı test edin.

<img src="../images/crew-studio-interface.png" alt="Visual Agent Builder Screenshot" />

Visual Agent Builder şunları sağlar:

- Form tabanlı arayüzlerle sezgisel agent yapılandırması
- Gerçek zamanlı test ve doğrulama
- Önceden yapılandırılmış agent türlerinden oluşan şablon kütüphanesi
- Agent özelliklerini ve davranışlarını kolayca özelleştirme


## Agent Özellikleri

| Özellik                                 | Parametre               | Tür                                   | Açıklama                                                                                                  |
| :-------------------------------------- | :---------------------- | :------------------------------------ | :--------------------------------------------------------------------------------------------------------- |
| **Role**                                | `role`                  | `str`                                 | Agent’ın crew içindeki fonksiyonunu ve uzmanlığını tanımlar.                                             |
| **Goal**                                | `goal`                  | `str`                                 | Agent’ın karar verme sürecini yönlendiren bireysel hedefi.                                               |
| **Backstory**                           | `backstory`             | `str`                                 | Agent’a bağlam ve kişilik kazandırır, etkileşimleri zenginleştirir.                                      |
| **LLM** _(isteğe bağlı)_                | `llm`                   | `Union[str, LLM, Any]`                | Agent’ı çalıştıran language model. Varsayılan olarak `OPENAI_MODEL_NAME` veya "gpt-4".                   |
| **Tools** _(isteğe bağlı)_              | `tools`                 | `List[BaseTool]`                      | Agent’ın kullanabileceği yetenekler veya fonksiyonlar. Varsayılan boş listedir.                          |
| **Function Calling LLM** _(isteğe bağlı)_ | `function_calling_llm`  | `Optional[Any]`                       | Tool çağrıları için kullanılan language model; belirtilirse crew’ün LLM’ini geçersiz kılar.              |
| **Max Iterations** _(isteğe bağlı)_     | `max_iter`              | `int`                                 | Agent’ın en iyi cevabını vermeden önce yapabileceği maksimum iterasyon sayısı. Varsayılan 20’dir.       |
| **Max RPM** _(isteğe bağlı)_            | `max_rpm`               | `Optional[int]`                       | Rate limit’lerden kaçınmak için dakikadaki maksimum istek sayısı.                                        |
| **Max Execution Time** _(isteğe bağlı)_ | `max_execution_time`    | `Optional[int]`                       | Task yürütme için maksimum süre (saniye cinsinden).                                                      |
| **Verbose** _(isteğe bağlı)_            | `verbose`               | `bool`                                | Hata ayıklama için detaylı yürütme log’larını etkinleştirir. Varsayılan False’tur.                       |
| **Allow Delegation** _(isteğe bağlı)_   | `allow_delegation`      | `bool`                                | Agent’ın diğer agent’lara task devretmesine izin verir. Varsayılan False’tur.                            |
| **Step Callback** _(isteğe bağlı)_      | `step_callback`         | `Optional[Any]`                       | Her agent adımından sonra çağrılan fonksiyon; crew callback’ini geçersiz kılar.                          |
| **Cache** _(isteğe bağlı)_              | `cache`                 | `bool`                                | Tool kullanımında cache’i etkinleştirir. Varsayılan True’dur.                                            |
| **System Template** _(isteğe bağlı)_    | `system_template`       | `Optional[str]`                       | Agent için özel system prompt şablonu.                                                                    |
| **Prompt Template** _(isteğe bağlı)_    | `prompt_template`       | `Optional[str]`                       | Agent için özel prompt şablonu.                                                                           |
| **Response Template** _(isteğe bağlı)_  | `response_template`     | `Optional[str]`                       | Agent yanıtları için özel şablon.                                                                         |
| **Allow Code Execution** _(isteğe bağlı)_ | `allow_code_execution` | `Optional[bool]`                      | Agent için code execution özelliğini etkinleştirir. Varsayılan False’tur.                                |
| **Max Retry Limit** _(isteğe bağlı)_    | `max_retry_limit`       | `int`                                 | Hata oluştuğunda maksimum yeniden deneme sayısı. Varsayılan 2’dir.                                       |
| **Respect Context Window** _(isteğe bağlı)_ | `respect_context_window` | `bool`                             | Mesajları context window boyutu altında tutmak için özetleme yapar. Varsayılan True’dur.                 |
| **Code Execution Mode** _(isteğe bağlı)_ | `code_execution_mode`  | `Literal["safe", "unsafe"]`           | Code execution modu: 'safe' (Docker kullanır) veya 'unsafe' (doğrudan). Varsayılan 'safe’tir.            |
| **Multimodal** _(isteğe bağlı)_         | `multimodal`            | `bool`                                | Agent’ın multimodal yetenekleri destekleyip desteklemediği. Varsayılan False’tur.                        |
| **Inject Date** _(isteğe bağlı)_        | `inject_date`           | `bool`                                | Mevcut tarihi task’lere otomatik ekler. Varsayılan False’tur.                                            |
| **Date Format** _(isteğe bağlı)_        | `date_format`           | `str`                                 | inject_date etkinleştirildiğinde kullanılacak tarih formatı. Varsayılan "%Y-%m-%d" (ISO formatı).        |
| **Reasoning** _(isteğe bağlı)_          | `reasoning`             | `bool`                                | Agent’ın task yürütmeden önce düşünüp plan oluşturmasını sağlar. Varsayılan False’tur.                   |
| **Max Reasoning Attempts** _(isteğe bağlı)_ | `max_reasoning_attempts` | `Optional[int]`                   | Task’i yürütmeden önce maksimum reasoning deneme sayısı. None ise hazır olana kadar dener.              |
| **Embedder** _(isteğe bağlı)_           | `embedder`              | `Optional[Dict[str, Any]]`            | Agent tarafından kullanılan embedder yapılandırması.                                                      |
| **Knowledge Sources** _(isteğe bağlı)_  | `knowledge_sources`     | `Optional[List[BaseKnowledgeSource]]` | Agent’ın erişebileceği bilgi kaynakları.                                                                  |
| **Use System Prompt** _(isteğe bağlı)_  | `use_system_prompt`     | `Optional[bool]`                      | System prompt kullanılıp kullanılmayacağı (o1 model desteği için). Varsayılan True’dur.                  |

## Agent Oluşturma

CrewAI’de agent oluşturmanın iki yolu vardır: **YAML yapılandırması (önerilir)** veya **doğrudan kod içinde tanımlama**.

### YAML Yapılandırması (Önerilir)

YAML yapılandırması, agent’ları tanımlamak için daha temiz ve sürdürülebilir bir yöntem sunar. CrewAI projelerinizde bu yaklaşımı kullanmanızı şiddetle öneririz.

CrewAI projenizi [Installation](/en/installation) bölümünde anlatıldığı gibi oluşturduktan sonra, `src/latest_ai_development/config/agents.yaml` dosyasına gidin ve şablonu ihtiyaçlarınıza göre düzenleyin.


YAML dosyalarındaki değişkenler (örneğin `{topic}`), crew çalıştırılırken verdiğiniz input değerleriyle değiştirilir:
```python Code
crew.kickoff(inputs={'topic': 'AI Agents'})
```


Aşağıda YAML kullanarak agent yapılandırma örneği yer almaktadır:

```yaml agents.yaml
# src/latest_ai_development/config/agents.yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.

reporting_analyst:
  role: >
    {topic} Reporting Analyst
  goal: >
    Create detailed reports based on {topic} data analysis and research findings
  backstory: >
    You're a meticulous analyst with a keen eye for detail. You're known for
    your ability to turn complex data into clear and concise reports, making
    it easy for others to understand and act on the information you provide.
```

Bu YAML yapılandırmasını kodunuzda kullanmak için CrewBase sınıfından türeyen bir crew sınıfı oluşturun:

```python Code
# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process
from crewai.project import CrewBase, agent, crew
from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

  agents_config = "config/agents.yaml"

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'], # type: ignore[index]
      verbose=True,
      tools=[SerperDevTool()]
    )

  @agent
  def reporting_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['reporting_analyst'], # type: ignore[index]
      verbose=True
    )
```

YAML dosyalarınızda (`agents.yaml`) kullandığınız isimler, Python kodunuzdaki method isimleriyle eşleşmelidir.
### Doğrudan Kod ile Tanımlama

Agent’ları doğrudan kod içinde `Agent` sınıfını örnekleyerek oluşturabilirsiniz. Aşağıda tüm mevcut parametreleri gösteren kapsamlı bir örnek yer almaktadır:


```python Code
from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent with all available parameters
agent = Agent(
    role="Senior Data Scientist",
    goal="Analyze and interpret complex datasets to provide actionable insights",
    backstory="With over 10 years of experience in data science and machine learning, "
              "you excel at finding patterns in complex datasets.",
    llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4"
    function_calling_llm=None,  # Optional: Separate LLM for tool calling
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    max_iter=20,  # Default: 20 iterations
    max_rpm=None,  # Optional: Rate limit for API calls
    max_execution_time=None,  # Optional: Maximum execution time in seconds
    max_retry_limit=2,  # Default: 2 retries on error
    allow_code_execution=False,  # Default: False
    code_execution_mode="safe",  # Default: "safe" (options: "safe", "unsafe")
    respect_context_window=True,  # Default: True
    use_system_prompt=True,  # Default: True
    multimodal=False,  # Default: False
    inject_date=False,  # Default: False
    date_format="%Y-%m-%d",  # Default: ISO format
    reasoning=False,  # Default: False
    max_reasoning_attempts=None,  # Default: None
    tools=[SerperDevTool()],  # Optional: List of tools
    knowledge_sources=None,  # Optional: List of knowledge sources
    embedder=None,  # Optional: Custom embedder configuration
    system_template=None,  # Optional: Custom system prompt template
    prompt_template=None,  # Optional: Custom prompt template
    response_template=None,  # Optional: Custom response template
    step_callback=None,  # Optional: Callback function for monitoring
```

Yaygın kullanım senaryoları için bazı önemli parametre kombinasyonlarını inceleyelim:

#### Temel Araştırma Agent’ı

```python Code
research_agent = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="You are an experienced researcher with attention to detail",
    tools=[SerperDevTool()],
    verbose=True  # Enable logging for debugging
)
```

#### Kod Geliştirme Agent’ı

```python Code
dev_agent = Agent(
    role="Senior Python Developer",
    goal="Write and debug Python code",
    backstory="Expert Python developer with 10 years of experience",
    allow_code_execution=True,
    code_execution_mode="safe",  # Uses Docker for safety
    max_execution_time=300,  # 5-minute timeout
    max_retry_limit=3  # More retries for complex code tasks
)
```

#### Uzun Süreli Analiz Agent’ı

```python Code
analysis_agent = Agent(
    role="Data Analyst",
    goal="Perform deep analysis of large datasets",
    backstory="Specialized in big data analysis and pattern recognition",
    memory=True,
    respect_context_window=True,
    max_rpm=10,  # Limit API calls
    function_calling_llm="gpt-4o-mini"  # Cheaper model for tool calls
)
```

#### Özel Şablonlu Agent

```python Code
custom_agent = Agent(
    role="Customer Service Representative",
    goal="Assist customers with their inquiries",
    backstory="Experienced in customer support with a focus on satisfaction",
    system_template="""<|start_header_id|>system<|end_header_id|>
                        {{ .System }}<|eot_id|>""",
    prompt_template="""<|start_header_id|>user<|end_header_id|>
                        {{ .Prompt }}<|eot_id|>""",
    response_template="""<|start_header_id|>assistant<|end_header_id|>
                        {{ .Response }}<|eot_id|>""",
)
```

#### Tarih Bilinçli ve Reasoning Özellikli Agent

```python Code
strategic_agent = Agent(
    role="Market Analyst",
    goal="Track market movements with precise date references and strategic planning",
    backstory="Expert in time-sensitive financial analysis and strategic reporting",
    inject_date=True,  # Automatically inject current date into tasks
    date_format="%B %d, %Y",  # Format as "May 21, 2025"
    reasoning=True,  # Enable strategic planning
    max_reasoning_attempts=2,  # Limit planning iterations
    verbose=True
)
```

#### Reasoning Agent

```python Code
reasoning_agent = Agent(
    role="Strategic Planner",
    goal="Analyze complex problems and create detailed execution plans",
    backstory="Expert strategic planner who methodically breaks down complex challenges",
    reasoning=True,  # Enable reasoning and planning
    max_reasoning_attempts=3,  # Limit reasoning attempts
    max_iter=30,  # Allow more iterations for complex planning
    verbose=True
)
```

#### Multimodal Agent

```python Code
multimodal_agent = Agent(
    role="Visual Content Analyst",
    goal="Analyze and process both text and visual content",
    backstory="Specialized in multimodal analysis combining text and image understanding",
    multimodal=True,  # Enable multimodal capabilities
    verbose=True
)
```

### Parametre Detayları

#### Kritik Parametreler

- `role`, `goal` ve `backstory` zorunludur ve agent'ın davranışını şekillendirir
- `llm` kullanılan dil modelini belirler (varsayılan: OpenAI'nin GPT-4'ü)

#### Bellek ve Bağlam

- `memory`: Konuşma geçmişini korumak için etkinleştirin
- `respect_context_window`: Token limiti sorunlarını önler
- `knowledge_sources`: Alana özgü bilgi tabanları ekleyin

#### Çalıştırma Kontrolü

- `max_iter`: En iyi cevabı vermeden önceki maksimum deneme sayısı
- `max_execution_time`: Saniye cinsinden zaman aşımı
- `max_rpm`: API çağrıları için hız sınırlama
- `max_retry_limit`: Hata durumunda yeniden deneme sayısı

#### Kod Çalıştırma

- `allow_code_execution`: Kod çalıştırmak için True olmalıdır
- `code_execution_mode`:
  - `"safe"`: Docker kullanır (production için önerilir)
  - `"unsafe"`: Doğrudan çalıştırma (yalnızca güvenilir ortamlarda kullanın)

Bu, varsayılan bir Docker image çalıştırır. Docker image'ı yapılandırmak istiyorsanız, araçlar bölümündeki Code Interpreter Tool'a göz atın. Code interpreter tool'u agent'a bir araç parametresi olarak ekleyin.

#### Gelişmiş Özellikler

- `multimodal`: Metin ve görsel içeriği işlemek için multimodal yetenekleri etkinleştirin
- `reasoning`: Agent'ın görevleri yürütmeden önce düşünüp plan oluşturmasını sağlar
- `inject_date`: Güncel tarihi otomatik olarak görev açıklamalarına ekler

#### Template'ler

- `system_template`: Agent'ın temel davranışını tanımlar
- `prompt_template`: Girdi formatını yapılandırır
- `response_template`: Agent yanıtlarını biçimlendirir

## Agent Araçları

Agent'lar, yeteneklerini geliştirmek için çeşitli araçlarla donatılabilir. CrewAI şu kaynaklardan gelen araçları destekler:

- [CrewAI Toolkit](https://github.com/joaomdmoura/crewai-tools)
- [LangChain Tools](https://python.langchain.com/docs/integrations/tools)

Bir agent'a araç ekleme yöntemi:

```python Code
from crewai import Agent
from crewai_tools import SerperDevTool, WikipediaTools

# Create tools
search_tool = SerperDevTool()
wiki_tool = WikipediaTools()

# Add tools to agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[search_tool, wiki_tool],
    verbose=True
)
```

## Agent Belleği ve Bağlamı

Agent'lar, etkileşimlerinin belleğini koruyabilir ve önceki görevlerden gelen bağlamı kullanabilir. Bu, bilginin birden fazla görev boyunca saklanması gereken karmaşık iş akışları için özellikle yararlıdır.

```python Code
from crewai import Agent

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and remember complex data patterns",
    memory=True,  # Enable memory
    verbose=True
)
```

`memory` parametresi, bir agent'ın birden fazla etkileşim boyunca bağlamı korumasını sağlayarak karmaşık, çok adımlı görevleri ele alma kapasitesini artırır.

## Context Window Yönetimi

CrewAI, konuşmaların dil modelinin token limitini aştığı durumları ele almak için gelişmiş otomatik context window yönetimi içerir. Bu güçlü özellik, `respect_context_window` parametresiyle kontrol edilir.

### Context Window Yönetimi Nasıl Çalışır?

Bir agent'ın konuşma geçmişi LLM'nin context window'u için fazla büyük hale geldiğinde, CrewAI bu durumu otomatik olarak algılar ve şunlardan birini yapabilir:

1. **İçeriği otomatik özetleme** (`respect_context_window=True` olduğunda)
2. **Hatayla çalışmayı durdurma** (`respect_context_window=False` olduğunda)

### Otomatik Bağlam İşleme (`respect_context_window=True`)

Bu, çoğu kullanım senaryosu için **varsayılan ve önerilen ayardır**. Etkinleştirildiğinde, CrewAI şunları yapacaktır:

```python Code
# Agent with automatic context management (default)
smart_agent = Agent(
    role="Research Analyst",
    goal="Analyze large documents and datasets",
    backstory="Expert at processing extensive information",
    respect_context_window=True,  # 🔑 Default: auto-handle context limits
    verbose=True
)
```

**Context limitleri aşıldığında ne olur:**

- ⚠️ **Uyarı mesajı**: `"Context length exceeded. Summarizing content to fit the model context window."`
- 🔄 **Otomatik özetleme**: CrewAI, konuşma geçmişini akıllıca özetler
- ✅ **Çalışmaya devam**: Görev yürütme, özetlenmiş bağlamla sorunsuz biçimde devam eder
- 📝 **Korunan bilgi**: Token sayısı azaltılırken önemli bilgiler saklanır

### Katı Context Limitleri (`respect_context_window=False`)

Kesin kontrole ihtiyaç duyduğunuzda ve bilgi kaybetmek yerine yürütmenin durmasını tercih ettiğinizde:

```python Code
# Agent with strict context limits
strict_agent = Agent(
    role="Legal Document Reviewer",
    goal="Provide precise legal analysis without information loss",
    backstory="Legal expert requiring complete context for accurate analysis",
    respect_context_window=False,  # ❌ Stop execution on context limit
    verbose=True
)
```

**Context limitleri aşıldığında ne olur:**

- ❌ **Hata mesajı**: `"Context length exceeded. Consider using smaller text or RAG tools from crewai_tools."`
- 🛑 **Çalışma durur**: Görev yürütme hemen durur
- 🔧 **Manuel müdahale gerekir**: Yaklaşımınızı değiştirmeniz gerekir

### Doğru Ayarı Seçmek

#### Şu durumlarda `respect_context_window=True` (Varsayılan) kullanın:

- Context limitlerini aşabilecek **büyük belgeleri işlerken**
- Bir miktar özetlemenin kabul edilebilir olduğu **uzun süreli konuşmalarda**
- Genel bağlamın tam ayrıntılardan daha önemli olduğu **araştırma görevlerinde**
- Sağlam bir çalışma ortamı istediğiniz **prototipleme ve geliştirme süreçlerinde**

```python Code
# Perfect for document processing
document_processor = Agent(
    role="Document Analyst",
    goal="Extract insights from large research papers",
    backstory="Expert at analyzing extensive documentation",
    respect_context_window=True,  # Handle large documents gracefully
    max_iter=50,  # Allow more iterations for complex analysis
    verbose=True
)
```

#### Şu durumlarda `respect_context_window=False` kullanın:

- **Kesinliğin kritik olduğu** ve bilgi kaybının kabul edilemez olduğu durumlarda
- Tam bağlam gerektiren **hukuki veya tıbbi görevlerde**
- Eksik ayrıntıların hata oluşturabileceği **kod incelemelerinde**
- Doğruluğun çok önemli olduğu **finansal analizlerde**

```python Code
# Perfect for precision tasks
precision_agent = Agent(
    role="Code Security Auditor",
    goal="Identify security vulnerabilities in code",
    backstory="Security expert requiring complete code context",
    respect_context_window=False,  # Prefer failure over incomplete analysis
    max_retry_limit=1,  # Fail fast on context issues
    verbose=True
)
```

### Büyük Veriler İçin Alternatif Yaklaşımlar

Çok büyük veri kümeleriyle çalışırken şu stratejileri göz önünde bulundurun:

#### 1. RAG Araçlarını Kullanın

```python Code
from crewai_tools import RagTool

# Create RAG tool for large document processing
rag_tool = RagTool()

rag_agent = Agent(
    role="Research Assistant",
    goal="Query large knowledge bases efficiently",
    backstory="Expert at using RAG tools for information retrieval",
    tools=[rag_tool],  # Use RAG instead of large context windows
    respect_context_window=True,
    verbose=True
)
```

#### 2. Knowledge Source Kullanın

```python Code
# Use knowledge sources instead of large prompts
knowledge_agent = Agent(
    role="Knowledge Expert",
    goal="Answer questions using curated knowledge",
    backstory="Expert at leveraging structured knowledge sources",
    knowledge_sources=[your_knowledge_sources],  # Pre-processed knowledge
    respect_context_window=True,
    verbose=True
)
```

### Context Window En İyi Uygulamaları

1. **Bağlam Kullanımını İzleyin**: Context yönetimini çalışırken görmek için `verbose=True` etkinleştirin
2. **Verimlilik için Tasarlayın**: Bağlam birikimini en aza indirmek için görevleri yapılandırın
3. **Uygun Modelleri Kullanın**: Görevlerinize uygun context window'a sahip LLM'leri seçin
4. **Her İki Ayarı da Test Edin**: Hangisinin kullanım senaryonuza daha uygun olduğunu görmek için hem `True` hem de `False`'u deneyin
5. **RAG ile Birleştirin**: Yalnızca context window'lara güvenmek yerine çok büyük veri kümeleri için RAG araçlarını kullanın

### Context Sorunlarını Giderme

**Context limiti hatası alıyorsanız:**

```python Code
# Quick fix: Enable automatic handling
agent.respect_context_window = True

# Better solution: Use RAG tools for large data
from crewai_tools import RagTool
agent.tools = [RagTool()]

# Alternative: Break tasks into smaller pieces
# Or use knowledge sources instead of large prompts
```

**Otomatik özetleme önemli bilgileri kaybediyorsa:**

```python Code
# Disable auto-summarization and use RAG instead
agent = Agent(
    role="Detailed Analyst",
    goal="Maintain complete information accuracy",
    backstory="Expert requiring full context",
    respect_context_window=False,  # No summarization
    tools=[RagTool()],  # Use RAG for large data
    verbose=True
)
```

Context window yönetimi özelliği arka planda otomatik olarak çalışır. Herhangi bir özel fonksiyon çağırmanıza gerek yoktur; yalnızca `respect_context_window`'u tercih ettiğiniz davranışa ayarlayın ve gerisini CrewAI halleder!

## `kickoff()` ile Doğrudan Agent Etkileşimi

Agent'lar, `kickoff()` yöntemi kullanılarak bir task veya crew iş akışından geçmeden doğrudan kullanılabilir. Bu, tam crew orkestrasyon özelliklerine ihtiyaç duymadığınızda bir agent ile etkileşim kurmanın daha basit bir yolunu sunar.

### `kickoff()` Nasıl Çalışır?

`kickoff()` yöntemi, tüm agent yetenekleriyle (araçlar, reasoning vb.) birlikte bir LLM ile etkileşim kurar gibi doğrudan bir agent'a mesaj gönderip yanıt almanızı sağlar.

```python Code
from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[SerperDevTool()],
    verbose=True
)

# Use kickoff() to interact directly with the agent
result = researcher.kickoff("What are the latest developments in language models?")

# Access the raw response
print(result.raw)
```

### Parametreler ve Dönüş Değerleri

| Parametre         | Tür                                | Açıklama                                                                   |
| :---------------- | :--------------------------------- | :------------------------------------------------------------------------- |
| `messages`        | `Union[str, List[Dict[str, str]]]` | Bir string sorgu veya role/content içeren mesaj sözlükleri listesi         |
| `response_format` | `Optional[Type[Any]]`              | Yapılandırılmış çıktı için isteğe bağlı Pydantic modeli                    |

Yöntem, aşağıdaki özelliklere sahip bir `LiteAgentOutput` nesnesi döndürür:

- `raw`: Ham çıktı metnini içeren string
- `pydantic`: Ayrıştırılmış Pydantic modeli (`response_format` sağlandıysa)
- `agent_role`: Çıktıyı üreten agent'ın rolü
- `usage_metrics`: Çalışma için token kullanım metrikleri

### Yapılandırılmış Çıktı

`response_format` olarak bir Pydantic modeli sağlayarak yapılandırılmış çıktı alabilirsiniz:

```python Code
from pydantic import BaseModel
from typing import List

class ResearchFindings(BaseModel):
    main_points: List[str]
    key_technologies: List[str]
    future_predictions: str

# Get structured output
result = researcher.kickoff(
    "Summarize the latest developments in AI for 2025",
    response_format=ResearchFindings
)

# Access structured data
print(result.pydantic.main_points)
print(result.pydantic.future_predictions)
```

### Çoklu Mesajlar

Ayrıca mesaj sözlükleri listesi olarak bir konuşma geçmişi de sağlayabilirsiniz:

```python Code
messages = [
    {"role": "user", "content": "I need information about large language models"},
    {"role": "assistant", "content": "I'd be happy to help with that! What specifically would you like to know?"},
    {"role": "user", "content": "What are the latest developments in 2025?"}
]

result = researcher.kickoff(messages)
```

### Async Desteği

Aynı parametrelerle `kickoff_async()` aracılığıyla asenkron bir sürüm mevcuttur:

```python Code

async def main():
    result = await researcher.kickoff_async("What are the latest developments in AI?")
    print(result.raw)

asyncio.run(main())
```

`kickoff()` yöntemi dahili olarak bir `LiteAgent` kullanır; bu, agent'ın tüm yapılandırmasını (role, goal, backstory, araçlar vb.) korurken daha basit bir çalışma akışı sağlar.

## Önemli Hususlar ve En İyi Uygulamalar

### Güvenlik ve Kod Çalıştırma

- `allow_code_execution` kullanılırken kullanıcı girişine dikkat edin ve her zaman doğrulayın
- Production ortamlarında `code_execution_mode: "safe"` (Docker) kullanın
- Sonsuz döngüleri önlemek için uygun `max_execution_time` limitleri ayarlamayı düşünün

### Performans Optimizasyonu

- Token limiti sorunlarını önlemek için `respect_context_window: true` kullanın
- Rate limiting'i önlemek için uygun `max_rpm` ayarlayın
- Tekrarlayan görevlerde performansı artırmak için `cache: true` etkinleştirin
- Görev karmaşıklığına göre `max_iter` ve `max_retry_limit` değerlerini ayarlayın

### Bellek ve Bağlam Yönetimi

- Alana özgü bilgiler için `knowledge_sources` kullanın
- Özel embedding modelleri kullanılırken `embedder` yapılandırın
- Agent davranışı üzerinde ince ayar kontrolü için özel template'ler (`system_template`, `prompt_template`, `response_template`) kullanın

### Gelişmiş Özellikler

- Karmaşık görevleri yürütmeden önce plan yapması ve düşünmesi gereken agent'lar için `reasoning: true` etkinleştirin
- Planlama yinelemelerini kontrol etmek için uygun `max_reasoning_attempts` ayarlayın (sınırsız deneme için None)
- Zamana duyarlı görevlerde agent'lara güncel tarih bilgisi vermek için `inject_date: true` kullanın
- Standart Python datetime format kodlarını kullanarak `date_format` ile tarih formatını özelleştirin
- Hem metin hem de görsel içeriği işlemesi gereken agent'lar için `multimodal: true` etkinleştirin

### Agent İş Birliği

- Agent'ların birlikte çalışması gerektiğinde `allow_delegation: true` etkinleştirin
- Agent etkileşimlerini izlemek ve kaydetmek için `step_callback` kullanın
- Farklı amaçlar için farklı LLM'ler kullanmayı düşünün:
  - Karmaşık reasoning için ana `llm`
  - Verimli araç kullanımı için `function_calling_llm`

### Tarih Farkındalığı ve Reasoning

- Zamana duyarlı görevlerde agent'lara güncel tarih bilgisi vermek için `inject_date: true` kullanın
- Standart Python datetime format kodlarını kullanarak `date_format` ile tarih formatını özelleştirin
- Geçerli format kodları şunları içerir: %Y (yıl), %m (ay), %d (gün), %B (tam ay adı) vb.
- Geçersiz tarih formatları uyarı olarak kaydedilir ve görev açıklamasını değiştirmez
- Önceden planlama ve düşünmeden yararlanan karmaşık görevler için `reasoning: true` etkinleştirin

### Model Uyumluluğu

- Sistem mesajlarını desteklemeyen eski modeller için `use_system_prompt: false` ayarlayın
- Seçtiğiniz `llm`'in ihtiyaç duyduğunuz özellikleri (fonksiyon çağırma gibi) desteklediğinden emin olun