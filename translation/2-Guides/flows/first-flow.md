## İlk Akışınızı Oluşturun

<mark>Açıklama:</mark> Yapılandırılmış, olay güdümlü iş akışlarını, yürütme üzerinde hassas kontrole sahip olarak nasıl oluşturacağınızı öğrenin.

<mark>Simgesi:</mark> diyagram-projesi

<mark>Mod:</mark> geniş

## Yapay Zeka İş Akışlarını Akışlarla Kontrol Altına Alma

CrewAI Akışları, yapay zeka aracısı ekiplerinin işbirliği gücünü işlemsel programlamanın hassasiyeti ve esnekliği ile birleştiren, yapay zeka orkestrasyonunda bir sonraki seviyedir. Ekiplerin işbirliği konusunda mükemmel olsalar da, akışlar farklı yapay zeka sisteminizin bileşenlerinin tam olarak nasıl ve ne zaman etkileşimde bulunacağını kontrol etmenize olanak tanır.

Bu kılavuzda, herhangi bir konuda kapsamlı bir öğrenme kılavuzu oluşturmak için güçlü bir CrewAI Akışı oluşturma adımlarını inceleyeceğiz. Bu eğitim, düzenli kod, doğrudan LLM çağrıları ve ekip tabanlı işleme birleştirerek Akışların yapay zeka iş akışlarınız üzerinde yapılandırılmış, olay güdümlü kontrol sağladığını göstermelidir.

### Akışların Gücünü Yaratır

Akışlar şunları yapmanızı sağlar:

1.  **Farklı yapay zeka etkileşim kalıplarını birleştirme**: Karmaşık işbirliği görevleri için ekipleri, daha basit işlemler için doğrudan LLM çağrılarını ve işlemsel mantık için düzenli kodu kullanın
2.  **Olay güdümlü sistemler oluşturma**: Bileşenlerin belirli olaylara ve veri değişikliklerine nasıl yanıt vereceğini tanımlayın
3.  **Bileşenler arasında durumu koruma**: Uygulamanızın farklı bölümleri arasında veri paylaşın ve dönüştürün
4.  **Harici sistemlerle entegre olun**: Yapay zeka iş akışınızı veritabanları, API'ler ve kullanıcı arayüzleri ile sorunsuz bir şekilde bağlayın
5.  **Karmaşık yürütme yolları oluşturun**: Koşullu dallanma, paralel işleme ve dinamik iş akışları tasarlayın

### Ne Oluşturacak ve Neler Öğreneceksiniz

Bu kılavuzun sonunda şunlara sahip olacaksınız:

1.  Kullanıcı girdisi, yapay zeka planlama ve çoklu-aracı içerik oluşturmayı birleştiren sofistike bir içerik oluşturma sistemi
2.  Sisteminize ait farklı bileşenler arasında bilgi akışını orkestrasyonu
3.  Her adımın bir önceki adımın tamamlanmasına yanıt verdiği olay güdümlü bir mimari
4.  Genişletebileceğiniz ve özelleştirebileceğiniz daha karmaşık yapay zeka uygulamaları için bir temel

Bu kılavuz oluşturma akışı, çok daha gelişmiş uygulamalar oluşturmak için uygulanabilecek temel kalıpları gösterir:

-   Çok sayıda özel alt sistemin birleşimiyle etkileşimli yapay zeka asistanları
-   Yapay zeka ile geliştirilmiş dönüşümler içeren karmaşık veri işleme boru hatları
-   Harici hizmetler ve API'lerle entegre olan özerk aracılar
-   İnsanların dahil olduğu süreçlerle çok aşamalı karar verme sistemleri

Haydi dalıp ilk akışınızı inşa edelim!

## Ön Koşullar

Başlamadan önce şunlara sahip olduğunuzdan emin olun:

1.  [kurulum kılavuzu](/en/installation) adresindeki kurulum kılavuzunu takip ederek CrewAI'yi yükleyin
2.  [LLM kurulum kılavuzu](/en/concepts/llms#setting-up-your-llm) adresindeki LLM kurulum kılavuzunu takip ederek ortamınızda LLM API anahtarınızı ayarlayın
3.  Python'a temel anlayış

## 1. Adım: Yeni Bir CrewAI Akışı Projesi Oluşturma

Öncelikle, CLI'yı kullanarak yeni bir CrewAI Akışı projesi oluşturun. Bu komut, akışınız için gerekli dizinleri ve şablon dosyalarını içeren bir iskelet projesi ayarlar.

```bash
crewai create flow guide_creator_flow
cd guide_creator_flow
```

Bu, temel yapısıyla bir proje oluşturacaktır.

```
guide_creator_flow/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env
├── main.py
├── crews/
│   └── poem_crew/
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── poem_crew.py
└── tools/
    └── custom_tool.py
```

## 2. Adım: Proje Yapısını Anlama

Oluşturulan proje, aşağıdaki yapıya sahiptir. Akışınızı oluştururken bu yapıyı anlamanıza yardımcı olmak için bir an ayırın.

Yukarıdaki yapı, akışınızın farklı bileşenleri arasında net bir ayrım sağlar:
- `main.py` dosyasındaki ana akış mantığı
- `crews` dizinindeki özel ekipler
- `tools` dizinindeki özel araçlar

Kapsamlı öğrenme kılavuzları oluşturacak olan içeriği yazma ekibini oluşturmak için yapıyı değiştireceğiz.

## 3. Adım: İçerik Yazma Ekibi Ekleme

Akışımız, içerik oluşturma sürecini ele alacak bir uzman ekibe ihtiyaç duyacaktır. İçerik yazma ekibini eklemek için CrewAI CLI'yı kullanalım:

```bash
crewai flow add-crew content-crew
```

Bu komut, ekip için gerekli dizinleri ve şablon dosyalarını otomatik olarak oluşturur. İçerik yazma ekibi, ana uygulamanız tarafından orkestrelenen genel akış içinde çalışarak bölüm yazma ve gözden geçirme görevlerinden sorumlu olacaktır.

## 4. Adım: İçerik Yazma Ekibini Yapılandırma

Şimdi, içerik yazma ekibi için oluşturulan dosyaları değiştirelim. Yüksek kaliteli içerik oluşturmak için işbirliği yapacak iki özel aracıyı - bir yazar ve bir gözden geçiren - ayarlayacağız.

1.  Öncelikle, içeriği oluşturma ekibinizi tanımlamak için aracılar yapılandırma dosyasını güncelleyin:

   Kullandığınız sağlayıcıya `llm` değerini ayarlamayı unutmayın.

```yaml
# src/guide_creator_flow/crews/content_crew/config/agents.yaml
content_writer:
  role: >
    Eğitim İçerik Yazarı
  goal: >
    Atanan konuyu kapsamlı bir şekilde açıklayan ilgi çekici, bilgilendirici içerik oluşturun
    ve okuyucuya değerli bilgiler verin
  backstory: >
    Açık, ilgi çekici bir dille karmaşık kavramları açıklama ve bilgiyi okuyucunun
    anlayışını geliştirmesine yardımcı olacak şekilde organize etme konusunda yetenekli, yetenekli bir
    eğitim yazarı olduğunuz.
  llm: provider/model-id  # örneğin openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...

content_reviewer:
  role: >
    Eğitim İçerik Gözden Geçiren ve Editör
  goal: >
    İçeriğin doğru, kapsamlı, iyi yapılandırılmış ve yazılan önceki bölümlerle
    tutarlı olmasını sağlayın
  backstory: >
    Yıllar önce eğitim içeriği inceleme konusunda deneyimli titiz bir editörsünüz.
    Ayrıntılara, açıklığa ve tutarlılığa gözünüz keskin. Orijinal yazarın sesini korurken ve
    birden çok bölümde tutarlı kaliteyi sağlayarak içeriği iyileştirmede mükemelsiniz.
  llm: provider/model-id  # örneğin openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...
```

Bu aracı tanımları, yapay zeka aracılarımızın içerik oluşturma yaklaşımını şekillendirecek özel rolleri ve bakış açılarını oluşturur. Her aracının farklı bir amaca ve uzmanlığa sahip olduğunu fark edin.

2.  Ardından, özel görevlerinizi tanımlamak için görev yapılandırma dosyasını güncelleyin:

```yaml
# src/guide_creator_flow/crews/content_crew/config/tasks.yaml
write_section_task:
  description: >
    "{section_title}" konusuna ilişkin kapsamlı bir bölüm yazın

    Bölüm açıklaması: {section_description}
    Hedef kitle: {audience_level} seviyesindeki öğrenciler

    İçeriğiniz şunları yapmalıdır:
    1. Bölüm konusuna kısa bir giriş yapın
    2. Tüm ana kavramları örneklerle açıkça açıklayın
    3. Uygun olduğunda pratik uygulamalar veya egzersizler ekleyin
    4. Ana noktaların bir özetini ekleyerek bitirin
    5. Yaklaşık 500-800 kelime uzunluğunda

    İçeriğinizi uygun başlıklar, listeler ve vurgu ile Markdown biçiminde biçimlendirin.

    Önceki yazılan bölümler:
    {previous_sections}

    İçeriğinizin yazılan önceki bölümlerle tutarlı olmasını ve zaten açıklanan kavramlar üzerine inşa etmesini sağlayın.
  expected_output: >
    Konuyu kapsamlı bir şekilde açıklayan ve hedef kitle için uygun olan Markdown biçiminde iyi yapılandırılmış bir bölüm.
  agent: content_writer

review_section_task:
  description: >
    Aşağıdaki "{section_title}" bölümünü inceleyin ve iyileştirin:

    {draft_content}

    Hedef kitle: {audience_level} seviyesindeki öğrenciler

    Önceki yazılan bölümler:
    {previous_sections}

    İncelemeniz şunları yapmalıdır:
    1. Herhangi bir dilbilgisi veya yazım hatasını düzeltin
    2. Açıklığı ve okunabilirliği iyileştirin
    3. İçeriğin kapsamlı ve doğru olduğundan emin olun
    4. Yazılan önceki bölümlerle tutarlılığını doğrulayın
    5. Yapıyı ve akışı geliştirin
    6. Eksik önemli bilgileri ekleyin

    İyileştirilmiş bölümün Markdown biçiminde sağlanan sürümünü sağlayın.
  expected_output: >
    Orijinal yapıyı korurken açıklığı, doğruluğu ve tutarlılığı artıran bölümün iyileştirilmiş, cilalı bir sürümü.
  agent: content_reviewer
  context:
    - write_section_task
```

Bu görev tanımları, aracılarımıza ayrıntılı talimatlar sağlayarak, kaliteli standartlarımızı karşılayan içerik oluşturmalarını sağlar. İnceleme görevinin bağlam parametresine dikkat edin; bu, inceleyicinin yazarın çıktısına erişebilmesini sağlar.

3.  Şimdi, ekibinizin aracılar ve görevler arasındaki ilişkiyi tanımlayarak nasıl çalıştığını tanımlamak için ekip uygulama dosyasını güncelleyin:

```python
# src/guide_creator_flow/crews/content_crew/content_crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ContentCrew():
    """İçerik yazma ekibi"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def content_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_reviewer'], # type: ignore[index]
            verbose=True
        )

    @task
    def write_section_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_section_task'] # type: ignore[index]
        )

    @task
    def review_section_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_section_task'], # type: ignore[index]
            context=[self.write_section_task()]
        )

    @crew
    def crew(self) -> Crew:
        """İçerik yazma ekibini oluşturur"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

Bu ekip tanımı, aracılarımız ve görevlerimiz arasındaki ilişkiyi, yazarın bir taslak oluşturduğu ve ardından inceleyicinin iyileştirdiği sıralı bir süreç ayarlayarak oluşturur. Bu ekip bağımsız olarak çalışabilse de, akışınızın daha büyük bir sistemin bir parçası olarak orkestre edilecek.

## 5. Adım: Akışı Oluşturma

Şimdi, heyecan verici kısma geldik - her şeyin bir araya geldiği akışı oluşturmak. İşte yapay zeka, doğrudan LLM çağrıları ve içerik oluşturma ekibimiz gibi farklı bileşenleri uyumlu bir sisteme dönüştüren bu adım:

Akışımız şunları yapacak:
1. Kullanıcıdan konu ve kitle seviyesi için giriş alın
2. Yapılandırılmış bir kılavuz taslağı oluşturmak için doğrudan bir LLM çağrısı yapın
3. Her bölümü sırayla içerik yazma ekibiyle işleyin
4. Her şeyi nihai kapsamlı belgeye birleştirin

Akışımızı `main.py` dosyasında oluşturun:

```python
#!/usr/bin/env python
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from guide_creator_flow.crews.content_crew.content_crew import ContentCrew

# Yapılandırılmış veri için modellerimizi tanımlayın
class Section(BaseModel):
    title: str = Field(description="Bölümün başlığı")
    description: str = Field(description="Bölümün ne hakkında olacağını kısaca açıklayın")

class GuideOutline(BaseModel):
    title: str = Field(description="Kılavuzun başlığı")
    introduction: str = Field(description="Konuya giriş")
    target_audience: str = Field(description="Hedef kitle açıklaması")
    sections: List[Section] = Field(description="Kılavuzdaki bölümlerin listesi")
    conclusion: str = Field(description="Kılavuzun sonucu veya özeti")

# Akış durumumuz için sınıf
class GuideCreatorState(BaseModel):
    topic: str = ""
    audience_level: str = ""
    guide_outline: GuideOutline = None
    sections_content: Dict[str, str] = {}

class GuideCreatorFlow(Flow[GuideCreatorState]):
    """Herhangi bir konuda kapsamlı bir kılavuz oluşturmak için akış"""

    @start()
    def get_user_input(self):
        """Kullanıcıdan kılavuz konusunu ve hedef kitleyi alın"""
        print("\n=== Kapsamlı Kılavuzunuzu Oluşturun ===\n")

        # Kullanıcıdan giriş alın
        self.state.topic = input("Hangi konuda bir kılavuz oluşturmak istersiniz? ")

        # Doğrulama ile kitle seviyesini alın
        while True:
            audience = input("Hedef kitleniz kim? (başlangıç/ara/ileri) ").lower()
            if audience in ["başlangıç", "ara", "ileri"]:
                self.state.audience_level = audience
                break
            print("Lütfen 'başlangıç', 'ara' veya 'ileri' girin")

        print(f"\n{self.state.topic} hakkında {self.state.audience_level} hedef kitle için bir kılavuz oluşturuluyor...\n")
        return self.state

    @listen(get_user_input)
    def create_guide_outline(self, state):
        """Kılavuz için yapılandırılmış bir taslak oluşturmak için doğrudan bir LLM çağrısı kullanın"""
        print("Kılavuz taslağını oluşturma...")

        # LLM'yi başlatın
        llm = LLM(model="openai/gpt-4o-mini", response_format=GuideOutline)

        # Taslak için mesajları oluşturun
        messages = [
            {"role": "system", "content": "JSON çıktısı vermek için tasarlanmış yardımcı bir asistan sizsiniz."},
            {"role": "user", "content": f"""
            {state.topic} konusunda kapsamlı bir kılavuz için ayrıntılı bir taslak oluşturun {state.audience_level} seviyesindeki öğrenciler için.

            Taslak şunları içermelidir:
            1. Kılavuz için ilgi çekici bir başlık
            2. Konuya giriş
            3. Konunun en önemli yönlerini kapsayan 4-6 ana bölüm
            4. Sonuç veya özet

            Her bölüm için, neyi kapsaması gerektiğine dair açık bir başlık ve kısa bir açıklama sağlayın.
            """}
        ]

        # JSON yanıt biçimini kullanarak LLM çağrısı yapın
        response = llm.call(messages=messages)

        # JSON yanıtını ayrıştırın
        outline_dict = json.loads(response)
        self.state.guide_outline = GuideOutline(**outline_dict)

        # Çıktı dizinini oluşturmadan önce var olduğundan emin olun
        os.makedirs("output", exist_ok=True)

        # Taslağı bir dosyaya kaydedin
        with open("output/guide_outline.json", "w") as f:
            json.dump(outline_dict, f, indent=2)

        print(f"Taslak {self.state.guide_outline.sections} bölümüyle oluşturuldu")
        return self.state.guide_outline

    @listen(create_guide_outline)
    def write_and_compile_guide(self, outline):
        """Tüm bölümleri yazın ve kılavuzu derleyin"""
        print("Bölümleri yazma ve kılavuzu derleme...")
        completed_sections = []

        # Bağlam akışını korumak için bölümleri tek tek işleyin
        for section in outline.sections:
            print(f"Bölümü işleme: {section.title}")

            # Önceki bölümlerden bağlam oluşturun
            previous_sections_text = ""
            if completed_sections:
                previous_sections_text = "# Önceki Yazılan Bölümler\n\n"
                for title in completed_sections:
                    previous_sections_text += f"## {title}\n\n"
                    previous_sections_text += self.state.sections_content.get(title, "") + "\n\n"
            else:
                previous_sections_text = "Hala yazılmamış önceki bölümler."

            # Bu bölüm için içerik yazma ekibini çalıştırın
            result = ContentCrew().crew().kickoff(inputs={
                "section_title": section.title,
                "section_description": section.description,
                "audience_level": self.state.audience_level,
                "previous_sections": previous_sections_text,
                "draft_content": ""
            })

            # İçeriği depolayın
            self.state.sections_content[section.title] = result.raw
            completed_sections.append(section.title)
            print(f"Bölüm tamamlandı: {section.title}")

        # Son kılavuzu derleyin
        guide_content = f"# {outline.title}\n\n"
        guide_content += f"## Giriş\n\n{outline.introduction}\n\n"

        # Her bölümü sırayla ekleyin
        for section in outline.sections:
            section_content = self.state.sections_content.get(section.title, "")
            guide_content += f"\n\n{section_content}\n\n"

        # Sonuç ekleyin
        guide_content += f"## Sonuç\n\n{outline.conclusion}\n\n"

        # Kılavuzu kaydedin
        with open("output/complete_guide.md", "w") as f:
            f.write(guide_content)

        print("\nKılavuz derlendi ve output/complete_guide.md adresine kaydedildi")
        return "Kılavuz oluşturma işlemi başarıyla tamamlandı"

def kickoff():
    """Kılavuz oluşturma akışını çalıştırın"""
    GuideCreatorFlow().kickoff()
    print("\n=== Akış Tamamlandı ===")
    print("Kapsamlı kılavuzunuz output dizininde hazır.")
    print("Bölümde görüntülemek için output/complete_guide.md'yi açın.")

def plot():
    """Akışın görselleştirmesini oluşturun"""
    flow = GuideCreatorFlow()
    flow.plot("guide_creator_flow")
    print("Akış görselleştirmesi guide_creator_flow.html dosyasına kaydedildi")

if __name__ == "__main__":
    kickoff()
```

Bu akışta neler olduğunu analiz edelim:

1.  Yapılandırılmış veri için Pydantic modellerini tanımlıyoruz ve tip güvenliğini ve net veri gösterimini sağlıyoruz
2.  Farklı akış adımları arasında veri paylaşmayı kolaylaştıran bir durum sınıfı oluşturuyoruz
3.  Üç ana akış adımı uyguluyoruz:
    - `@start()` dekoratörü ile kullanıcıdan giriş alma
    - Doğrudan bir LLM çağrısıyla bir kılavuz taslağı oluşturma
    - İçerik yazma ekibi ile bölümleri işleme
4.  Adımlar arasındaki ilişkileri kurmak için `@listen()` dekoratörünü kullanıyoruz

Bu, akışların gücünü göstermektedir - kullanıcı etkileşimi, doğrudan LLM çağrıları, ekip tabanlı görevler gibi farklı işlem türlerini uyumlu, olay güdümlü bir sisteme birleştirmek.

## 6. Adım: Ortam Değişkenlerinizi Ayarlama

API anahtarlarınızla `.env` dosyasını projenizin kök dizininde oluşturun. Sağlayıcıyı nasıl yapılandıracağınıza dair ayrıntılar için [LLM kurulum
kılavuzuna](/en/concepts/llms#setting-up-your-llm) bakın.

```sh .env
OPENAI_API_KEY=your_openai_api_key
# veya
GEMINI_API_KEY=your_gemini_api_key
# veya
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 7. Adım: Bağımlılıkları Yükleme

Gerekli bağımlılıkları yükleyin:

```bash
crewai install
```

## 8. Adım: Akışınızı Çalıştırma

Şimdi akışınızı aksiyona geçirme zamanı! Akışınızı çalıştırmak için CrewAI CLI'sını kullanın:

```bash
crewai flow kickoff
```

Bu komutu çalıştırdığınızda, akışınızın nasıl hayata geçtiğini göreceksiniz:
1. Bir konu ve kitle seviyesi için sizden giriş isteyecek
2. Kılavuz için yapılandırılmış bir taslak oluşturacak
3. Her bölümü işleyecek, içerik yazar ve inceleyicisi işbirliği yapacak
4. Son olarak, her şeyi kapsamlı bir kılavuzda birleştirecektir

Bu, kullanıcı girdisi, yapay zeka etkileşimleri ve işbirliği içinde çalışan aracılar gibi farklı bileşenleri birleştiren bir sistemin gücünü göstermektedir.

## 9. Adım: Akışınızı Görselleştirme

Akışların güçlü özelliklerinden biri, yapılarının görselleştirme yeteneğidir:

```bash
crewai flow plot
```

Bu, akışınızın yapısını gösteren bir HTML dosyası oluşturacak, farklı adımlar arasındaki ilişkiler ve aralarındaki veri akışı dahil. Bu görselleştirme, karmaşık akışları anlamak ve hata ayıklamak için çok değerli olabilir.

## 10. Adım: Çıktıyı Gözden Geçirme

Akış tamamlandıktan sonra, `output` dizininde iki dosya bulacaksınız:

1.  `guide_outline.json`: Kılavuzun yapılandırılmış taslağını içerir
2.  `complete_guide.md`: Tüm bölümlerle kapsamlı kılavuz

Bu dosyaları inceleyin ve neler inşa ettiğinizi takdir edin - kullanıcı girdisi, doğrudan yapay zeka etkileşimleri ve işbirliği içinde çalışan araçların bir araya gelerek karmaşık ve yüksek kaliteli bir çıktı oluşturduğu bir sistem.

## Olası Sanat: İlk Akışınızın Ötesinde

Bu kılavuzdaki adımları izleyerek ilk akışınızı oluşturduktan sonra şunları yapabilirsiniz:

1.  Daha karmaşık akış yapıları ve kalıplarıyla deney yapın
2.  Koşullu dallanma için `@router()`'ı kullanmayı deneyin
3.  Daha karmaşık paralel yürütme için `and_` ve `or_` fonksiyonlarını keşfedin
4.  Akışınızı harici API'ler, veritabanları veya kullanıcı arayüzleri ile bağlayın
5.  Birden çok özel ekibi tek bir akışta birleştirin

### Kullanıcı Etkileşimini Geliştirme

Aşağıdakilerle daha etkileşimli akışlar oluşturabilirsiniz:
- Girdi ve çıktı için web arayüzleri
- Gerçek zamanlı ilerleme güncellemeleri
- Etkileşimli geri bildirim ve iyileştirme döngüleri
- Çok aşamalı kullanıcı etkileşimleri

### Daha Fazla İşleme Adımı Ekleme

Şunları ekleyerek akışınızı genişletebilirsiniz:
- Taslak oluşturmadan önce araştırma
- İllüstrasyonlar için resim oluşturma
- Teknik kılavuzlar için kod parçacığı oluşturma
- Son kalite güvencesi ve doğruluk kontrolü

### Daha Karmaşık Akışlar Oluşturma

Şunları uygulayabilirsiniz:
- Kullanıcı tercihleri ​​veya içerik türüne göre koşullu dallanma
- Bağımsız bölümlerin paralel işlenmesi
- Geri bildirim içeren yinelemeli iyileştirme döngüleri
- Harici API'ler ve hizmetlerle entegrasyon

### Farklı Alanlara Uygulama

Aynı kalıplar şunları oluşturmak için kullanılabilir:
- **Etkileşimli hikaye anlatımı**: Kullanıcı girdisine göre kişiselleştirilmiş hikayeler oluşturun
- **İş zekası**: Verileri işleyin, içgörüler oluşturun ve raporlar oluşturun
- **Ürün geliştirme**: Fikri birleştirmeyi, tasarım ve planlamayı kolaylaştırın
- **Eğitim sistemleri**: Kişiselleştirilmiş öğrenme deneyimleri oluşturun

## Gösterilen Temel Özellikler

Bu kılavuz oluşturma akışı, CrewAI'nın aşağıdaki özellikleri şunları gösterir:

1.  **Kullanıcı etkileşimi**: Akış, kullanıcıdan doğrudan giriş alır
2.  **Doğrudan LLM çağrıları**: Basit, yapılandırılmış yanıtlar için LLM sınıfını kullanır
3.  **Yapılandırılmış veri ile Pydantic**: Tip güvenliğini ve açık veri gösterimini sağlamak için Pydantic modellerini kullanır
4.  **Bağlam ile sıralı işleme**: Bölümleri sırayla yazarak önceki bölümler için bağlam sağlar
5.  **Çoklu-aracı ekipleri**: İçerik oluşturma için uzmanlaşmış araçları (yazar ve inceleyici) kullanır
6.  **Durum yönetimi**: Farklı adımlar genelinde durumu korur
7.  **Olay güdümlü mimari**: Adımlar arasındaki ilişkileri kurmak için `@listen` dekoratörünü kullanır

## Sonraki Adımlar

İlk akışınızı oluşturduktan sonra şunları yapabilirsiniz:

1.  Daha karmaşık akış yapıları ve kalıplarıyla deney yapın
2.  Akışlarınızda koşullu dallanma için `@router()` kullanmayı deneyin
3.  Daha karmaşık paralel yürütme için `and_` ve `or_` fonksiyonlarını keşfedin
4.  Akışınızı harici API'ler, veritabanları veya kullanıcı arayüzleri ile bağlayın
5.  Tek bir akış içinde birden çok özel ekibi birleştirin

Tebrikler! Yapay zeka, doğrudan LLM çağrıları ve ekip tabanlı işleme birleştiren ilk CrewAI Akışınızı başarıyla oluşturmuşsunuz. Bu temel beceriler, karmaşık, çok aşamalı sorunları işlemsel kontrol ve işbirlikçi zeka kombinasyonu yoluyla gidermek için giderek daha sofistike yapay zeka uygulamaları oluşturmanıza olanak tanır.