> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# XML RAG Arama

> `XMLSearchTool`, bir XML dosyasının içeriğinde RAG (Retrieval-Augmented Generation) araması yapmak için tasarlanmıştır.

# `XMLSearchTool`

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

XMLSearchTool, XML dosyaları içinde anlamsal aramalar yapmak için geliştirilmiş modern bir RAG aracıdır.
XML içeriğini verimli şekilde ayrıştırıp bilgi çıkarması gereken kullanıcılar için ideal olan bu araç, bir arama sorgusu ve isteğe bağlı bir XML dosya yolu almayı destekler.
Bir XML yolu belirterek kullanıcılar aramalarını o dosyanın içeriğine daha hassas şekilde yöneltebilir ve böylece daha ilgili sonuçlar elde edebilir.

## Kurulum

XMLSearchTool'u kullanmaya başlamak için önce crewai\_tools paketini kurmanız gerekir. Bu, aşağıdaki komutla kolayca yapılabilir:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

Burada XMLSearchTool'un nasıl kullanılacağını gösteren iki örnek bulunmaktadır.
İlk örnek belirli bir XML dosyasında arama yapmayı, ikinci örnek ise önceden bir XML yolu tanımlamadan arama başlatmayı gösterir; böylece arama kapsamı konusunda esneklik sağlar.

```python Code theme={null}
from crewai_tools import XMLSearchTool

# Ajanların çalışma sırasında yollarını öğrendikleri
# herhangi bir XML dosyasının içeriğinde arama yapmasına izin ver
tool = XMLSearchTool()

# OR

# Aracı belirli bir XML dosya yoluyla başlat;
# böylece arama yalnızca o belge içinde yapılsın
tool = XMLSearchTool(xml='path/to/your/xmlfile.xml')
```

## Argümanlar

* `xml`: Aramak istediğiniz XML dosyasının yoludur.
  Aracın başlatılması sırasında isteğe bağlı bir parametredir; ancak arama yapmak için ya başlatma sırasında ya da `run` metodunun argümanları içinde verilmelidir.

## Özel model ve embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code   theme={null}
from chromadb.config import Settings

tool = XMLSearchTool(
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
