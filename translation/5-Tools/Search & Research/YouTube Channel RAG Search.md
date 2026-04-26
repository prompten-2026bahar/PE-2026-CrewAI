> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# YouTube Kanalı RAG Arama

> `YoutubeChannelSearchTool`, bir YouTube kanalının içeriğinde RAG (Retrieval-Augmented Generation) araması yapmak için tasarlanmıştır.

# `YoutubeChannelSearchTool`

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

Bu araç, belirli bir YouTube kanalının içeriğinde anlamsal aramalar yapmak için tasarlanmıştır.
RAG (Retrieval-Augmented Generation) metodolojisinden yararlanarak ilgili arama sonuçları sağlar;
böylece videoları tek tek incelemeye gerek kalmadan bilgi çıkarmak veya belirli içerikleri bulmak için son derece değerli hale gelir.
YouTube kanalları içindeki arama sürecini kolaylaştırır; araştırmacılar, içerik üreticileri ve belirli bilgi veya konular arayan izleyicilere hitap eder.

## Kurulum

YoutubeChannelSearchTool'u kullanmak için `crewai_tools` paketinin kurulmuş olması gerekir. Kurmak için shell içinde aşağıdaki komutu çalıştırın:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

Aşağıdaki örnek, `YoutubeChannelSearchTool` aracının bir CrewAI ajanı ile nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import YoutubeChannelSearchTool

# Aracı genel YouTube kanal aramaları için başlat
youtube_channel_tool = YoutubeChannelSearchTool()

# Aracı kullanan bir ajan tanımla
channel_researcher = Agent(
    role="Kanal Araştırmacısı",
    goal="YouTube kanallarından ilgili bilgileri çıkar",
    backstory="YouTube kanal içeriklerini analiz etme konusunda uzman bir araştırmacı.",
    tools=[youtube_channel_tool],
    verbose=True,
)

# Belirli bir kanalda bilgi aramak için örnek görev
research_task = Task(
    description="{youtube_channel_handle} YouTube kanalında makine öğrenimi eğitimleri hakkında bilgi ara",
    expected_output="Kanalda bulunan temel makine öğrenimi eğitimlerinin özeti.",
    agent=channel_researcher,
)

# Ekibi oluştur ve çalıştır
crew = Crew(agents=[channel_researcher], tasks=[research_task])
result = crew.kickoff(inputs={"youtube_channel_handle": "@exampleChannel"})
```

Aracı belirli bir YouTube kanal handle’ı ile de başlatabilirsiniz:

```python Code theme={null}
# Aracı belirli bir YouTube kanal handle’ı ile başlat
youtube_channel_tool = YoutubeChannelSearchTool(
    youtube_channel_handle='@exampleChannel'
)

# Aracı kullanan bir ajan tanımla
channel_researcher = Agent(
    role="Kanal Araştırmacısı",
    goal="Belirli bir YouTube kanalından ilgili bilgileri çıkar",
    backstory="YouTube kanal içeriklerini analiz etme konusunda uzman bir araştırmacı.",
    tools=[youtube_channel_tool],
    verbose=True,
)
```

## Parametreler

`YoutubeChannelSearchTool` şu parametreleri kabul eder:

* **youtube\_channel\_handle**: İsteğe bağlı. İçinde arama yapılacak YouTube kanalının handle değeri. Başlatma sırasında verilirse ajan aracı kullanırken bunu ayrıca belirtmek zorunda kalmaz. Handle `@` ile başlamıyorsa otomatik olarak eklenir.
* **config**: İsteğe bağlı. Altta yatan RAG sistemi için yapılandırma; buna LLM ve embedder ayarları dahildir.
* **summarize**: İsteğe bağlı. Getirilen içeriğin özetlenip özetlenmeyeceği. Varsayılan `False`.

Araç bir ajan ile kullanıldığında, ajanın şunları sağlaması gerekir:

* **search\_query**: Gerekli. Kanal içeriğinde ilgili bilgiyi bulmak için kullanılacak arama sorgusu.
* **youtube\_channel\_handle**: Yalnızca başlatma sırasında verilmediyse gereklidir. İçinde arama yapılacak YouTube kanalının handle değeri.

## Özel Model ve Embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code   theme={null}
youtube_channel_tool = YoutubeChannelSearchTool(
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

İşte `YoutubeChannelSearchTool` aracını bir CrewAI ajanı ile entegre etmeye dair daha ayrıntılı bir örnek:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import YoutubeChannelSearchTool

# Aracı başlat
youtube_channel_tool = YoutubeChannelSearchTool()

# Aracı kullanan bir ajan tanımla
channel_researcher = Agent(
    role="Kanal Araştırmacısı",
    goal="YouTube kanallarından bilgi çıkar ve analiz et",
    backstory="""You are an expert channel researcher who specializes in extracting 
    and analyzing information from YouTube channels. You have a keen eye for detail 
    and can quickly identify key points and insights from video content across an entire channel.""",
    tools=[youtube_channel_tool],
    verbose=True,
)

# Ajan için bir görev oluştur
research_task = Task(
    description="""
    {youtube_channel_handle} YouTube kanalında
    veri bilimi projeleri ve eğitimleri hakkında bilgi ara. 
    
    Şunlara odaklan:
    1. Ele alınan temel veri bilimi teknikleri
    2. Popüler eğitim serileri
    3. En çok izlenen veya önerilen videolar
    
    Bu noktaların kapsamlı bir özetini sun.
    """,
    expected_output="Kanalda bulunan veri bilimi içeriklerine dair ayrıntılı özet.",
    agent=channel_researcher,
)

# Görevi çalıştır
crew = Crew(agents=[channel_researcher], tasks=[research_task])
result = crew.kickoff(inputs={"youtube_channel_handle": "@exampleDataScienceChannel"})
```

## Uygulama Ayrıntıları

`YoutubeChannelSearchTool`, Retrieval-Augmented Generation için temel işlevselliği sağlayan `RagTool` alt sınıfı olarak uygulanmıştır:

```python Code theme={null}
class YoutubeChannelSearchTool(RagTool):
    name: str = "Search a Youtube Channels content"
    description: str = "A tool that can be used to semantic search a query from a Youtube Channels content."
    args_schema: Type[BaseModel] = YoutubeChannelSearchToolSchema

    def __init__(self, youtube_channel_handle: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if youtube_channel_handle is not None:
            kwargs["data_type"] = DataType.YOUTUBE_CHANNEL
            self.add(youtube_channel_handle)
            self.description = f"A tool that can be used to semantic search a query the {youtube_channel_handle} Youtube Channels content."
            self.args_schema = FixedYoutubeChannelSearchToolSchema
            self._generate_description()

    def add(
        self,
        youtube_channel_handle: str,
        **kwargs: Any,
    ) -> None:
        if not youtube_channel_handle.startswith("@"):
            youtube_channel_handle = f"@{youtube_channel_handle}"
        super().add(youtube_channel_handle, **kwargs)
```

## Sonuç

`YoutubeChannelSearchTool`, RAG tekniklerini kullanarak YouTube kanal içeriği içinde arama yapmak ve bilgi çıkarmak için güçlü bir yol sunar. Ajanların bir kanalın tüm videoları boyunca arama yapmasını sağlayarak, aksi halde gerçekleştirilmesi zor olacak bilgi çıkarımı ve analiz görevlerini kolaylaştırır. Bu araç özellikle araştırma, içerik analizi ve YouTube kanallarından bilgi çıkarımı için kullanışlıdır.
