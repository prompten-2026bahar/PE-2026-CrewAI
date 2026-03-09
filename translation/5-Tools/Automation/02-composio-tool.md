# Composio Aracı

> Composio, esnek kimlik doğrulama yönetimi (authentication management) ile yapay zeka ajanları için üretime hazır 250'den fazla araç sunar.

# `ComposioToolSet`

## Açıklama

Composio, yapay zeka ajanlarınızı 250'den fazla araca bağlamanıza olanak tanıyan bir entegrasyon platformudur. Temel özellikleri şunlardır:

* **Kurumsal Seviyede Kimlik Doğrulama**: Otomatik belirteç (token) yenileme ile OAuth, API Anahtarları ve JWT için yerleşik destek.
* **Tam Gözlemlenebilirlik**: Ayrıntılı araç kullanım günlükleri (logs), yürütme zaman damgaları ve daha fazlası.

## Kurulum

Composio araçlarını projenize dahil etmek için aşağıdaki talimatları izleyin:

```shell  theme={null}
pip install composio composio-crewai
pip install crewai
```

Kurulum tamamlandıktan sonra Composio API anahtarınızı `COMPOSIO_API_KEY` olarak ayarlayın. Composio API anahtarınızı [buradan](https://platform.composio.dev) alabilirsiniz.

## Örnek

Aşağıdaki örnek, aracın nasıl başlatılacağını ve bir GitHub eyleminin nasıl yürütüleceğini gösterir:

1. Composio'yu CrewAI Sağlayıcısı ile Başlatın

```python Code theme={null}
from composio_crewai import ComposioProvider
from composio import Composio
from crewai import Agent, Task, Crew

composio = Composio(provider=ComposioProvider())
```

2. Yeni bir Composio Oturumu (Session) oluşturun ve araçları alın

```python  theme={null}
session = composio.create(
    user_id="kullanici-id-niz",
    toolkits=["gmail", "github"] # opsiyonel, varsayılan tüm araç setleridir
)
tools = session.tools()
```

Oturumlar ve kullanıcı yönetimi hakkında daha fazlasını [buradan](https://docs.composio.dev/docs/configuring-sessions) okuyabilirsiniz.

3. Kullanıcıların kimliğini manuel olarak doğrulama

Composio, ajan sohbet oturumu sırasında kullanıcıların kimliğini otomatik olarak doğrular. Ancak, `authorize` metodunu çağırarak kullanıcı kimliğini manuel olarak da doğrulayabilirsiniz.

```python Code theme={null}
connection_request = session.authorize("github")
print(f"Kimlik doğrulaması yapmak için bu URL'yi açın: {connection_request.redirect_url}")
```

4. Ajan Tanımlayın

```python Code theme={null}
crewai_agent = Agent(
    role="GitHub Ajanı",
    goal="GitHub API'lerini kullanarak GitHub üzerinde işlem yaparsınız",
    backstory="Kullanıcılar adına GitHub API'lerini kullanarak GitHub üzerinde işlem yapmaktan sorumlu bir yapay zeka ajanısınız",
    verbose=True,
    tools=tools,
    llm= # bir llm geçirin
)
```

5. Görevi Yürütün

```python Code theme={null}
task = Task(
    description="GitHub'da composiohq/composio deposuna yıldız ver",
    agent=crewai_agent,
    expected_output="İşlemin durumu",
)

crew = Crew(agents=[crewai_agent], tasks=[task])

crew.kickoff()
```

* Araçların daha ayrıntılı bir listesini [burada](https://docs.composio.dev/toolkits) bulabilirsiniz.
