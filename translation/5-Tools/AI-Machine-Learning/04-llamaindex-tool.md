# LlamaIndex Aracı

> `LlamaIndexTool`, LlamaIndex araçları ve sorgu motorları (query engines) için bir sarmalayıcıdır (wrapper).

# `LlamaIndexTool`

## Açıklama

`LlamaIndexTool`, LlamaIndex araçları ve sorgu motorları çevresinde genel bir sarmalayıcı olarak tasarlanmıştır. Bu araç, LlamaIndex kaynaklarını (RAG/ajan hattı bileşenleri gibi) CrewAI ajanlarına eklenebilecek araçlar olarak kullanmanıza olanak tanır. LlamaIndex'in güçlü veri işleme ve veri alma (retrieval) yeteneklerini CrewAI iş akışlarınıza sorunsuz bir şekilde entegre etmenizi sağlar.

## Kurulum

Bu aracı kullanmak için LlamaIndex'i yüklemeniz gerekir:

```shell  theme={null}
uv add llama-index
```

## Başlangıç Adımları

`LlamaIndexTool`'u etkili bir şekilde kullanmak için şu adımları izleyin:

1. **LlamaIndex'i Kurun**: Yukarıdaki komutu kullanarak LlamaIndex paketini yükleyin.
2. **LlamaIndex'i Yapılandırın**: Bir RAG veya ajan hattı kurmak için [LlamaIndex dökümantasyonunu](https://docs.llamaindex.ai/) takip edin.
3. **Araç veya Sorgu Motoru Oluşturun**: CrewAI ile kullanmak istediğiniz bir LlamaIndex aracı veya sorgu motoru oluşturun.

## Örnek

Aşağıdaki örnekler; aracın, farklı LlamaIndex bileşenlerinden nasıl başlatılacağını gösterir:

### Bir LlamaIndex Aracından

```python Code theme={null}
from crewai_tools import LlamaIndexTool
from crewai import Agent
from llama_index.core.tools import FunctionTool

# Örnek 1: FunctionTool'dan başlatma
def search_data(query: str) -> str:
    """Verilerde bilgi ara."""
    # Uygulamanız buraya gelecek
    return f"Sonuçlar: {query}"

# Bir LlamaIndex FunctionTool oluşturun
og_tool = FunctionTool.from_defaults(
    search_data, 
    name="DataSearchTool",
    description="Verilerde bilgi aramak için kullanılır"
)

# LlamaIndexTool ile sarmalayın
tool = LlamaIndexTool.from_tool(og_tool)

# Aracı kullanan bir ajan tanımlayın
@agent
def researcher(self) -> Agent:
    '''
    Bu ajan, bilgi aramak için LlamaIndexTool'u kullanır.
    '''
    return Agent(
        config=self.agents_config["researcher"],
        tools=[tool]
    )
```

### LlamaHub Araçlarından

```python Code theme={null}
from crewai_tools import LlamaIndexTool
from llama_index.tools.wolfram_alpha import WolframAlphaToolSpec

# LlamaHub Araçlarından başlatma
wolfram_spec = WolframAlphaToolSpec(app_id="your_app_id")
wolfram_tools = wolfram_spec.to_tool_list()
tools = [LlamaIndexTool.from_tool(t) for t in wolfram_tools]
```

### Bir LlamaIndex Sorgu Motorundan

```python Code theme={null}
from crewai_tools import LlamaIndexTool
from llama_index.core import VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader

# Belgeleri yükleyin
documents = SimpleDirectoryReader("./data").load_data()

# Bir dizin (index) oluşturun
index = VectorStoreIndex.from_documents(documents)

# Bir sorgu motoru oluşturun
query_engine = index.as_query_engine()

# Sorgu motorundan bir LlamaIndexTool oluşturun
query_tool = LlamaIndexTool.from_query_engine(
    query_engine,
    name="Şirket Veri Sorgulama Aracı",
    description="Şirket belgelerinde bilgi aramak için bu aracı kullanın"
)
```

## Sınıf Metotları

`LlamaIndexTool`, örnekler oluşturmak için iki ana sınıf metodu sağlar:

### from\_tool

Bir LlamaIndex aracından `LlamaIndexTool` oluşturur.

```python Code theme={null}
@classmethod
def from_tool(cls, tool: Any, **kwargs: Any) -> "LlamaIndexTool":
    # Uygulama detayları
```

### from\_query\_engine

Bir LlamaIndex sorgu motorundan `LlamaIndexTool` oluşturur.

```python Code theme={null}
@classmethod
def from_query_engine(
    cls,
    query_engine: Any,
    name: Optional[str] = None,
    description: Optional[str] = None,
    return_direct: bool = False,
    **kwargs: Any,
) -> "LlamaIndexTool":
    # Uygulama detayları
```

## Parametreler

`from_query_engine` metodu aşağıdaki parametreleri kabul eder:

* **query\_engine**: Zorunlu. Sarmalanacak LlamaIndex sorgu motoru.
* **name**: Opsiyonel. Aracın adı.
* **description**: Opsiyonel. Aracın açıklaması.
* **return\_direct**: Opsiyonel. Yanıtın doğrudan döndürülüp döndürülmeyeceği. Varsayılan: `False`.

## Sonuç

`LlamaIndexTool`, LlamaIndex'in yeteneklerini CrewAI ajanlarına entegre etmenin güçlü bir yolunu sunar. LlamaIndex araçlarını ve sorgu motorlarını sarmalayarak, ajanların karmaşık bilgi kaynaklarıyla çalışma yeteneklerini artıran gelişmiş veri alma ve işleme işlevlerinden yararlanmalarına olanak tanır.
