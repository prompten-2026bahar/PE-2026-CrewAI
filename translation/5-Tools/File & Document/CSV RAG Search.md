> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# CSV RAG Arama

> `CSVSearchTool`, bir CSV dosyasının içeriğinde anlamsal aramalar yapmak için tasarlanmış güçlü bir RAG (Retrieval-Augmented Generation) aracıdır.

# `CSVSearchTool`

<Note>
  **Deneysel**: Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

Bu araç, bir CSV dosyasının içeriğinde RAG (Retrieval-Augmented Generation) araması yapmak için kullanılır. Kullanıcıların, belirtilen bir CSV dosyasının içeriğinde sorguları anlamsal olarak aramasını sağlar.
Bu özellik, geleneksel arama yöntemlerinin yetersiz kalabildiği büyük CSV veri kümelerinden bilgi çıkarmak için özellikle kullanışlıdır. CSVSearchTool dahil, adında "Search" geçen tüm araçlar,
farklı veri kaynaklarında arama yapmak üzere tasarlanmış RAG araçlarıdır.

## Kurulum

crewai\_tools paketini kurun

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

```python Code theme={null}
from crewai_tools import CSVSearchTool

# Aracı belirli bir CSV dosyasıyla başlat.
# Bu kurulum, ajanın yalnızca verilen CSV dosyasında arama yapmasına izin verir.
tool = CSVSearchTool(csv='path/to/your/csvfile.csv')

# OR

# Aracı belirli bir CSV dosyası olmadan başlat.
# Ajanın çalışma anında CSV yolunu sağlaması gerekir.
tool = CSVSearchTool()
```

## Argümanlar

`CSVSearchTool` davranışını özelleştirmek için aşağıdaki parametreler kullanılabilir:

| Argument | Type     | Description                                                                                                                                                               |
| :------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **csv**  | `string` | *İsteğe bağlı*. Aramak istediğiniz CSV dosyasının yolu. Araç belirli bir CSV dosyası olmadan başlatıldıysa bu zorunludur; aksi halde isteğe bağlıdır. |

## Özel model ve embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code theme={null}
from chromadb.config import Settings

tool = CSVSearchTool(
    config={
        "embedding_model": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
                # "api_key": "sk-...",
            },
        },
        "vectordb": {
            "provider": "chromadb",  # or "qdrant"
            "config": {
                # "settings": Settings(persist_directory="/content/chroma", allow_reset=True, is_persistent=True),
                # from qdrant_client.models import VectorParams, Distance
                # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),
            }
        },
    }
)
```
