# Merge Ajan Yöneticisi Aracı (Merge Agent Handler Tool)

> CrewAI ajanlarının, Merge'ün Ajan Yöneticisi (Agent Handler) platformu aracılığıyla Linear, GitHub, Slack ve daha fazlası gibi üçüncü taraf entegrasyonlara güvenli bir şekilde erişmesini sağlar.

# `MergeAgentHandlerTool`

`MergeAgentHandlerTool`, CrewAI ajanlarının [Merge'ün Ajan Yöneticisi](https://www.merge.dev/products/merge-agent-handler) platformu aracılığıyla üçüncü taraf entegrasyonlara güvenli bir şekilde erişmesine olanak tanır. Ajan Yöneticisi; Linear, GitHub, Slack, Notion ve yüzlerce diğer popüler araca —hepsi yerleşik kimlik doğrulama, izinler ve izleme özellikleriyle donatılmış— önceden oluşturulmuş, güvenli konektörler sağlar.

## Kurulum

```bash  theme={null}
uv pip install 'crewai[tools]'
```

## Gereksinimler

* Yapılandırılmış bir Araç Paketi (Tool Pack) ile Merge Ajan Yöneticisi hesabı
* Ajan Yöneticisi API anahtarı
* Araç Paketinize bağlı en az bir kayıtlı kullanıcı
* Araç Paketinizde yapılandırılmış üçüncü taraf entegrasyonlar

## Ajan Yöneticisine Başlangıç

1. [ah.merge.dev/signup](https://ah.merge.dev/signup) adresinden bir Merge Ajan Yöneticisi hesabı için **kaydolun**.
2. Bir **Araç Paketi oluşturun** ve ihtiyacınız olan entegrasyonları yapılandırın.
3. Üçüncü taraf servislerle kimlik doğrulaması yapacak **kullanıcıları kaydedin**.
4. Ajan Yöneticisi panelinden **API anahtarınızı alın**.
5. **Ortam değişkenini ayarlayın**: `export AGENT_HANDLER_API_KEY='anahtariniz-buraya'`
6. CrewAI'de MergeAgentHandlerTool ile **geliştirmeye başlayın**.

## Notlar

* Araç Paketi ID'leri (Tool Pack IDs) ve Kayıtlı Kullanıcı ID'leri (Registered User IDs) Ajan Yöneticisi panelinizde bulunabilir veya API aracılığıyla oluşturulabilir.
* Araç, Ajan Yöneticisi ile iletişim kurmak için Model Bağlam Protokolü'nü (MCP) kullanır.
* Oturum ID'leri (Session IDs) otomatik olarak oluşturulur ancak bağlam kalıcılığı için özelleştirilebilir.
* Tüm araç çağrıları, Ajan Yöneticisi platformu üzerinden günlüğe kaydedilir ve denetlenebilir.
* Araç parametreleri, Ajan Yöneticisi API'sinden dinamik olarak keşfedilir ve otomatik olarak doğrulanır.

## Kullanım

### Tek Araç Kullanımı

Araç Paketinizden belirli bir aracı şu şekilde kullanabilirsiniz:

```python {2, 4-9} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

# Linear'da sorun oluşturma için bir araç oluşturun
linear_create_tool = MergeAgentHandlerTool.from_tool_name(
    tool_name="linear__create_issue",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa"
)

# Aracı kullanan bir CrewAI ajanı oluşturun
project_manager = Agent(
    role='Proje Yöneticisi',
    goal='Proje görevlerini ve sorunları verimli bir şekilde yönet',
    backstory='Proje çalışmalarını takip etme ve eyleme dönüştürülebilir görevler oluşturma konusunda uzmanım.',
    tools=[linear_create_tool],
    verbose=True
)

# Ajan için bir görev oluşturun
create_issue_task = Task(
    description="Linear'da 'Kullanıcı kimlik doğrulamasını uygula' başlıklı, gereksinimlerin detaylı bir açıklamasını içeren yeni bir yüksek öncelikli sorun oluştur.",
    agent=project_manager,
    expected_output="Sorunun ID'si ile birlikte oluşturulduğuna dair onay"
)

# Ajanla bir ekip oluşturun
crew = Crew(
    agents=[project_manager],
    tasks=[create_issue_task],
    verbose=True
)

# Ekibi çalıştırın
result = crew.kickoff()
print(result)
```

### Bir Araç Paketinden Birden Fazla Aracı Yükleme

Araç Paketinizdeki tüm mevcut araçları tek seferde yükleyebilirsiniz:

```python {2, 4-8} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

# Araç Paketindeki tüm araçları yükleyin
tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa"
)

# Tüm araçlara erişimi olan bir ajan oluşturun
automation_expert = Agent(
    role='Otomasyon Uzmanı',
    goal='Birden fazla platformda iş akışlarını otomatikleştir',
    backstory='İşleri halletmek için araç kutusundaki her araçla çalışabilirim.',
    tools=tools,
    verbose=True
)

automation_task = Task(
    description="Linear'daki yüksek öncelikli sorunları kontrol et ve Slack'e bir özet gönder.",
    agent=automation_expert
)

crew = Crew(
    agents=[automation_expert],
    tasks=[automation_task],
    verbose=True
)

result = crew.kickoff()
```

### Sadece Belirli Araçları Yükleme

Sadece ihtiyacınız olan araçları yükleyin:

```python {2, 4-10} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

# Araç Paketinden belirli araçları yükleyin
selected_tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    tool_names=["linear__create_issue", "linear__get_issues", "slack__post_message"]
)

developer_assistant = Agent(
    role='Geliştirici Asistanı',
    goal='Geliştiricilerin çalışmalarını takip etmelerine ve iletişim kurmalarına yardımcı ol',
    backstory='Geliştiricilerin düzenli kalmasına ve ekibi bilgilendirmesine yardımcı olurum.',
    tools=selected_tools,
    verbose=True
)

daily_update_task = Task(
    description="Linear'da mevcut kullanıcıya atanan tüm sorunları getir ve #dev-updates Slack kanalına bir özet gönder.",
    agent=developer_assistant
)

crew = Crew(
    agents=[developer_assistant],
    tasks=[daily_update_task],
    verbose=True
)

result = crew.kickoff()
```

## Araç Argümanları

### `from_tool_name()` Metodu

| Argüman                  | Tip   | Zorunlu | Varsayılan                                              | Açıklama                                                           |
| :----------------------- | :---- | :------ | :------------------------------------------------------ | :----------------------------------------------------------------- |
| **tool\_name**           | `str` | Evet    | Yok                                                     | Kullanılacak özel aracın adı (örn. "linear\_\_create\_issue")      |
| **tool\_pack\_id**       | `str` | Evet    | Yok                                                     | Ajan Yöneticisi Araç Paketinizin UUID'si                           |
| **registered\_user\_id** | `str` | Evet    | Yok                                                     | Kayıtlı kullanıcının UUID'si veya origin\_id'si                    |
| **base\_url**            | `str` | Hayır   | "[https://ah-api.merge.dev](https://ah-api.merge.dev)"  | Ajan Yöneticisi API'si için temel URL                              |
| **session\_id**          | `str` | Hayır   | Otomatik oluşturulur                                    | Bağlamı korumak için MCP oturum ID'si                              |

### `from_tool_pack()` Metodu

| Argüman                  | Tip         | Zorunlu | Varsayılan                                              | Açıklama                                                        |
| :----------------------- | :---------- | :------ | :------------------------------------------------------ | :-------------------------------------------------------------- |
| **tool\_pack\_id**       | `str`       | Evet    | Yok                                                     | Ajan Yöneticisi Araç Paketinizin UUID'si                        |
| **registered\_user\_id** | `str`       | Evet    | Yok                                                     | Kayıtlı kullanıcının UUID'si veya origin\_id'si                 |
| **tool\_names**          | `list[str]` | Hayır   | Yok                                                     | Yüklenecek özel araç adları. Yoksa tüm mevcut araçları yükler   |
| **base\_url**            | `str`       | Hayır   | "[https://ah-api.merge.dev](https://ah-api.merge.dev)"  | Ajan Yöneticisi API'si için temel URL                           |

## Ortam Değişkenleri

```bash  theme={null}
AGENT_HANDLER_API_KEY=api_anahtariniz_buraya  # Kimlik doğrulama için gereklidir
```

## Gelişmiş Kullanım

### Farklı Araç Erişimi ile Çoklu Ajan İş Akışı

```python {2, 4-20} theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MergeAgentHandlerTool

# Farklı ajanlar için uzmanlaşmış araçlar oluşturun
github_tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    tool_names=["github__create_pull_request", "github__get_pull_requests"]
)

linear_tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    tool_names=["linear__create_issue", "linear__update_issue"]
)

slack_tool = MergeAgentHandlerTool.from_tool_name(
    tool_name="slack__post_message",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa"
)

# Uzman ajanlar oluşturun
code_reviewer = Agent(
    role='Kod İnceleyici',
    goal='Pull request'leri incele ve kod kalitesini sağla',
    backstory='Kod değişikliklerini inceleme ve yapıcı geri bildirim sağlama konusunda uzmanım.',
    tools=github_tools
)

task_manager = Agent(
    role='Görev Yöneticisi',
    goal='Kod değişikliklerine göre proje görevlerini takip et ve güncelle',
    backstory='Proje panosunu en son geliştirme ilerlemesiyle güncel tutarım.',
    tools=linear_tools
)

communicator = Agent(
    role='Ekip İletişimcisi',
    goal='Önemli güncellemeler hakkında ekibi bilgilendir',
    backstory='Projede neler olup bittiğini herkesin bildiğinden emin olurum.',
    tools=[slack_tool]
)

# Ardışık görevler oluşturun
review_task = Task(
    description="'api-service' deposundaki tüm açık pull request'leri incele ve dikkat gerektirenleri belirle.",
    agent=code_reviewer,
    expected_output="İncelenmesi gereken veya sorunlu pull request listesi"
)

update_task = Task(
    description="Pull request inceleme bulgularına göre Linear sorunlarını güncelle. Tamamlanan PR'ları 'done' olarak işaretle.",
    agent=task_manager,
    expected_output="Güncellenen Linear sorunlarının özeti"
)

notify_task = Task(
    description="Bugünkü kod incelemesi ve görev güncellemelerinin özetini #engineering Slack kanalına gönder.",
    agent=communicator,
    expected_output="Mesajın gönderildiğine dair onay"
)

# Ardışık işlemeli bir ekip oluşturun
crew = Crew(
    agents=[code_reviewer, task_manager, communicator],
    tasks=[review_task, update_task, notify_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
```

### Özel Oturum Yönetimi

Oturum ID'lerini kullanarak birden fazla araç çağrısı arasında bağlamı koruyun:

```python {2, 4-17} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

# Bağlamı korumak için aynı oturum ID'sine sahip araçlar oluşturun
session_id = "proje-sprint-planlama-2024"

create_tool = MergeAgentHandlerTool(
    name="linear_create_issue",
    description="Linear'da yeni bir sorun oluşturur",
    tool_name="linear__create_issue",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    session_id=session_id
)

update_tool = MergeAgentHandlerTool(
    name="linear_update_issue",
    description="Linear'da mevcut bir sorunu günceller",
    tool_name="linear__update_issue",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    session_id=session_id
)

sprint_planner = Agent(
    role='Sprint Planlayıcısı',
    goal='Sprint görevlerini planla ve düzenle',
    backstory='Ekiplerin iyi tanımlanmış görevlerle etkili sprintler planlamasına yardımcı olurum.',
    tools=[create_tool, update_tool],
    verbose=True
)

planning_task = Task(
    description="Kimlik doğrulama özelliği için 5 sprint görevi oluştur ve bağımlılıklara göre önceliklerini ayarla.",
    agent=sprint_planner
)

crew = Crew(
    agents=[sprint_planner],
    tasks=[planning_task],
    verbose=True
)

result = crew.kickoff()
```

## Kullanım Durumları

### Birleşik Entegrasyon Erişimi

* Birden fazla SDK yönetmeden tek bir birleşik API üzerinden yüzlerce üçüncü taraf araca erişin.
* Ajanların Linear, GitHub, Slack, Notion, Jira, Asana ve daha fazlasıyla tek bir entegrasyon noktasından çalışmasını sağlayın.
* Kimlik doğrulama ve API sürüm yönetimini Ajan Yöneticisi'ne devrederek entegrasyon karmaşıklığını azaltın.

### Güvenli Kurumsal İş Akışları

* Tüm üçüncü taraf entegrasyonlar için yerleşik kimlik doğrulama ve izin yönetiminden yararlanın.
* Merkezi erişim kontrolü ve denetim günlüğü ile kurumsal güvenlik standartlarını koruyun.
* Ajanların, API anahtarlarını veya kimlik bilgilerini kod içinde ifşa etmeden şirket araçlarına erişmesini sağlayın.

### Platformlar Arası Otomasyon

* Birden fazla platformu kapsayan iş akışları oluşturun (örn. Linear görevlerinden GitHub sorunları oluşturun, Notion sayfalarını Slack ile senkronize edin).
* Teknoloji yığınınızdaki farklı araçlar arasında sorunsuz veri akışı sağlayın.
* Farklı platformlar arasındaki bağlamı anlayan akıllı otomasyonlar oluşturun.

### Dinamik Araç Keşfi

* Entegrasyon mantığını doğrudan kodlamadan çalışma zamanında (runtime) tüm mevcut araçları yükleyin.
* Araç Paketinize yeni araçlar eklendikçe ajanların bunları keşfetmesini ve kullanmasını sağlayın.
* Değişen araç mevcudiyetine uyum sağlayabilen esnek ajanlar oluşturun.

### Kullanıcıya Özel Araç Erişimi

* Farklı kullanıcılar farklı araç izinlerine ve erişim seviyelerine sahip olabilir.
* Ajanların belirli kullanıcılar adına hareket ettiği çok kiracılı (multi-tenant) iş akışlarını etkinleştirin.
* Tüm araç eylemleri için uygun niteliklendirme ve izinleri sürdürün.

## Mevcut Entegrasyonlar

Merge Ajan Yöneticisi, birden fazla kategoride yüzlerce entegrasyonu destekler:

* **Proje Yönetimi**: Linear, Jira, Asana, Monday.com, ClickUp
* **Kod Yönetimi**: GitHub, GitLab, Bitbucket
* **İletişim**: Slack, Microsoft Teams, Discord
* **Dokümantasyon**: Notion, Confluence, Google Docs
* **CRM**: Salesforce, HubSpot, Pipedrive
* **Ve çok daha fazlası...**

Mevcut entegrasyonların tam listesi için [Merge Ajan Yöneticisi dökümantasyonunu](https://docs.ah.merge.dev/) ziyaret edin.

## Hata Yönetimi

Araç kapsamlı hata yönetimi sağlar:

* **Kimlik Doğrulama Hataları**: Geçersiz veya eksik API anahtarları.
* **İzin Hataları**: Kullanıcının talep edilen eylem için izni olmaması.
* **API Hataları**: Ajan Yöneticisi veya üçüncü taraf servislerle iletişim sorunları.
* **Doğrulama Hataları**: Araç metotlarına iletilen geçersiz parametreler.

Tutarlı hata yönetimi için tüm hatalar `MergeAgentHandlerToolError` içine sarmalanır.
