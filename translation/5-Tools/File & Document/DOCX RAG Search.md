> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# DOCX RAG Arama

> `DOCXSearchTool`, DOCX belgeleri içinde anlamsal arama yapmak için tasarlanmış bir RAG aracıdır.

# `DOCXSearchTool`

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

`DOCXSearchTool`, DOCX belgeleri içinde anlamsal arama yapmak için tasarlanmış bir RAG aracıdır.
Kullanıcıların sorgu tabanlı aramalar kullanarak DOCX dosyalarından ilgili bilgileri etkili biçimde arayıp çıkarmasını sağlar.
Bu araç, veri analizi, bilgi yönetimi ve araştırma görevleri için son derece değerlidir;
büyük belge koleksiyonlarında belirli bilgileri bulma sürecini kolaylaştırır.

## Kurulum

Terminalinizde aşağıdaki komutu çalıştırarak crewai\_tools paketini kurun:

```shell  theme={null}
uv pip install docx2txt 'crewai[tools]'
```

## Örnek

Aşağıdaki örnek, DOCXSearchTool'un herhangi bir DOCX dosyasının içeriğinde arama yapacak şekilde veya belirli bir DOCX dosya yoluyla nasıl başlatılacağını gösterir.

```python Code theme={null}
from crewai_tools import DOCXSearchTool

# Aracı herhangi bir DOCX dosyasının içeriğinde arama yapacak şekilde başlat
tool = DOCXSearchTool()

# OR

# Aracı belirli bir DOCX dosyasıyla başlat;
# böylece ajan yalnızca belirtilen DOCX dosyasının içeriğinde arama yapabilsin
tool = DOCXSearchTool(docx='path/to/your/document.docx')
```

## Argümanlar

`DOCXSearchTool` davranışını özelleştirmek için aşağıdaki parametreler kullanılabilir:

| Argument | Type     | Description                                                                                                                                                                                                        |
| :------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **docx** | `string` | *İsteğe bağlı*. Aramak istediğiniz DOCX dosyasının yolunu belirtir. Başlatma sırasında verilmezse araç, daha sonra arama için herhangi bir DOCX dosyasının içerik yolunun belirtilmesine izin verir. |

## Özel model ve embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code theme={null}
from chromadb.config import Settings

tool = DOCXSearchTool(
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
