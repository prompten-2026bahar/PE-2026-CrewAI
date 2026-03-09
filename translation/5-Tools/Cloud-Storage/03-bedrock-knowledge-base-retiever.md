# Bedrock Bilgi Tabanı Getirici (Bedrock Knowledge Base Retriever)

> Doğal dil sorgularını kullanarak Amazon Bedrock Bilgi Tabanlarından bilgi getirin.

# `BedrockKBRetrieverTool`

`BedrockKBRetrieverTool`, CrewAI ajanlarının doğal dil sorguları kullanarak Amazon Bedrock Bilgi Tabanlarından (Knowledge Bases) bilgi getirmesini sağlar.

## Kurulum

```bash  theme={null}
uv pip install 'crewai[tools]'
```

## Gereksinimler

* Yapılandırılmış AWS kimlik bilgileri (ortam değişkenleri veya AWS CLI aracılığıyla)
* `boto3` ve `python-dotenv` paketleri
* Amazon Bedrock Bilgi Tabanına erişim

## Kullanım

Aracın bir CrewAI ajanıyla nasıl kullanılacağı aşağıda açıklanmıştır:

```python {2, 4-17} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.bedrock.knowledge_base.retriever_tool import BedrockKBRetrieverTool

# Aracı başlatın
kb_tool = BedrockKBRetrieverTool(
    knowledge_base_id="bilgi-tabani-id-niz",
    number_of_results=5
)

# Aracı kullanan bir CrewAI ajanı oluşturun
researcher = Agent(
    role='Bilgi Tabanı Araştırmacısı',
    goal='Şirket politikaları hakkında bilgi bul',
    backstory='Şirket dökümantasyonunu getirme ve analiz etme konusunda uzmanlaşmış bir araştırmacıyım.',
    tools=[kb_tool],
    verbose=True
)

# Ajan için bir görev oluşturun
research_task = Task(
    description="Şirketimizin uzaktan çalışma politikasını bul ve temel noktaları özetle.",
    agent=researcher
)

# Ajanla bir ekip oluşturun
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=2
)

# Ekibi çalıştırın
result = crew.kickoff()
print(result)   
```

## Araç Argümanları

| Argüman                      | Tip    | Zorunlu  | Varsayılan | Açıklama                                                                    |
| :--------------------------- | :----- | :------- | :--------- | :-------------------------------------------------------------------------- |
| **knowledge\_base\_id**      | `str`  | Evet     | Yok        | Bilgi tabanının benzersiz tanımlayıcısı (0-10 alfasayısal karakter)         |
| **number\_of\_results**      | `int`  | Hayır    | 5          | Döndürülecek maksimum sonuç sayısı                                          |
| **retrieval\_configuration** | `dict` | Hayır    | Yok        | Bilgi tabanı sorgusu için özel yapılandırmalar                              |
| **guardrail\_configuration** | `dict` | Hayır    | Yok        | İçerik filtreleme ayarları                                                  |
| **next\_token**              | `str`  | Hayır    | Yok        | Sayfalandırma (pagination) için belirteç                                    |

## Ortam Değişkenleri

```bash  theme={null}
BEDROCK_KB_ID=bilgi-tabani-id-niz      # knowledge_base_id geçirmeye alternatif
AWS_REGION=aws-bolgeniz               # Varsayılan: us-east-1
AWS_ACCESS_KEY_ID=erisim-anahtariniz   # AWS kimlik doğrulaması için gereklidir
AWS_SECRET_ACCESS_KEY=gizli-anahtariniz # AWS kimlik doğrulaması için gereklidir
```

## Yanıt Formatı

Araç, sonuçları JSON formatında döndürür:

```json  theme={null}
{
  "results": [
    {
      "content": "Getirilen metin içeriği",
      "content_type": "text",
      "source_type": "S3",
      "source_uri": "s3://bucket/belge.pdf",
      "score": 0.95,
      "metadata": {
        "ek": "metaveri"
      }
    }
  ],
  "nextToken": "sayfalandirma-belirteci",
  "guardrailAction": "NONE"
}
```

## Gelişmiş Kullanım

### Özel Veri Getirme Yapılandırması

```python  theme={null}
kb_tool = BedrockKBRetrieverTool(
    knowledge_base_id="bilgi-tabani-id-niz",
    retrieval_configuration={
        "vectorSearchConfiguration": {
            "numberOfResults": 10,
            "overrideSearchType": "HYBRID"
        }
    }
)

policy_expert = Agent(
    role='Politika Uzmanı',
    goal='Şirket politikalarını ayrıntılı olarak analiz et',
    backstory='Düzenleyici gereklilikler konusunda derin bilgiye sahip kurumsal politika analizi uzmanıyım.',
    tools=[kb_tool]
)
```

## Desteklenen Veri Kaynakları

* Amazon S3
* Confluence
* Salesforce
* SharePoint
* Web sayfaları
* Özel belge konumları
* Amazon Kendra
* SQL veritabanları

## Kullanım Durumları

### Kurumsal Bilgi Entegrasyonu

* Hassas verileri ifşa etmeden CrewAI ajanlarının kuruluşunuzun tescilli bilgilerine erişmesini sağlayın.
* Ajanların şirketinizin özel politikalarına, prosedürlerine ve dökümantasyonuna dayalı kararlar almasına olanak tanıyın.
* Veri güvenliğini korurken dahili dökümantasyonunuza dayalı soruları yanıtlayabilen ajanlar oluşturun.

### Uzmanlık Alanı Bilgisi

* Modelleri yeniden eğitmeden CrewAI ajanlarını alana özgü (hukuki, tıbbi, teknik) bilgi tabanlarına bağlayın.
* AWS ortamınızda halihazırda tutulan mevcut bilgi depolarından yararlanın.
* CrewAI'nin akıl yürütme yeteneğini bilgi tabanlarınızdaki alana özgü bilgilerle birleştirin.

### Veriye Dayalı Karar Verme

* CrewAI ajanı yanıtlarını genel bilgiler yerine gerçek şirket verilerinize dayandırın.
* Ajanların özel iş bağlamınıza ve dökümantasyonunuza dayalı öneriler sunmasını sağlayın.
* Bilgi tabanlarınızdan gerçek bilgileri getirerek halüsinasyonları (hallucinations) azaltın.

### Ölçeklenebilir Bilgi Erişimi

* Hepsini modellerinize gömmeden terabaytlarca kurumsal bilgiye erişin.
* Yalnızca belirli görevler için gereken ilgili bilgileri dinamik olarak sorgulayın.
* Büyük bilgi tabanlarını verimli bir şekilde yönetmek için AWS'nin ölçeklenebilir altyapısından yararlanın.

### Uyumluluk ve Yönetişim

* CrewAI ajanlarının şirketinizin onaylı dökümantasyonuyla uyumlu yanıtlar vermesini sağlayın.
* Ajanlarınız tarafından kullanılan bilgi kaynaklarının denetlenebilir izlerini oluşturun.
* Ajanlarınızın hangi bilgi kaynaklarına erişebileceği üzerinde kontrol sahibi olun.
