# Genel Bakış

> CrewAI ajanlarını harici otomasyonlar ve yönetilen yapay zeka servisleriyle bağlayın.

Entegrasyon araçları, ajanlarınızın işleri diğer otomasyon platformlarına ve yönetilen yapay zeka servislerine devretmesine olanak tanır. Bir iş akışının mevcut bir CrewAI dağıtımını çağırması veya Amazon Bedrock gibi sağlayıcılara özel görevler ataması gerektiğinde bunları kullanın.

## **Mevcut Araçlar**

- **[Merge Agent Handler Tool](/en/tools/integration/mergeagenthandlertool)**: Merge'ün birleşik API'si aracılığıyla Linear, GitHub, Slack ve daha fazlası gibi yüzlerce üçüncü taraf araca güvenli bir şekilde erişin.
- **[CrewAI Run Automation Tool](/en/tools/integration/crewaiautomationtool)**: Canlı CrewAI Platformu otomasyonlarını çağırın, özel girişler iletin ve sonuçları doğrudan ajanınızdan takip edin.
- **[Bedrock Invoke Agent Tool](/en/tools/integration/bedrockinvokeagenttool)**: Ekiplerinizden Amazon Bedrock Ajanlarını çağırın, AWS güvenlik duvarlarını (guardrails) yeniden kullanın ve yanıtları iş akışına aktarın.

## **Genel Kullanım Durumları**

* **Zincirleme Otomasyonlar**: Mevcut bir CrewAI dağıtımını başka bir ekip veya akış içinden başlatın.
* **Kurumsal Devir**: Görevleri, şirket mantığını ve güvenlik prosedürlerini halizade içeren Bedrock Ajanlarına yönlendirin.
* **Hibrit İş Akışları**: CrewAI'nin akıl yürütme yeteneğini, kendi ajan API'lerini sunan alt sistemlerle birleştirin.
* **Uzun Süreli İşler**: Harici otomasyonları takip edin ve nihai sonuçları mevcut çalışmaya geri dahil edin.

## **Hızlı Başlangıç Örneği**

```python  theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import InvokeCrewAIAutomationTool
from crewai_tools.aws.bedrock.agents.invoke_agent_tool import BedrockInvokeAgentTool

# Harici otomasyon
analysis_automation = InvokeCrewAIAutomationTool(
    crew_api_url="https://analysis-crew.acme.crewai.com",
    crew_bearer_token="BEARER_TOKENINIZ",
    crew_name="Analiz Otomasyonu",
    crew_description="Üretim seviyesindeki analiz hattını çalıştırır",
)

# Bedrock üzerindeki yönetilen ajan
knowledge_router = BedrockInvokeAgentTool(
    agent_id="bedrock-agent-id",
    agent_alias_id="prod",
)

automation_strategist = Agent(
    role="Otomasyon Stratejisti",
    goal="Harici otomasyonları yönet ve çıktılarını özetle",
    backstory="Kurumsal iş akışlarını koordine edersiniz ve görevleri ne zaman uzman servislere devredeceğinizi bilirsiniz.",
    tools=[analysis_automation, knowledge_router],
    verbose=True,
)

execute_playbook = Task(
    description="Analiz otomasyonunu çalıştırın ve Bedrock ajanından yönetici özeti isteyin.",
    agent=automation_strategist,
)

Crew(agents=[automation_strategist], tasks=[execute_playbook]).kickoff()
```

## **En İyi Uygulamalar (Best Practices)**

* **Güvenli Kimlik Bilgileri**: API anahtarlarını ve taşıyıcı belirteçleri (bearer tokens) ortam değişkenlerinde veya bir sırlar yöneticisinde (secrets manager) saklayın.
* **Gecikme Planı**: Harici otomasyonlar daha uzun sürebilir; uygun yoklama (polling) aralıkları ve zaman aşımları ayarlayın.
* **Oturumları Yeniden Kullanma**: Bedrock Ajanları oturum ID'lerini destekler, böylece birden fazla araç çağrısı arasında bağlamı koruyabilirsiniz.
* **Yanıtları Doğrulayın**: Uzak çıktıları (JSON, metin, durum kodları) alt görevlere iletmeden önce normalize edin.
* **Kullanımı İzleyin**: Kota sınırlarının ve hataların önünde kalmak için CrewAI Platformu veya AWS CloudWatch'taki denetim günlüklerini takip edin.
