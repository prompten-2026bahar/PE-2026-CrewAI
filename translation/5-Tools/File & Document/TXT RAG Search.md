> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# TXT RAG Arama

> `TXTSearchTool`, bir metin dosyasının içeriğinde RAG (Retrieval-Augmented Generation) araması yapmak için tasarlanmıştır.

## Genel Bakış

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

Bu araç, bir metin dosyasının içeriğinde RAG (Retrieval-Augmented Generation) araması yapmak için kullanılır.
Belirtilen bir metin dosyasının içeriğinde sorguların anlamsal olarak aranmasını sağlar
ve verilen sorguya göre bilgiyi hızlıca çıkarmak veya metnin belirli bölümlerini bulmak için çok değerli bir kaynak haline gelir.

## Kurulum

`TXTSearchTool` kullanmak için önce `crewai_tools` paketini kurmanız gerekir.
Bu işlem Python paket yöneticisi olan pip ile yapılabilir.
Terminalinizi veya komut istemcinizi açıp aşağıdaki komutu girin:

```shell  theme={null}
pip install 'crewai[tools]'
```

Bu komut, gerekli bağımlılıklarla birlikte TXTSearchTool'u indirip kuracaktır.

## Örnek

Aşağıdaki örnek, TXTSearchTool'un bir metin dosyasında arama yapmak için nasıl kullanılacağını gösterir.
Bu örnek, hem aracı belirli bir metin dosyasıyla başlatmayı hem de ardından bu dosyanın içeriğinde arama yapmayı gösterir.

```python Code theme={null}
from crewai_tools import TXTSearchTool

# Aracı, ajan çalışması sırasında öğrendiği
# herhangi bir metin dosyasının içeriğinde arama yapabilecek şekilde başlat
tool = TXTSearchTool()

# OR

# Aracı belirli bir metin dosyasıyla başlat;
# böylece ajan verilen metin dosyasının içeriğinde arama yapabilsin
tool = TXTSearchTool(txt='path/to/text/file.txt')
```

## Argümanlar

* `txt` (str): **İsteğe bağlı**. Aramak istediğiniz metin dosyasının yolu.
  Bu argüman yalnızca araç belirli bir metin dosyasıyla başlatılmadıysa gereklidir;
  aksi halde arama başlangıçta verilen metin dosyası içinde yapılacaktır.

## Özel model ve embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır.
Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code theme={null}
from chromadb.config import Settings

tool = TXTSearchTool(
    config={
        # Gerekli: embedding sağlayıcısı + yapılandırma
        "embedding_model": {
            "provider": "openai",  # veya google-generativeai, cohere, ollama, ...
            "config": {
                "model": "text-embedding-3-small",
                # "api_key": "sk-...",  # ortam değişkeni ayarlıysa isteğe bağlıdır (ör. OPENAI_API_KEY veya EMBEDDINGS_OPENAI_API_KEY)
                # Sağlayıcı örnekleri:
                # Google → model_name: "gemini-embedding-001", task_type: "RETRIEVAL_DOCUMENT"
                # Cohere → model: "embed-english-v3.0"
                # Ollama → model: "nomic-embed-text"
            },
        },

        # Gerekli: vektör veritabanı yapılandırması
        "vectordb": {
            "provider": "chromadb",  # or "qdrant"
            "config": {
                # Chroma ayarları (isteğe bağlı kalıcılık)
                # "settings": Settings(
                #     persist_directory="/content/chroma",
                #     allow_reset=True,
                #     is_persistent=True,
                # ),

                # Qdrant vektör parametresi örneği:
                # from qdrant_client.models import VectorParams, Distance
                # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),

                # Not: koleksiyon adı araç tarafından kontrol edilir (varsayılan: "rag_tool_collection").
            }
        },
    }
)
```
