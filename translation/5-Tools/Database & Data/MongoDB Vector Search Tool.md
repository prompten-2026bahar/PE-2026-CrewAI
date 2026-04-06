> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# MongoDB Vektör Arama Aracı

> `MongoDBVectorSearchTool`, isteğe bağlı indeksleme yardımcılarıyla MongoDB Atlas üzerinde vektör araması yapar.

# `MongoDBVectorSearchTool`

## Açıklama

MongoDB Atlas koleksiyonları üzerinde vektör benzerliği sorguları yapar. İndeks oluşturma yardımcılarını ve embedding uygulanmış metinlerin toplu eklenmesini destekler.

MongoDB Atlas yerel vektör aramasını destekler. Daha fazla bilgi:
[https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/)

## Kurulum

MongoDB eklentisiyle kurun:

```shell  theme={null}
pip install crewai-tools[mongodb]
```

or

```shell  theme={null}
uv add crewai-tools --extra mongodb
```

## Parametreler

### Başlatma

* `connection_string` (str, required)
* `database_name` (str, required)
* `collection_name` (str, required)
* `vector_index_name` (str, default `vector_index`)
* `text_key` (str, default `text`)
* `embedding_key` (str, default `embedding`)
* `dimensions` (int, default `1536`)

### Çalıştırma Parametreleri

* `query` (str, gerekli): Embedding uygulanıp aranacak doğal dil sorgusu.

## Hızlı başlangıç

```python Code theme={null}
from crewai_tools import MongoDBVectorSearchTool

tool = MongoDBVectorSearchTool(
  connection_string="mongodb+srv://...",
  database_name="mydb",
  collection_name="docs",
)

print(tool.run(query="how to create vector index"))
```

## İndeks oluşturma yardımcıları

Doğru boyutlar ve benzerlik ayarlarıyla bir Atlas Vector Search indeksi oluşturmak için `create_vector_search_index(...)` kullanın.

## Yaygın sorunlar

* Kimlik doğrulama hataları: Atlas IP Access List'in çalıştırıcınıza izin verdiğinden ve bağlantı dizesinin kimlik bilgilerini içerdiğinden emin olun.
* İndeks bulunamadı: önce vektör indeksini oluşturun; adı `vector_index_name` ile eşleşmelidir.
* Boyut uyuşmazlığı: embedding modelinin boyutlarını `dimensions` ile hizalayın.

## Daha fazla örnek

### Temel başlatma

```python Code theme={null}
from crewai_tools import MongoDBVectorSearchTool

tool = MongoDBVectorSearchTool(
    database_name="example_database",
    collection_name="example_collection",
    connection_string="<your_mongodb_connection_string>",
)
```

### Özel sorgu yapılandırması

```python Code theme={null}
from crewai_tools import MongoDBVectorSearchConfig, MongoDBVectorSearchTool

query_config = MongoDBVectorSearchConfig(limit=10, oversampling_factor=2)
tool = MongoDBVectorSearchTool(
    database_name="example_database",
    collection_name="example_collection",
    connection_string="<your_mongodb_connection_string>",
    query_config=query_config,
    vector_index_name="my_vector_index",
)

rag_agent = Agent(
    name="rag_agent",
    role="You are a helpful assistant that can answer questions with the help of the MongoDBVectorSearchTool.",
    goal="...",
    backstory="...",
    tools=[tool],
)
```

### Veritabanını önceden yükleme ve indeks oluşturma

```python Code theme={null}
import os
from crewai_tools import MongoDBVectorSearchTool

tool = MongoDBVectorSearchTool(
    database_name="example_database",
    collection_name="example_collection",
    connection_string="<your_mongodb_connection_string>",
)

# Yerel klasörden metin içeriğini yükleyin ve MongoDB'ye ekleyin
texts = []
for fname in os.listdir("knowledge"):
    path = os.path.join("knowledge", fname)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())

tool.add_texts(texts)

# Atlas Vector Search indeksini oluşturun (ör. text-embedding-3-large için 3072 boyut)
tool.create_vector_search_index(dimensions=3072)
```

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MongoDBVectorSearchTool

tool = MongoDBVectorSearchTool(
    connection_string="mongodb+srv://...",
    database_name="mydb",
    collection_name="docs",
)

agent = Agent(
    role="RAG Ajanı",
    goal="MongoDB vektör aramasını kullanarak yanıt ver",
    backstory="Bilgi getirme uzmanı",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="'indexing guidance' için ilgili içeriği bul",
    expected_output="En ilgili eşleşmeleri referans alan kısa bir yanıt",
    agent=agent,
)

crew = Crew(
    agents=[agent], 
    tasks=[task],
    verbose=True,
)

result = crew.kickoff()
```
