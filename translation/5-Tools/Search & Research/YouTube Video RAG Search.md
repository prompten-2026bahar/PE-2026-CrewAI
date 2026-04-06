> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# YouTube Video RAG Arama

> `YoutubeVideoSearchTool`, bir YouTube videosunun içeriğinde RAG (Retrieval-Augmented Generation) araması yapmak için tasarlanmıştır.

# `YoutubeVideoSearchTool`

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

Bu araç, `crewai_tools` paketinin bir parçasıdır ve Retrieval-Augmented Generation (RAG) tekniklerini kullanarak YouTube video içeriği içinde anlamsal arama yapmak için tasarlanmıştır.
Paket içindeki farklı kaynaklar için RAG kullanan birden fazla "Search" aracından biridir.
YoutubeVideoSearchTool, aramalarda esneklik sağlar; kullanıcılar video URL’si belirtmeden herhangi bir YouTube videosu içeriğinde arama yapabilir,
veya URL’yi vererek aramalarını belirli bir YouTube videosuna odaklayabilir.

## Kurulum

`YoutubeVideoSearchTool` aracını kullanmak için önce `crewai_tools` paketini kurmanız gerekir.
Bu paket, veri analizi ve işleme görevlerinizi geliştirmek için tasarlanmış diğer yardımcı araçların yanı sıra `YoutubeVideoSearchTool` aracını da içerir.
Paketi terminalinizde aşağıdaki komutu çalıştırarak kurun:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

Aşağıdaki örnek, `YoutubeVideoSearchTool` aracının bir CrewAI ajanı ile nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import YoutubeVideoSearchTool

# Aracı genel YouTube video aramaları için başlat
youtube_search_tool = YoutubeVideoSearchTool()

# Aracı kullanan bir ajan tanımla
video_researcher = Agent(
    role="Video Araştırmacısı",
    goal="YouTube videolarından ilgili bilgileri çıkar",
    backstory="Video içeriğini analiz etme konusunda uzman bir araştırmacı.",
    tools=[youtube_search_tool],
    verbose=True,
)

# Belirli bir videoda bilgi aramak için örnek görev
research_task = Task(
    description="{youtube_video_url} adresindeki YouTube videosunda makine öğrenimi çatılar hakkında bilgi ara",
    expected_output="Videoda geçen temel makine öğrenimi çatılarının özeti.",
    agent=video_researcher,
)

# Ekibi oluştur ve çalıştır
crew = Crew(agents=[video_researcher], tasks=[research_task])
result = crew.kickoff(inputs={"youtube_video_url": "https://youtube.com/watch?v=example"})
```

Aracı belirli bir YouTube video URL’siyle de başlatabilirsiniz:

```python Code theme={null}
# Aracı belirli bir YouTube video URL’siyle başlat
youtube_search_tool = YoutubeVideoSearchTool(
    youtube_video_url='https://youtube.com/watch?v=example'
)

# Aracı kullanan bir ajan tanımla
video_researcher = Agent(
    role="Video Araştırmacısı",
    goal="Belirli bir YouTube videosundan ilgili bilgileri çıkar",
    backstory="Video içeriğini analiz etme konusunda uzman bir araştırmacı.",
    tools=[youtube_search_tool],
    verbose=True,
)
```

## Parametreler

`YoutubeVideoSearchTool` şu parametreleri kabul eder:

* **youtube\_video\_url**: İsteğe bağlı. İçinde arama yapılacak YouTube videosunun URL’si. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz.
* **config**: İsteğe bağlı. Altta yatan RAG sistemi için yapılandırma; buna LLM ve embedder ayarları dahildir.
* **summarize**: İsteğe bağlı. Getirilen içeriğin özetlenip özetlenmeyeceği. Varsayılan `False`.

Araç bir ajan ile kullanıldığında, ajanın şunları sağlaması gerekir:

* **search\_query**: Gerekli. Video içeriğinde ilgili bilgiyi bulmak için kullanılacak arama sorgusu.
* **youtube\_video\_url**: Yalnızca başlatma sırasında verilmediyse gereklidir. İçinde arama yapılacak YouTube videosunun URL’si.

## Özel Model ve Embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code   theme={null}
youtube_search_tool = YoutubeVideoSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google-generativeai", # or openai, ollama, ...
            config=dict(
                model_name="gemini-embedding-001",
                task_type="RETRIEVAL_DOCUMENT",
                # title="Embeddings",
            ),
        ),
    )
)
```

## Ajan Entegrasyonu Örneği

İşte `YoutubeVideoSearchTool` aracını bir CrewAI ajanı ile entegre etmeye dair daha ayrıntılı bir örnek:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import YoutubeVideoSearchTool

# Aracı başlat
youtube_search_tool = YoutubeVideoSearchTool()

# Aracı kullanan bir ajan tanımla
video_researcher = Agent(
    role="Video Araştırmacısı",
    goal="YouTube videolarından bilgi çıkar ve analiz et",
    backstory="""You are an expert video researcher who specializes in extracting 
    and analyzing information from YouTube videos. You have a keen eye for detail 
    and can quickly identify key points and insights from video content.""",
    tools=[youtube_search_tool],
    verbose=True,
)

# Ajan için bir görev oluştur
research_task = Task(
    description="""
    {youtube_video_url} adresindeki YouTube videosunda
    yapay zekadaki son gelişmeler hakkında bilgi ara. 
    
    Şunlara odaklan:
    1. Bahsedilen temel yapay zeka teknolojileri
    2. Tartışılan gerçek dünya uygulamaları
    3. Konuşmacının yaptığı gelecek öngörüleri
    
    Bu noktaların kapsamlı bir özetini sun.
    """,
    expected_output="Videodaki yapay zeka gelişmeleri, uygulamalar ve gelecek öngörülerine dair ayrıntılı özet.",
    agent=video_researcher,
)

# Görevi çalıştır
crew = Crew(agents=[video_researcher], tasks=[research_task])
result = crew.kickoff(inputs={"youtube_video_url": "https://youtube.com/watch?v=example"})
```

## Uygulama Ayrıntıları

`YoutubeVideoSearchTool`, Retrieval-Augmented Generation için temel işlevselliği sağlayan `RagTool` alt sınıfı olarak uygulanmıştır:

```python Code theme={null}
class YoutubeVideoSearchTool(RagTool):
    name: str = "Search a Youtube Video content"
    description: str = "A tool that can be used to semantic search a query from a Youtube Video content."
    args_schema: Type[BaseModel] = YoutubeVideoSearchToolSchema

    def __init__(self, youtube_video_url: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if youtube_video_url is not None:
            kwargs["data_type"] = DataType.YOUTUBE_VIDEO
            self.add(youtube_video_url)
            self.description = f"A tool that can be used to semantic search a query the {youtube_video_url} Youtube Video content."
            self.args_schema = FixedYoutubeVideoSearchToolSchema
            self._generate_description()
```

## Sonuç

`YoutubeVideoSearchTool`, RAG tekniklerini kullanarak YouTube video içeriği içinde arama yapmak ve bilgi çıkarmak için güçlü bir yol sunar. Ajanların video içeriği içinde arama yapmasını sağlayarak, aksi halde yapılması zor olacak bilgi çıkarımı ve analiz görevlerini kolaylaştırır. Bu araç özellikle araştırma, içerik analizi ve video kaynaklarından bilgi çıkarımı için kullanışlıdır.
