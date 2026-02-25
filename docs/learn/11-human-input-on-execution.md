# Yürütme Sırasında İnsan Girdisi

> Karmaşık karar alma süreçlerinde yürütme sırasında CrewAI'yi insan girdisiyle entegre etme ve ajanın nitelikleri ile araçlarının tüm kapasitesinden yararlanma.

## Ajan Yürütmesinde İnsan Girdisi

İnsan girdisi, ajanların gerektiğinde ek bilgi veya açıklama talep etmesine imkân tanıyarak çeşitli ajan yürütme senaryolarında kritik bir rol oynar. Bu özellik özellikle karmaşık karar alma süreçlerinde veya ajanların bir görevi etkin biçimde tamamlamak için daha fazla ayrıntıya ihtiyaç duyduğu durumlarda kullanışlıdır.

## CrewAI ile İnsan Girdisini Kullanma

İnsan girdisini ajan yürütmesine entegre etmek için görev tanımında `human_input` bayrağını ayarlayın. Etkinleştirildiğinde ajan, nihai yanıtını vermeden önce kullanıcıdan girdi ister. Bu girdi ek bağlam sağlayabilir, belirsizlikleri giderebilir veya ajanın çıktısını doğrulayabilir.

### Örnek

```shell
pip install crewai
```

```python
import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "Your Key"  # serper.dev API anahtarı
os.environ["OPENAI_API_KEY"] = "Your Key"

# Araçları yükleme
search_tool = SerperDevTool()

# Ajanlarınızı roller, hedefler, araçlar ve ek niteliklerle tanımlayın
researcher = Agent(
    role='Senior Research Analyst',
    goal='Yapay zeka ve veri bilimindeki son gelişmeleri ortaya çıkar',
    backstory=(
        "Önde gelen bir teknoloji düşünce kuruluşunda Kıdemli Araştırma Analistisiniz. "
        "Uzmanlığınız, yapay zeka ve veri bilimindeki yeni ortaya çıkan trendleri ve teknolojileri tespit etmekte yatmaktadır. "
        "Karmaşık verileri çözümleme ve uygulanabilir içgörüler sunma konusunda üstünsünüz."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)
writer = Agent(
    role='Tech Content Strategist',
    goal='Teknolojik gelişmeler hakkında etkileyici içerikler üret',
    backstory=(
        "Teknoloji ve inovasyon üzerine özgün ve ilgi çekici makaleleriyle tanınan ünlü bir Teknoloji İçerik Stratejistisiniz. "
        "Teknoloji sektörüne derin anlayışınızla karmaşık kavramları etkileyici anlatılara dönüştürürsünüz."
    ),
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    cache=False,  # Bu ajan için önbelleği devre dışı bırak
)

# Ajanlarınız için görevler oluşturun
task1 = Task(
    description=(
        "2025 yılındaki yapay zeka alanındaki son gelişmelerin kapsamlı bir analizini yapın. "
        "Temel trendleri, çığır açan teknolojileri ve potansiyel sektör etkilerini tespit edin. "
        "Bulgularınızı ayrıntılı bir raporda derleyin. "
        "Nihai yanıtı vermeden önce taslağın uygun olup olmadığını bir insanla mutlaka kontrol edin."
    ),
    expected_output='2025 yılındaki en son yapay zeka gelişmeleri hakkında hiçbir şey atlanmamış kapsamlı bir tam rapor',
    agent=researcher,
    human_input=True
)

task2 = Task(
    description=(
        "Araştırmacının raporundaki içgörüleri kullanarak en önemli yapay zeka gelişmelerini öne çıkaran ilgi çekici bir blog yazısı geliştirin. "
        "Yazınız teknoloji meraklısı bir kitleye hitap edecek şekilde hem bilgilendirici hem de erişilebilir olmalıdır. "
        "Bu atılımların özünü ve geleceğe yönelik çıkarımlarını aktaran bir anlatı hedefleyin."
    ),
    expected_output='2025 yılındaki en son yapay zeka gelişmeleri hakkında markdown formatında yazılmış etkileyici 3 paragraflık blog yazısı',
    agent=writer,
    human_input=True
)

# Ekibinizi sıralı süreçle oluşturun
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=True,
    memory=True,
    planning=True  # Ekip için planlama özelliğini etkinleştir
)

# Ekibinizi çalışmaya başlatın!
result = crew.kickoff()

print("######################")
print(result)
```
