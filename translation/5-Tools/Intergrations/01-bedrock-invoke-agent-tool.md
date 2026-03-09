# Bedrock Ajan Çağırma Aracı (Bedrock Invoke Agent Tool)

> CrewAI ajanlarının Amazon Bedrock Ajanlarını çağırmasına ve yeteneklerinden iş akışlarınızda yararlanmasına olanak tanır.

# `BedrockInvokeAgentTool`

`BedrockInvokeAgentTool`, CrewAI ajanlarının Amazon Bedrock Ajanlarını çağırmasını ve bu ajanların yeteneklerini iş akışlarınızda kullanmasını sağlar.

## Kurulum

```bash  theme={null}
uv pip install 'crewai[tools]'
```

## Gereksinimler

* Yapılandırılmış AWS kimlik bilgileri (ortam değişkenleri veya AWS CLI aracılığıyla)
* `boto3` ve `python-dotenv` paketleri
* Amazon Bedrock Ajanlarına erişim

## Kullanım

Aracın bir CrewAI ajanıyla nasıl kullanılacağı aşağıda açıklanmıştır:

```python {2, 4-8} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.bedrock.agents.invoke_agent_tool import BedrockInvokeAgentTool

# Aracı başlatın
agent_tool = BedrockInvokeAgentTool(
    agent_id="ajan-id-niz",
    agent_alias_id="ajan-takma-ad-id-niz"
)

# Aracı kullanan bir CrewAI ajanı oluşturun
aws_expert = Agent(
    role='AWS Servis Uzmanı',
    goal='Kullanıcıların AWS servislerini ve kotalarını anlamalarına yardımcı ol',
    backstory='AWS servisleri konusunda uzmanım ve bunlar hakkında detaylı bilgi sağlayabilirim.',
    tools=[agent_tool],
    verbose=True
)

# Ajan için bir görev oluşturun
quota_task = Task(
    description="us-west-2 bölgesindeki EC2 için mevcut servis kotalarını bul ve son değişiklikleri açıkla.",
    agent=aws_expert
)

# Ajanla bir ekip oluşturun
crew = Crew(
    agents=[aws_expert],
    tasks=[quota_task],
    verbose=2
)

# Ekibi çalıştırın
result = crew.kickoff()
print(result)
```

## Araç Argümanları

| Argüman              | Tip    | Zorunlu | Varsayılan | Açıklama                                     |
| :------------------- | :----- | :------ | :--------- | :------------------------------------------- |
| **agent\_id**        | `str`  | Evet    | Yok        | Bedrock ajanının benzersiz tanımlayıcısı     |
| **agent\_alias\_id** | `str`  | Evet    | Yok        | Ajan takma adının benzersiz tanımlayıcısı    |
| **session\_id**      | `str`  | Hayır   | zaman damgası | Oturumun benzersiz tanımlayıcısı             |
| **enable\_trace**    | `bool` | Hayır   | False      | Hata ayıklama için izlemeyi (trace) etkinleştirir |
| **end\_session**     | `bool` | Hayır   | False      | Çağrıdan sonra oturumun sonlandırılıp sonlandırılmayacağı |
| **description**      | `str`  | Hayır   | Yok        | Araç için özel açıklama                      |

## Ortam Değişkenleri

```bash  theme={null}
BEDROCK_AGENT_ID=ajan-id-niz             # agent_id geçirmeye alternatif
BEDROCK_AGENT_ALIAS_ID=ajan-takma-ad-id-niz # agent_alias_id geçirmeye alternatif
AWS_REGION=aws-bolgeniz                  # Varsayılan: us-west-2
AWS_ACCESS_KEY_ID=erisim-anahtariniz     # AWS kimlik doğrulaması için gereklidir
AWS_SECRET_ACCESS_KEY=gizli-anahtariniz    # AWS kimlik doğrulaması için gereklidir
```

## Gelişmiş Kullanım

### Oturum Yönetimi ile Çoklu Ajan İş Akışı

```python {2, 4-22} theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools.aws.bedrock.agents.invoke_agent_tool import BedrockInvokeAgentTool

# Oturum yönetimi ile araçları başlatın
initial_tool = BedrockInvokeAgentTool(
    agent_id="ajan-id-niz",
    agent_alias_id="ajan-takma-ad-id-niz",
    session_id="ozel-oturum-id"
)

followup_tool = BedrockInvokeAgentTool(
    agent_id="ajan-id-niz",
    agent_alias_id="ajan-takma-ad-id-niz",
    session_id="ozel-oturum-id"
)

final_tool = BedrockInvokeAgentTool(
    agent_id="ajan-id-niz",
    agent_alias_id="ajan-takma-ad-id-niz",
    session_id="ozel-oturum-id",
    end_session=True
)

# Farklı aşamalar için ajanlar oluşturun
researcher = Agent(
    role='AWS Servis Araştırmacısı',
    goal='AWS servisleri hakkında bilgi topla',
    backstory='Detaylı AWS servis bilgisi bulma konusunda uzmanım.',
    tools=[initial_tool]
)

analyst = Agent(
    role='Servis Uyumluluk Analisti',
    goal='Servis uyumluluğunu ve gereksinimlerini analiz et',
    backstory='AWS servislerini uyumluluk ve entegrasyon olanakları açısından analiz ederim.',
    tools=[followup_tool]
)

summarizer = Agent(
    role='Teknik Dokümantasyon Yazarı',
    goal='Net teknik özetler oluştur',
    backstory='Net ve özlü teknik dokümantasyon oluşturma konusunda uzmanım.',
    tools=[final_tool]
)

# Görevleri oluşturun
research_task = Task(
    description="us-west-2 bölgesindeki tüm mevcut AWS servislerini bul.",
    agent=researcher
)

analysis_task = Task(
    description="Hangi servislerin IPv6'yı desteklediğini ve uygulama gereksinimlerini analiz et.",
    agent=analyst
)

summary_task = Task(
    description="IPv6 uyumlu servislerin ve temel özelliklerinin özetini oluştur.",
    agent=summarizer
)

# Ajanlar ve görevlerle bir ekip oluşturun
crew = Crew(
    agents=[researcher, analyst, summarizer],
    tasks=[research_task, analysis_task, summary_task],
    process=Process.sequential,
    verbose=2
)

# Ekibi çalıştırın
result = crew.kickoff()
```

## Kullanım Durumları

### Hibrit Çoklu Ajan İşbirlikleri

* CrewAI ajanlarının AWS'de servis olarak çalışan yönetilen Bedrock ajanlarıyla işbirliği yaptığı iş akışları oluşturun.
* Hassas veri işlemenin AWS ortamınızda gerçekleştiği, diğer ajanların harici olarak çalıştığı senaryoları etkinleştirin.
* Dağıtılmış zeka iş akışları için şirket içi CrewAI ajanlarını bulut tabanlı Bedrock ajanlarıyla bağlayın.

### Veri Egemenliği ve Uyumluluk

* Veriye duyarlı ajan iş akışlarını AWS ortamınızda tutarken harici CrewAI ajanlarının görevleri koordine etmesine olanak tanıyın.
* Hassas bilgileri yalnızca AWS hesabınız içinde işleyerek veri barındırma gereksinimlerine uyumluluğu sürdürün.
* Bazı ajanların kuruluşunuzun özel verilerine erişemediği güvenli çoklu ajan işbirlikleri sağlayın.

### Sorunsuz AWS Servis Entegrasyonu

* Karmaşık entegrasyon kodları yazmadan Amazon Bedrock Eylemleri aracılığıyla herhangi bir AWS servisine erişin.
* CrewAI ajanlarının doğal dil istekleri aracılığıyla AWS servisleriyle etkileşim kurmasını sağlayın.
* Bedrock Bilgi Tabanları, Lambda ve daha fazlası gibi AWS servisleriyle etkileşim kurmak için önceden oluşturulmuş Bedrock ajan yeteneklerinden yararlanın.

### Ölçeklenebilir Hibrit Ajan Mimarileri

* Hesaplama açısından yoğun görevleri yönetilen Bedrock ajanlarına devrederken, hafif görevleri CrewAI'de çalıştırın.
* İş yüklerini yerel CrewAI ajanları ve bulut tabanlı Bedrock ajanları arasında dağıtarak ajan işlemeyi ölçeklendirin.

### Kuruluşlar Arası Ajan İşbirliği

* Kuruluşunuzun CrewAI ajanları ile ortak kuruluşların Bedrock ajanları arasında güvenli işbirliği sağlayın.
* Hassas verileri ifşa etmeden Bedrock ajanlarından gelen harici uzmanlığın dahil edilebileceği iş akışları oluşturun.
* Güvenliği ve veri kontrolünü korurken kuruluş sınırlarını aşan ajan ekosistemleri oluşturun.
