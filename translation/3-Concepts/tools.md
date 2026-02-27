## Araçlar
Aracılar arasındaki işbirliğini ve görev yürütmeyi kolaylaştıran CrewAI çerçevesinde araçları anlama ve kullanma.

## Genel Bakış

CrewAI araçları, aracılara web araması ve veri analizi ile işbirliği ve çalışanlar arasında görev devretme gibi çeşitli yetenekler sağlayan gücün verilmesini sağlar. Bu belge, işbirliği araçları üzerindeki yeni bir odaklanma da dahil olmak üzere CrewAI çerçevesi içinde bu araçların nasıl oluşturulacağını, entegre edileceğini ve kullanılacağını özetlemektedir.

## Araç Nedir?

CrewAI'de bir araç, aracılar tarafından çeşitli eylemleri gerçekleştirmek için kullanılabilecek bir beceri veya fonksiyondur. Bu, [CrewAI Araç Seti](https://github.com/joaomdmoura/crewai-tools) ve [LangChain Araçları](https://python.langchain.com/docs/integrations/tools) gibi araçları içerir; basit aramadan karmaşık etkileşimlere ve aracılar arasındaki etkili takım çalışmasına olanak tanır.

CrewAI AMP, genel iş sistemleri ve API'ler için önceden oluşturulmuş entegrasyonlarla kapsamlı bir Araçlar Deposu sağlar. Aracılar için kuruluşu günlerce değil dakikalar içinde gerçekleştirin.

Kurumsal Araçlar Deposu şunları içerir:

- Popüler kurumsal sistemler için önceden oluşturulmuş bağlayıcılar
- Özel araç oluşturma arayüzü
- Sürüm kontrolü ve paylaşım yetenekleri
- Güvenlik ve uyumluluk özellikleri

## Araçların Temel Özellikleri

- **Kullanılabilirlik**: Web araması, veri analizi, içerik oluşturma ve aracı işbirliği gibi görevler için tasarlanmıştır.
- **Entegrasyon**: Aracılarının iş akışına sorunsuz bir şekilde entegre edilerek yeteneklerini artırır.
- **Özelleştirilebilirlik**: Aracılara özel ihtiyaçlara göre uyarlanabilmeleri için özel araçlar geliştirmeyi veya mevcut olanları kullanmayı sağlar.
- **Hata Yönetimi**: Sorunsuz çalışma sağlamak için sağlam hata yönetimi mekanizmaları içerir.
- **Önbellekleme Mekanizması**: Performansı optimize etmek ve gereksiz işlemleri azaltmak için akıllı bir önbellekleme özelliği sunar.
- **Asenkron Destek**: Engelleme dışı işlemler sağlamak için hem senkron hem de asenkron araçları işler.

## CrewAI Araçlarını Kullanma

Aracılarının yeteneklerini geliştirmek için CrewAI araçlarını kullanmak için, paket ek araçlarınızı kurmaya başlayın:

```bash
pip install 'crewai[tools]'
```

Kullanımlarını gösteren bir örnek:

```python
from crewai import Agent, Task, Crew
# crewAI araçlarını içe aktarma
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

# API anahtarlarını ayarlayın
os.environ["SERPER_API_KEY"] = "Anahtarınız" # serper.dev API anahtarı
os.environ["OPENAI_API_KEY"] = "Anahtarınız"

# Araçları örnekleme
docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

# Aracılar oluşturma
researcher = Agent(
    role='Pazar Araştırması Uzmanı',
    goal='AI sektörü hakkında güncel pazar analizleri sağlama',
    backstory='Pazar trendlerine dair keskin bir gözü olan bir uzman analist.',
    tools=[search_tool, web_rag_tool],
    verbose=True
)

writer = Agent(
    role='İçerik Yazarı',
    goal='AI sektörü hakkında ilgi çekici blog yazıları oluşturma',
    backstory='Teknolojiye tutkuyla bağlı, yetenekli bir yazar.',
    tools=[docs_tool, file_tool],
    verbose=True
)

# Görevleri tanımlayın
research = Task(
    description='AI sektöründeki son trendleri araştırın ve bir özet sağlayın.',
    expected_output='AI sektöründeki en iyi 3 gelişimin özeti, bunların önemine dair benzersiz bir bakış açısıyla.',
    agent=researcher
)

write = Task(
    description='Araştırma analistinin özetine dayanarak AI sektörü hakkında ilgi çekici bir blog yazısı yazın. Klasördeki en son blog yazılarını örnek alın.',
    expected_output='Etkileyici, bilgilendirici ve erişilebilir içerikle biçimlendirilmiş 4 paragraflık bir blog yazısı, karmaşık jargonlardan kaçınarak Markdown formatında.',
    agent=writer,
    output_file='blog-posts/new_post.md'  # Blog yazısı burada kaydedilecektir
)

# Planlama etkinleştirilmiş bir ekip toplayın
crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    verbose=True,
    planning=True  # Planlama özelliğini etkinleştirin
)

# Görevleri yürütün
crew.kickoff()
```

## Mevcut CrewAI Araçları

- **Hata Yönetimi**: Tüm araçlar hata yönetimi yetenekleri ile birlikte oluşturulmuştur, böylece aracılar istisnaları zarifçe yönetebilir ve görevlerine devam edebilir.
- **Önbellekleme Mekanizması**: Tüm araçlar önbellekleme özelliğini destekler, böylece aracılar daha önce elde edilen sonuçları verimli bir şekilde yeniden kullanabilir, harici kaynaklardaki yükü azaltabilir ve yürütme süresini hızlandırabilir. `tool` özelliğindeki `cache_function` özniteliğini kullanarak önbellekleme mekanizması üzerinde daha ince kontrol de tanımlayabilirsiniz.

İşte mevcut araçların ve açıklamalarının bir listesi:

| Araç                             | Açıklama                                                                                    |
| :------------------------------- | :--------------------------------------------------------------------------------------------- |
| **ApifyActorsTool**              | Çalışma akışlarınız için web kazıma ve otomasyon görevleri için Apify Actors'u entegre eden bir araç. |
| **BrowserbaseLoadTool**          | Veri çıkarmak için web tarayıcılarıyla etkileşim kurmak için bir araç.                             |
| **CodeDocsSearchTool**           | Kod belgeleri ve ilgili teknik belgeleri aramak için optimize edilmiş bir RAG aracı. |
| **CodeInterpreterTool**          | Python kodunu yorumlamak için bir araç.                                                           |
| **ComposioTool**                 | Composio araçlarının kullanımını sağlar.                                                                 |
| **CSVSearchTool**                | Yapılandırılmış verileri işlemek için tasarlanmış, CSV dosyaları içinde arama yapmak için bir RAG aracı.        |
| **DALL-E Tool**                  | DALL-E API'sini kullanarak resim oluşturmak için bir araç.                                             |
| **DirectorySearchTool**          | Dosya sistemlerinde gezinmek için kullanışlı olan dizinler içinde arama yapmak için bir RAG aracı.       |
| **DOCXSearchTool**               | Word dosyalarını işlemek için ideal olan DOCX belgeleri içinde arama yapmak için tasarlanmış bir RAG aracı.          |
| **DirectoryReadTool**            | Dizin yapılarını ve içeriklerini okumayı ve işlemesini kolaylaştırır.                 |
| **EXASearchTool**                | Çeşitli veri kaynakları genelinde kapsamlı aramalar yapmak için tasarlanmış bir araç.                |
| **FileReadTool**                 | Çeşitli dosya formatlarını destekleyerek dosyalardan veri okumayı ve çıkarmayı sağlar.               |
| **FirecrawlSearchTool**          | Firecrawl kullanarak sayfaları arayan ve sonuçları döndüren bir araç.                              |
| **FirecrawlCrawlWebsiteTool**    | Firecrawl kullanarak web sayfalarını taramak için bir araç.                                                  |
| **FirecrawlScrapeWebsiteTool**   | Firecrawl kullanarak bir web sayfasının URL'sini kazıyıp içeriğini döndüren bir araç.                   |
| **GithubSearchTool**             | Kod ve dokümantasyon araması için GitHub depolarında arama yapmak için bir RAG aracı. |
| **SerperDevTool**                | Geliştirme amaçlı, geliştirme aşamasında belirli işlevlere sahip bir araç.  |
| **TXTSearchTool**                | Yapılandırılmamış veri için uygun, metin (.txt) dosyaları içinde arama yapmak için odaklanmış bir RAG aracı.      |
| **JSONSearchTool**               | Yapılandırılmış veri işleme için tasarlanmış JSON dosyaları içinde arama yapmak için bir RAG aracı.     |
| **LlamaIndexTool**               | LlamaIndex araçlarının kullanımını sağlar.                                                           |
| **MDXSearchTool**                | Dokümantasyon için uygun Markdown (MDX) dosyaları içinde arama yapmak için tasarlanmış bir RAG aracı.       |
| **PDFSearchTool**                | Taranmış belgeleri işlemek için ideal olan PDF belgeleri içinde arama yapmak için tasarlanmış bir RAG aracı.    |
| **PGSearchTool**                 | Veritabanı sorguları için uygun, PostgreSQL veritabanlarında arama yapmak için optimize edilmiş bir RAG aracı. |
| **Vision Tool**                  | DALL-E API'sini kullanarak resim oluşturmak için bir araç.                                             |
| **RagTool**                      | Çeşitli veri kaynaklarını ve türlerini işleyebilen genel amaçlı bir RAG aracı.                 |
| **ScrapeElementFromWebsiteTool** | Hedefli veri çıkarma için kullanışlı, web sitelerinden belirli öğeleri kazımayı sağlar.         |
| **ScrapeWebsiteTool**            | Kapsamlı veri toplama için ideal, tüm web sitelerini kazımayı kolaylaştırır.                 |
| **WebsiteSearchTool**            | Web verisi çıkarma için optimize edilmiş bir web sitesi içeriği aramak için bir RAG aracı.                   |
| **XMLSearchTool**                | Yapılandırılmış veri formatları için uygun, XML dosyaları içinde arama yapmak için tasarlanmış bir RAG aracı.      |
| **YoutubeChannelSearchTool**     | Video içerik analizi için kullanışlı, YouTube kanalları içinde arama yapmak için bir RAG aracı.           |
| **YoutubeVideoSearchTool**       | Video veri çıkarma için ideal, YouTube videoları içinde arama yapmak için tasarlanmış bir RAG aracı.          |

## Kendi Araçlarınızı Oluşturma

Geliştiriciler, aracının ihtiyaçları için özel araçlar oluşturabilir veya önceden oluşturulmuş seçenekleri kullanabilir.

Araç oluşturmanın iki ana yolu vardır:

### `BaseTool`'u Alt Sınıflandırma

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """Özel Araçım için giriş şeması."""
    argument: str = Field(..., description="Argümanın açıklaması.")

class MyCustomTool(BaseTool):
    name: str = "Özel aracımın adı"
    description: str = "Bu aracın ne işe yaradığını anlatır. Etkili kullanış için önemlidir."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, argument: str) -> str:
        # Aracınızın mantığı burada
        return "Aracımın sonucu"
```

## Asenkron Araç Desteği

CrewAI, asenkron araçları destekler, böylece ağ istekleri, dosya G/Ç'si veya diğer asenkron işlemler gibi engellemeyen işlemleri gerçekleştiren araçları uygulayabilirsiniz.

### Asenkron Araçlar Oluşturma

Asenkron araçları oluşturmanın iki yolu vardır:

#### 1. Asenkron Fonksiyonlarla `tool` Süsleyiciyi Kullanma

```python
from crewai.tools import tool

@tool("fetch_data_async")
async def fetch_data_async(query: str) -> str:
    """Sorguya göre verileri asenkron olarak alın."""
    # Asenkron işlem simüle etme
    await asyncio.sleep(1)
    return f"{query} için veri alındı"
```

#### 2. Özel Araç Sınıflarında Asenkron Yöntemler Uygulama

```python
from crewai.tools import BaseTool

class AsyncCustomTool(BaseTool):
    name: str = "async_custom_tool"
    description: "Asenkron özel bir araç"

    async def _run(self, query: str = "") -> str:
        """Aracı asenkron olarak çalıştırın"""
        # Asenkron uygulamanız burada
        await asyncio.sleep(1)
        return f"{query} asenkron olarak işlendi"
```

### Asenkron Araçları Kullanma

Asenkron araçlar hem standart Ekip iş akışlarında hem de Akış tabanlı iş akışlarında sorunsuz çalışır:

```python
# Standart Ekip'te
agent = Agent(role="araştırmacı", tools=[async_custom_tool])

# Akış'ta
class MyFlow(Flow):
    @start()
    async def begin(self):
        crew = Crew(agents=[agent])
        result = await crew.kickoff_async()
        return result
```

CrewAI çerçevesi hem senkron hem de asenkron araçların yürütülmesini otomatik olarak işler, bu yüzden bunları farklı bir şekilde nasıl çağıracağınızı merak etmenize gerek yoktur.

### `tool` Süsleyiciyi Kullanma

```python
from crewai.tools import tool
@tool("Özel aracımın adı")
def my_tool(question: str) -> str:
    """Bu aracın ne için kullanışlı olduğunu anlatan açık bir açıklama, aracınızın bunu kullanabilmesi için bu bilgiye ihtiyacı olacaktır."""
    # İşlev mantığı burada
    return "Özel aracınızdan sonuç"
```

### Özel Önbellekleme Mekanizması

Araçlar, önbellekleme davranışını iyileştirmek için isteğe bağlı olarak bir `cache_function` uygulayabilir. Bu fonksiyon, belirli koşullara göre sonuçların ne zaman önbelleğe alınacağını belirler ve önbellekleme mantığı üzerinde hassas kontrol sağlar.

```python
from crewai.tools import tool

@tool
def multiplication_tool(first_number: int, second_number: int) -> str:
    """İki sayıyı çarpmak gerektiğinde faydalıdır."""
    return first_number * second_number

def cache_func(args, result):
    # Bu durumda, sonuç sadece 2'nin katıysa önbelleğe alırız
    cache = result % 2 == 0
    return cache

multiplication_tool.cache_function = cache_func

writer1 = Agent(
        role="Yazar",
        goal="Çocuklar için matematik dersleri yazarsınız.",
        backstory="Uzmansınız, yazmayı seviyorsunuz ama matematikten anlamıyorsunuz.",
        tools=[multiplication_tool],
        allow_delegation=False,
    )
    #...
```

## Sonuç

Araçlar, CrewAI aracılarının yeteneklerini genişletmede çok önemlidir, onlara çok çeşitli görevleri üstlenmelerini ve etkili bir şekilde işbirliği yapmalarını sağlar. CrewAI ile çözümler oluştururken, hem özel hem de mevcut araçları kullanarak aracılarınızı güçlendirin ve AI ekosistemini geliştirin. Aracılarının performansını ve yeteneklerini optimize etmek için hata yönetiminden, önbellekleme mekanizmalarından ve araç argümanlarının esnekliğinden yararlanın.