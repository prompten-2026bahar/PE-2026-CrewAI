## Bilgi

CrewAI'de bilgi nedir ve görevler sırasında harici bilgi kaynaklarına nasıl erişilir ve kullanılır.


## Genel Bakış

CrewAI'deki Bilgi, yapay zeka ajanlarının görevleri sırasında harici bilgi kaynaklarına erişmesini ve bunları kullanmasını sağlayan güçlü bir sistemdir.
Bunu, çalışanları kullanırken başvurabilecekleri bir referans kütüphane vermek olarak düşünebilirsiniz.

Ana faydaları:
- Ajanları alan özel bilgilerle zenginleştirme
- Gerçek dünya verileriyle kararları destekleme
- Bağlamı konuşmalar genelinde koruma
- Yanıtları gerçek bilgilere dayandırma

## Hızlı Başlangıç Örnekleri

Dosya tabanlı Bilgi Kaynakları için, dosyalarınızı projenizin kök dizininde `knowledge` adlı bir dizine yerleştirdiğinizden emin olun.
Ayrıca kaynak oluştururken `knowledge` dizininden göreceli yollar kullanın.

### Vektör mağazası (RAG) istemci yapılandırması

CrewAI, vektör mağazaları için sağlayıcıdan bağımsız bir RAG istemci soyutlaması sunar. Varsayılan sağlayıcı ChromaDB'dir ve Qdrant da desteklenmektedir. Yapılandırma yardımcı programları kullanarak sağlayıcıları değiştirebilirsiniz.

Desteklenenler:
- ChromaDB (varsayılan)
- Qdrant

```python
from crewai.rag.config.utils import set_rag_config, get_rag_client, clear_rag_config

# ChromaDB (varsayılan)
from crewai.rag.chromadb.config import ChromaDBConfig
set_rag_config(ChromaDBConfig())
chromadb_client = get_rag_client()

# Qdrant
from crewai.rag.qdrant.config import QdrantConfig
set_rag_config(QdrantConfig())
qdrant_client = get_rag_client()

# Örnek işlemler (herhangi bir sağlayıcı için aynı API)
client = qdrant_client  # veya chromadb_client
client.create_collection(collection_name="docs")
client.add_documents(
    collection_name="docs",
    documents=[{"id": "1", "content": "CrewAI, işbirlikçi yapay zeka ajanlarını etkinleştirir."}],
)
results = client.search(collection_name="docs", query="işbirlikçi ajanlar", limit=3)

clear_rag_config()  # isteğe bağlı sıfırlama
```

Bu RAG istemcisi, Bilginin yerleşik depolamasından ayrıdır. Vektör mağazası kontrolüne veya özel alma işlem hatlarına ihtiyacınız olduğunda bunu kullanın.

### Temel String Bilgi Örneği

```python
from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Bir bilgi kaynağı oluşturun
content = "Kullanıcı adının John'udur. 30 yaşındadır ve San Francisco'da yaşıyor."
string_source = StringKnowledgeSource(content=content)

# Belirli çıktıları garanti etmek için 0 sıcaklığı ile bir LLM oluşturun
llm = LLM(model="gpt-4o-mini", temperature=0)

# Bilgi deposu ile bir ajan oluşturun
agent = Agent(
    role="Kullanıcı Hakkında",
    goal="Kullanıcı hakkında her şeyi bilirsiniz.",
    backstory="İnsanları ve tercihlerini anlamakta ustasınız.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

task = Task(
    description="Kullanıcıyla ilgili şu soruları yanıtlayın: {question}",
    expected_output="Sorunun cevabı.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge_sources=[string_source], # Bilgiyi buraya kaynakları ekleyerek etkinleştirin
)

result = crew.kickoff(inputs={"question": "John hangi şehirde yaşıyor ve kaç yaşında?"})
```

### Web İçeriği Bilgi Örneği

Aşağıdaki örneğin çalışması için `docling` kurmanız gerekir: `uv add docling`

```python
from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource

# Web içeriğinden bir bilgi kaynağı oluşturun
content_source = CrewDoclingSource(
    file_paths=[
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination",
    ],
)

# Belirli çıktıları garanti etmek için 0 sıcaklığı ile bir LLM oluşturun
llm = LLM(model="gpt-4o-mini", temperature=0)

# Bilgi deposu ile bir ajan oluşturun
agent = Agent(
    role="Çalışmalar Hakkında",
    goal="Çalışmalar hakkında her şeyi bilirsiniz.",
    backstory="Çalışmaları ve içeriklerini anlamakta ustasınız.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

task = Task(
    description="Çalışmalarla ilgili şu soruları yanıtlayın: {question}",
    expected_output="Sorunun cevabı.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge_sources=[content_source],
)

result = crew.kickoff(
    inputs={"question": "Ödül hackleme makalesi ne hakkında? Kaynakları belirtmeyi unutmayın."}
)
```

## Desteklenen Bilgi Kaynakları

CrewAI, birçok bilgi kaynağını hazır olarak destekler:

### Metin Kaynakları

- Ham dizeler
- Metin dosyaları (.txt)
- PDF belgeleri

### Yapılandırılmış Veri

- CSV dosyaları
- Excel elektronik tabloları
- JSON belgeleri

### Metin Dosyası Bilgi Kaynağı

```python
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

text_source = TextFileKnowledgeSource(
    file_paths=["document.txt", "another.txt"]
)
```

### PDF Bilgi Kaynağı

```python
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

pdf_source = PDFKnowledgeSource(
    file_paths=["document.pdf", "another.pdf"]
)
```

### CSV Bilgi Kaynağı

```python
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource

csv_source = CSVKnowledgeSource(
    file_paths=["data.csv"]
)
```

### Excel Bilgi Kaynağı

```python
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource

excel_source = ExcelKnowledgeSource(
    file_paths=["spreadsheet.xlsx"]
)
```

### JSON Bilgi Kaynağı

```python
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource

json_source = JSONKnowledgeSource(
    file_paths=["data.json"]
)
```

Lütfen ./knowledge klasörünü oluşturduğunuzdan emin olun. Merkezi yönetim için tüm kaynak dosyaları (örneğin, .txt, .pdf, .xlsx, .json) bu klasörde bulunmalıdır.

## Ajan vs Mürettebat Bilgisi: Kapsamlı Kılavuz

**Bilgi Seviyelerini Anlama**: CrewAI, hem ajan hem de mürettebat seviyesinde bilgi desteği sunar. Bu bölüm, her birinin nasıl çalıştığını, ne zaman başlatıldığını ve bağımlılıklarla ilgili yaygın yanlış anlamaları giderir.

### Bilgi Başlatılmasının Tam Olarak Nasıl Çalıştığı

Bilgiyi kullanırken tam olarak ne olduğuna dair aşağıda bir açıklama bulunmaktadır:

#### Ajan Seviyesi Bilgi (Bağımsız)

```python
from crewai import Agent, Task, Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Sadece bu ajan için özel olan bir bilgiyle ajan - mürettebat bilgisi gerekli değil
specialist_knowledge = StringKnowledgeSource(
    content="Bu ajan için sadece özel teknik bilgiler"
)

specialist_agent = Agent(
    role="Teknik Uzman",
    goal="Teknik uzmanlık sağlamak",
    backstory="Özel teknik alanlarda uzman",
    knowledge_sources=[specialist_knowledge]  # Ajana özel bilgi
)

task = Task(
    description="Kullanıcı sorularını yanıtlayın",
    agent=specialist_agent,
    expected_output="Teknik cevap"
)

# Mürettebat bilgisi gerekli değil
crew = Crew(
    agents=[specialist_agent],
    tasks=[task]
)

result = crew.kickoff()  # Ajan bilgisi bağımsız olarak çalışır
```

#### `crew.kickoff()` Sırasında Ne Olur

`crew.kickoff()`'u çağırdığınızda, tam olarak aşağıdaki sıralama gerçekleşir:

```python
# Başlatma sırasında
for agent in self.agents:
    agent.crew = self  # Ajan mürettebat referansını alır
    agent.set_knowledge(crew_embedder=self.embedder)  # Ajan bilgisi başlatılır
    agent.create_agent_executor()
```

#### Depolama Bağımsızlığı

Her bilgi seviyesi, bağımsız depolama koleksiyonları kullanır:

```python
# Ajan bilgisi depolama
agent_collection_name = agent.role  # Örneğin, "Teknik Uzman"

# Mürettebat bilgisi depolama
crew_collection_name = "crew"

# İkisi de aynı ChromaDB örneğinde ancak farklı koleksiyonlarda depolanır
# Yol: ~/.local/share/CrewAI/{proje}/knowledge/
#   ├── crew/                    # Mürettebat bilgisi koleksiyonu
#   ├── Teknik Uzman/    # Ajan bilgisi koleksiyonu
#   └── Başka Bir Ajan Rolü/      # Başka bir ajanın koleksiyonu
```

## Tam Çalışır Örnekler

#### Örnek 1: Yalnızca Ajan Bilgisi

```python
from crewai import Agent, Task, Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Ajan özelinde bilgi
agent_knowledge = StringKnowledgeSource(
    content="Sadece bu ajan için gereken ajan özelinde bilgi"
)

agent = Agent(
    role="Uzman",
    goal="Özel bilgiyi kullanın",
    backstory="Özel bilgiye sahip uzman",
    knowledge_sources=[agent_knowledge],
    embedder={  # Ajan kendi embedder'ına sahip olabilir
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)

task = Task(
    description="Özel bilginizi kullanarak cevaplayın",
    agent=agent,
    expected_output="Ajan bilgisine göre cevap"
)

# Mürettebat bilgisi gerekli değil
crew = Crew(agents=[agent], tasks=[])
result = crew.kickoff()  # Mükemmel şekilde çalışır
```

#### Örnek 2: Hem Ajan Hem de Mürettebat Bilgisi

```python
# Tüm ajanlar tarafından paylaşılan mürettebat çapında bilgi (paylaşılan)
crew_knowledge = StringKnowledgeSource(
    content="Tüm ajanlar için şirket politikaları ve genel bilgiler"
)

# Ajan özelinde bilgi
specialist_knowledge = StringKnowledgeSource(
    content="Sadece uzman tarafından ihtiyaç duyulan teknik spesifikasyonlar"
)

specialist = Agent(
    role="Teknik Uzman",
    goal="Teknik uzmanlık sağlayın",
    backstory="Teknik uzman",
    knowledge_sources=[specialist_knowledge]  # Ajan özelinde
)

generalist = Agent(
    role="Genel Yardımcı", 
    goal="Genel yardım sağlayın",
    backstory="Genel yardımcı"
    # Ajan özelinde bilgi yok
)

crew = Crew(
    agents=[specialist, generalist],
    tasks=[...],
    knowledge_sources=[crew_knowledge]  # Mürettebat çapında bilgi
)

# Sonuç:
# - uzman: mürettebat_bilgisi + uzman_bilgisi alır
# - generalist: sadece mürettebat_bilgisini alır
```

#### Örnek 3: Farklı Bilgilerle Birden Çok Ajan

```python
# Farklı ajanlar için farklı bilgi
sales_knowledge = StringKnowledgeSource(content="Satış prosedürleri ve fiyatlandırma")
tech_knowledge = StringKnowledgeSource(content="Teknik dokümantasyon")
support_knowledge = StringKnowledgeSource(content="Destek prosedürleri")

sales_agent = Agent(
    role="Satış Temsilcisi",
    knowledge_sources=[sales_knowledge],
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}}
)

tech_agent = Agent(
    role="Teknik Uzman", 
    knowledge_sources=[tech_knowledge],
    embedder={"provider": "ollama", "config": {"model": "mxbai-embed-large"}}
)

support_agent = Agent(
    role="Destek Uzmanı",
    knowledge_sources=[support_knowledge]
    # Varsayılan embedder'ı kullanacak
)

crew = Crew(
    agents=[sales_agent, tech_agent, support_agent],
    tasks=[...],
    embedder={  # Ajanların kendi embedder'ları yoksa varsayılan embedder
        "provider": "google-generativeai",
        "config": {"model_name": "gemini-embedding-001"}
    }
)

# Her ajan sadece kendi özel bilgisine sahip
# Her biri farklı embedding sağlayıcılarını kullanabilir
```

Alet bir görevle başlatıldığında, araç bilgiyi bir araç olarak bir vektör veritabanından alma ihtiyacı duymadan bilgiyle önceden yüklenecektir.
Sadece ajanın veya mürettebatın çalışması için gereken ilgili bilgi kaynaklarını ekleyin.

Bilgi kaynakları hem ajan hem de mürettebat seviyesinde eklenebilir.
Mürettebat seviyesi bilgisi kaynakları, **mürettebattaki tüm ajanlar** tarafından kullanılacaktır.
Ajan seviyesi bilgisi kaynakları, **önceden bilgiyle yüklenmiş özel ajanı** tarafından kullanılacaktır.

## Bilgi Yapılandırması

Mürettebat veya ajan için bilgi yapılandırmasını yapılandırabilirsiniz.

```python Code
from crewai.knowledge.knowledge_config import KnowledgeConfig

knowledge_config = KnowledgeConfig(results_limit=10, score_threshold=0.5)

agent = Agent(
    ...
    knowledge_config=knowledge_config
)
```

`results_limit`: geri döndürülecek ilgili belgelerin sayısıdır. Varsayılan olarak 3'tür.
`score_threshold`: bir belgenin alakalı olarak kabul edilmesi için gereken minimum puandır. Varsayılan olarak 0,35'tir.

## Desteklenen Bilgi Parametreleri

Bilgi kaynakları listesi, depolanacak ve sorgulanacak içerik sağlamak için kullanılır. PDF, CSV, Excel, JSON, metin dosyaları veya dize içeriği içerebilir.

Bilginin depolanacağı koleksiyonun adı. Farklı bilgi kümelerini tanımlamak için kullanılır. Sağlanmazsa varsayılan olarak "bilgi" olarak ayarlanır.

Bilginin nasıl depolanacağını ve alınacağını yönetmek için özel depolama yapılandırması. Sağlanmazsa varsayılan bir depolama oluşturulacaktır.

## Bilgi Depolama Şeffaflığı

**Bilgi Depolama Anlayışı**: CrewAI, vektör depolama için ChromaDB'yi kullanarak platforma özgü dizinlerde bilgileri otomatik olarak depolar. Bu konumları ve varsayılanları anlamak, üretim dağıtımları, hata ayıklama ve depolama yönetimi için yardımcı olur.

### CrewAI'nin Bilgi Dosyalarını Depoladığı Yerler

Varsayılan olarak CrewAI, Bellek ile aynı depolama sistemini kullanarak bilginin platforma özgü dizinlerde depolandığı aynı depolama sistemini kullanır:

#### Platforma Göre Varsayılan Depolama Konumları

**macOS:**
```
~/Library/Application Support/CrewAI/{proje_adı}/
└── knowledge/                    # Bilgi ChromaDB dosyaları
    ├── chroma.sqlite3           # ChromaDB meta verileri
    ├── {collection_id}/         # Vektör yerleştirmeleri
    └── knowledge_{collection}/  # İsimli koleksiyonlar
```

**Linux:**
```
~/.local/share/CrewAI/{proje_adı}/
└── knowledge/
    ├── chroma.sqlite3
    ├── {collection_id}/
    └── knowledge_{collection}/
```

**Windows:**
```
C:\Users\{kullanıcı adı}\AppData\Local\CrewAI\{proje_adı}\
└── knowledge\
    ├── chroma.sqlite3
    ├── {collection_id}\
    └── knowledge_{collection}\
```

### Bilgi Depolama Konumunuzu Bulma

Bilginizin depolandığı yeri görmek için:

```python
from crewai.utilities.paths import db_storage_path

# Bilgi depolama yolunu alın
knowledge_path = os.path.join(db_storage_path(), "knowledge")
print(f"Bilgi depolama konumu: {knowledge_path}")

# Bilgi koleksiyonlarının içeriğini listeleyin
if os.path.exists(knowledge_path):
    print("\nBilgi depolama içeriği:")
    for item in os.listdir(knowledge_path):
        item_path = os.path.join(knowledge_path, item)
        if os.path.isdir(item_path):
            print(f"📁 Koleksiyon: {item}/")
            # Koleksiyon içeriğini göster
            try:
                for subitem in os.listdir(item_path):
                    print(f"   └── {subitem}")
            except PermissionError:
                print(f"   └── (izin reddedildi)")
        else:
            print(f"📄 {item}")
else:
    print("Henüz bir bilgi depolama bulunamadı.")
```

### Bilgi Depolama Konumlarını Kontrol Etme

#### Seçenek 1: Ortam Değişkeni (Önerilen)
```python
from crewai import Crew

# Tüm CrewAI verileri için özel depolama konumunu ayarlayın
os.environ["CREWAI_STORAGE_DIR"] = "./my_project_storage"

# Tüm bilgi şimdi ./my_project_storage/knowledge/ dizininde depolanacaktır
crew = Crew(
    agents=[...],
    tasks=[...],
    knowledge_sources=[...]
)
```

#### Seçenek 2: Özel Bilgi Depolama

```python
from pathlib import Path

# Bilgiyi proje dizininde depolayın
project_root = Path(__file__).parent
knowledge_dir = project_root / "knowledge_storage"

os.environ["CREWAI_STORAGE_DIR"] = str(knowledge_dir)

# Şimdi tüm bilgi proje dizininizde depolanacaktır
```

#### Seçenek 3: Proje Özel Bilgi Depolama

```python
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Özel embedder ile özel depolama oluşturun
custom_storage = KnowledgeStorage(
    embedder={
        "provider": "ollama",
        "config": {
            "model": "mxbai-embed-large"
        }
    },
    collection_name="my_custom_knowledge"
)

# Bilgi kaynağıyla kullanın
knowledge_source = StringKnowledgeSource(
    content="Bilgi içeriğiniz burada"
)
knowledge_source.storage = custom_storage
```

### Varsayılan Embedder Sağlayıcı Davranışı

**Varsayılan Embedder Sağlayıcı**: CrewAI, bilgi depolama için varsayılan olarak OpenAI yerleştirmeleri (`text-embedding-3-small`) kullanır, diğer LLM sağlayıcılarını kullanırken bile. Bunu kurulumunuza göre kolayca özelleştirebilirsiniz.

#### Varsayılan Davranışı Anlama
```python
from crewai import Agent, Crew, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Claude'u LLM olarak kullanırken...
agent = Agent(
    role="Araştırmacı",
    goal="Konular hakkında araştırma yapın",
    backstory="Uzman araştırmacı",
    llm=LLM(provider="anthropic", model="claude-3-sonnet")  # Claude'u kullanarak
)

# CrewAI yine de OpenAI yerleştirmelerini varsayılan olarak kullanır
# Bu tutarlılığı sağlar, ancak LLM sağlayıcınızla eşleşmeyebilir
knowledge_source = StringKnowledgeSource(content="Araştırma verileri...")

crew = Crew(
    agents=[agent],
    tasks=[...],
    knowledge_sources=[knowledge_source]
    # Varsayılan: Claude LLM ile bile OpenAI yerleştirmelerini kullanır
)
```

#### Bilgi Embedder Sağlayıcılarını Özelleştirme
```python
# Seçenek 1: Voyage AI'ı kullanın (Anthropic tarafından Claude kullanıcıları için önerilir)
crew = Crew(
    agents=[agent],
    tasks=[...],
    knowledge_sources=[knowledge_source],
    embedder={
        "provider": "voyageai",  # Claude kullanıcıları için önerilir
        "config": {
            "api_key": "your-voyage-api-key",
            "model": "voyage-3"  # veya en iyi kalite için "voyage-3-large"
        }
    }
)

# Seçenek 2: Yerel yerleştirmeleri kullanın (harici API çağrıları yok)
crew = Crew(
    agents=[agent],
    tasks=[...],
    knowledge_sources=[knowledge_source],
    embedder={
        "provider": "ollama",
        "config": {
            "model": "mxbai-embed-large",
            "url": "http://localhost:11434/api/embeddings"
        }
    }
)

# Seçenek 3: Ajan seviyesi embedder özelleştirmesi
agent = Agent(
    role="Araştırmacı",
    goal="Konular hakkında araştırma yapın",
    backstory="Uzman araştırmacı",
    knowledge_sources=[knowledge_source],
    embedder={
        "provider": "google-generativeai",
        "config": {
            "model_name": "gemini-embedding-001",
            "api_key": "your-google-key"
        }
    }
)
```

#### Azure OpenAI Embeddings'leri Yapılandırma

Azure OpenAI yerleştirmelerini kullanırken:
1. Öncelikle embedder modelini Azure platformunda dağıttığınızdan emin olun
2. Ardından aşağıdakini kullanmanız gerekir:

```python
agent = Agent(
    role="Araştırmacı",
    goal="Konular hakkında araştırma yapın",
    backstory="Uzman araştırmacı",
    knowledge_sources=[knowledge_source],
    embedder={
        "provider": "azure",
        "config": {
            "api_key": "your-azure-api-key",
            "model": "text-embedding-ada-002", # Kullandığınız ve Azure'da dağıtılan modele göre değiştirin
            "api_base": "https://your-azure-endpoint.openai.azure.com/",
            "api_version": "2024-02-01"
        }
    }
)
```

## Gelişmiş Özellikler

### Sorgu Yeniden Yazma

CrewAI, bilgi alma işlemini optimize etmek için akıllı bir sorgu yeniden yazma mekanizması uygular. Bir ajanın bilgi kaynakları aracılığıyla arama yapması gerektiğinde, ham görev istemi daha etkili bir arama sorgusuna otomatik olarak dönüştürülür.

#### Sorgu Yeniden Yazma Nasıl Çalışır

1. Bir ajan bilgi kaynaklarıyla bir görev yürütürken `_get_knowledge_search_query` yöntemi tetiklenir
2. Ajanın LLM'si orijinal görev istemini optimize edilmiş bir arama sorgusuna dönüştürmek için kullanılır
3. Bu optimize edilmiş sorgu daha sonra bilgi kaynaklarından ilgili bilgileri almak için kullanılır

#### Sorgu Yeniden Yazmanın Faydaları

- İyileştirilmiş Alma Doğruluğu
- Bağlam Farkındalığı

#### Örnek

```python
# Orijinal görev istemi
task_prompt = "Kullanıcının en sevdiği filmlerle ilgili şu soruları yanıtlayın: John geçen hafta hangi filmi izledi? Cevabınızı JSON formatında verin."

# Arka planda bu şu şekilde yeniden yazılabilir:
rewritten_query = "John geçen hafta hangi filmleri izledi?"
```

Yeniden yazılan sorgu, çekirdek bilgi ihtiyacına daha odaklıdır ve çıktı biçimlendirmesiyle ilgili gereksiz talimatları kaldırır.

Bu mekanizma tamamen otomatik olup kullanıcıların herhangi bir yapılandırma gerektirmesi gerekmez. Ajanın LLM'si sorgu yeniden yazmayı gerçekleştirmek için kullanılır, bu nedenle daha yetenekli bir LLM kullanmak, yeniden yazılan sorguların kalitesini artırabilir.

### Bilgi Olayları

CrewAI, bilgi alma sürecinde dinleyebileceğiniz olay sistemi kullanarak dinleyebileceğiniz olaylar çıkarır. Bu olaylar, bilginin nasıl alındığını ve kullanıldığını izlemenize, hata ayıklamanıza ve analiz etmenize olanak tanır.

#### Kullanılabilir Bilgi Olayları

- **KnowledgeRetrievalStartedEvent**: Bir ajan bilgi kaynaklarından bilgi almaya başladığında çıkarılır
- **KnowledgeRetrievalCompletedEvent**: Bilgi alma tamamlandığında, kullanılan sorgu ve alınan içerik dahil olmak üzere çıkarılır
- **KnowledgeQueryStartedEvent**: Bilgi kaynaklarına bir sorgu başladığında çıkarılır
- **KnowledgeQueryCompletedEvent**: Bir sorgu başarıyla tamamlandığında çıkarılır
- **KnowledgeQueryFailedEvent**: Bilgi kaynaklarına bir sorgu başarısız olduğunda çıkarılır
- **KnowledgeSearchQueryFailedEvent**: Bilgi kaynaklarına bir arama sorgusu başarısız olduğunda çıkarılır

#### Örnek: Bilgi Alma İzleme

```python
from crewai.events import (
    KnowledgeRetrievalStartedEvent,
    KnowledgeRetrievalCompletedEvent,
    BaseEventListener,
)

class KnowledgeMonitorListener(BaseEventListener):
    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(KnowledgeRetrievalStartedEvent)
        def on_knowledge_retrieval_started(source, event):
            print(f"Ajan '{event.agent.role}' bilgi almaya başladı")
            
        @crewai_event_bus.on(KnowledgeRetrievalCompletedEvent)
        def on_knowledge_retrieval_completed(source, event):
            print(f"Ajan '{event.agent.role}' bilgi almayı tamamladı")
            print(f"Sorgu: {event.query}")
            print(f"Alınan {len(event.retrieved_knowledge)} bilgi parçası")

# Dinleyicinizin bir örneğini oluşturun
knowledge_monitor = KnowledgeMonitorListener()
```

Olayları kullanma hakkında daha fazla bilgi için [Olay Dinleyicileri](/en/concepts/event-listener) dokümanlarına bakın.

### Özel Bilgi Kaynakları

Herhangi bir veri türü için özel bilgi kaynakları oluşturmak için `BaseKnowledgeSource` sınıfını genişleterek CrewAI, özel bilgi kaynakları oluşturmanıza olanak tanır. Pratikte boşluk haberleri almak ve işlemek için bir örnek oluşturulmuştur.

#### Boşluk Haberleri Bilgi Kaynağı Örneği

```python
from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field
import requests

class SpaceNewsKnowledgeSource(BaseKnowledgeSource):
    """Bilgiyi Uzay Haberleri API'sinden çeken bir bilgi kaynağı."""

    api_endpoint: str = Field(description="API uç noktası URL'si")
    limit: int = Field(default=10, description="Alınacak makale sayısı")

    def load_content(self) -> Dict[Any, str]:
        """Uzay haberlerini çekin ve biçimlendirin."""
        try:
            response = requests.get(
                f"{self.api_endpoint}?limit={self.limit}"
            )
            response.raise_for_status()

            data = response.json()
            articles = data.get('results', [])

            formatted_data = self.validate_content(articles)
            return {self.api_endpoint: formatted_data}
        except Exception as e:
            raise ValueError(f"Uzay haberleri alınamadı: {str(e)}")

    def validate_content(self, articles: list) -> str:
        """Makaleleri okunabilir metne dönüştürün."""
        formatted = "Uzay Haberleri Makaleleri:\n\n"
        for article in articles:
            formatted += f"""
                Başlık: {article['title']}
                Yayınlanma Tarihi: {article['published_at']}
                Özet: {article['summary']}
                Haber Sitesi: {article['news_site']}
                URL: {article['url']}
                -------------------"""
        return formatted

    def add(self) -> None:
        """Makaleleri işleyin ve depolayın."""
        content = self.load_content()
        for _, text in content.items():
            chunks = self._chunk_text(text)
            self.chunks.extend(chunks)

        self._save_documents()

# Bilgi kaynağı oluşturun
recent_news = SpaceNewsKnowledgeSource(
    api_endpoint="https://api.spaceflightnewsapi.net/v4/articles",
    limit=10,
)

# Özel bir ajan oluşturun
space_analyst = Agent(
    role="Uzay Haberleri Analisti",
    goal="Uzay haberleri hakkında doğru ve kapsamlı cevaplar verin",
    backstory=""""Uzay keşfi, uydu teknolojisi ve uzay endüstrisi trendleri konusunda uzmanlığa sahip bir uzay endüstrisi analistisiniz. Uzay haberleri hakkında soruları yanıtlamakta ve ayrıntılı ve doğru bilgiler sağlamakta mükemmeldir.""",
    knowledge_sources=[recent_news],
    llm=LLM(model="gpt-4", temperature=0.0)
)

# Kullanıcı sorularını işleyen bir görev oluşturun
analysis_task = Task(
    description="Uzay haberleriyle ilgili bu soruyu yanıtlayın: {user_question}",
    expected_output="Yeni uzay haberleri makalelerine göre ayrıntılı bir cevap",
    agent=space_analyst
)

# Mürettebatı oluşturun ve çalıştırın
crew = Crew(
    agents=[space_analyst],
    tasks=[analysis_task],
    verbose=True,
    process=Process.sequential
)

# Örnek kullanım
result = crew.kickoff(
    inputs={"user_question": "Uzay keşfindeki son gelişmeler nelerdir?"}
)
```

## Hata Ayıklama ve Sorun Giderme

### Bilgi Sorunlarını Hata Ayıklama

#### Ajan Bilgi Başlatılmasını Kontrol Etme
```python
from crewai import Agent, Crew, Task
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

knowledge_source = StringKnowledgeSource(
    content="Test bilgisi"
)

agent = Agent(
    role="Test Ajanı",
    goal="Bilgiyi test et",
    backstory="Test",
    knowledge_sources=[knowledge_source]
)

crew = Crew(agents=[agent], tasks=[Task(...)])

# Başlatmadan önce - bilgi başlatılmadı
print(f"Başlatmadan önce - Ajan bilgisi: {getattr(agent, 'knowledge', None)}")

crew.kickoff()

# Başlatmadan sonra - bilgi başlatıldı
print(f"Başlatmadan sonra - Ajan bilgisi: {agent.knowledge}")
print(f"Ajan bilgisi koleksiyonu: {agent.knowledge.storage.collection_name}")
print(f"Kaynak sayısı: {len(agent.knowledge.sources)}")
```

#### Bilgi Depolama Konumlarını Doğrulama
```python
from crewai.utilities.paths import db_storage_path

# Depolama yapısını kontrol edin
storage_path = db_storage_path()
knowledge_path = os.path.join(storage_path, "knowledge")

if os.path.exists(knowledge_path):
    print("Bilgi koleksiyonları bulundu:")
    for collection in os.listdir(knowledge_path):
        collection_path = os.path.join(knowledge_path, collection)
        if os.path.isdir(collection_path):
            print(f"  - {collection}/")
            # Koleksiyon içeriğini göster
            for item in os.listdir(collection_path):
                print(f"    └── {item}")
```

#### Bilgi Alma Testi
```python
# Ajan bilgisi almayı test edin
if hasattr(agent, 'knowledge') and agent.knowledge:
    test_query = ["test sorgusu"]
    results = agent.knowledge.query(test_query)
    print(f"Ajan bilgisi sonuçları: {len(results)} belge bulundu")
    
    # Mürettebat bilgisi almayı test edin (varsa)
    if hasattr(crew, 'knowledge') and crew.knowledge:
        crew_results = crew.query_knowledge(test_query)
        print(f"Mürettebat bilgisi sonuçları: {len(crew_results)} belge bulundu")
```

#### Bilgi Koleksiyonlarını İnceleme
```python
from crewai.utilities.paths import db_storage_path

# CrewAI'nin bilgi ChromaDB'sine bağlanın
knowledge_path = os.path.join(db_storage_path(), "knowledge")

if os.path.exists(knowledge_path):
    client = chromadb.PersistentClient(path=knowledge_path)
    collections = client.list_collections()
    
    print("Bilgi Koleksiyonları:")
    for collection in collections:
        print(f"  - {collection.name}: {collection.count()} belge")
        
        # İçeriği doğrulamak için birkaç belge örneğini gösterin
        if collection.count() > 0:
            sample = collection.peek(limit=2)
            print(f"    Örnek içerik: {sample['documents'][0][:100]}...")
else:
    print("Henüz bir bilgi depolama bulunamadı")
```

#### Bilgi İşleme Kontrolü
```python
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Bir test bilgi kaynağı oluşturun
test_source = StringKnowledgeSource(
    content="Hata ayıklama için test bilgisi içeriği",
    chunk_size=100,  # Test için küçük parçalar
    chunk_overlap=20
)

# Parçalanma davranışını kontrol edin
print(f"Orijinal içerik uzunluğu: {len(test_source.content)}")
print(f"Parça boyutu: {test_source.chunk_size}")
print(f"Parça örtüşmesi: {test_source.chunk_overlap}")

# ve incelemek için işlem ve parça
test_source.add()
print(f"Oluşturulan parça sayısı: {len(test_source.chunks)}")
for i, chunk in enumerate(test_source.chunks[:3]):  # İlk 3 parçayı gösterin
    print(f"Parça {i+1}: {chunk[:50]}...")
```

### Yaygın Bilgi Depolama Sorunları

**"Dosya bulunamadı" hataları:**
```python
# Dosyaların doğru konumda olduğundan emin olun
from crewai.utilities.constants import KNOWLEDGE_DIRECTORY

knowledge_dir = KNOWLEDGE_DIRECTORY  # Genellikle "bilgi"
file_path = os.path.join(knowledge_dir, "your_file.pdf")

if not os.path.exists(file_path):
    print(f"Dosya bulunamadı: {file_path}")
    print(f"Mevcut çalışma dizini: {os.getcwd()}")
    print(f"Beklenen bilgi dizini: {os.path.abspath(knowledge_dir)}")
```

**"Embedding boyut eşleşme hatası" hataları:**
```python
# Bu, embedding sağlayıcılarını değiştirdiğinizde olur
# Eski gömülmeleri temizlemek için bilgi depolamasını sıfırlayın
crew.reset_memories(command_type='knowledge')

# Veya tutarlı embedding sağlayıcıları kullanın
crew = Crew(
    agents=[...],
    tasks=[...],
    knowledge_sources=[...]
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}}
)
```

**"ChromaDB izin reddedildi" hataları:**
```bash
# Depolama izinlerini düzeltin
chmod -R 755 ~/.local/share/CrewAI/
```

**Bilginin çalıştırımlar arasında kalmaması:**
```python
from crewai.utilities.paths import db_storage_path

# Depolama konumunun tutarlılığını doğrulayın
print("CREWAI_STORAGE_DIR:", os.getenv("CREWAI_STORAGE_DIR"))
print("Hesaplanan depolama yolu:", db_storage_path())
print("Bilgi yolu:", os.path.join(db_storage_path(), "knowledge"))
```

### Bilgi Sıfırlama Komutları

```python
# Sadece ajan özelinde bilgiyi sıfırlayın
crew.reset_memories(command_type='agent_knowledge')

# Hem mürettebat hem de ajan bilgisini sıfırlayın
crew.reset_memories(command_type='knowledge')

# CLI komutları
# crewai reset-memories --agent-knowledge  # Sadece ajan bilgisi
# crewai reset-memories --knowledge        # Tüm bilgi
```

### Bilgi Temizleme

Bilginizi temizlemeniz gerekirse, `crewai reset-memories` komutunu `--knowledge` seçeneğiyle kullanabilirsiniz.

```bash Komut
crewai reset-memories --knowledge
```

Bu, bilgi kaynaklarınızı güncellediğinizde ve ajanların en son bilgileri kullandığından emin olmak istediğinizde kullanışlıdır.

## En İyi Uygulamalar

    - İçeriğinizin türü için uygun parça boyutlarını koruyun
    - Bağlamın korunması için içerik örtüşmesini göz önünde bulundurun
    - İlgili bilgileri ayrı bilgi kaynakları halinde düzenleyin

    - İçeriğin karmaşıklığına göre parça boyutlarını ayarlayın
    - Uygun embedding modellerini yapılandırın
    - Daha hızlı işleme için yerel embedding sağlayıcılarını kullanmayı göz önünde bulundurun

    - Tipik CrewAI dosya yapısı tarafından sağlanan yapıyla, bilgi kaynakları her kickoff tetiklendiğinde yerleştirilir.
    - Bilgi kaynakları büyükse bu, aynı verinin her seferinde gömülerek verimsizliğe ve artan gecikmeye yol açar.
    - Bunu çözmek için bilgiyi parametreler yerine bilgi_kaynakları parametresi aracılığıyla doğrudan başlatın.
    - Tam fikri edinmek için [Github Sorunu](https://github.com/crewAIInc/crewAI/issues/2755) bağlantısına bakın

    - Rol bazlı bilgi için ajan seviyesinde bilgi kullanın
    - Tüm ajanların ihtiyaç duyduğu paylaşılan bilgi için mürettebat seviyesinde bilgi kullanın
    - Farklı gömme stratejileri için ajan seviyesinde embedder'ları ayarlayın
    - Ajan rollerini tanımlayıcı olacak şekilde koleksiyon adlandırma konusunda tutarlı olun
    - Ajan.knowledge'ı kickoff'tan sonra kontrol ederek bilgi başlatılmasını test edin
    - Bilginin nerede depolandığını anlamak için depolama konumlarını izleyin
    - Bilgiyi doğru komut türleriyle uygun şekilde sıfırlayın

    - Üretimde `CREWAI_STORAGE_DIR`'i bilinen bir konuma ayarlayın
    - API anahtarı ve hassas yapılandırma için örtülü API anahtarlarından kaçınarak tutarlı embedding sağlayıcıları seçin
    - Belge eklemeleriyle büyüdükçe bilgi depolama boyutunu izleyin
    - Amaç veya amaçla bilgi kaynaklarını düzenleyin ve koleksiyon adları kullanın
    - Bilgi dizinlerini yedekleme ve dağıtım stratejilerinizde dahil edin
    - Bilgi dosyaları ve depolama dizinleri için uygun dosya izinlerini ayarlayın
    - API anahtarları ve hassas yapılandırmalar için ortam değişkenlerini kullanın

