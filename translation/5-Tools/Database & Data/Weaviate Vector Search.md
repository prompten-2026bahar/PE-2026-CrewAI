> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Weaviate Vektör Arama

> `WeaviateVectorSearchTool`, hibrit arama kullanarak Weaviate vektör veritabanında anlamsal olarak benzer belgeleri aramak için tasarlanmıştır.

## Genel Bakış

`WeaviateVectorSearchTool`, Weaviate vektör veritabanında saklanan belgeler üzerinde anlamsal arama yapmak için özel olarak hazırlanmıştır. Bu araç, verilen bir sorguya anlamsal olarak benzer belgeleri bulmanızı sağlar; daha doğru ve bağlama daha uygun arama sonuçları için vektör ve anahtar kelime aramasının gücünden yararlanır.

[Weaviate](https://weaviate.io/) is a vector database that stores and queries vector embeddings, enabling semantic search capabilities.
[Weaviate](https://weaviate.io/), vektör embedding'leri saklayan ve sorgulayan, anlamsal arama yetenekleri sunan bir vektör veritabanıdır.

## Kurulum

Bu aracı projenize dahil etmek için Weaviate istemcisini kurmanız gerekir:

```shell  theme={null}
uv add weaviate-client
```

## Başlamak İçin Adımlar

`WeaviateVectorSearchTool` aracını etkili şekilde kullanmak için şu adımları izleyin:

1. **Paket Kurulumu**: `crewai[tools]` ve `weaviate-client` paketlerinin Python ortamınızda kurulu olduğunu doğrulayın.
2. **Weaviate Kurulumu**: Bir Weaviate kümesi kurun. Talimatlar için [Weaviate documentation](https://weaviate.io/developers/wcs/manage-clusters/connect) sayfasını izleyebilirsiniz.
3. **API Anahtarları**: Weaviate küme URL'nizi ve API anahtarınızı edinin.
4. **OpenAI API Anahtarı**: Ortam değişkenlerinizde `OPENAI_API_KEY` olarak bir OpenAI API anahtarınızın ayarlı olduğundan emin olun.

## Örnek

Aşağıdaki örnek, aracın nasıl başlatılacağını ve bir aramanın nasıl yürütüleceğini gösterir:

```python Code theme={null}
from crewai_tools import WeaviateVectorSearchTool

# Aracı başlat
tool = WeaviateVectorSearchTool(
    collection_name='example_collections',
    limit=3,
    alpha=0.75,
    weaviate_cluster_url="https://your-weaviate-cluster-url.com",
    weaviate_api_key="your-weaviate-api-key",
)

@agent
def search_agent(self) -> Agent:
    '''
    Bu ajan, Weaviate vektör veritabanında
    anlamsal olarak benzer belgeleri aramak için WeaviateVectorSearchTool kullanır.
    '''
    return Agent(
        config=self.agents_config["search_agent"],
        tools=[tool]
    )
```

## Parametreler

`WeaviateVectorSearchTool` şu parametreleri kabul eder:

* **collection\_name**: Gerekli. Arama yapılacak koleksiyonun adı.
* **weaviate\_cluster\_url**: Gerekli. Weaviate kümesinin URL'si.
* **weaviate\_api\_key**: Gerekli. Weaviate kümesi için API anahtarı.
* **limit**: İsteğe bağlı. Döndürülecek sonuç sayısı. Varsayılan `3`.
* **alpha**: İsteğe bağlı. Vektör ve anahtar kelime (BM25) araması arasındaki ağırlığı kontrol eder. alpha = 0 -> yalnızca BM25, alpha = 1 -> yalnızca vektör araması. Varsayılan `0.75`.
* **vectorizer**: İsteğe bağlı. Kullanılacak vectorizer. Verilmezse `nomic-embed-text` modeliyle `text2vec_openai` kullanılır.
* **generative\_model**: İsteğe bağlı. Kullanılacak üretici model. Verilmezse OpenAI'nin `gpt-4o` modeli kullanılır.

## Gelişmiş Yapılandırma

Araç tarafından kullanılan vectorizer ve üretici modeli özelleştirebilirsiniz:

```python Code theme={null}
from crewai_tools import WeaviateVectorSearchTool
from weaviate.classes.config import Configure

# Vectorizer ve üretici model için özel model ayarla
tool = WeaviateVectorSearchTool(
    collection_name='example_collections',
    limit=3,
    alpha=0.75,
    vectorizer=Configure.Vectorizer.text2vec_openai(model="nomic-embed-text"),
    generative_model=Configure.Generative.openai(model="gpt-4o-mini"),
    weaviate_cluster_url="https://your-weaviate-cluster-url.com",
    weaviate_api_key="your-weaviate-api-key",
)
```

## Belgeleri Önceden Yükleme

Aracı kullanmadan önce Weaviate veritabanınızı belgelerle önceden yükleyebilirsiniz:

```python Code theme={null}
import os
from crewai_tools import WeaviateVectorSearchTool
import weaviate
from weaviate.classes.init import Auth

# Weaviate'e bağlan
client = weaviate.connect_to_weaviate_cloud(
    cluster_url="https://your-weaviate-cluster-url.com",
    auth_credentials=Auth.api_key("your-weaviate-api-key"),
    headers={"X-OpenAI-Api-Key": "your-openai-api-key"}
)

# Koleksiyonu al veya oluştur
test_docs = client.collections.get("example_collections")
if not test_docs:
    test_docs = client.collections.create(
        name="example_collections",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(model="nomic-embed-text"),
        generative_config=Configure.Generative.openai(model="gpt-4o"),
    )

# Belgeleri yükle
docs_to_load = os.listdir("knowledge")
with test_docs.batch.dynamic() as batch:
    for d in docs_to_load:
        with open(os.path.join("knowledge", d), "r") as f:
            content = f.read()
        batch.add_object(
            {
                "content": content,
                "year": d.split("_")[0],
            }
        )

# Aracı başlat
tool = WeaviateVectorSearchTool(
    collection_name='example_collections', 
    limit=3,
    alpha=0.75,
    weaviate_cluster_url="https://your-weaviate-cluster-url.com",
    weaviate_api_key="your-weaviate-api-key",
)
```

## Ajan Entegrasyonu Örneği

İşte `WeaviateVectorSearchTool` aracını bir CrewAI ajanı ile entegre etmenin yolu:

```python Code theme={null}
from crewai import Agent
from crewai_tools import WeaviateVectorSearchTool

# Aracı başlat
weaviate_tool = WeaviateVectorSearchTool(
    collection_name='example_collections',
    limit=3,
    alpha=0.75,
    weaviate_cluster_url="https://your-weaviate-cluster-url.com",
    weaviate_api_key="your-weaviate-api-key",
)

# Araç ile bir ajan oluştur
rag_agent = Agent(
    name="rag_agent",
    role="WeaviateVectorSearchTool yardımıyla soruları yanıtlayabilen faydalı bir asistansın.",
    llm="gpt-4o-mini",
    tools=[weaviate_tool],
)
```

## Sonuç

`WeaviateVectorSearchTool`, Weaviate vektör veritabanında anlamsal olarak benzer belgeleri aramak için güçlü bir yol sunar. Vektör embedding'lerden yararlanarak geleneksel anahtar kelime tabanlı aramalara kıyasla daha doğru ve bağlama daha uygun sonuçlar sağlar. Bu araç, özellikle tam eşleşmeler yerine anlam temelli bilgi bulmayı gerektiren uygulamalar için kullanışlıdır.
