> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Dizin RAG Arama

> `DirectorySearchTool`, bir dizinin içeriğinde anlamsal aramalar yapmak için tasarlanmış güçlü bir RAG (Retrieval-Augmented Generation) aracıdır.

# `DirectorySearchTool`

<Note>
  **Deneysel**: DirectorySearchTool sürekli geliştirme altındadır. Özellikler ve işlevler zamanla değişebilir; aracı iyileştirirken beklenmeyen davranışlar görülebilir.
</Note>

## Açıklama

DirectorySearchTool, dosyalar arasında verimli gezinme için Retrieval-Augmented Generation (RAG) yönteminden yararlanarak belirtilen dizinlerin içeriğinde anlamsal arama yapmayı sağlar. Esnek olacak şekilde tasarlanmıştır; kullanıcıların çalışma anında arama dizinlerini dinamik olarak belirtmesine veya ilk kurulum sırasında sabit bir dizin tanımlamasına izin verir.

## Kurulum

DirectorySearchTool'u kullanmak için önce crewai\_tools paketini kurun. Terminalinizde aşağıdaki komutu çalıştırın:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Başlatma ve Kullanım

Başlamak için DirectorySearchTool'u `crewai_tools` paketinden içe aktarın. Aracı bir dizin belirtmeden başlatabilir ve böylece arama dizinini çalışma anında ayarlayabilirsiniz. Alternatif olarak araç önceden tanımlı bir dizinle de başlatılabilir.

```python Code theme={null}
from crewai_tools import DirectorySearchTool

# Çalışma anında dinamik dizin belirtimi için
tool = DirectorySearchTool()

# Sabit dizin aramaları için
tool = DirectorySearchTool(directory='/path/to/directory')
```

## Argümanlar

* `directory`: Arama dizinini belirten string türünde bir argüman. Başlatma sırasında isteğe bağlıdır, ancak başlangıçta ayarlanmadıysa arama sırasında gereklidir.

## Özel Model ve Embedding'ler

DirectorySearchTool varsayılan olarak embedding ve özetleme için OpenAI kullanır. Bu ayarları özelleştirmek için model sağlayıcısını ve yapılandırmayı değiştirebilir, böylece ileri düzey kullanıcılar için daha fazla esneklik sağlayabilirsiniz.

```python Code theme={null}
from chromadb.config import Settings

tool = DirectorySearchTool(
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
