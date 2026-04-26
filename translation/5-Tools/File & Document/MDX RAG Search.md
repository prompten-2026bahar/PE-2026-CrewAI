> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# MDX RAG Arama

> `MDXSearchTool`, MDX dosyalarında arama yapmak ve en ilgili sonuçları döndürmek için tasarlanmıştır.

# `MDXSearchTool`

<Note>
  MDXSearchTool sürekli geliştirme halindedir. Aracı iyileştirirken özellikler eklenebilir veya kaldırılabilir ve işlevsellik öngörülemeyen şekilde değişebilir.
</Note>

## Açıklama

MDX Search Tool, gelişmiş markdown dili çıkarımını kolaylaştırmayı amaçlayan `crewai_tools` paketinin bir bileşenidir. Kullanıcıların sorgu tabanlı aramalar kullanarak MD dosyalarından ilgili bilgileri etkili şekilde aramasını ve çıkarmasını sağlar. Bu araç, veri analizi, bilgi yönetimi ve araştırma görevleri için son derece değerlidir; büyük belge koleksiyonlarında belirli bilgileri bulma sürecini hızlandırır.

## Kurulum

MDX Search Tool'u kullanmadan önce `crewai_tools` paketinin kurulu olduğundan emin olun. Kurulu değilse aşağıdaki komutla yükleyebilirsiniz:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Kullanım Örneği

MDX Search Tool'u kullanmak için önce gerekli ortam değişkenlerini ayarlamalısınız. Ardından pazar araştırmanıza başlamak için aracı crewAI projenize entegre edin. Aşağıda bunun nasıl yapılacağına dair temel bir örnek yer alır:

```python Code theme={null}
from crewai_tools import MDXSearchTool

# Aracı, çalışma sırasında öğrendiği herhangi bir MDX içeriğinde arama yapacak şekilde başlat
tool = MDXSearchTool()

# OR

# Aracı belirli bir MDX dosya yoluyla başlat; böylece arama yalnızca o belge içinde yapılsın
tool = MDXSearchTool(mdx='path/to/your/document.mdx')
```

## Parametreler

* mdx: **İsteğe bağlı**. Arama için MDX dosyasının yolunu belirtir. Başlatma sırasında verilebilir.

## Model ve Embedding Özelleştirmesi

Araç varsayılan olarak embedding ve özetleme için OpenAI kullanır. Özelleştirme için aşağıda gösterildiği gibi bir yapılandırma sözlüğü kullanın:

```python Code theme={null}
from chromadb.config import Settings

tool = MDXSearchTool(
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
