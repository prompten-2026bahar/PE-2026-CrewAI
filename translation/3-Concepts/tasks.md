## Görevler (Tasks)

### Genel Bakış (Overview)

CrewAI çerçevesinde, bir `Görev`, bir `Ajan` tarafından tamamlanan özel bir atamadır.

Görevler, yürütme için gerekli tüm ayrıntıları sağlar; bunlar arasında açıklama, sorumlu ajan, gerekli araçlar ve daha fazlası bulunur ve geniş bir eylem karmaşıklığını kolaylaştırır.

CrewAI içindeki görevler işbirliğine dayalı olabilir; bu, birden fazla ajanın birlikte çalışmasını gerektirir. Bu, görev özellikler aracılığıyla yönetilir ve mürettebatın sürecince düzenlenir; bu da ekip çalışmasını ve verimliliği artırır.

CrewAI AMP, karmaşık görev oluşturmayı ve zincirlemeyi basitleştiren Crew Studio'da Görsel Görev Oluşturucu içerir. Görev akışlarınızı görsel olarak tasarlayın ve kod yazmadan gerçek zamanlı olarak test edin.

![Görev Oluşturucu Ekran Görüntüsü](../images/crew-studio-interface.png)

Görsel Görev Oluşturucu şunları sağlar:

- Sürükle-bırakla görev oluşturma
- Görsel görev bağımlılıkları ve akış
- Gerçek zamanlı test ve doğrulama
- Kolay paylaşım ve işbirliği

### Görev Yürütme Akışı (Task Execution Flow)

Görevler iki şekilde yürütülebilir:

- **Sıralı**: Görevler, tanımlandıkları sırayla yürütülür
- **Hiyerarşik**: Görevler, ajanların rolleri ve uzmanlıkları temelinde atanır

Yürütme akışı, mürettebat oluşturulurken tanımlanır:

```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sıralı  # veya Process.hiyerarşik
)
```

## Görev Özellikleri (Task Attributes)

| Özellik                                | Parametreler              | Tür                        | Açıklama                                                                                                     |
| :------------------------------------- | :---------------------- | :-------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| **Açıklama**                        | `description`           | `str`                       | Görevin ne içerdiğinin net ve öz bir ifadesi.                                                            |
| **Beklenen Çıktı**                    | `expected_output`       | `str`                       | Görevin tamamlanmasının nasıl görüneceğinin ayrıntılı bir açıklaması.                                                |
| **İsim** _(isteğe bağlı)_                  | `name`                  | `Optional[str]`             | Görevin tanımlayıcı bir adı.                                                                                 |
| **Ajan** _(isteğe bağlı)_                 | `agent`                 | `Optional[BaseAgent]`       | Görevi yürütecek sorumlu ajan.                                                                   |
| **Araçlar** _(isteğe bağlı)_                 | `tools`                 | `List[BaseTool]`            | Ajanın bu görev için kullanabileceği araçlar/kaynaklar.                                                  |
| **Bağlam** _(isteğe bağlı)_               | `context`               | `Optional[List["Task"]]`    | Bu görevin çıktısının bu görev için bağlam olarak kullanılacağı diğer görevler.                                                |
| **Asenkron Yürütme** _(isteğe bağlı)_       | `async_execution`       | `Optional[bool]`            | Görevin asenkron olarak yürütülüp yürütülmeyeceği. Varsayılan olarak False.                                          |
| **İnsan Girdisi** _(isteğe bağlı)_           | `human_input`           | `Optional[bool]`            | Görevin ajanın son cevabını bir insanın incelemesini gerektirip gerektirmediği. Varsayılan olarak False.                   |
| **Markdown** _(isteğe bağlı)_              | `markdown`              | `Optional[bool]`            | Görevin ajanın son cevabı Markdown formatında döndürmesini sağlayıp sağlamayacağı. Varsayılan olarak False. |
| **Yapılandırma** _(isteğe bağlı)_                | `config`                | `Optional[Dict[str, Any]]`  | Göreve özel yapılandırma parametreleri.                                                                         |
| **Çıktı Dosyası** _(isteğe bağlı)_           | `output_file`           | `Optional[str]`             | Görev çıktısını saklamak için dosya yolu.                                                                          |
| **Dizin Oluştur** _(isteğe bağlı)_      | `create_directory`      | `Optional[bool]`            | `output_file` yoksa dizini oluşturulup oluşturulmayacağı. Varsayılan olarak True.                          |
| **Çıktı JSON** _(isteğe bağlı)_           | `output_json`           | `Optional[Type[BaseModel]]` | Görev çıktısını yapılandırmak için Pydantic modeli.                                                                  |
| **Çıktı Pydantic** _(isteğe bağlı)_       | `output_pydantic`       | `Optional[Type[BaseModel]]` | Görev çıktısı için Pydantic modeli.                                                                               |
| **Geri Çağırma** _(isteğe bağlı)_              | `callback`              | `Optional[Any]`             | Görev tamamlandıktan sonra yürütülecek fonksiyon/nesne.                                                           |
| **Koruma** _(isteğe bağlı)_             | `guardrail`             | `Optional[Callable]`        | Bir sonraki göreve geçmeden önce görev çıktısını doğrulamak için fonksiyon.                                                |
| **Koruma Önlemleri** _(isteğe bağlı)_            | `guardrails`            | `Optional[List[Callable]]`  | Bir sonraki göreve geçmeden önce görev çıktısını doğrulamak için koruma önlemlerinin listesi.                                      |
| **Koruma Önlemi Maks Retriler** _(isteğe bağlı)_ | `guardrail_max_retries` | `Optional[int]`             | Koruma önlemi doğrulaması başarısız olduğunda deneme sayısı. Varsayılan olarak 3.                                       |

`max_retries` görev özelliği kullanımdan kaldırılmıştır ve v1.0.0'da kaldırılacaktır.
Koruma önlemi başarısız olduğunda deneme girişimlerini kontrol etmek için `guardrail_max_retries` kullanın.

## Görev Oluşturma (Creating Tasks)

Görev oluşturmanın iki yolu vardır: **YAML yapılandırması (önerilir)** veya bunları **doğrudan kodda tanımlama**.

### YAML Yapılandırması (Önerilen) (YAML Configuration (Recommended))

YAML yapılandırması kullanmak, görevleri tanımlamanın daha temiz ve daha bakılabilir bir yolunu sağlar. Görevleri tanımlamak için bu yaklaşımı kullanmanızı şiddetle tavsiye ediyoruz.

[Yükleme](/en/installation) bölümünde belirtildiği gibi CrewAI projenizi oluşturduktan sonra, `src/latest_ai_development/config/tasks.yaml` dosyasına gidin ve şablonu, özel görev gereksinimlerinizi karşılayacak şekilde değiştirin.

YAML dosyalarınızdaki değişkenler (örn. `{topic}`), mürettebatı çalıştırırken girdilerinizden değerlerle değiştirilecektir:
```python
crew.kickoff(inputs={'topic': 'AI Ajanları'})
```

Görevleri YAML kullanarak nasıl yapılandıracağınızın bir örneği:

````yaml tasks.yaml
araştırma_görevi:
  description: >
    {topic} hakkında kapsamlı bir araştırma yapın
    2025'in mevcut yılı göz önüne alındığında, bulduğunuz ilgili ve ilgili bilgileri kontrol edin.
  beklenen_çıktı: >
    {topic} ile ilgili en alakalı bilgilerin 10 madde listesi
  ajan: araştırmacı

raporlama_görevi:
  description: >
    Bağlamı inceleyin ve her konuyu tam bir rapor için bir bölüme genişletin.
    Raporun ayrıntılı olduğundan ve tüm ilgili bilgileri içerdiğinden emin olun.
  beklenen_çıktı: >
    Ana konuların her biri tam bir bölümle birlikte tamamen donatılmış bir rapor.
    '```' olmadan Markdown olarak biçimlendirilmiştir
  ajan: raporlama_analisti
  markdown: true
  çıktı_dosyası: rapor.md
````

Bu YAML yapılandırmasını kodunuzda kullanmak için `CrewBase`'den miras alan bir mürettebat sınıfı oluşturun:

```python crew.py
# src/latest_ai_development/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopmentCrew():
  """En Son AI Gelişimi mürettebatı"""

  @agent
  def araştırmacı(self) -> Agent:
    return Agent(
      config=self.agents_config['araştırmacı'], # type: ignore[index]
      verbose=True,
      tools=[SerperDevTool()]
    )

  @agent
  def raporlama_analisti(self) -> Agent:
    return Agent(
      config=self.agents_config['raporlama_analisti'], # type: ignore[index]
      verbose=True
    )

  @task
  def araştırma_görevi(self) -> Task:
    return Task(
      config=self.tasks_config['araştırma_görevi'] # type: ignore[index]
    )

  @task
  def raporlama_görevi(self) -> Task:
    return Task(
      config=self.tasks_config['raporlama_görevi'] # type: ignore[index]
    )

  @crew
  def mürettebat(self) -> Crew:
    return Crew(
      agents=[
        self.araştırmacı(),
        self.raporlama_analisti()
      ],
      tasks=[
        self.araştırma_görevi(),
        self.raporlama_görevi()
      ],
      process=Process.sıralı
    )
```

YAML dosyalarınızda (`agents.yaml` ve `tasks.yaml`) kullandığınız adlar, Python kodunuzdaki yöntem adlarıyla eşleşmelidir.

### Doğrudan Kod Tanımı (Alternatif) (Direct Code Definition (Alternative))

Alternatif olarak, YAML yapılandırması kullanmadan doğrudan kodunuzda görevler tanımlayabilirsiniz:

```python task.py
from crewai import Task

araştırma_görevi = Task(
    description="""
        AI ajanları hakkında kapsamlı bir araştırma yapın.
        2025'in mevcut yılı göz önüne alındığında, bulduğunuz ilgili ve ilgili bilgileri kontrol edin.
    """,
    beklenen_çıktı="""
        AI ajanları hakkında en alakalı bilgilerin 10 madde listesi
    """,
    agent=araştırmacı
)

raporlama_görevi = Task(
    description="""
        Bağlamı inceleyin ve her konuyu tam bir rapor için bir bölüme genişletin.
        Raporun ayrıntılı olduğundan ve tüm ilgili bilgileri içerdiğinden emin olun.
    """,
    beklenen_çıktı="""
        Tam fledge rapor ana konularıyla ve her biri tam bir bilgi bölümüyle.
    """,
    agent=raporlama_analisti,
    markdown=True,  # Son çıktının Markdown biçimlendirmesini etkinleştirin
    çıktı_dosyası="rapor.md"
)
```

Ajan için atama belirtmek için doğrudan belirtin veya hiyerarşik CrewAI'nin süreci rollere, kullanılabilirliğe vb. göre karar vermesini sağlayın.

## Görev Çıktısı (Task Output)

Görev çıktılarını anlamak, etkili AI iş akışları oluşturmak için çok önemlidir. CrewAI, çoklu çıktı formatlarını destekleyen ve kolayca görevler arasında geçirilebilen `TaskOutput` sınıfıyla yapılandırılmış bir yol sağlar.

CrewAI çerçevesindeki bir görevin çıktısı, çeşitli formatları içeren, çıktıları etkileşimli ve sunmak için bir yapılandırılmış yol sağlayan `TaskOutput` sınıfı içinde kapsanır; bu formatlar ham çıktı, JSON ve Pydantic modellerini içerir.

Varsayılan olarak, `TaskOutput` yalnızca `ham` çıktıyı içerir. `Task` nesnesi `output_pydantic` veya `output_json` ile yapılandırıldığında yalnızca `pydantic` veya `json_dict` çıktısı içerilecektir.

### Görev Çıktısı Özellikleri (Task Output Attributes)

| Özellik         | Parametreler      | Tür                       | Açıklama                                                                                        |
| :---------------- | :-------------- | :------------------------- | :------------------------------------------------------------------------------------------------- |
| **Açıklama**   | `description`   | `str`                      | Görevin ne içerdiğinin açıklaması.                                                                          |
| **Özet**       | `summary`       | `Optional[str]`            | Açıklamanın ilk 10 kelimesinden otomatik olarak oluşturulan görev özeti.                    |
| **Ham**           | `raw`           | `str`                      | Görevin ham çıktısı. Bu, varsayılan formattır.                             |
| **Pydantic**      | `pydantic`      | `Optional[BaseModel]`      | Görevin yapılandırılmış çıktısını temsil eden bir Pydantic model nesnesi.                            |
| **JSON Sözlüğü**     | `json_dict`     | `Optional[Dict[str, Any]]` | Görevin JSON çıktısını temsil eden bir sözlük.                                             |
| **Ajan**         | `agent`         | `str`                      | Görevi yürüten ajan.                                                                  |
| **Çıktı Formatı** | `output_format` | `OutputFormat`             | Çıktı formatı; seçenekler arasında RAW, JSON ve Pydantic bulunur. Varsayılan olarak RAW. |
| **Mesajlar**      | `messages`      | `list[LLMMessage]`         | Son görev yürütmesinden mesajlar.                                                         |

### Görev Yöntemleri ve Özellikleri (Task Methods and Properties)

| Yöntem/Özellik | Açıklama                                                                                       |
| :-------------- | :------------------------------------------------------------------------------------------------ |
| **json**        | Çıktı formatı JSON ise görev çıktısının JSON dizesini döndürür.           |
| **to_dict**     | JSON ve Pydantic çıktılarını bir sözlüğe dönüştürür.                                           |
| **str**         | Çıktının önceliği Pydantic, ardından JSON, ardından ham olan görev çıktısının dize gösterimini döndürür. |

### Görev Çıktılarına Erişme (Accessing Task Outputs)

Bir görev yürütüldükten sonra, görevin çıktısı `Task` nesnesinin `output` özelliği aracılığıyla erişilebilir. `TaskOutput` sınıfı, bu çıktıyla etkileşim kurmanın ve sunmanın çeşitli yollarını sağlar.

#### Örnek (Example)

```python Code
# Örnek görev
task = Task(
    description="En son AI haberlerini bulun ve özetleyin",
    beklenen_çıktı="En önemli 5 AI haberinin madde listesi",
    agent=research_agent,
    tools=[search_tool]
)

# Mürettebatı başlatın
crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()

# Görev çıktısına erişim
task_output = task.output

print(f"Görev Açıklaması: {task_output.description}")
print(f"Görev Özeti: {task_output.summary}")
print(f"Ham Çıktı: {task_output.raw}")
if task_output.json_dict:
    print(f"JSON Çıktısı: {json.dumps(task_output.json_dict, indent=2)}")
if task_output.pydantic:
    print(f"Pydantic Çıktısı: {task_output.pydantic}")
```

## Markdown Çıktı Biçimlendirmesi (Markdown Output Formatting)

`markdown` parametresi, otomatik Markdown biçimlendirmeyi etkinleştirmek için kullanılır. `True` olarak ayarlandığında, ajan son çıktıyı uygun Markdown sözdizimini kullanarak biçimlendirme talimatlarını alır.

### Markdown Biçimlendirmesi Kullanma (Using Markdown Formatting)

```python Code
# Markdown biçimlendirmesi etkinleştirilmiş bir görev örneği
formatted_task = Task(
    description="AI eğilimleri hakkında kapsamlı bir rapor oluşturun",
    beklenen_çıktı="Başlıklar, bölümler ve madde işaretleri içeren iyi yapılandırılmış bir rapor",
    agent=reporter_agent,
    markdown=True  # Otomatik Markdown biçimlendirmesini etkinleştirin
)
```

`markdown=True` olduğunda, ajan çıktıyı aşağıdaki şekilde biçimlendirme talimatlarını alır:

- `#` başlıklar için
- `**metin**` için kalın metin
- `*metin*` için italik metin
- `-` veya `*` için madde işaretleri
- `code` için satır içi kod
- ` ```dil` için kod blokları

### Markdown Çıktısının Faydaları (Benefits of Markdown Output)

- **Tutarlı Biçimlendirme**: Tüm çıktıların uygun Markdown kurallarına uygun olmasını sağlar
- **Daha İyi Okunabilirlik**: Başlıklar, listeler ve vurgularla yapılandırılmış içerik
- **Belgeleme Hazırlığı**: Çıktı doğrudan dokümantasyon sistemlerinde kullanılabilir
- **Platformlar Arası Uyumluluk**: Markdown, herkes tarafından desteklenir

`markdown=True` olduğunda, ajana ek biçimlendirme talimatları otomatik olarak görev istemine eklenir, bu nedenle görev açıklamanızda biçimlendirme gereksinimlerini belirtmenize gerek yoktur.

## Görev Bağımlılıkları ve Bağlam (Task Dependencies and Context)

Görevler, `bağlam` özelliği kullanılarak diğer görevlerin çıktısına bağlı olabilir. Örneğin:

```python Code
# ...

research_ai_task = Task(
    description="AI'daki en son gelişmeleri araştırın",
    beklenen_çıktı="AI'daki son gelişmelerin listesi",
    agent=research_agent,
    tools=[search_tool]
)

research_ops_task = Task(
    description="AI Operasyonlarındaki en son gelişmeleri araştırın",
    beklenen_çıktı="AI Operasyonlarındaki son gelişmelerin listesi",
    agent=research_agent,
    tools=[search_tool]
)

write_blog_task = Task(
    description="AI ve en son haberler hakkında tam bir blog yazısı yazın",
    beklenen_çıktı="4 paragraf uzunluğunda bir blog yazısı",
    agent=writer_agent,
    context=[research_ai_task, research_ops_task] # Bu görev, iki görevin çıktısının tamamlanmasını bekleyecektir
)

#...
```

## Görev Koruma Önlemleri (Task Guardrails)

Görev koruma önlemleri, görev çıktılarını bir sonraki göreve geçirmeden önce doğrulamak ve dönüştürmek için bir yol sağlar. Bu özellik, veri kalitesini sağlamaya ve ajana çıktı belirli kriterleri karşılamadığında geri bildirim sağlamaya yardımcı olur.

CrewAI, iki tür koruma önlemi destekler:

1. **Fonksiyon tabanlı koruma önlemleri**: Özellikler, doğrulama sürecini tamamen kontrol etmenizi sağlayan ve güvenilir, deterministik sonuçlar sağlamak için özel doğrulama mantığına sahip Python fonksiyonları.
2. **LLM tabanlı koruma önlemleri**: Doğal dil kriterlerini kullanarak ajanın LLM'sini doğrulama sürecini güdüleyen dize açıklamaları. Bu, karmaşık veya öznel doğrulama gereksinimleri için idealdir.

### Fonksiyon Tabanlı Koruma Önlemleri (Function-Based Guardrails)

Bir göreve fonksiyon tabanlı bir koruma önlemi eklemek için `guardrail` parametresine bir doğrulama fonksiyonu sağlayın:

```python Code
from typing import Tuple, Union, Dict, Any
from crewai import TaskOutput

def validate_blog_content(result: TaskOutput) -> Tuple[bool, Any]:
    """Blog içeriğini doğrulayın."""
    try:
        # Kelime sayısını kontrol edin
        word_count = len(result.raw.split())
        if word_count > 200:
            return (False, "Blog içeriği 200 kelimeyi aşmaktadır")

        # Ek doğrulama mantığı buraya
        return (True, result.raw.strip())
    except Exception as e:
        return (False, "Beklenmeyen bir hata oluştu")

blog_task = Task(
    description="AI hakkında bir blog yazısı yazın",
    beklenen_çıktı="200 kelimeden az iyi yazılmış bir blog yazısı",
    agent=blog_agent,
    guardrail=validate_blog_content  # Koruma önlemi fonksiyonunu ekleyin
)
```

### LLM Tabanlı Koruma Önlemleri (String Descriptions)

Özel doğrulama fonksiyonları yazmak yerine, LLM tabanlı doğrulama amacıyla doğal dil açıklamaları kullanabilirsiniz. Bir dizeye `guardrail` veya `guardrails` parametresini sağladığınızda, CrewAI otomatik olarak ajanın LLM'sini kullanacak olan bir `LLMGuardrail` oluşturur.

**Gereksinimler**:

- Görevde bir ajan atanmalıdır (koruma önlemi ajanın LLM'sini kullanır)
- Doğrulama kriterlerini açıklayan açık bir dize sağlayın

```python Code
blog_task = Task(
    description="AI hakkında bir blog yazısı yazın",
    beklenen_çıktı="200 kelimeden az blog yazısı",
    agent=blog_agent,
    guardrail="Blog yazısı 200 kelimeden az olmalı ve teknik jargon içermemelidir"
)
```

LLM tabanlı koruma önlemleri özellikle şunlar için kullanışlıdır:

- Programatik olarak ifade etmenin zor olduğu **karmaşık doğrulama mantığı**
- Ton, stil veya kalite değerlendirmeleri gibi **öznel kriterler**
- Doğrudan kodlanmasından daha kolay açıklanabilen **doğal dil gereksinimleri**

LLM koruma önlemi şunları yapar:

1. Görev çıktısını açıklamanıza göre analiz eder
2. Çıktı kriterlere uygunsa `(True, çıktı)` döndürür
3. Doğrulama başarısız olursa `(False, geri bildirim)` ile özel geri bildirim döndürür

**Ayrıntılı doğrulama kriterleriyle Örnek**:

```python Code
research_task = Task(
    description="Kuantum bilişimindeki son gelişmeleri araştırın",
    beklenen_çıktı="AI trendlerinin kapsamlı bir araştırma raporu",
    agent=researcher_agent,
    guardrail="""
    Araştırma raporu şunları yapmalıdır:
    - 1000 kelime uzunluğunda olmalıdır
    - En az 5 güvenilir kaynak içermelidir
    - Hem teknik hem de pratik uygulamaları kapsamalıdır
    - Profesyonel, akademik bir üslupla yazılmış olmalıdır
    - Doğrulama yapılmamış iddiaları veya spekülasyonları içermemelidir
    """
)
```

Birden fazla koruma önlemi (Multiple Guardrails):

Bir göreve birden fazla koruma önlemi uygulamak için `guardrails` parametresini kullanabilirsiniz. Birden fazla koruma önlemi sırayla yürütülür, her koruma önlemi bir önceki çıktıdan yararlanır. Bu, doğrulama ve dönüşüm adımlarının zincirlenmesini sağlar.

`guardrails` parametresi şunları kabul eder:

- Koruma önlemi fonksiyonlarının veya dize açıklamalarının bir listesi
- Tek bir koruma önlemi fonksiyonu veya dize ( `guardrail` ile aynı)

**Not**: `guardrail` sağlanırsa, `guardrails`in önüne geçecektir. `guardrail` ayarlandığında `guardrails` görmezden gelinir.

Fonksiyon tabanlı ve dize tabanlı koruma önlemlerini aynı listede birleştirebilirsiniz:

```python Code
from typing import Tuple, Any
from crewai import TaskOutput, Task

def validate_word_count(result: TaskOutput) -> Tuple[bool, Any]:
    """Kelime sayısını doğrulamak için bir işlev."""
    word_count = len(result.raw.split())
    if word_count < 100:
        return (False, f"İçerik çok kısa: {word_count} kelime. En az 100 kelime gerekir.")
    if word_count > 500:
        return (False, f"İçerik çok uzun: {word_count} kelime. Maksimum 500 kelime.")
    return (True, result.raw)

# Fonksiyon tabanlı ve dize tabanlı koruma önlemlerini birleştirin
blog_task = Task(
    description="AI hakkında bir blog yazısı yazın",
    beklenen_çıktı="100-500 kelimeler arasında iyi biçimlendirilmiş bir blog yazısı",
    agent=blog_agent,
    guardrails=[
        validate_word_count,  # Fonksiyon tabanlı: hassas kelime sayısı kontrolü
        "İçerik ilgi çekici ve genel bir kitle için uygun olmalıdır",  # LLM tabanlı: öznel kalite kontrolü
        "Yazım tarzı açık, öz ve teknik jargon içermemeli"  # LLM tabanlı: stil doğrulama
    ],
    guardrail_max_retries=3
)
```

Bu yaklaşım, programatik doğrulamanın hassasiğini öznel kriterlerin esnekliğiyle birleştirir.

### Koruma Önlemi Fonksiyonu Gereksinimleri (Guardrail Function Requirements)

1. **Fonksiyon İmzası**:

   - Tam olarak bir parametre (görev çıktısı) kabul etmelidir
   - `(bool, Any)` tuple'ını döndürmelidir
   - Tip ipuçları isteğe bağlıdır ancak önerilir

2. **Dönüş Değerleri**:
   - Başarılı olursa: `(True, doğrulanmış_sonuç)` tuple'ını döndürür.
   - Başarısız olursa: `(False, "hata mesajı açıklayıcı hata")` tuple'ını döndürür

### Hata İşleme En İyi Uygulamaları (Error Handling Best Practices)

1. **Yapılandırılmış Hata Yanıtları**:

```python Code
from crewai import TaskOutput, LLMGuardrail

def validate_with_context(result: TaskOutput) -> Tuple[bool, Any]:
    """Bağlamla doğrulayın."""
    try:
        # Ana doğrulama mantığı
        validated_data = perform_validation(result)
        return (True, validated_data)
    except ValidationError as e:
        return (False, f"VALIDATION_ERROR: {str(e)}")
    except Exception as e:
        return (False, str(e))
```

2. **Hata Kategorileri**:

   - Özel hata kodları kullanın
   - İlgili bağlamı dahil edin
   - Eyleme geçirilebilir geri bildirim sağlayın

3. **Doğrulama Zinciri**:

```python Code
from typing import Any, Dict, List, Tuple, Union
from crewai import TaskOutput

def complex_validation(result: TaskOutput) -> Tuple[bool, Any]:
    """Çoklu doğrulama adımını zincirleyin."""
    # Adım 1: Temel doğrulama
    if not result:
        return (False, "Boş sonuç")

    # Adım 2: İçerik doğrulaması
    try:
        validated = validate_content(result)
        if not validated:
            return (False, "Geçersiz içerik")

        # Adım 3: Format doğrulaması
        formatted = format_output(validated)
        return (True, formatted)
    except Exception as e:
        return (False, str(e))
```

## Koruma Önlemi Sonuçlarını İşleme (Handling Guardrail Results)

Bir koruma önlemi `(False, hata)` döndürdüğünde:

1. Hata, ajana geri gönderilir
2. Ajan sorunu çözmeye çalışır
3. Süreç şunlar olana kadar tekrarlanır:
   - Koruma önlemi `(True, sonuç)` döndürür
   - Maksimum denemeler sayısına ulaşılır (`guardrail_max_retries`)

## Araçları Görevlerle Entegre Etme (Integrating Tools with Tasks)

Gelişmiş görev performansı ve ajan etkileşimi için [CrewAI Araç Seti](https://github.com/joaomdmoura/crewai-tools) ve [LangChain Araçları](https://python.langchain.com/docs/integrations/tools) araçlarını kullanın.

## Görevlerle Araçlar Oluşturma (Creating a Task with Tools)

```python Code
os.environ["OPENAI_API_KEY"] = "Anahtarınız"
os.environ["SERPER_API_KEY"] = "Anahtarınız" # serper.dev API anahtarı

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

research_agent = Agent(
  role='Araştırmacı',
  goal='En son AI haberlerini bulun ve özetleyin',
  backstory="""Büyük bir şirkette araştırmacı olarak çalışıyorsunuz.
  Verileri analiz etmek ve şirket için içgörüler sağlamakla sorumlusunuz.""",
  verbose=True
)

# belirtilen metnin içeriğinden semantik bir arama yapmak için
search_tool = SerperDevTool()

task = Task(
  description='En son AI haberlerini bulun ve özetleyin',
  beklenen_çıktı='En önemli 5 AI haberinin madde listesi',
  agent=research_agent,
  tools=[search_tool]
)

crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

Bu, belirli araçlara sahip görevlerin, ajanın varsayılanlarını aşan uyarlanabilir görev yürütmesini vurgular.

## Hata İşleme ve Doğrulama Mekanizmaları (Error Handling and Validation Mechanisms)

Görev oluşturma ve yürütme sırasında, görev niteliklerinin sağlamlığını ve güvenilirliğini sağlamak için belirli doğrulama mekanizmaları uygulanır. Bunlar arasında, ancak bunlarla sınırlı olmamakla birlikte şunlar yer alır:

- Açık ve öz çıktı beklentilerini korumak için yalnızca bir çıktı türünün göreve göre tanımlandığından emin olunur.
- Eşsiz tanımlayıcı sistemin bütünlüğünü korumak için `id` özelliğinin manuel olarak atanmasını engellemek.

Bu doğrulama, CrewAI çerçevesindeki görev yürütmelerinin tutarlılığını ve güvenilirliğini sağlamaya yardımcı olur.

## Dosya Kaydetme sırasında Dizinler Oluşturma (Creating Directories when Saving Files)

`create_directory` parametresi, CrewAI'nın görev çıktılarını dosyalara kaydederken otomatik olarak dizinler oluşturup oluşturamayacağını kontrol eder. Bu özellik, özellikle karmaşık proje hiyerarşileriyle çalışırken çıktıları düzenlemek ve dosya yollarının doğru yapılandırıldığından emin olmak için özellikle kullanışlıdır.

### Varsayılan Davranış (Default Behavior)

Varsayılan olarak, `create_directory=True`, yani CrewAI, çıktı dosya yolundaki tüm eksik dizinleri otomatik olarak oluşturur:

```python Code
# Varsayılan davranış - dizinler otomatik olarak oluşturulur
report_task = Task(
    description='Kapsamlı bir pazar analiz raporu oluşturun',
    beklenen_çıktı='Grafikleri ve içgörüleri içeren ayrıntılı bir pazar analiz raporu',
    agent=analyst_agent,
    output_file='reports/2025/market_analysis.md',  # 'reports/2025/' yoksa oluşturur
    markdown=True
)
```

### Dizin Oluşturmayı Devre Dışı Bırakma (Disabling Directory Creation)

Dizinin zaten var olduğundan emin olmak için otomatik dizin oluşturmayı engellemek isterseniz, `create_directory=False` olarak ayarlayın:

```python Code
# Katı mod - dizinin zaten var olması gerekir
strict_output_task = Task(
    description='Mevcut altyapıya sahip önceden yapılandırılmış bir konuma veri kaydetme',
    beklenen_çıktı='Veri önceden yapılandırılmış konuma kaydedilir',
    agent=data_agent,
    output_file='secure/vault/critical_data.json',
    create_directory=False  # Yoksa RuntimeError yükseltir
)
```

### YAML Yapılandırması (YAML Configuration)

Bu davranışı YAML görev tanımlarınızda da yapılandırabilirsiniz:

```yaml tasks.yaml
analysis_task:
  description: >
    Çeyreklik finansal analiz oluşturun
  beklenen_çıktı: >
    Çeyreklik içgörüleri içeren kapsamlı bir finansal rapor
  agent: financial_analyst
  output_file: reports/quarterly/q4_2024_analysis.pdf
  create_directory: true # 'reports/quarterly/' dizinini otomatik olarak oluşturun

audit_task:
  description: >
    Uyumluluk denetimi gerçekleştirin ve mevcut denetim dizinine kaydedin
  beklenen_çıktı: >
    Uyumluluk denetim raporu
  agent: auditor
  output_file: audit/compliance_report.md
  create_directory: false # Dizin zaten var olmalıdır
```

### Kullanım Durumları (Use Cases)

**Otomatik Dizin Oluşturma (`create_directory=True`):**

- Geliştirme ve prototip ortamları
- Tarih tabanlı klasörlerle dinamik rapor oluşturma
- Dizin yapısının değişebileceği otomatik iş akışları
- Kullanıcıya özel klasörlere sahip çok kiracılı uygulamalar

**Manuel Dizin Yönetimi (`create_directory=False`):**

- Dosya sistemi kontrolleri üzerinde sıkı kontrol gerektiren üretim ortamları
- Dizinlerin önceden yapılandırılması gereken güvenlik açısından hassas uygulamalar
- Dizin oluşturulmasının denetlendiği uyumluluk ortamları

### Hata İşleme (Error Handling)

`create_directory=False` ve dizin mevcut değilse, CrewAI bir `RuntimeError` yükseltir:

```python Code
try:
    result = crew.kickoff()
except RuntimeError as e:
    # Eksik dizin hatasını işleyin
    print(f"Dizin oluşturma başarısız oldu: {e}")
    # Dizini manuel olarak oluşturun veya yedek konum kullanın
```

Altı çizili videoyu, CrewAI'de yapılandırılmış çıktıların nasıl kullanılacağını görmek için kontrol edin:

[![CrewAI'de Yapılandırılmış Çıktılar](https://img.youtube.com/vi/dNpKQk5uxHw/0.jpg)](https://www.youtube.com/watch?v=dNpKQk5uxHw)

## Sonuç (Conclusion)

Görevler, CrewAI'deki ajanların eylemlerinin itici gücüdür. Görevleri ve çıktılarını uygun şekilde tanımlayarak, AI ajanlarınızın etkin bir şekilde çalışması için sahneyi hazırlarsınız; ya bağımsız olarak ya da işbirliğine dayalı bir birim olarak. Görevleri uygun araçlarla donatmak, yürütme sürecini anlamak ve sağlam doğrulama uygulamaları izlemek, CrewAI'nin potansiyelini en üst düzeye çıkarmak, ajanların atamalarına etkin bir şekilde hazırlanmasını ve görevlerin amaçlandığı gibi yürütülmesini sağlamak için çok önemlidir.