## İş Birliğine Dayalı Yapay Zekanın Gücünü Serbest Bırakma

Kendinize, karmaşık sorunları çözmek için birlikte kusursuz bir şekilde çalışan, her biri ortak bir hedefe ulaşmak için benzersiz becerilerini katkı sağlayan uzmanlaşmış yapay zeka aracılarından oluşan bir ekibe sahip olduğunuzu hayal edin. Bu, CrewAI'nin gücüdür - size tek başına tek bir yapay zekanın başarabileceğinden çok daha fazla görevi tamamlayabilen iş birliğine dayalı yapay zeka sistemleri oluşturmanızı sağlayan bir çerçeve.

Bu kılavuzda, bir konuyu araştırmak ve analiz etmek ve ardından kapsamlı bir rapor oluşturmak için bizimle birlikte çalışacak bir araştırma ekibi oluşturma sürecinden geçeceğiz. Bu pratik örnek, yapay zeka aracılarının karmaşık görevleri tamamlamak için nasıl iş birliği yapabileceğini göstermektedir, ancak bu sadece CrewAI ile mümkün olanın başlangıcıdır.

### Neler Yapacaksınız ve Neler Öğreneceksiniz

Bu kılavuzun sonunda şunlara sahip olacaksınız:

1. **Ayrı roller ve sorumluluklara sahip uzmanlaşmış bir yapay zeka araştırma ekibi** oluşturmuş olacaksınız
2. **Birden fazla yapay zeka aracı arasındaki iş birliğini düzenlemiş olacaksınız**
3. **Bilgi toplama, analiz ve rapor oluşturmayı içeren karmaşık bir iş akışını otomatikleştirmiş olacaksınız**
4. **Daha iddialı projelerde uygulayabileceğiniz temel beceriler geliştirmiş olacaksınız**

Bu kılavuzda basit bir araştırma ekibi oluştururken, aynı desenler ve teknikler şu gibi görevler için çok daha karmaşık ekipler oluşturmak için de uygulanabilir:

- Özel yazarlar, editörler ve doğrulayıcıların bulunduğu çok aşamalı içerik oluşturma
- Hiyerarşik destek aracılarının bulunduğu karmaşık müşteri hizmetleri sistemleri
- Verileri toplayan, görselleştirmeler oluşturan ve fikirler üreten otonom iş analistleri
- Fikir üreten, tasarlayan ve uygulama planlaması yapan ürün geliştirme ekipleri

İlk ekibinizi oluşturmaya başlayalım!

### Ön Koşullar

Başlamadan önce, aşağıdaki gereksinimlerin olduğundan emin olun:

1. [kurulum kılavuzu](/en/installation) adresindeki kurulum kılavuzunu takip ederek CrewAI'yi kurmuş olun
2. [LLM kurulum kılavuzu](/en/concepts/llms#setting-up-your-llm) adresindeki LLM kurulum kılavuzunu takip ederek ortamınızda LLM API anahtarınızı ayarlamış olun
3. Python hakkında temel bilgi sahibi olun

## 1. Adım: Yeni Bir CrewAI Projesi Oluşturma

İlk olarak, CLI'yı kullanarak yeni bir CrewAI projesi oluşturalım. Bu komut, tanım adımlarından kaçınmanıza olanak tanıyan, gerekli tüm dosyalarla eksiksiz bir proje yapısı ayarlayacaktır.

```bash
crewai create crew research_crew
cd research_crew
```

Bu, temel yapıya sahip bir proje oluşturacaktır. CLI otomatik olarak şunları oluşturur:

- Gerekli dosyalara sahip bir proje dizini
- Aracılar ve görevler için yapılandırma dosyaları
- İş birliği sağlamak için temel bir ekip uygulaması
- Ekibi çalıştırmak için bir ana betik


  <img src="../../images/crews.png" alt="CrewAI Framework Overview" />



## 2. Adım: Proje Yapısını İnceleme

CLI tarafından oluşturulan proje yapısını anlamak için bir an ayırın. CrewAI, Python projeleri için en iyi uygulamaları takip eder, bu da ekipleriniz karmaşıklaştıkça kodunuzu sürdürmeyi ve genişletmeyi kolaylaştırır.

```
research_crew/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── research_crew/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```

Bu yapı, Python projeleri için en iyi uygulamaları takip eder ve kodunuzu düzenlemeyi kolaylaştırır. Yapılandırma dosyalarının (YAML içinde) uygulama kodundan (Python içinde) ayrılması, kodun altında yatan koda dokunmadan ekibinizin davranışını değiştirmeyi kolaylaştırır.

## 3. Adım: Aracılarınızı Yapılandırma

Şimdi eğlenceli kısma geçelim - yapay zeka aracılarınızı tanımlayın! CrewAI'de, aracılar belirli roller, hedefler ve davranışlarını şekillendiren arka plan hikayelerine sahip uzmanlaşmış varlıklardır. Bunları, ortak bir amacı başarmak için her birinin kendine özgü bir kişiliği ve amacı olan bir oyundaki karakterler gibi düşünün.

Araştırma ekibimiz için şu iki aracı oluşturacağız:

1. **Araştırmacı**, bilgi bulma ve düzenlemede mükemmeldir
2. **Analist**, araştırma bulgularını yorumlayabilir ve içgörülü raporlar oluşturabilir

Bu uzmanlaşmış araçları tanımlamak için `agents.yaml` dosyasını değiştirelim. Kullandığınız sağlayıcıya `llm` olarak ayırdığınızdan emin olun.

```yaml
# src/research_crew/config/agents.yaml
researcher:
  role: >
    {konu} için Kıdemli Araştırma Uzmanı
  goal: >
    {konu} hakkında kapsamlı ve doğru bilgi bulun
    özellikle son gelişmeler ve temel içgörülere odaklanın
  backstory: >
    Siz, çeşitli kaynaklardan ilgili bilgileri bulma konusunda yeteneği olan deneyimli bir araştırma uzmanısınız.
    Karmaşık konuları başkalarına erişilebilir hale getiren açık ve yapılandırılmış bir şekilde bilgiyi düzenlemede mükemmeldirsiniz.
  llm: sağlayıcı/model-kimliği  # örneğin openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...

analyst:
  role: >
    {konu} için Veri Analisti ve Rapor Yazarı
  goal: >
    Araştırma bulgularını analiz edin ve {konu} hakkında kapsamlı, iyi yapılandırılmış
    bir rapor oluşturun.
  backstory: >
    Veri yorumlama ve teknik yazma geçmişine sahip yetenekli bir analistsiniz.
    Araştırma verilerinden kalıpları belirleme ve bunları etkili bir şekilde ileten, iyi hazırlanmış
    raporlar yoluyla anlamlı içgörüler çıkarma yeteneğiniz var.
  llm: sağlayıcı/model-kimliği  # örneğin openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...
```

Her aracının ayrı bir rolü, hedefi ve arka plan hikayesi olduğunu fark edin. Bu unsurlar sadece açıklayıcı değil - aynı zamanda aracının görevlerine yaklaşma şeklini de aktif olarak şekillendiriyor. Bunları dikkatlice oluşturarak, birbirini tamamlayan özel becerilere ve perspektiflere sahip araçlar oluşturabilirsiniz.

## 4. Adım: Görevlerinizi Tanımlayın

Aracılarımızı tanımladıktan sonra, şimdi onlara belirli görevler vermek gerekecektir. CrewAI'deki görevler, aracılar tarafından gerçekleştirilecek somut çalışmaları temsil eder, ayrıntılı talimatlara ve beklenen çıktılara sahiptir.

Araştırma ekibimiz için şu iki ana görevi tanımlayacağız:

1. Kapsamlı bilgi toplamak için bir **araştırma görevi**
2. İçgörülü bir rapor oluşturmak için bir **analiz görevi**

`tasks.yaml` dosyasını değiştirelim:

```yaml
# src/research_crew/config/tasks.yaml
research_task:
  description: >
    {konu} üzerinde kapsamlı bir araştırma yapın. Şu konulara odaklanın:
    1. Temel kavramlar ve tanımlar
    2. Tarihi gelişim ve son trendler
    3. Temel zorluklar ve fırsatlar
    4. Önemli uygulamalar veya vaka çalışmaları
    5. Gelecek görünümü ve potansiyel gelişmeler

    Bulgularınızı net bölümlerle yapılandırılmış bir biçimde düzenlediğinizden emin olun.
  expected_output: >
    {konu}nun tüm talep edilen yönlerini kapsayan kapsamlı bir araştırma belgesi.
    İlgili özel gerçekler, rakamlar ve örnekler ekleyin.
  agent: researcher

analysis_task:
  description: >
    Araştırma bulgularını analiz edin ve {konu} hakkında kapsamlı bir rapor oluşturun.
    Raporunuz şunları içermelidir:
    1. Yönetici özeti ile başlayın
    2. Araştırmadan tüm temel bilgileri dahil edin
    3. Trend ve kalıpların içgörülü bir analizi sağlayın
    4. Öneriler veya gelecekteki hususlar sunun
    5. Açık başlıklarla profesyonel, okunması kolay bir üslupla biçimlendirin
  expected_output: >
    Araştırma bulgularını ek analiz ve içgörülerle sunan, cilalı, profesyonel bir {konu} raporu.
    Rapor, yönetici özeti, ana bölümler ve sonuç içeren iyi yapılandırılmış olmalıdır.
  agent: analyst
  context:
    - research_task
  output_file: output/report.md
```

Analiz görevinin `context` alanına dikkat edin - bu, analistin araştırma görevinin çıktısına erişmesini sağlayan güçlü bir özelliktir. Bu, bilgilerin insan ekibinde olduğu gibi aracılar arasında doğal olarak akmasını sağlayan bir iş akışı oluşturur.

## 5. Adım: Ekibinizi Yapılandırın

Her şeyi ekibinizi yapılandırarak bir araya getirme zamanı geldi. Ekip, aracılar arasındaki iş birliğini düzenleyen ve görevleri tamamlamak için birlikte çalışan konteynerdir.

`crew.py` dosyasını değiştirelim:

```python
# src/research_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ResearchCrew():
    """Kapsamlı konu analizi ve raporlama için araştırma ekibi"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'] # type: ignore[index]
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Araştırma ekibini oluşturur"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

Bu kodda şunları yapıyoruz:
1. Araştırmacı aracı oluşturuyoruz ve web'de arama yapmak için SerperDevTool ile donatıyoruz
2. Analist aracı oluşturuyoruz
3. Araştırma ve analiz görevlerini ayarlıyoruz
4. Ekibi sırasıyla görevleri çalıştırması için yapılandırıyoruz (analist, araştırmacı bitirdikten sonra bekleyecektir)

İşte sihirin gerçekleştiği yer - sadece birkaç satır kodla, uzmanlaşmış aracılar koordineli bir süreçte birlikte çalışan iş birliğine dayalı bir yapay zeka sistemi tanımlamış oluyoruz.

## 6. Adım: Ana Betiğinizi Yapılandırın

Şimdi, ekibimizin araştıracağı belirli konuyu sağlayan, ekibi çalıştıran ana betiği ayarlama zamanı.

```python
#!/usr/bin/env python
# src/research_crew/main.py
from research_crew.crew import ResearchCrew

# Çıkış dizinini mevcut değilse oluşturun
import os
os.makedirs('output', exist_ok=True)

def run():
    """
    Araştırma ekibini çalıştırın.
    """
    inputs = {
        'topic': 'Sağlık Hizmetlerinde Yapay Zeka'
    }

    # Ekibi oluşturun ve çalıştırın
    result = ResearchCrew().crew().kickoff(inputs=inputs)

    # Sonucu yazdırın
    print("\n\n=== SON RAPOR ===\n\n")
    print(result.raw)

    print("\n\nRapor output/report.md'ye kaydedildi")

if __name__ == "__main__":
    run()
```

Bu betik ortamı hazırlar, araştırma konusunu belirtir ve ekibin çalışmasını başlatır. CrewAI'nin gücü, tüm çoklu yapay zeka aracısı yönetimi karmaşıklığının çerçeve tarafından ele alınmasıyla, bunun ne kadar basit kod olduğuna tanık olacaksınız.

## 7. Adım: Ortam Değişkenlerinizi Yapılandırın

API anahtarlarınızı içeren bir `.env` dosyası oluşturun:

```sh
SERPER_API_KEY=serper_api anahtarınız
# Seçtiğiniz sağlayıcı için API anahtarınızı buraya da ekleyin.
```

Seçtiğiniz sağlayıcıyı yapılandırma hakkında ayrıntılar için [LLM Kurulum kılavuzuna](/en/concepts/llms#setting-up-your-llm) bakın. Bir Serper API anahtarını [Serper.dev](https://serper.dev/) adresinden alabilirsiniz.

## 8. Adım: Bağımlılıkları Yükleyin

Gerekli bağımlılıkları CrewAI CLI kullanarak yükleyin:

```bash
crewai install
```

Bu komut şunları yapacaktır:

1. Proje yapılandırmanızdan bağımlılıkları okur
2. Gerekirse sanal bir ortam oluşturur
3. Tüm gerekli paketleri yükler

## 9. Adım: Ekibinizi Çalıştırın

Şimdi heyecan verici ana ana - ekibinizi çalıştırın ve yapay zeka iş birliğini eyleme geçirin!

```bash
crewai run
```

Bu komutu çalıştırdığınızda, ekibinizin hayata geçtiğini göreceksiniz. Araştırmacı, belirtilen konu hakkında bilgi toplayacak ve analist daha sonra o araştırmaya göre kapsamlı bir rapor oluşturacaktır. Birden fazla yapay zeka aracısının birlikte çalıştığı, karmaşık bir görevi tamamlamak için uzmanlaşmış becerilerini katkı sağladığı bir sistemi başarıyla oluşturduğunuzu takdir etmek için aracılarının düşünce süreçlerini, eylemlerini ve çıktılarını gerçek zamanlı olarak göreceksiniz.

## 10. Adım: Çıktıyı İnceleyin

Ekibiniz çalışmasını bitirdikten sonra, son raporu `output/report.md` dosyasında bulacaksınız. Rapor şunları içerecektir:

1. Yönetici özeti
2. Konuyla ilgili ayrıntılı bilgi
3. Analiz ve içgörüler
4. Öneriler veya gelecekteki hususlar

Bir an ayırın ve ne başardığınıza hayranlık duyun - çoklu yapay zeka aracılarının karmaşık bir görevde iş birliği yaptığı ve her birinin özel becerilerini katkı sağlayarak tek bir aracının tek başına başarabileceğinden daha büyük bir sonuç ürettiği bir sistem oluşturmuşsunuz.

## Diğer CLI Komutlarını Keşfetme

CrewAI, ekiplerle çalışırken kullanabileceğiniz diğer yararlı CLI komutlarını da sunar:

```bash
# Mevcut tüm komutları görüntüleyin
crewai --help

# Ekibi çalıştırın
crewai run

# Ekibi test edin
crewai test

# Ekip anılarını sıfırlayın
crewai reset-memories

# Belirli bir görevden başlayarak oynatın
crewai replay -t <görev kimliği>
```

## Mümkün Olanlar: İlk Ekibinizin Ötesinde

Bu kılavuzda oluşturduğunuz şey sadece bir başlangıç. Öğrendiğiniz beceriler ve desenler, giderek daha karmaşık yapay zeka sistemleri oluşturmak için uygulanabilir. Bu temel ekibi şu şekilde genişletebilirsiniz:

### Ekibinizi Genişletme

Ekibinize daha fazla uzmanlaşmış araç ekleyebilirsiniz:
- Araştırma bulgularını doğrulamak için bir **doğrulayıcı**
- Grafikler ve grafikler oluşturmak için bir **veri görselleştirici**
- Belirli bir alanda özel bilgiye sahip bir **alan uzmanı**
- Zayıflıkları belirlemek için bir **eleştirmen**

### Araçlar ve Yetenekler Ekleyin

Aracılara ek araçlarla güç verebilirsiniz:
- Gerçek zamanlı araştırma için web'e göz atma araçları
- Veri analizi için CSV/veritabanı araçları
- Veri işleme için kod yürütme araçları
- Dış hizmetlere API bağlantıları

### Daha Karmaşık İş Akışları Oluşturma

Daha karmaşık süreçleri uygulayabilirsiniz:
- Yöneticilerin işçi aracılara devretmesiyle hiyerarşik süreçler
- Geri bildirim döngülerine sahip yinelemeli süreçler
- Birden fazla aracının aynı anda çalıştığı paralel süreçler
- Ara sonuçlara göre uyum sağlayan dinamik süreçler

### Farklı Alanlara Uygulama

Aynı desenler şunlar için ekipler oluşturmak için uygulanabilir:
- **İçerik oluşturma**: Birlikte çalışan yazarlar, editörler ve doğrulayıcılar
- **Müşteri hizmetleri**: Derecelendirilmiş destek aracılarının bulunduğu karmaşık müşteri hizmetleri sistemleri
- **Ürün geliştirme**: Fikir üreten, tasarlayan ve uygulama planlaması yapan ürün geliştirme ekipleri
- **Veri analizi**: Veri toplayıcılar, analistler ve görselleştirme uzmanları

### Sonraki Adımlar

İlk ekibinizi oluşturduktan sonra şunları yapabilirsiniz:

1. Farklı araç yapılandırmaları ve kişiliklerle deney yapın
2. Daha karmaşık görev yapıları ve iş akışları deneyin
3. Aracılarınıza yeni yetenekler vermek için özel araçlar uygulayın
4. Ekibinizi farklı konulara veya problem alanlarına uygulayın
5. [CrewAI Akışlarını](/en/guides/flows/first-flow) daha gelişmiş iş akışları için keşfedin


Tebrikler! Araştırmayı ve analiz etmeyi sağlayabilecek ilk CrewAI ekibinizi başarıyla oluşturdunuz. Bu temel deneyim, karmaşık, çok aşamalı sorunları iş birliğine dayalı zeka ile çözebilecek giderek daha karmaşık yapay zeka sistemleri oluşturmak için size gereken becerileri donatmıştır.