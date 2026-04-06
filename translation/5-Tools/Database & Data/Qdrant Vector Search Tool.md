> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Qdrant Vektör Arama Aracı

> Qdrant vektör veritabanını kullanarak CrewAI ajanları için anlamsal arama yetenekleri

## Genel Bakış

Qdrant Vektör Arama Aracı, bir vektör benzerlik arama motoru olan [Qdrant](https://qdrant.tech/) üzerinden CrewAI ajanlarınıza anlamsal arama yetenekleri kazandırır. Bu araç, ajanlarınızın bir Qdrant koleksiyonunda saklanan belgeler arasında anlamsal benzerlik kullanarak arama yapmasını sağlar.

## Kurulum

Gerekli paketleri kurun:

```bash  theme={null}
uv add qdrant-client
```

## Temel Kullanım

Aracın nasıl kullanılacağına dair minimal bir örnek:

```python  theme={null}
from crewai import Agent
from crewai_tools import QdrantVectorSearchTool, QdrantConfig

# Aracı QdrantConfig ile başlat
qdrant_tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url="your_qdrant_url",
        qdrant_api_key="your_qdrant_api_key",
        collection_name="your_collection"
    )
)

# Aracı kullanan bir ajan oluştur
agent = Agent(
    role="Araştırma Asistanı",
    goal="Belgelerde ilgili bilgiyi bul",
    tools=[qdrant_tool]
)

# Araç otomatik olarak OpenAI embedding'lerini kullanır
# ve skoru > 0.35 olan en ilgili 3 sonucu döndürür
```

## Tam Çalışan Örnek

İşte şunların nasıl yapılacağını gösteren tam bir örnek:

1. Bir PDF'den metin çıkarma
2. OpenAI kullanarak embedding üretme
3. Qdrant içinde saklama
4. Anlamsal arama için CrewAI ajan tabanlı bir RAG iş akışı oluşturma

```python  theme={null}
import os
import uuid
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import QdrantVectorSearchTool
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

# Ortam değişkenlerini yükle
load_dotenv()

# OpenAI istemcisini başlat
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# PDF'den metin çıkar
def extract_text_from_pdf(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text.strip())
    return text

# OpenAI embedding'leri üret
def get_openai_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

# Metni ve embedding'leri Qdrant içinde sakla
def load_pdf_to_qdrant(pdf_path, qdrant, collection_name):
    # PDF'den metin çıkar
    text_chunks = extract_text_from_pdf(pdf_path)

    # Qdrant koleksiyonu oluştur
    if qdrant.collection_exists(collection_name):
        qdrant.delete_collection(collection_name)
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
    )

    # Embedding'leri sakla
    points = []
    for chunk in text_chunks:
        embedding = get_openai_embedding(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk}
        ))
    qdrant.upsert(collection_name=collection_name, points=points)

# Qdrant istemcisini başlat ve veriyi yükle
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
collection_name = "example_collection"
pdf_path = "path/to/your/document.pdf"
load_pdf_to_qdrant(pdf_path, qdrant, collection_name)

# Qdrant arama aracını başlat
from crewai_tools import QdrantConfig

qdrant_tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url=os.getenv("QDRANT_URL"),
        qdrant_api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=collection_name,
        limit=3,
        score_threshold=0.35
    )
)

# CrewAI ajanlarını oluştur
search_agent = Agent(
    role="Kıdemli Anlamsal Arama Ajanı",
    goal="Anlamsal aramaya göre belgeleri bul ve analiz et",
    backstory="""You are an expert research assistant who can find relevant
    information using semantic search in a Qdrant database.""",
    tools=[qdrant_tool],
    verbose=True
)

answer_agent = Agent(
    role="Kıdemli Yanıt Asistanı",
    goal="Verilen bağlama göre sorulara yanıt üret",
    backstory="""You are an expert answer assistant who can generate
    answers to questions based on the context provided.""",
    tools=[qdrant_tool],
    verbose=True
)

# Görevleri tanımla
search_task = Task(
    description="""Search for relevant documents about the {query}.
    Your final answer should include:
    - The relevant information found
    - The similarity scores of the results
    - The metadata of the relevant documents""",
    agent=search_agent
)

answer_task = Task(
    description="""Given the context and metadata of relevant documents,
    generate a final answer based on the context.""",
    agent=answer_agent
)

# CrewAI iş akışını çalıştır
crew = Crew(
    agents=[search_agent, answer_agent],
    tasks=[search_task, answer_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(
    inputs={"query": "What is the role of X in the document?"}
)
print(result)
```

## Araç Parametreleri

### Gerekli Parametreler

* `qdrant_config` (QdrantConfig): Tüm Qdrant ayarlarını içeren yapılandırma nesnesi

### QdrantConfig Parametreleri

* `qdrant_url` (str): Qdrant sunucunuzun URL'si
* `qdrant_api_key` (str, isteğe bağlı): Qdrant ile kimlik doğrulama için API anahtarı
* `collection_name` (str): Arama yapılacak Qdrant koleksiyonunun adı
* `limit` (int): Döndürülecek maksimum sonuç sayısı (varsayılan: 3)
* `score_threshold` (float): Minimum benzerlik skoru eşiği (varsayılan: 0.35)
* `filter` (Any, isteğe bağlı): Gelişmiş filtreleme için Qdrant Filter örneği (varsayılan: None)

### İsteğe Bağlı Araç Parametreleri

* `custom_embedding_fn` (Callable\[\[str], list\[float]]): Metni vektörleştirmek için özel fonksiyon
* `qdrant_package` (str): Qdrant için temel paket yolu (varsayılan: `"qdrant_client"`)
* `client` (Any): Önceden başlatılmış Qdrant istemcisi (isteğe bağlı)

## Gelişmiş Filtreleme

QdrantVectorSearchTool, arama sonuçlarınızı iyileştirmek için güçlü filtreleme yeteneklerini destekler:

### Dinamik Filtreleme

Sonuçları anlık olarak filtrelemek için aramanızda `filter_by` ve `filter_value` parametrelerini kullanın:

```python  theme={null}
# Ajan, aracı çağırırken bu parametreleri kullanacaktır
# Araç şeması filter_by ve filter_value kabul eder
# Örnek: kategori filtresiyle arama
# Sonuçlar category == "technology" olduğunda filtrelenecektir
```

### QdrantConfig ile Ön Tanımlı Filtreler

Karmaşık filtreleme için yapılandırmanızda Qdrant Filter örneklerini kullanın:

```python  theme={null}
from qdrant_client.http import models as qmodels
from crewai_tools import QdrantVectorSearchTool, QdrantConfig

# Belirli koşullar için filtre oluştur
preset_filter = qmodels.Filter(
    must=[
        qmodels.FieldCondition(
            key="category",
            match=qmodels.MatchValue(value="research")
        ),
        qmodels.FieldCondition(
            key="year",
            match=qmodels.MatchValue(value=2024)
        )
    ]
)

# Aracı ön tanımlı filtre ile başlat
qdrant_tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url="your_url",
        qdrant_api_key="your_key",
        collection_name="your_collection",
        filter=preset_filter  # Tüm aramalara uygulanan ön tanımlı filtre
    )
)
```

### Filtreleri Birleştirme

Araç, `QdrantConfig` içindeki ön tanımlı filtreleri `filter_by` ve `filter_value` içindeki dinamik filtrelerle otomatik olarak birleştirir:

```python  theme={null}
# If QdrantConfig has a preset filter for category="research"
# And the search uses filter_by="year", filter_value=2024
# Both filters will be combined (AND logic)
```

## Search Parameters

The tool accepts these parameters in its schema:

* `query` (str): The search query to find similar documents
* `filter_by` (str, optional): Metadata field to filter on
* `filter_value` (Any, optional): Value to filter by

## Return Format

The tool returns results in JSON format:

```json  theme={null}
[
  {
    "metadata": {
      // Any metadata stored with the document
    },
    "context": "The actual text content of the document",
    "distance": 0.95  // Similarity score
  }
]
```

## Default Embedding

By default, the tool uses OpenAI's `text-embedding-3-large` model for vectorization. This requires:

* OpenAI API key set in environment: `OPENAI_API_KEY`

## Custom Embeddings

Instead of using the default embedding model, you might want to use your own embedding function in cases where you:

1. Want to use a different embedding model (e.g., Cohere, HuggingFace, Ollama models)
2. Need to reduce costs by using open-source embedding models
3. Have specific requirements for vector dimensions or embedding quality
4. Want to use domain-specific embeddings (e.g., for medical or legal text)

Here's an example using a HuggingFace model:

```python  theme={null}
from transformers import AutoTokenizer, AutoModel
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def custom_embeddings(text: str) -> list[float]:
    # Tokenize and get model outputs
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)

    # Use mean pooling to get text embedding
    embeddings = outputs.last_hidden_state.mean(dim=1)

    # Convert to list of floats and return
    return embeddings[0].tolist()

# Use custom embeddings with the tool
from crewai_tools import QdrantConfig

tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url="your_url",
        qdrant_api_key="your_key",
        collection_name="your_collection"
    ),
    custom_embedding_fn=custom_embeddings  # Pass your custom function
)
```

## Error Handling

The tool handles these specific errors:

* Raises ImportError if `qdrant-client` is not installed (with option to auto-install)
* Raises ValueError if `QDRANT_URL` is not set
* Prompts to install `qdrant-client` if missing using `uv add qdrant-client`

## Environment Variables

Required environment variables:

```bash  theme={null}
export QDRANT_URL="your_qdrant_url"  # If not provided in constructor
export QDRANT_API_KEY="your_api_key"  # If not provided in constructor
export OPENAI_API_KEY="your_openai_key"  # If using default embeddings
```
