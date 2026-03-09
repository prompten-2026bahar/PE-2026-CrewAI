# RAG Aracı

> `RagTool`, Veri Alma Destekli Nesil (Retrieval-Augmented Generation) kullanarak soruları yanıtlamak için dinamik bir bilgi tabanı aracıdır.

# `RagTool`

## Açıklama

`RagTool`, CrewAI'nin yerel RAG sistemi aracılığıyla Veri Alma Destekli Nesil (RAG) gücünden yararlanarak soruları yanıtlamak için tasarlanmıştır. Çeşitli veri kaynaklarından ilgili bilgileri almak için sorgulanabilen dinamik bir bilgi tabanı sağlar. Bu araç, özellikle çok çeşitli bilgilere erişim gerektiren ve bağlamsal olarak ilgili yanıtlar sağlaması gereken uygulamalar için kullanışlıdır.

## Örnek

Aşağıdaki örnek, aracın nasıl başlatılacağını ve farklı veri kaynaklarıyla nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai_tools import RagTool

# Varsayılan ayarlarla bir RAG aracı oluşturun
rag_tool = RagTool()

# Bir dosyadan içerik ekleyin
rag_tool.add(data_type="file", path="yol/belgeniz.pdf")

# Bir web sayfasından içerik ekleyin
rag_tool.add(data_type="web_page", url="https://example.com")

# RagTool'u kullanan bir ajan tanımlayın
@agent
def knowledge_expert(self) -> Agent:
    '''
    Bu ajan, bilgi tabanı hakkında soruları yanıtlamak için RagTool'u kullanır.
    '''
    return Agent(
        config=self.agents_config["knowledge_expert"],
        allow_delegation=False,
        tools=[rag_tool]
    )
```

## Desteklenen Veri Kaynakları

`RagTool` çok çeşitli veri kaynaklarıyla kullanılabilir:

* 📰 PDF dosyaları
* 📊 CSV dosyaları
* 📃 JSON dosyaları
* 📝 Metin (Text)
* 📁 Dizinler/Klasörler
* 🌐 HTML Web sayfaları
* 📽️ YouTube Kanalları
* 📺 YouTube Videoları
* 📚 Dökümantasyon web siteleri
* 📝 MDX dosyaları
* 📄 DOCX dosyaları
* 🧾 XML dosyaları
* 📬 Gmail
* 📝 GitHub depoları
* 🐘 PostgreSQL veritabanları
* 🐬 MySQL veritabanları
* 🤖 Slack konuşmaları
* 💬 Discord mesajları
* 🗨️ Discourse forumları
* 📝 Substack bültenleri
* 🐝 Beehiiv içeriği
* 💾 Dropbox dosyaları
* 🖼️ Görüntüler
* ⚙️ Özel veri kaynakları

## Parametreler

`RagTool` aşağıdaki parametreleri kabul eder:

* **summarize**: Opsiyonel. Alınan içeriğin özetlenip özetlenmeyeceği. Varsayılan: `False`.
* **adapter**: Opsiyonel. Bilgi tabanı için özel bir adaptör. Sağlanmazsa `CrewAIRagAdapter` kullanılacaktır.
* **config**: Opsiyonel. Temel CrewAI RAG sistemi yapılandırması. Opsiyonel `embedding_model` (ProviderSpec) ve `vectordb` (VectorDbConfig) anahtarlarını içeren bir `RagToolConfig` sözlüğü kabul eder. Programatik olarak sağlanan tüm yapılandırma değerleri, ortam değişkenlerine göre önceliklidir.

## İçerik Ekleme

`add` metodunu kullanarak bilgi tabanına içerik ekleyebilirsiniz:

```python Code theme={null}
# Bir PDF dosyası ekleyin
rag_tool.add(data_type="file", path="yol/belgeniz.pdf")

# Bir web sayfası ekleyin
rag_tool.add(data_type="web_page", url="https://example.com")

# Bir YouTube videosu ekleyin
rag_tool.add(data_type="youtube_video", url="https://www.youtube.com/watch?v=VIDEO_ID")

# Bir dosya dizini ekleyin
rag_tool.add(data_type="directory", path="yol/dizininiz")
```

## Ajan Entegrasyon Örneği

`RagTool`'un bir CrewAI ajanıyla nasıl entegre edileceği aşağıda açıklanmıştır:

```python Code theme={null}
from crewai import Agent
from crewai.project import agent
from crewai_tools import RagTool

# Aracı başlatın ve içerik ekleyin
rag_tool = RagTool()
rag_tool.add(data_type="web_page", url="https://docs.crewai.com")
rag_tool.add(data_type="file", path="sirket_verisi.pdf")

# RagTool ile bir ajan tanımlayın
@agent
def knowledge_expert(self) -> Agent:
    return Agent(
        config=self.agents_config["knowledge_expert"],
        allow_delegation=False,
        tools=[rag_tool]
    )
```

## Gelişmiş Yapılandırma

Bir yapılandırma sözlüğü sağlayarak `RagTool` davranışını özelleştirebilirsiniz:

```python Code theme={null}
from crewai_tools import RagTool
from crewai_tools.tools.rag import RagToolConfig, VectorDbConfig, ProviderSpec

# Özel yapılandırma ile bir RAG aracı oluşturun

vectordb: VectorDbConfig = {
    "provider": "qdrant",
    "config": {
        "collection_name": "koleksiyonum"
    }
}

embedding_model: ProviderSpec = {
    "provider": "openai",
    "config": {
        "model_name": "text-embedding-3-small"
    }
}

config: RagToolConfig = {
    "vectordb": vectordb,
    "embedding_model": embedding_model
}

rag_tool = RagTool(config=config, summarize=True)
```

## Gömme (Embedding) Modeli Yapılandırması

`embedding_model` parametresi, şu yapıya sahip bir `crewai.rag.embeddings.types.ProviderSpec` sözlüğü kabul eder:

```python  theme={null}
{
    "provider": "provider-name",  # Zorunlu
    "config": {                    # Opsiyonel
        # Sağlayıcıya özel yapılandırma
    }
}
```

### Desteklenen Sağlayıcılar

#### OpenAI
```python main.py theme={null}
from crewai.rag.embeddings.providers.openai.types import OpenAIProviderSpec

embedding_model: OpenAIProviderSpec = {
    "provider": "openai",
    "config": {
        "api_key": "api-anahtarınız",
        "model_name": "text-embedding-ada-002",
        "dimensions": 1536,
        "organization_id": "org-id",
        "api_base": "https://api.openai.com/v1",
        "api_version": "v1",
        "default_headers": {"Custom-Header": "value"}
    }
}
```

**Yapılandırma Seçenekleri:**

* `api_key` (str): OpenAI API anahtarı
* `model_name` (str): Kullanılacak model. Varsayılan: `text-embedding-ada-002`. Seçenekler: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`
* `dimensions` (int): Gömme (embedding) boyut sayısı
* `organization_id` (str): OpenAI organizasyon ID'si
* `api_base` (str): Özel API temel URL'si
* `api_version` (str): API sürümü
* `default_headers` (dict): API istekleri için özel başlıklar

**Ortam Değişkenleri:**

* `OPENAI_API_KEY` veya `EMBEDDINGS_OPENAI_API_KEY`: `api_key`
* `OPENAI_ORGANIZATION_ID` veya `EMBEDDINGS_OPENAI_ORGANIZATION_ID`: `organization_id`
* `OPENAI_MODEL_NAME` veya `EMBEDDINGS_OPENAI_MODEL_NAME`: `model_name`
* `OPENAI_API_BASE` or `EMBEDDINGS_OPENAI_API_BASE`: `api_base`
* `OPENAI_API_VERSION` or `EMBEDDINGS_OPENAI_API_VERSION`: `api_version`
* `OPENAI_DIMENSIONS` or `EMBEDDINGS_OPENAI_DIMENSIONS`: `dimensions`

#### Cohere
```python main.py theme={null}
from crewai.rag.embeddings.providers.cohere.types import CohereProviderSpec

embedding_model: CohereProviderSpec = {
    "provider": "cohere",
    "config": {
        "api_key": "api-anahtarınız",
        "model_name": "embed-english-v3.0"
    }
}
```

**Yapılandırma Seçenekleri:**

* `api_key` (str): Cohere API anahtarı
* `model_name` (str): Kullanılacak model. Varsayılan: `large`. Seçenekler: `embed-english-v3.0`, `embed-multilingual-v3.0`, `large`, `small`

**Ortam Değişkenleri:**

* `COHERE_API_KEY` veya `EMBEDDINGS_COHERE_API_KEY`: `api_key`
* `EMBEDDINGS_COHERE_MODEL_NAME`: `model_name`

#### VoyageAI
```python main.py theme={null}
from crewai.rag.embeddings.providers.voyageai.types import VoyageAIProviderSpec

embedding_model: VoyageAIProviderSpec = {
    "provider": "voyageai",
    "config": {
        "api_key": "api-anahtarınız",
        "model": "voyage-3",
        "input_type": "document",
        "truncation": True,
        "output_dtype": "float32",
        "output_dimension": 1024,
        "max_retries": 3,
        "timeout": 60.0
    }
}
```

**Yapılandırma Seçenekleri:**

* `api_key` (str): VoyageAI API anahtarı
* `model` (str): Kullanılacak model. Varsayılan: `voyage-2`. Seçenekler: `voyage-3`, `voyage-3-lite`, `voyage-code-3`, `voyage-large-2`
* `input_type` (str): Giriş türü. Seçenekler: `document` (depolama için), `query` (arama için)
* `truncation` (bool): Maksimum uzunluğu aşan girişlerin kesilip kesilmeyeceği. Varsayılan: `True`
* `output_dtype` (str): Çıktı veri tipi
* `output_dimension` (int): Çıktı gömmelerinin boyutu
* `max_retries` (int): Maksimum yeniden deneme denemesi. Varsayılan: `0`
* `timeout` (float): Saniye cinsinden istek zaman aşımı

**Ortam Değişkenleri:**

* `VOYAGEAI_API_KEY` veya `EMBEDDINGS_VOYAGEAI_API_KEY`: `api_key`
* `VOYAGEAI_MODEL` veya `EMBEDDINGS_VOYAGEAI_MODEL`: `model`
* `VOYAGEAI_INPUT_TYPE` veya `EMBEDDINGS_VOYAGEAI_INPUT_TYPE`: `input_type`
* `VOYAGEAI_TRUNCATION` veya `EMBEDDINGS_VOYAGEAI_TRUNCATION`: `truncation`
* `VOYAGEAI_OUTPUT_DTYPE` veya `EMBEDDINGS_VOYAGEAI_OUTPUT_DTYPE`: `output_dtype`
* `VOYAGEAI_OUTPUT_DIMENSION` veya `EMBEDDINGS_VOYAGEAI_OUTPUT_DIMENSION`: `output_dimension`
* `VOYAGEAI_MAX_RETRIES` veya `EMBEDDINGS_VOYAGEAI_MAX_RETRIES`: `max_retries`
* `VOYAGEAI_TIMEOUT` veya `EMBEDDINGS_VOYAGEAI_TIMEOUT`: `timeout`

#### Ollama
```python main.py theme={null}
from crewai.rag.embeddings.providers.ollama.types import OllamaProviderSpec

embedding_model: OllamaProviderSpec = {
    "provider": "ollama",
    "config": {
        "model_name": "llama2",
        "url": "http://localhost:11434/api/embeddings"
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_name` (str): Ollama model adı (örn. `llama2`, `mistral`, `nomic-embed-text`)
* `url` (str): Ollama API uç nokta URL'si. Varsayılan: `http://localhost:11434/api/embeddings`

**Ortam Değişkenleri:**

* `OLLAMA_MODEL` veya `EMBEDDINGS_OLLAMA_MODEL`: `model_name`
* `OLLAMA_URL` veya `EMBEDDINGS_OLLAMA_URL`: `url`

#### Amazon Bedrock
```python main.py theme={null}
from crewai.rag.embeddings.providers.aws.types import BedrockProviderSpec

embedding_model: BedrockProviderSpec = {
    "provider": "amazon-bedrock",
    "config": {
        "model_name": "amazon.titan-embed-text-v2:0",
        "session": boto3_session
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_name` (str): Bedrock model ID'si. Varsayılan: `amazon.titan-embed-text-v1`. Seçenekler: `amazon.titan-embed-text-v1`, `amazon.titan-embed-text-v2:0`, `cohere.embed-english-v3`, `cohere.embed-multilingual-v3`
* `session` (Any): AWS kimlik doğrulaması için Boto3 session nesnesi

**Ortam Değişkenleri:**

* `AWS_ACCESS_KEY_ID`: AWS erişim anahtarı
* `AWS_SECRET_ACCESS_KEY`: AWS gizli anahtarı
* `AWS_REGION`: AWS bölgesi (örn. `us-east-1`)

#### Azure OpenAI
```python main.py theme={null}
from crewai.rag.embeddings.providers.microsoft.types import AzureProviderSpec

embedding_model: AzureProviderSpec = {
    "provider": "azure",
    "config": {
        "deployment_id": "deployment-id-niz",
        "api_key": "api-anahtarınız",
        "api_base": "https://kaynaginiz.openai.azure.com",
        "api_version": "2024-02-01",
        "model_name": "text-embedding-ada-002",
        "api_type": "azure"
    }
}
```

**Yapılandırma Seçenekleri:**

* `deployment_id` (str): **Zorunlu** - Azure OpenAI dağıtım ID'si
* `api_key` (str): Azure OpenAI API anahtarı
* `api_base` (str): Azure OpenAI kaynak uç noktası
* `api_version` (str): API sürümü. Örnek: `2024-02-01`
* `model_name` (str): Model adı. Varsayılan: `text-embedding-ada-002`
* `api_type` (str): API türü. Varsayılan: `azure`
* `dimensions` (int): Çıktı boyutları
* `default_headers` (dict): Özel başlıklar

**Ortam Değişkenleri:**

* `AZURE_OPENAI_API_KEY` veya `EMBEDDINGS_AZURE_API_KEY`: `api_key`
* `AZURE_OPENAI_ENDPOINT` veya `EMBEDDINGS_AZURE_API_BASE`: `api_base`
* `EMBEDDINGS_AZURE_DEPLOYMENT_ID`: `deployment_id`
* `EMBEDDINGS_AZURE_API_VERSION`: `api_version`
* `EMBEDDINGS_AZURE_MODEL_NAME`: `model_name`
* `EMBEDDINGS_AZURE_API_TYPE`: `api_type`
* `EMBEDDINGS_AZURE_DIMENSIONS`: `dimensions`

#### Google Generative AI
```python main.py theme={null}
from crewai.rag.embeddings.providers.google.types import GenerativeAiProviderSpec

embedding_model: GenerativeAiProviderSpec = {
    "provider": "google-generativeai",
    "config": {
        "api_key": "api-anahtarınız",
        "model_name": "gemini-embedding-001",
        "task_type": "RETRIEVAL_DOCUMENT"
    }
}
```

**Yapılandırma Seçenekleri:**

* `api_key` (str): Google AI API anahtarı
* `model_name` (str): Model adı. Varsayılan: `gemini-embedding-001`. Seçenekler: `gemini-embedding-001`, `text-embedding-005`, `text-multilingual-embedding-002`
* `task_type` (str): Gömme işi türü. Varsayılan: `RETRIEVAL_DOCUMENT`. Seçenekler: `RETRIEVAL_DOCUMENT`, `RETRIEVAL_QUERY`

**Ortam Değişkenleri:**

* `GOOGLE_API_KEY`, `GEMINI_API_KEY`, veya `EMBEDDINGS_GOOGLE_API_KEY`: `api_key`
* `EMBEDDINGS_GOOGLE_GENERATIVE_AI_MODEL_NAME`: `model_name`
* `EMBEDDINGS_GOOGLE_GENERATIVE_AI_TASK_TYPE`: `task_type`

#### Google Vertex AI
```python main.py theme={null}
from crewai.rag.embeddings.providers.google.types import VertexAIProviderSpec

embedding_model: VertexAIProviderSpec = {
    "provider": "google-vertex",
    "config": {
        "model_name": "text-embedding-004",
        "project_id": "proje-id-niz",
        "region": "us-central1",
        "api_key": "api-anahtarınız"
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_name` (str): Model adı. Varsayılan: `textembedding-gecko`. Seçenekler: `text-embedding-004`, `textembedding-gecko`, `textembedding-gecko-multilingual`
* `project_id` (str): Google Cloud proje ID'si. Varsayılan: `cloud-large-language-models`
* `region` (str): Google Cloud bölgesi. Varsayılan: `us-central1`
* `api_key` (str): Kimlik doğrulama için API anahtarı

**Ortam Değişkenleri:**

* `GOOGLE_APPLICATION_CREDENTIALS`: Servis hesabı JSON dosyasının yolu
* `GOOGLE_CLOUD_PROJECT` veya `EMBEDDINGS_GOOGLE_VERTEX_PROJECT_ID`: `project_id`
* `EMBEDDINGS_GOOGLE_VERTEX_MODEL_NAME`: `model_name`
* `EMBEDDINGS_GOOGLE_VERTEX_REGION`: `region`
* `EMBEDDINGS_GOOGLE_VERTEX_API_KEY`: `api_key`

#### Jina AI
```python main.py theme={null}
from crewai.rag.embeddings.providers.jina.types import JinaProviderSpec

embedding_model: JinaProviderSpec = {
    "provider": "jina",
    "config": {
        "api_key": "api-anahtarınız",
        "model_name": "jina-embeddings-v3"
    }
}
```

**Yapılandırma Seçenekleri:**

* `api_key` (str): Jina AI API anahtarı
* `model_name` (str): Model adı. Varsayılan: `jina-embeddings-v2-base-en`. Seçenekler: `jina-embeddings-v3`, `jina-embeddings-v2-base-en`, `jina-embeddings-v2-small-en`

**Ortam Değişkenleri:**

* `JINA_API_KEY` veya `EMBEDDINGS_JINA_API_KEY`: `api_key`
* `EMBEDDINGS_JINA_MODEL_NAME`: `model_name`

#### HuggingFace
```python main.py theme={null}
from crewai.rag.embeddings.providers.huggingface.types import HuggingFaceProviderSpec

embedding_model: HuggingFaceProviderSpec = {
    "provider": "huggingface",
    "config": {
        "url": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    }
}
```

**Yapılandırma Seçenekleri:**

* `url` (str): HuggingFace çıkarım (inference) API uç noktasının tam URL'si

**Ortam Değişkenleri:**

* `HUGGINGFACE_URL` veya `EMBEDDINGS_HUGGINGFACE_URL`: `url`

#### Instructor
```python main.py theme={null}
from crewai.rag.embeddings.providers.instructor.types import InstructorProviderSpec

embedding_model: InstructorProviderSpec = {
    "provider": "instructor",
    "config": {
        "model_name": "hkunlp/instructor-xl",
        "device": "cuda",
        "instruction": "Belgeyi temsil et"
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_name` (str): HuggingFace model ID'si. Varsayılan: `hkunlp/instructor-base`. Seçenekler: `hkunlp/instructor-xl`, `hkunlp/instructor-large`, `hkunlp/instructor-base`
* `device` (str): Çalıştırılacak cihaz. Varsayılan: `cpu`. Seçenekler: `cpu`, `cuda`, `mps`
* `instruction` (str): Gömmeler için talimat ön eki

**Ortam Değişkenleri:**

* `EMBEDDINGS_INSTRUCTOR_MODEL_NAME`: `model_name`
* `EMBEDDINGS_INSTRUCTOR_DEVICE`: `device`
* `EMBEDDINGS_INSTRUCTOR_INSTRUCTION`: `instruction`

#### Sentence Transformer
```python main.py theme={null}
from crewai.rag.embeddings.providers.sentence_transformer.types import SentenceTransformerProviderSpec

embedding_model: SentenceTransformerProviderSpec = {
    "provider": "sentence-transformer",
    "config": {
        "model_name": "all-mpnet-base-v2",
        "device": "cuda",
        "normalize_embeddings": True
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_name` (str): Sentence Transformers model adı. Varsayılan: `all-MiniLM-L6-v2`. Seçenekler: `all-mpnet-base-v2`, `all-MiniLM-L6-v2`, `paraphrase-multilingual-MiniLM-L12-v2`
* `device` (str): Çalıştırılacak cihaz. Varsayılan: `cpu`. Seçenekler: `cpu`, `cuda`, `mps`
* `normalize_embeddings` (bool): Gömmelerin normalize edilip edilmeyeceği. Varsayılan: `False`

**Ortam Değişkenleri:**

* `EMBEDDINGS_SENTENCE_TRANSFORMER_MODEL_NAME`: `model_name`
* `EMBEDDINGS_SENTENCE_TRANSFORMER_DEVICE`: `device`
* `EMBEDDINGS_SENTENCE_TRANSFORMER_NORMALIZE_EMBEDDINGS`: `normalize_embeddings`

#### ONNX
```python main.py theme={null}
from crewai.rag.embeddings.providers.onnx.types import ONNXProviderSpec

embedding_model: ONNXProviderSpec = {
    "provider": "onnx",
    "config": {
        "preferred_providers": ["CUDAExecutionProvider", "CPUExecutionProvider"]
    }
}
```

**Yapılandırma Seçenekleri:**

* `preferred_providers` (list\[str]): Tercih sırasına göre ONNX yürütme sağlayıcılarının listesi

**Ortam Değişkenleri:**

* `EMBEDDINGS_ONNX_PREFERRED_PROVIDERS`: `preferred_providers` (virgülle ayrılmış liste)

#### OpenCLIP
```python main.py theme={null}
from crewai.rag.embeddings.providers.openclip.types import OpenCLIPProviderSpec

embedding_model: OpenCLIPProviderSpec = {
    "provider": "openclip",
    "config": {
        "model_name": "ViT-B-32",
        "checkpoint": "laion2b_s34b_b79k",
        "device": "cuda"
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_name` (str): OpenCLIP model mimarisi. Varsayılan: `ViT-B-32`. Seçenekler: `ViT-B-32`, `ViT-B-16`, `ViT-L-14`
* `checkpoint` (str): Önceden eğitilmiş kontrol noktası adı. Varsayılan: `laion2b_s34b_b79k`. Seçenekler: `laion2b_s34b_b79k`, `laion400m_e32`, `openai`
* `device` (str): Çalıştırılacak cihaz. Varsayılan: `cpu`. Seçenekler: `cpu`, `cuda`

**Ortam Değişkenleri:**

* `EMBEDDINGS_OPENCLIP_MODEL_NAME`: `model_name`
* `EMBEDDINGS_OPENCLIP_CHECKPOINT`: `checkpoint`
* `EMBEDDINGS_OPENCLIP_DEVICE`: `device`

#### Text2Vec
```python main.py theme={null}
from crewai.rag.embeddings.providers.text2vec.types import Text2VecProviderSpec

embedding_model: Text2VecProviderSpec = {
    "provider": "text2vec",
    "config": {
        "model_name": "shibing624/text2vec-base-multilingual"
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_name` (str): HuggingFace'ten Text2Vec model adı. Varsayılan: `shibing624/text2vec-base-chinese`. Seçenekler: `shibing624/text2vec-base-multilingual`, `shibing624/text2vec-base-chinese`

**Ortam Değişkenleri:**

* `EMBEDDINGS_TEXT2VEC_MODEL_NAME`: `model_name`

#### Roboflow
```python main.py theme={null}
from crewai.rag.embeddings.providers.roboflow.types import RoboflowProviderSpec

embedding_model: RoboflowProviderSpec = {
    "provider": "roboflow",
    "config": {
        "api_key": "api-anahtarınız",
        "api_url": "https://infer.roboflow.com"
    }
}
```

**Yapılandırma Seçenekleri:**

* `api_key` (str): Roboflow API anahtarı. Varsayılan: `""` (boş dize)
* `api_url` (str): Roboflow çıkarım API URL'si. Varsayılan: `https://infer.roboflow.com`

**Ortam Değişkenleri:**

* `ROBOFLOW_API_KEY` veya `EMBEDDINGS_ROBOFLOW_API_KEY`: `api_key`
* `ROBOFLOW_API_URL` veya `EMBEDDINGS_ROBOFLOW_API_URL`: `api_url`

#### WatsonX (IBM)
```python main.py theme={null}
from crewai.rag.embeddings.providers.ibm.types import WatsonXProviderSpec

embedding_model: WatsonXProviderSpec = {
    "provider": "watsonx",
    "config": {
        "model_id": "ibm/slate-125m-english-rtrvr",
        "url": "https://us-south.ml.cloud.ibm.com",
        "api_key": "api-anahtarınız",
        "project_id": "proje-id-niz",
        "batch_size": 100,
        "concurrency_limit": 10,
        "persistent_connection": True
    }
}
```

**Yapılandırma Seçenekleri:**

* `model_id` (str): WatsonX model tanımlayıcısı
* `url` (str): WatsonX API uç noktası
* `api_key` (str): IBM Cloud API anahtarı
* `project_id` (str): WatsonX proje ID'si
* `space_id` (str): WatsonX space ID (project\_id'ye alternatif)
* `batch_size` (int): Gömmeler için toplu iş boyutu. Varsayılan: `100`
* `concurrency_limit` (int): Maksimum eşzamanlı istek sayısı. Varsayılan: `10`
* `persistent_connection` (bool): Kalıcı bağlantıları kullan. Varsayılan: `True`
* Ayrıca 20'den fazla ek kimlik doğrulama ve yapılandırma seçeneği

**Ortam Değişkenleri:**

* `WATSONX_API_KEY` veya `EMBEDDINGS_WATSONX_API_KEY`: `api_key`
* `WATSONX_URL` veya `EMBEDDINGS_WATSONX_URL`: `url`
* `WATSONX_PROJECT_ID` veya `EMBEDDINGS_WATSONX_PROJECT_ID`: `project_id`
* `EMBEDDINGS_WATSONX_MODEL_ID`: `model_id`
* `EMBEDDINGS_WATSONX_SPACE_ID`: `space_id`
* `EMBEDDINGS_WATSONX_BATCH_SIZE`: `batch_size`
* `EMBEDDINGS_WATSONX_CONCURRENCY_LIMIT`: `concurrency_limit`
* `EMBEDDINGS_WATSONX_PERSISTENT_CONNECTION`: `persistent_connection`

#### Özel (Custom)
```python main.py theme={null}
from crewai.rag.core.base_embeddings_callable import EmbeddingFunction
from crewai.rag.embeddings.providers.custom.types import CustomProviderSpec

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input):
        # Özel gömme mantığınız
        return embeddings

embedding_model: CustomProviderSpec = {
    "provider": "custom",
    "config": {
        "embedding_callable": MyEmbeddingFunction
    }
}
```

**Yapılandırma Seçenekleri:**

* `embedding_callable` (type\[EmbeddingFunction]): Özel gömme fonksiyonu sınıfı

**Not:** Özel gömme fonksiyonları, `crewai.rag.core.base_embeddings_callable` içinde tanımlanan `EmbeddingFunction` protokolünü uygulamalıdır. `__call__` metodu giriş verilerini kabul etmeli ve gömmeleri bir numpy dizileri listesi (veya normalize edilecek uyumlu bir format) olarak döndürmelidir. Döndürülen gömmeler otomatik olarak normalize edilir ve doğrulanır.

### Notlar

* Belirtilen tüm yapılandırma alanları, **Zorunlu** olarak işaretlenmediği sürece opsiyoneldir.
* API anahtarları genellikle yapılandırma yerine ortam değişkenleri aracılığıyla sağlanabilir.
* Geçerli olduğu yerlerde varsayılan değerler gösterilmiştir.

## Sonuç

`RagTool`, çeşitli veri kaynaklarından bilgi tabanları oluşturmak ve bunları sorgulamak için güçlü bir yol sunar. Veri Alma Destekli Nesil'den yararlanarak, ajanların ilgili bilgilere verimli bir şekilde erişmesini ve bunları almasını sağlayarak, doğru ve bağlamsal olarak uygun yanıtlar verme yeteneklerini artırır.
