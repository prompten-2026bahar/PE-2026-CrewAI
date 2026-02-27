
# Hızlı Başlangıç
 İlk yapay zeka agent'inizi 5 dakikadan kısa sürede CrewAI ile oluşturun.


## İlk CrewAI Agent'inizi Oluşturun

`araştırma` ve `bildiri` yapabilen, belirli bir konu veya konuda `en son yapay zeka gelişmelerini` araştıran basit bir crew oluşturalım.

Devam etmeden önce, CrewAI'ı kurduğunuzdan emin olun.
Henüz kurmadıysanız, [kurulum kılavuzu](/en/installation) adresindeki adımları takip ederek kurabilirsiniz.

Crew'lerinizi çalıştırmaya başlamak için aşağıdaki adımları izleyin! 🚣‍♂️


  
  Aşağıdaki komutu terminalinizde çalıştırarak yeni bir crew projesi oluşturun.
  Bu, crew'nuz için temel yapıya sahip `latest-ai-development` adlı yeni bir dizin oluşturacaktır.
    
      ```shell Terminal
      crewai create crew latest-ai-development
      ```
    
  
  
    
      ```shell Terminal
      cd latest_ai_development
      ```
    
  
  
  
  Gerekirse agent'leri kullanım durumunuza uyacak şekilde değiştirebilir veya olduğu gibi projenize kopyalayıp yapıştırabilirsiniz.
  `agents.yaml` ve `tasks.yaml` dosyalarınızdaki `{topic}` gibi değişkenler, `main.py` dosyasındaki değişkenin değeriyle değiştirilecektir.
  
    ```yaml agents.yaml
    # src/latest_ai_development/config/agents.yaml
    researcher:
      role: >
        {topic} Kıdemli Veri Araştırmacısı
      goal: >
        {topic} konusundaki son gelişmeleri ortaya çıkarın
      backstory: >
        Siz, {topic} konusunda en son
        gelişmeleri ortaya çıkarma konusunda becerikli, deneyimli bir araştırmacısınız. En alakalı
        bilgileri bulma ve açık ve öz bir şekilde sunma becerisiyle tanınıyorsunuz.

    reporting_analyst:
      role: >
        {topic} Raporlama Analisti
      goal: >
        {topic} veri analizi ve araştırma bulgularına dayalı ayrıntılı raporlar oluşturun
      backstory: >
        Siz, ayrıntılara büyük önem veren titiz bir analistsiniz. Karmaşık verileri, herkesin kolayca anlayabileceği ve üzerinde harekete geçebileceği açık ve öz raporlara dönüştürme yeteneğinizle tanınıyorsunuz.
    ```

  
  
    ```yaml tasks.yaml
    # src/latest_ai_development/config/tasks.yaml
    research_task:
      description: >
        {topic} hakkında kapsamlı bir araştırma yapın
        2025'in şu anki yılı göz önüne alındığında ilgili ve ilginç herhangi bir bilgi bulun.
      expected_output: >
        {topic} ile ilgili en alakalı bilgilerin 10 madde içeren bir listesi
      agent: researcher

    reporting_task:
      description: >
        Aldığınız bağlamı gözden geçirin ve her konuyu tam bir rapor için ayrı bir bölüme genişletin.
        Raporun ayrıntılı ve sağladığınız tüm ilgili bilgileri içermesini sağlayın.
      expected_output: >
        Tamamen flet raporlar ana konularla ve her biri ayrıntılı bir bölümle birlikte.
        '```' olmadan markdown olarak biçimlendirilmiş.
      agent: reporting_analyst
      output_file: report.md
    ```

  
  
    ```python crew.py
    # src/latest_ai_development/crew.py
    from crewai import Agent, Crew, Process, Task
    from crewai.project import CrewBase, agent, crew, task
    from crewai_tools import SerperDevTool
    from crewai.agents.agent_builder.base_agent import BaseAgent
    from typing import List

    @CrewBase
    class LatestAiDevelopmentCrew():
      """LatestAiDevelopment crew"""

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
      def reporting_analyst(self) -> Agent:
        return Agent(
          config=self.agents_config['reporting_analyst'], # type: ignore[index]
          verbose=True
        )

      @task
      def research_task(self) -> Task:
        return Task(
          config=self.tasks_config['research_task'], # type: ignore[index]
        )

      @task
      def reporting_task(self) -> Task:
        return Task(
          config=self.tasks_config['reporting_task'], # type: ignore[index]
          output_file='output/report.md' # Bu dosya nihai raporu içerecektir.
        )

      @crew
      def crew(self) -> Crew:
        """LatestAiDevelopment crew oluşturur"""
        return Crew(
          agents=self.agents, # Otomatik olarak @agent dekoratörü tarafından oluşturulur
          tasks=self.tasks, # Otomatik olarak @task dekoratörü tarafından oluşturulur
          process=Process.sequential,
          verbose=True,
        )
    ```

  
  
    ```python crew.py
    # src/latest_ai_development/crew.py
    from crewai import Agent, Crew, Process, Task
    from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
    from crewai_tools import SerperDevTool

    @CrewBase
    class LatestAiDevelopmentCrew():
      """LatestAiDevelopment crew"""

      @before_kickoff
      def before_kickoff_function(self, inputs):
        print(f"Başlangıç öncesi fonksiyon girdileriyle: {inputs}")
        return inputs # Girdileri döndürebilir veya gerektiği gibi değiştirebilirsiniz

      @after_kickoff
      def after_kickoff_function(self, result):
        print(f"Başlangıç sonrası fonksiyon sonuçla: {result}")
        return result # Sonucu döndürebilir veya gerektiği gibi değiştirebilirsiniz

      # ... kalan kod
    ```

  
  
  Örneğin, araştırmayı ve raporlamayı özelleştirmek için crew'nize `topic` girdisini iletebilirsiniz.
    ```python main.py
    #!/usr/bin/env python
    # src/latest_ai_development/main.py
    import sys
    from latest_ai_development.crew import LatestAiDevelopmentCrew

    def run():
      """
      Crew'yü çalıştırın.
      """
      inputs = {
        'topic': 'AI Agentları'
      }
      LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
    ```

  
  
  Crew'nizi çalıştırmadan önce, aşağıdaki anahtarların `.env` dosyanızda ortam değişkenleri olarak ayarlandığından emin olun:
    - [Serper.dev](https://serper.dev/) API anahtarı: `SERPER_API_KEY=YOUR_KEY_HERE`
    - Seçtiğiniz model için yapılandırma, örneğin bir API anahtarı. Nasıl yapılandırılacağını öğrenmek için
        [LLM kurulum kılavuzu](/en/concepts/llms#setting-up-your-llm) adresine bakın herhangi bir sağlayıcıdan modeller.
  
  
    - Bağımlılıkları kilitleyin ve CLI komutuyla kurun:
      
        ```shell Terminal
        crewai install
        ```
      
    - Kurmak istediğiniz ek paketler varsa, şunu çalıştırarak yapabilirsiniz:
      
        ```shell Terminal
        uv add <paket_adı>
        ```
      
  
  
    - Crew'nizi çalıştırmak için, projenizin kök dizininde aşağıdaki komutu çalıştırın:
      
        ```bash Terminal
        crewai run
        ```
      
  

  
  
    
  CrewAI AMP kullanıcıları için, kod yazmadan aynı crew'yi oluşturabilirsiniz:

1. CrewAI AMP hesabınıza giriş yapın (ücretsiz bir hesap oluşturun [app.crewai.com](https://app.crewai.com))
2. Crew Studio'yu açın
3. Oluşturmaya çalıştığınız otomasyonu yazın
4. Görevleri görsel olarak oluşturun ve sırayla bağlayın
5. Girdilerinizi yapılandırın ve "Kodu İndir" veya "Dağıt" düğmesine tıklayın

<img src="../images/crew-studio-interface.png" alt="Crew Studio Hızlı Başlangıç" />

### CrewAI AMP'de Dağıtın

    CrewAI AMP'de ücretsiz hesabınızı başlatın ve crew'nizi sadece birkaç tıklamayla üretim ortamında dağıtın.
  
  
  
  Çıktıyı konsolda görmeli ve nihai raporla birlikte kök dizininde `report.md` dosyası oluşturulmalıdır.

İşte raporun nasıl görünebileceğinin bir örneği:

  
    ```markdown output/report.md
    # 2025 Yılında AI Agentlarının Yükselişi ve Etkisi Hakkında Kapsamlı Rapor

    ## 1. AI Agentlarına Giriş
    2025'te, Yapay Zeka (AI) ajanları çeşitli sektörlerde inovasyonun ön saflarında yer almaktadır. Genellikle insan bilişini gerektiren görevleri yerine getirebilen akıllı sistemler olarak, AI ajanları operasyonel verimlilikte, karar vermede ve genel üretkenlikte önemli ilerlemeler için zemin hazırlamaktadır. Bu rapor, bir konu veya konuda AI ajanlarının yükselişini, çerçevelerini, uygulamalarını ve potansiyel etkilerini açıklamayı amaçlamaktadır.

    ## 2. AI Ajanlarının Faydaları
    AI ajanları, geleneksel çalışma ortamlarını dönüştüren sayısız avantaj getiriyor. Temel avantajlar şunları içerir:

    - **Görev Otomasyonu**: AI ajanları, veri girişi, planlama ve bordro işleme gibi tekrarlayan görevleri insan müdahalesi olmadan gerçekleştirebilir ve bu görevlere harcanan zamanı ve kaynakları büyük ölçüde azaltabilir.
    - **Gelişmiş Verimlilik**: Büyük veri kümelerini hızla işleyerek ve insanların önemli ölçüde daha uzun zaman alacak analizler yaparak, AI ajanları operasyonel verimliliği artırır. Bu, ekiplerin daha yüksek düzeyde düşünmeyi gerektiren stratejik görevlere odaklanmasını sağlar.
    - **Gelişmiş Karar Verme**: AI ajanları, verilerdeki eğilimleri ve örüntüleri analiz edebilir, fikirler sunabilir ve hatta eylemler önerebilir ve paydaşların gerçek verilere dayalı bilinçli kararlar almasına yardımcı olabilir.

    AI'nın sürekli gelişmesiyle, bu ajanları kullanan İK departmanları hem verimlilikte hem de çalışan memnuniyetinde önemli iyileşmeler kaydedebilir.

    ## 3. Popüler AI Ajanı Çerçeveleri
    AI ajanlarının geliştirilmesini kolaylaştıran çeşitli çerçeveler ortaya çıkmıştır, her biri kendi benzersiz özelliklerine ve yeteneklerine sahiptir. En popüler çerçevelerden bazıları şunlardır:

    - **Autogen**: Kod oluşturma otomasyonu yoluyla AI ajanlarının geliştirilmesini kolaylaştırmak için tasarlanmış bir çerçeve.
    - **Semantic Kernel**: Doğal dil işlemesi ve anlaması üzerine odaklanarak, ajanların kullanıcı niyetini daha iyi anlamasını sağlar.
    - **Promptflow**: Geliştiricilerin karmaşık etkileşimleri sorunsuz bir şekilde gezinebilen sohbetçi ajanlar oluşturması için araçlar sağlar.
    - **Langchain**: Ajanların çeşitli API'lere erişmesini ve bunları etkili bir şekilde kullanmasını sağlamak için çeşitli API'leri kullanma konusunda uzmanlaşmıştır.
    - **CrewAI**: İşbirliğine yönelik ortamlar için tasarlanmıştır, CrewAI AI tarafından sağlanan bilgilerle iletişimi kolaylaştırarak ekip çalışmasını güçlendirir.
    - **MemGPT**: Daha kişiselleştirilmiş etkileşimler için üretken yeteneklerle bellek optimize edilmiş mimarileri birleştirir.

    Bu çerçeveler, geliştiricilerin çok yönlü ve akıllı ajanlar oluşturmasını sağayarak kullanıcılarla etkileşim kurabilen, gelişmiş analizler gerçekleştirebilen ve örgütsel hedeflerle uyumlu çeşitli görevleri yürütebilen ajanlar oluşturmalarına olanak tanır.

    ## 4. İnsan Kaynakları'nda AI Ajanları
    AI ajanları, temel fonksiyonları otomatikleştirerek ve optimize ederek İK uygulamelerinde devrim yaratıyor:

    - **İşe Alım**: AI ajanları özgeçmişleri tarayabilir, mülakatları planlayabilir ve hatta ilk değerlendirmeler yapabilir ve bu da işe alım sürecini hızlandırırken önyargıları en aza indirebilir.
    - **Yönetim Devri**: AI sistemleri, çalışan performans verilerini ve potansiyeli analiz ederek kuruluşların gelecekteki liderleri belirlemesine ve uygun eğitimi planlamasına yardımcı olur.
    - **Çalışan Bağlılığı**: AI tarafından desteklenen sohbet robotları, çalışanlar ve yönetim arasında bir geri bildirim döngüsünü kolaylaştırarak açık bir kültür teşvik eder ve endişeleri derhal ele alır.

    AI'nın evrimi devam ettikçe, bu ajanları kullanan İK departmanları hem verimlilikte hem de çalışan memnuniyetinde önemli iyileşmeler kaydedebilir.

    ## 5. Finansta AI Ajanları
    Finans sektörü, finansal uygulamaları geliştiren AI ajanlarının kapsamlı bir şekilde entegrasyonu görüyor:

    - **Gider Takibi**: Otomatik sistemler, anormallikleri işaretleyen ve harcama örüntülerini temel alan öneriler sunan giderleri yönetir ve izler.
    - **Risk Değerlendirmesi**: AI modelleri, işlem verilerini ve davranış örüntülerini analiz ederek kredi riskini değerlendirir ve olası sahtekârlığı ortaya çıkarır.
    - **Yatırım Kararları**: AI ajanları, tarihsel verilere ve mevcut piyasa koşullarına göre stok tahminleri ve analizleri sağlayarak yatırımcıları bilgilendirici bilgilerle güçlendirir.

    Finansa AI ajanlarının entegrasyonu, daha duyarlı ve risk bilincinde bir finansal manzara yaratmaktadır.

    ## 6. Piyasa Trendleri ve Yatırımlar
    AI ajanlarının büyümesi, özellikle sohbet robotları ve üretken yapay zeka teknolojilerinin popülaritesinin artmasıyla önemli yatırımları çekmiştir. Şirketler ve girişimciler, bu sistemlerin potansiyelini keşfetmeye istekli ve operasyonları düzene sokma ve müşteri katılımını iyileştirme yeteneklerini tanıyorlar.

    Microsoft gibi şirketler, ürün tekliflerine AI ajanlarını entegre etmek için önemli adımlar atıyor ve bu da işyerinde yapay zeka okuryazarlığının önemini vurguluyor ve AI ajanlarının temel iş araçları olarak istikrara kavuştuğunun bir işareti.

    ## 7. Gelecek Tahminleri ve Etkileri
    Uzmanlar, AI ajanlarının çalışma yaşamının temel yönlerini dönüştüreceğini tahmin ediyor. Geleceğe baktığımızda, birkaç beklenen değişiklik şunları içerir:

    - İşlevselliğin her işletme fonksiyonuna entegre edilmesi, tüm departmanlar arasında veri akışını kullanan bağlantılı sistemler oluşturarak kapsamlı karar alma imkanı sağlar.
    - Yapay zeka teknolojilerinde sürekli bir ilerleme, kullanıcı etkileşimlerinden öğrenme ve evrimleşme yeteneğine sahip daha akıllı ve daha uyarlanabilir ajanlara yol açar.
    - Veri gizliliği ve çalışan gözetimi konusunda özellikle endişe duyulan etik kullanım konusunda artan yasal inceleme, AI ajanları daha yaygın hale geldikçe.

    Rekabet avantajı elde etmek ve AI ajanlarının tüm potansiyelini kullanmak için kuruluşlar, AI teknolojilerindeki en son gelişmelerden haberdar kalmalı ve stratejik planlamalarında sürekli öğrenme ve uyum sağlama hususunu dikkate almalıdır.

    ## 8. Sonuç
    AI ajanlarının yükselişi, 2025 yılında çalışma manzarası üzerinde kaçınılmaz bir etki yaratıyor. Görevleri otomatikleştirme, verimliliği artırma ve karar vermeyi iyileştirme yetenekleri ile AI ajanları operasyonel başarı için kritik öneme sahiptir. Kuruluşların rekabetçi bir ortamda gelişmek için AI gelişmelerini benimsemesi ve uyum sağlaması gerekmektedir.
    ```

  
  
Tebrikler!

Crew projenizi başarıyla kurdunuz ve kendi agentik iş akışlarınızı oluşturmaya hazırız!



### Adlandırma Tutarlılığı Hakkında Not

`agents.yaml` ve `tasks.yaml` dosyalarınızda kullandığınız adların, Python kodunuzdaki yöntem adlarıyla eşleşmesi gerekir.
Örneğin, görevler için `tasks.yaml` dosyasından agent'a referans verebilirsiniz.
Bu adlandırma tutarlılığı, CrewAI'ın yapılandırmalarınızı kodunuzla otomatik olarak ilişkilendirmesini sağlar; aksi takdirde göreviniz referansı düzgün şekilde tanıyamaz.

#### Örnek Referanslar


  Agent'ın adının `agents.yaml`
  (`email_summarizer`) dosyasında yöntem adıyla nasıl aynı olduğunu not edin
  (`crew.py`) dosyasında (`email_summarizer`).


```yaml agents.yaml
email_summarizer:
  role: >
    E-posta Özeti
  goal: >
    E-postaları öz ve açık bir özete dönüştürün
  backstory: >
    Raporun 5 maddelik bir özetini oluşturacaksınız
  llm: provider/model-id # Burada tercih ettiğiniz modeli ekleyin
```


  Görev adının `tasks.yaml`
  (`email_summarizer_task`) dosyasında yöntem adıyla nasıl aynı olduğunu not edin
  (`crew.py`) dosyasında (`email_summarizer_task`).


```yaml tasks.yaml
email_summarizer_task:
  description: >
    E-postayı 5 maddelik bir özete dönüştürün
  expected_output: >
    E-postanın 5 maddelik özeti
  agent: email_summarizer
  context:
    - reporting_task
    - research_task
```

## Crew'nuzu Dağıtın

Crew'nizi üretime dağıtmanın en kolay yolu [CrewAI AMP](http://app.crewai.com) adresinden yapmaktır.

Adım adım bir gösterim için bu video eğitimine bakın crew'nuzu [CrewAI AMP](http://app.crewai.com) adresine dağıtın.

[![CrewAI Dağıtım Kılavuzu](https://img.youtube.com/vi/3EqSV-CYDZA/0.jpg)](https://www.youtube.com/watch?v=3EqSV-CYDZA)


  ### Şirket Ortamında Dağıtın

    CrewAI AMP'de ücretsiz hesabınızı başlatın ve crew'nuzu sadece birkaç tıklamayla üretim ortamında dağıtın.
  
  
  
  ### Topluluğa Katılın

    Fikirleri tartışmak, projelerinizi paylaşmak ve
    diğer CrewAI geliştiricileriyle bağlantı kurmak için açık kaynak topluluğumuza katılın.