# crew.py Dosyasında Notasyonların (Annotations) Kullanımı

> CrewAI'da temsilcileri (agents), görevleri (tasks) ve bileşenleri düzgün bir şekilde yapılandırmak için notasyonları nasıl kullanacağınızı öğrenin.

Bu kılavuz, `crew.py` dosyasındaki **temsilcilere**, **görevlere** ve diğer bileşenlere düzgün şekilde atıfta bulunmak için notasyonların nasıl kullanılacağını açıklamaktadır.

## Giriş

CrewAI çerçevesindeki notasyonlar, sınıfları ve yöntemleri süslemek (decorate) için kullanılır; ekibinizin çeşitli bileşenlerine meta veriler ve işlevler sağlar. Bu notasyonlar, kodunuzu organize etmeye ve yapılandırmaya yardımcı olarak daha okunabilir ve bakımı kolay hale getirir.

## Mevcut Notasyonlar

CrewAI çerçevesi aşağıdaki notasyonları sağlar:

* `@CrewBase`: Ana ekip (crew) sınıfını süslemek için kullanılır.
* `@agent`: Agent nesnelerini tanımlayan ve döndüren yöntemleri süsler.
* `@task`: Task nesnelerini tanımlayan ve döndüren yöntemleri süsler.
* `@crew`: Crew nesnesini oluşturan ve döndüren yöntemi süsler.
* `@llm`: Dil Modeli (Language Model) nesnelerini başlatan ve döndüren yöntemleri süsler.
* `@tool`: Araç (Tool) nesnelerini başlatan ve döndüren yöntemleri süsler.
* `@callback`: Geri çağırma (callback) yöntemlerini tanımlamak için kullanılır.
* `@output_json`: JSON verisi çıktılayan yöntemler için kullanılır.
* `@output_pydantic`: Pydantic modelleri çıktılayan yöntemler için kullanılır.
* `@cache_handler`: Önbellek işleme yöntemlerini tanımlamak için kullanılır.

## Kullanım Örnekleri

Bu notasyonların nasıl kullanılacağına dair örneklere göz atalım:

### 1. Crew Temel Sınıfı

```python
@CrewBase
class LinkedinProfileCrew():
    """LinkedinProfile ekibi"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
```

`@CrewBase` notasyonu ana ekip sınıfını süslemek için kullanılır. Bu sınıf tipik olarak temsilciler, görevler ve ekibin kendisini oluşturmak için yapılandırmaları ve yöntemleri içerir.

> [!TIP]
> `@CrewBase` sadece sınıfı kaydetmekten fazlasını yapar:
>
> * **Yapılandırma önyüklemesi (Configuration bootstrapping):** Sınıf dosyasının yanında `agents_config` ve `tasks_config` (varsayılan olarak `config/agents.yaml` ve `config/tasks.yaml`) dosyalarını arar, bunları örnekleme sırasında yükler ve dosyalar eksikse güvenli bir şekilde boş sözlüklere (dicts) döner.
> * **Dekoratör orkestrasyonu (Decorator orchestration):** `@agent`, `@task`, `@before_kickoff` veya `@after_kickoff` ile işaretlenmiş her yöntemin hafızaya alınmış (memoized) referanslarını tutar, böylece ekip başına bir kez örneklenir ve bildirim sırasına göre yürütülür.
> * **Hook bağlantısı (Hook wiring):** Korunan kickoff hook'larını otomatik olarak `@crew` yöntemi tarafından döndürülen `Crew` nesnesine ekler, böylece bunların `.kickoff()` öncesinde ve sonrasında çalışmasını sağlar.
> * **MCP entegrasyonu:** Sınıf `mcp_server_params` tanımladığında, `get_mcp_tools()` yavaşça (lazily) bir MCP sunucu adaptörü başlatır, bildirilen araçları doldurur ve dahili bir after-kickoff hook'u adaptörü durdurur. Adaptör yapılandırma ayrıntıları için [MCP genel bakış](/en/mcp/overview) sayfasına bakın.

### 2. Araç Tanımlama

```python
@tool
def myLinkedInProfileTool(self):
    return LinkedInProfileTool()
```

`@tool` notasyonu araç nesneleri döndüren yöntemleri süslemek için kullanılır. Bu araçlar, temsilciler tarafından belirli görevleri gerçekleştirmek için kullanılabilir.

### 3. LLM Tanımlama

```python
@llm
def groq_llm(self):
    api_key = os.getenv('api_key')
    return ChatGroq(api_key=api_key, temperature=0, model_name="mixtral-8x7b-32768")
```

`@llm` notasyonu Dil Modeli nesnelerini başlatan ve döndüren yöntemleri süslemek için kullanılır. Bu LLM'ler, temsilciler tarafından doğal dil işleme görevleri için kullanılır.

### 4. Temsilci Tanımlama

```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher']
    )
```

`@agent` notasyonu Agent nesnelerini tanımlayan ve döndüren yöntemleri süslemek için kullanılır.

### 5. Görev Tanımlama

```python
@task
def research_task(self) -> Task:
    return Task(
        config=self.tasks_config['research_linkedin_task'],
        agent=self.researcher()
    )
```

`@task` notasyonu Task nesnelerini tanımlayan ve döndüren yöntemleri süslemek için kullanılır. Bu yöntemler görev yapılandırmasını ve görevden sorumlu temsilciyi belirtir.

### 6. Ekip Oluşturma

```python
@crew
def crew(self) -> Crew:
    """LinkedinProfile ekibini oluşturur"""
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True
    )
```

`@crew` notasyonu `Crew` nesnesini oluşturan ve döndüren yöntemi süslemek için kullanılır. Bu yöntem tüm bileşenleri (temsilciler ve görevler) işlevsel bir ekipte birleştirir.

## YAML Yapılandırması

Temsilci yapılandırmaları genellikle bir YAML dosyasında saklanır. İşte araştırmacı temsilci için `agents.yaml` dosyasının nasıl görünebileceğine dair bir örnek:

```yaml
researcher:
    role: >
        LinkedIn Profili Kıdemli Veri Araştırmacısı
    goal: >
        Sağlanan ad {name} ve alan adına {domain} dayalı olarak ayrıntılı LinkedIn profillerini ortaya çıkarın
        Alan adına {domain} dayalı bir Dall-E resmi oluşturun
    backstory: >
        En ilgili LinkedIn profillerini ortaya çıkarma becerisine sahip deneyimli bir araştırmacısınız.
        LinkedIn'de verimli bir şekilde gezinme yeteneğinizle tanınırsınız; profesyonel bilgileri 
        açık ve öz bir şekilde toplama ve sunma konusunda mükemmelsiniz.
    allow_delegation: False
    verbose: True
    llm: groq_llm
    tools:
        - myLinkedInProfileTool
        - mySerperDevTool
        - myDallETool
```

Bu YAML yapılandırması, `LinkedinProfileCrew` sınıfında tanımlanan araştırmacı temsilciye karşılık gelir. Yapılandırma, temsilcinin rolünü, hedefini, geçmişini ve kullandığı LLM ve araçlar gibi diğer özellikleri belirtir.

YAML dosyasındaki `llm` ve `tools` kısımlarının, Python sınıfındaki `@llm` ve `@tool` ile süslenmiş yöntemlere nasıl karşılık geldiğine dikkat edin.

## En İyi Uygulamalar

* **Tutarlı İsimlendirme**: Yöntemleriniz için net ve tutarlı isimlendirme kuralları kullanın. Örneğin, temsilci yöntemleri rollerine göre adlandırılabilir (örn. researcher, reporting\_analyst).
* **Ortam Değişkenleri**: API anahtarları gibi hassas bilgiler için ortam değişkenlerini kullanın.
* **Esneklik**: Temsilci ve görevlerin kolayca eklenmesine veya çıkarılmasına izin vererek ekibinizi esnek olacak şekilde tasarlayın.
* **YAML-Kod Uyumu**: YAML dosyalarınızdaki adların ve yapıların Python kodunuzdaki süslenmiş yöntemlerle doğru şekilde eşleştiğinden emin olun.

Bu yönergeleri izleyerek ve notasyonları düzgün bir şekilde kullanarak CrewAI çerçevesini kullanarak iyi yapılandırılmış ve bakımı kolay ekipler oluşturabilirsiniz.
