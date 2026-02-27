# Ekipler
CrewAI çerçevesinde ekipleri, kapsamlı nitelik ve işlevselliklerle anlayarak ve kullanarak.


## Genel Bakış

crewAI'da bir ekip, bir dizi görevi tamamlamak için birlikte çalışan işbirlikçi bir ajan grubunu temsil eder. Her ekip, görev yürütme stratejisi, ajan işbirliği ve genel iş akışı için stratejiyi tanımlar.

## Ekip Nitelikleri

| Nitelik                             | Parametreler             | Açıklama                                                                                                                                                                                                                                               |
| :------------------------------------ | :--------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Görevler**                             | `tasks`                | Ekipe atanan görevlerin listesi.                                                                                                                                                                                                                     |
| **Ajanlar**                            | `agents`               | Ekibin parçası olan ajanların listesi.                                                                                                                                                                                                               |
| **Süreç** _(isteğe bağlı)_              | `process`              | Ekibin izlediği süreç akışı (örneğin, sıralı, hiyerarşik). Varsayılan olarak `sıralı`dır.                                                                                                                                                              |
| **Ayrıntı Düzeyi** _(isteğe bağlı)_              | `verbose`              | Yürütme sırasında günlük kaydı için ayrıntı düzeyi. Varsayılan olarak `False`'dur.                                                                                                                                                     |
| **Yönetici LLM** _(isteğe bağlı)_          | `manager_llm`          | Hiyerarşik bir süreçte yönetici ajanın kullandığı dil modeli. **Hiyerarşik bir süreç kullanırken gereklidir.**                                                                                                                                   |
| **Fonksiyon Çağırma LLM** _(isteğe bağlı)_ | `function_calling_llm` | Eğer verilirse, ekip bu LLM'yi araçlar için fonksiyon çağırmak için kullanır. Her ajanın kendi LLM'si olabilir, bu da ekip LLM'sini fonksiyon çağırma için geçersiz kılar.                                                                  |
| **Yapılandırma** _(isteğe bağlı)_               | `config`               | Ekip için isteğe bağlı yapılandırma ayarları, `Json` veya `Dict[str, Any]` biçiminde.                                                                                                                                                                       |
| **Maks RPM** _(isteğe bağlı)_              | `max_rpm`              | Ekibin yürütme sırasında uyduğu maksimum istek sayısı dakika. Varsayılan olarak `None`'dır.                                                                                                                                                                     |
| **Bellek** _(isteğe bağlı)_               | `memory`               | Kısa süreli, uzun süreli ve varlık belleği için yürütme anılarını depolamak için kullanılır.                                                                                                                                                                           |
| **Önbellek** _(isteğe bağlı)_                | `cache`                | Araçların yürütme sonuçlarını depolamak için bir önbellek kullanılıp kullanılmadığını belirtir. Varsayılan olarak `True`'dur.                                                                                                                                                         |
| **Gömme Aracı** _(isteğe bağlı)_             | `embedder`             | Ekip tarafından kullanılacak gömme aracının yapılandırması. Çoğunlukla şu anda bellek tarafından kullanılır. Varsayılan olarak `{"provider": "openai"}`'dir.                                                                                                                                |
| **Adım Geri Çağırma** _(isteğe bağlı)_        | `step_callback`        | Her ajan adımının ardından çağrılan bir fonksiyon. Bu, ajanın eylemlerini günlüğe kaydetmek veya diğer işlemleri gerçekleştirmek için kullanılabilir; ajan spesifik `step_callback`'i geçersiz kılmaz.                                                               |
| **Görev Geri Çağırma** _(isteğe bağlı)_        | `task_callback`        | Her görevin tamamlanmasının ardından çağrılan bir fonksiyon. Görev yürütme sonrası izleme veya ek işlemler için kullanışlıdır.                                                                                                                          |
| **Ekibi Paylaş** _(isteğe bağlı)_           | `share_crew`           | Tam ekip bilgilerini ve yürütmeyi ekipAI ekibiyle paylaşarak kütüphaneyi daha iyi hale getirmek ve model eğitmek isteyip istemediğinizi gösterir.                                                                                                      |
| **Çıkış Günlük Dosyası** _(isteğe bağlı)_      | `output_log_file`      | Günlükleri mevcut dizindeki logs.txt olarak kaydetmek için True olarak ayarlayın veya bir dosya yolu belirtin. Dosya adı .json ile bitiyorsa günlükler JSON biçiminde, aksi takdirde .txt olarak kaydedilir. Varsayılan olarak `None`'dır.                                                                      |
| **Yönetici Ajan** _(isteğe bağlı)_        | `manager_agent`        | `manager` özel bir ajanı ayarlayarak kullanılır.                                                                                                                                                                                             |
| **İstem Şablonu** _(isteğe bağlı)_          | `prompt_file`          | Ekip için kullanılacak istem JSON dosyasının yolu.                                                                                                                                                                                                     |
| **Planlama** *(isteğe bağlı)*             | `planning`             | Ekibe planlama yeteneği ekler. Her ekip yinelemesinden önce etkinleştirildiğinde, tüm ekip verileri bir AgentPlanner'a gönderilir ve bu plan her görev tanımına eklenir.                                                     |
| **Planlama LLM** *(isteğe bağlı)*         | `planning_llm`         | Planlama sürecinde AgentPlanner tarafından kullanılan dil modeli.                                                                                                                                                                                        |
| **Bilgi Kaynakları** _(isteğe bağlı)_    | `knowledge_sources`    | Tüm ajanlara erişilebilir ekip düzeyindeki bilgi kaynakları.                                                                                                                                                                                    |
| **Akış** _(isteğe bağlı)_               | `stream`               | Ekip yürütmesi sırasında gerçek zamanlı güncellemeler almak için akışı etkinleştirin. Çekirdekler için bir `CrewStreamingOutput` nesnesi döndürür. Varsayılan olarak `False`'dur.                                                                                    |


**Ekip Maks RPM**: `max_rpm` niteliği, ekibin hız sınırlamalarından kaçınmak için dakika başına gerçekleştirebileceği maksimum istek sayısını ayarlar ve ekip spesifik `max_rpm` ayarlarını geçersiz kılar.


## Ekip Oluşturma

CrewAI'da ekipler oluşturmanın iki yolu vardır: **YAML yapılandırması kullanmak (önerilir)** veya bunları **doğrudan kodda tanımlamak**.

### YAML Yapılandırması (Önerilir)

YAML yapılandırması kullanmak, ekipleri tanımlamanın daha temiz ve daha bakılabilir bir yolunu sağlar ve CrewAI projelerinde ajanların ve görevlerin nasıl tanımlandığıyla tutarlıdır.

[Kurulum](/en/installation) bölümünde belirtildiği gibi CrewAI projenizi oluşturduktan sonra, ekibinizi `CrewBase` sınıfından devralan ve ajanları, görevleri ve ekibi kendisini tanımlamak için dekoratörleri kullanan bir sınıfta tanımlayabilirsiniz.

#### Dekoratörlerle Örnek Ekip Sınıfı

```python code
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class YourCrewName:
    """Ekibinizin açıklaması"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # YAML yapılandırma dosyalarınızın yolları
    # Ajan ve görev tanımının YAML'de nasıl tanımlandığını görmek için aşağıdaki bağlantılara bakın:
    # - Görev: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    # - Ajanlar: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def prepare_inputs(self, inputs):
        # Ekip başlamadan önce girdileri değiştirin
        inputs['additional_data'] = "Ekstra bilgiler"
        return inputs

    @after_kickoff
    def process_output(self, output):
        # Ekip tamamlandıktan sonra çıktıyı değiştirin
        output.raw += "\nBaşlangıç sonrası işleme yapıldı."
        return output

    @agent
    def agent_one(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_one'], # type: ignore[index]
            verbose=True
        )

    @agent
    def agent_two(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_two'], # type: ignore[index]
            verbose=True
        )

    @task
    def task_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_one'] # type: ignore[index]
        )

    @task
    def task_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_two'] # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # @agent dekoratörü tarafından otomatik olarak toplanır
            tasks=self.tasks,    # @task dekoratörü tarafından otomatik olarak toplanır.
            process=Process.sequential,
            verbose=True,
        )
```

Yukarıdaki kodu çalıştırma şekli:

```python code
YourCrewName().crew().kickoff(inputs={"any": "girdi burası"})
```


Görevler, tanımlandıkları sırayla yürütülür.


`CrewBase` sınıfı ve bu dekoratörler, ajanları ve görevleri otomatik olarak toplayarak, manuel yönetim ihtiyacını azaltır.

#### Dekoratörler özeti `annotations.py` dosyasından

CrewAI, `annotations.py` dosyasında ekip yapınızı düzenlemek için kullanılan çeşitli dekoratörler sağlar:

- `@CrewBase`: Sınıfı ekip temel sınıfı olarak işaretler.
- `@agent`: Bir `Agent` nesnesi döndüren bir yöntemi gösterir.
- `@task`: Bir `Task` nesnesi döndüren bir yöntemi gösterir.
- `@crew`: `Crew` nesnesi döndüren yöntemi gösterir.
- `@before_kickoff`: (İsteğe bağlı) Ekip başlamadan önce yürütülmesi gereken bir yöntemi işaretler.
- `@after_kickoff`: (İsteğe bağlı) Ekip tamamlandıktan sonra yürütülmesi gereken bir yöntemi işaretler.

Bu dekoratörler, ekibinizin yapısını düzenlemeye ve ajanları ve görevleri manuel olarak listelemeye gerek kalmadan otomatik olarak toplamaya yardımcı olur.

### Doğrudan Kod Tanımı (Alternatif)

Alternatif olarak, YAML yapılandırma dosyalarını kullanmadan doğrudan kodda ekibi tanımlayabilirsiniz.

```python code
from crewai import Agent, Crew, Task, Process
from crewai_tools import YourCustomTool

class YourCrewName:
    def agent_one(self) -> Agent:
        return Agent(
            role="Veri Analisti",
            goal="Piyasadaki veri trendlerini analiz et",
            backstory="Ekonomi alanında deneyimli bir veri analisti",
            verbose=True,
            tools=[YourCustomTool()]
        )

    def agent_two(self) -> Agent:
        return Agent(
            role="Piyasa Araştırmacısı",
            goal="Piyasa dinamikleri hakkında bilgi toplamak",
            backstory="Detaylara dikkat eden çalışkan bir araştırmacı",
            verbose=True
        )

    def task_one(self) -> Task:
        return Task(
            description="Yakın tarihli piyasa verilerini toplayın ve trendleri belirleyin.",
            expected_output="Piyasadaki kilit trendleri özetleyen bir rapor.",
            agent=self.agent_one()
        )

    def task_two(self) -> Task:
        return Task(
            description="Piyasa dinamiklerini etkileyen faktörleri araştırın.",
            expected_output="Piyasa üzerinde etkili olan faktörlerin analizi.",
            agent=self.agent_two()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.agent_one(), self.agent_two()],
            tasks=[self.task_one(), self.task_two()],
            process=Process.sequential,
            verbose=True
        )
```
Yukarıdaki kodu çalıştırma şekli:

```python code
YourCrewName().crew().kickoff(inputs={})
```

Bu örnekte:

- Ajanlar ve görevler sınıf içinde dekoratörler olmadan doğrudan tanımlanır.
- Ajanlar ve görevlerin listesi manuel olarak oluşturulur ve yönetilir.
- Bu yaklaşım daha fazla kontrol sağlasa da, daha büyük projeler için daha az bakılabilir olabilir.

## Ekip Çıktısı

CrewAI çerçevesindeki bir ekibin çıktısı, `CrewOutput` sınıfı içinde kapsülendirilmiştir.
Bu sınıf, ekibin yürütmesinin sonuçlarına erişmek için yapılandırılmış bir yol sağlar ve çıktı biçimleri gibi çeşitli formatlar içerir. `CrewOutput`, son görev çıktısı, belirteç kullanımı ve ayrı ayrı görev çıktıları dahil olmak üzere çeşitli biçimlerde sonuçlara erişmek için çeşitli yöntemler ve özellikler sunar.

### CrewOutput Nitelikleri

| Nitelik        | Parametreler     | Tipi                       | Açıklama                                                                                          |
| :--------------- | :------------- | :------------------------- | :--------------------------------------------------------------------------------------------------- |
| **Ham**          | `raw`          | `str`                      | Ekibin ham çıktısı. Bu, varsayılan çıktı biçimidir.                               |
| **Pydantic**     | `pydantic`     | `Optional[BaseModel]`      | Ekibin yapılandırılmış çıktısını temsil eden bir Pydantic model nesnesi.                              |
| **JSON Sözlüğü**    | `json_dict`    | `Optional[Dict[str, Any]]` | Ekibin JSON çıktısını temsil eden bir sözlük.                                               |
| **Görev Çıktısı** | `tasks_output` | `List[TaskOutput]`         | Ekip içindeki her görev için bir `TaskOutput` nesnesi içeren bir liste.                  |
| **Belirteç Kullanımı**  | `token_usage`  | `Dict[str, Any]`           | Dil modelinin yürütme sırasında performansına ilişkin içgörüler sağlayan belirteç kullanımı özeti. |

### CrewOutput Yöntemleri ve Özellikleri

| Yöntem/Özellik | Açıklama                                                                                       |
| :-------------- | :------------------------------------------------------------------------------------------------ |
| **json**        | Çıktı biçimi JSON ise ekibin JSON dizesi gösterimini döndürür.           |
| **to_dict**     | JSON ve Pydantic çıktılarını bir sözlüğe dönüştürür.                                           |
| \***\*str\*\*** | Ham, JSON ve ardından Pydantic çıktıları sırasını içeren ekibin dize gösterimini döndürür. |

### Ekip Çıktısına Erişim

Bir ekip yürütüldükten sonra, çıktısı `Crew` nesnesinin `output` özelliği aracılığıyla erişilebilir. `CrewOutput` sınıfı, bu çıktıyla etkileşim kurmak ve sunmak için çeşitli yollar sağlar.

#### Örnek

```python Code
# Ekip yürütmesi örneği
crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_task, write_article_task],
    verbose=True
)

crew_output = crew.kickoff()

# Ekip çıktısına erişim
print(f"Ham Çıktı: {crew_output.raw}")
if crew_output.json_dict:
    print(f"JSON Çıktısı: {json.dumps(crew_output.json_dict, indent=2)}")
if crew_output.pydantic:
    print(f"Pydantic Çıktısı: {crew_output.pydantic}")
print(f"Görev Çıktısı: {crew_output.tasks_output}")
print(f"Belirteç Kullanımı: {crew_output.token_usage}")
```

## Ekip Günlüklerine Erişim

Ekip yürütmesi sırasında gerçek zamanlı görünürlük için, `output_log_file`'ı bir `True(Boolean)` veya bir `file_name(str)` olarak ayarlayarak akışı etkinleştirebilirsiniz.  `file_name.json` olarak ayarlanırsa hem `file_name.txt` hem de `file_name.json` olarak günlükleri destekler.
`output_log_file` `False(Boolean)` veya `None` olarak ayarlanırsa günlükler kaydedilmez.

```python Code
# Ekip günlüklerini kaydetme
crew = Crew(output_log_file = True)  # Günlükler logs.txt olarak kaydedilecektir
crew = Crew(output_log_file = file_name)  # Günlükler file_name.txt olarak kaydedilecektir
crew = Crew(output_log_file = file_name.txt)  # Günlükler file_name.txt olarak kaydedilecektir
crew = Crew(output_log_file = file_name.json)  # Günlükler file_name.json olarak kaydedilecektir
```



## Bellek Kullanımı

Ekipler, zaman içinde yürütmelerini ve öğrenmelerini geliştirmek için (kısa vadeli, uzun vadeli ve varlık belleği) belleği kullanabilir. Bu özellik, ekiplerin yürütme anılarını depolamasına ve geri çağırmasına izin vererek karar vermede ve görev yürütme stratejilerinde yardımcı olur.

## Önbellek Kullanımı

Araçların yürütme sonuçlarını depolayarak daha verimli bir hale getirmek için önbellekler kullanılabilir.

## Ekip Kullanım Metrikleri

Ekip yürütmesinden sonra, ekip tarafından yürütülen tüm görevler için dil modeli (LLM) kullanım metriklerini görüntülemek için `usage_metrics` özelliğini kullanabilirsiniz. Bu, operasyonel verimliliğe ve iyileştirilebilecek alanlara ilişkin bilgiler sağlar.

```python Code
# Ekibin kullanım metriklerine erişin
crew = Crew(agents=[agent1, agent2], tasks=[task1, task2])
crew.kickoff()
print(crew.usage_metrics)
```

## Ekip Yürütme Süreci

- **Sıralı Süreç**: Görevler, doğrusal bir iş akışına izin vererek birbiri ardına yürütülür.
- **Hiyerarşik Süreç**: Bir yönetici ajan, görevi delege eder ve devam etmeden önce çıktıları doğrulayarak ekibi koordine eder. **Not**: Bu süreç için bir `manager_llm` veya `manager_agent` gereklidir ve akışın doğrulanması için esastır.

### Ekibi Başlatma

Ekibinizi derledikten sonra, tanımlanmış süreç akışına göre yürütme işlemini başlatmak için `kickoff()` yöntemini kullanın.

```python Code
# Ekibin görev yürütmesini başlatın
result = my_crew.kickoff()
print(result)
```

### Ekibi Başlatmanın Farklı Yolları

Ekibinizi derledikten sonra, iş akışını yönetmek ve yürütmek için hem senkronize hem de asenkron iş akışlarına uygun olarak çeşitli yöntemler sağlar.

#### Senkron Yöntemler

- `kickoff()`: Tanımlanmış süreç akışına göre yürütme işlemini başlatır.
- `kickoff_for_each()`: Sağlanan her girdi olayı veya koleksiyondaki öğe için sıralı olarak görevleri yürütür.

#### Asenkron Yöntemler

CrewAI, iki yaklaşım sunar:

| Yöntem | Tipi | Açıklama |
|--------|------|-------------|
| `akickoff()` | Yerel asenkron | Tüm yürütme zinciri boyunca yerel asenkron/bekleme |
| `akickoff_for_each()` | Yerel asenkron | Liste içindeki her girdi için yerel asenkron |
| `kickoff_async()` | İpli | `asyncio.to_thread` ile senkron yürütmeyi sarmalar |
| `kickoff_for_each_async()` | İpli | Liste içindeki her girdi için ipli asenkron |

Yüksek eşzamanlılık iş yükleri için `akickoff()` ve `akickoff_for_each()` önerilir çünkü görev yürütme, bellek işlemleri ve bilgi alma için yerel asenkron kullanırlar.

```python Code
# Ekibin görev yürütmesini başlatın
result = my_crew.kickoff()
print(result)

# kickoff_for_each kullanma örneği
inputs_array = [{'konu': 'yapay zeka sağlık'}, {'konu': 'yapay zeka finans'}]
results = my_crew.kickoff_for_each(inputs=inputs_array)
for result in results:
    print(result)

# Yerel asenkron kullanımı akickoff ile
inputs = {'konu': 'yapay zeka sağlık'}
async_result = await my_crew.akickoff(inputs=inputs)
print(async_result)

# Yerel asenkron kullanımı akickoff_for_each ile
inputs_array = [{'konu': 'yapay zeka sağlık'}, {'konu': 'yapay zeka finans'}]
async_results = await my_crew.akickoff_for_each(inputs=inputs_array)
for async_result in async_results:
    print(async_result)

# İpli kickoff_async kullanımı
inputs = {'konu': 'yapay zeka sağlık'}
async_result = await my_crew.kickoff_async(inputs=inputs)
print(async_result)

# İpli kickoff_for_each_async kullanımı
inputs_array = [{'konu': 'yapay zeka sağlık'}, {'konu': 'yapay zeka finans'}]
async_results = await my_crew.kickoff_for_each_async(inputs=inputs_array)
for async_result in async_results:
    print(async_result)
```

Bu yöntemler, ekip içinde görevleri yönetme ve yürütme şeklinizde esneklik sağladığından hem senkronize hem de asenkron iş akışlarına uyum sağlamanıza olanak tanır. Ayrıntılı asenkron örnekler için [Asenkron Olarak Ekip Başlatma](/en/learn/kickoff-async) kılavuzuna bakın.

### Akışı Etkinleştirme Ekip Yürütme

Ekip yürütmesi hakkında gerçek zamanlı görünürlük için, çıktının üretildiği gibi alınması için akışı etkinleştirebilirsiniz:

```python Code
# Akışı etkinleştirme
crew = Crew(
    agents=[researcher],
    tasks=[task],
    stream=True
)

# Akış çıktısı üzerinde yineleyin
streaming = crew.kickoff(inputs={"konu": "yapay zeka"})
for chunk in streaming:
    print(chunk.content, end="", flush=True)

# Sonucu alın
result = streaming.result
```

Akış hakkında daha fazla bilgi için [Akış Ekip Yürütme](/en/learn/streaming-crew-execution) kılavuzuna bakın.

### Belirli Bir Görevden Başlatma

Şimdi görevi `replay` komut satırı aracı kullanılarak yeniden başlatabilirsiniz.

CrewAI'daki yeniden başlatma özelliği, komut satırı arayüzü (CLI) aracılığıyla belirli bir görevden yeniden başlatmanıza olanak tanır. `crewai replay -t <görev_id>` komutunu çalıştırarak yeniden başlatma işlemi için `<görev_id>`'yi belirtebilirsiniz.

Yeniden başlatma özelliği, daha önce yürütülen görevlerden bağlamı korurken en son kickoff görevlerinizden yeniden başlatmanıza olanak tanır.

### CLI'den Belirli Bir Görevden Başlatma

Yeniden başlatma özelliğini kullanmak için aşağıdaki adımları izleyin:

1. Terminalinizi veya komut isteminizi açın.
2. CrewAI projenizin bulunduğu dizine gidin.
3. Aşağıdaki komutu çalıştırın:

En son kickoff görev kimliklerini görüntülemek için:

```shell
crewai log-tasks-outputs
```

Ardından, belirli bir görevden yeniden başlatmak için:

```shell
crewai replay -t <görev_id>
```

Bu komutlar, en son kickoff görevlerinizden yeniden başlatmanıza ve bağlamı korumanıza olanak tanır.