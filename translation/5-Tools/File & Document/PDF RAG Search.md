> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# PDF RAG Arama

> `PDFSearchTool`, PDF dosyalarında arama yapmak ve en ilgili sonuçları döndürmek için tasarlanmıştır.

# `PDFSearchTool`

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

PDFSearchTool, PDF içeriğinde anlamsal arama yapmak için tasarlanmış bir RAG aracıdır. Bir arama sorgusu ve bir PDF belgesi alarak ilgili içeriği verimli biçimde bulmak için gelişmiş arama tekniklerinden yararlanır.
Bu yetenek, büyük PDF dosyalarından belirli bilgileri hızlıca çıkarmak için onu özellikle kullanışlı hale getirir.

## Kurulum

PDFSearchTool'u kullanmaya başlamak için önce crewai\_tools paketinin aşağıdaki komutla kurulu olduğundan emin olun:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

PDFSearchTool'u bir PDF belgesi içinde arama yapmak için şu şekilde kullanabilirsiniz:

```python Code theme={null}
from crewai_tools import PDFSearchTool

# Yol çalışma sırasında verilirse herhangi bir PDF içeriğinde aramaya izin verecek şekilde aracı başlat
tool = PDFSearchTool()

# OR

# Aracı belirli bir PDF yoluyla başlat; böylece arama yalnızca o belge içinde yapılsın
tool = PDFSearchTool(pdf='path/to/your/document.pdf')
```

## Argümanlar

* `pdf`: **İsteğe bağlı** Arama için PDF yolu. Başlatma sırasında veya `run` metodunun argümanları içinde verilebilir. Başlatma sırasında verilirse araç aramayı belirtilen belgeyle sınırlar.

## Özel model ve embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz. Not: Üretilen embedding'lerin bir vectordb içinde saklanması ve sorgulanması gerektiğinden bir vektör veritabanı zorunludur.

```python Code theme={null}
from crewai_tools import PDFSearchTool

# - embedding_model (gerekli): sağlayıcıyı ve sağlayıcıya özgü yapılandırmayı seçin
# - vectordb (gerekli): vektör veritabanını seçin ve yapılandırmasını iletin

tool = PDFSearchTool(
    config={
        "embedding_model": {
            # Desteklenen sağlayıcılar: "openai", "azure", "google-generativeai", "google-vertex",
            # "voyageai", "cohere", "huggingface", "jina", "sentence-transformer",
            # "text2vec", "ollama", "openclip", "instructor", "onnx", "roboflow", "watsonx", "custom"
            "provider": "openai",  # veya: "google-generativeai", "cohere", "ollama", ...
            "config": {
                # Seçilen sağlayıcı için model tanımlayıcısı. "model", içeride otomatik olarak "model_name" alanına eşlenir.
                "model": "text-embedding-3-small",
                # İsteğe bağlı: API anahtarı. Verilmezse araç sağlayıcıya özgü ortam değişkenlerini kullanır
                # (ör. OpenAI için OPENAI_API_KEY veya EMBEDDINGS_OPENAI_API_KEY).
                # "api_key": "sk-...",

                # Sağlayıcıya özgü örnekler:
                # --- Google Generative AI ---
                # (Yukarıda provider="google-generativeai" olarak ayarlayın)
                # "model_name": "gemini-embedding-001",
                # "task_type": "RETRIEVAL_DOCUMENT",
                # "title": "Embeddings",

                # --- Cohere ---
                # (Yukarıda provider="cohere" olarak ayarlayın)
                # "model": "embed-english-v3.0",

                # --- Ollama (yerel) ---
                # (Yukarıda provider="ollama" olarak ayarlayın)
                # "model": "nomic-embed-text",
            },
        },
        "vectordb": {
                    "provider": "chromadb",  # or "qdrant"
                    "config": {
                        # ChromaDB için: "settings" (chromadb.config.Settings) geçin veya varsayılanlara güvenin.
                        # Örnek (yorumu kaldırın ve içe aktarın):
                        # from chromadb.config import Settings
                        # "settings": Settings(
                        #     persist_directory="/content/chroma",
                        #     allow_reset=True,
                        #     is_persistent=True,
                        # ),

                        # Qdrant için: "vectors_config" (qdrant_client.models.VectorParams) geçin.
                        # Örnek (yorumu kaldırın ve içe aktarın):
                        # from qdrant_client.models import VectorParams, Distance
                        # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),

                        # Not: koleksiyon adı burada değil, araç tarafından kontrol edilir (varsayılan: "rag_tool_collection").
                    }
        },
    }
)
```
