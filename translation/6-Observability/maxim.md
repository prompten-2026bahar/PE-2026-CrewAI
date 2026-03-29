# Maxim Genel Bakış

Maxim AI, CrewAI uygulamalarınız için kapsamlı agent izleme, değerlendirme ve gözlemlenebilirlik sağlar. Maxim'in tek satırlık entegrasyonu sayesinde agent etkileşimlerini, performans metriklerini ve daha fazlasını kolayca izleyebilir ve analiz edebilirsiniz.

## Özellikler

### Prompt Yönetimi

Maxim'in Prompt Yönetimi yetenekleri sayesinde agent'larınız için prompt'ları oluşturabilir, düzenleyebilir ve optimize edebilirsiniz. Talimatları sabit kodlamak yerine, Maxim'in SDK'sını kullanarak sürüm kontrollü prompt'ları dinamik olarak alıp uygulayabilirsiniz.

  
    Prompt'larınızı oyun alanında oluşturun, iyileştirin, deney yapın ve dağıtın. Prompt'larınızı klasörler ve sürümler kullanarak düzenleyin, araçları ve bağlamı ilişkilendirerek gerçek dünya durumlarıyla deney yapın ve özel mantık kullanarak dağıtın.

    [**Modelleri yapılandırın**](https://www.getmaxim.ai/docs/introduction/quickstart/setting-up-workspace#add-model-api-keys) ve prompt oyun alanının en üstündeki ilgili modeli seçerek kolayca farklı modeller üzerinde deney yapın.

  <img src='https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_playground.png'> </img>
  
  
    Takımlar AI uygulamalarını oluştururken, prompt yapısını yinelemek büyük bir parçadır. Etkili bir şekilde işbirliği yapmak ve değişikliklerinizi açıkça düzenlemek için Maxim prompt sürümleme ve sürümler arasında karşılaştırma çalıştırmalarına olanak tanır.

  <img src='https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_versions.png'> </img>
  
  
    AI uygulamanız geliştikçe, prompt yapıları, modeller vb. üzerinde deneyler yapmak gerekecektir. Değişiklikler hakkında bilinçli kararlar verebilmek için, karşılaştırma oyun alanı sonuçların yan yana görünümünü sağlar.

    ## **Neden Prompt karşılaştırması kullanmalı?**

    Prompt karşılaştırması, birden çok tek tek Prompt'u tek bir görünümde birleştirerek çeşitli iş akışları için düzgün bir yaklaşım sağlar:

    1. **Model karşılaştırması**: Aynı Prompt üzerinde farklı modellerin performansını değerlendirin.
    2. **Prompt optimizasyonu**: En etkili formülasyonu belirlemek için bir Prompt'un farklı sürümlerini karşılaştırın.
    3. **Çapraz Model tutarlılığı**: Aynı Prompt için çeşitli modellerde tutarlı çıktılar sağladığınızdan emin olun.
    4. **Performans kıyaslaması**: Farklı modeller ve Prompt'lar arasında gecikme, maliyet ve belirteç sayımı gibi metrikleri analiz edin.
  


### Gözlemlenebilirlik & Değerlendirmeler

Maxim AI, CrewAI agent'larınız için kapsamlı gözlemlenebilirlik ve değerlendirme sağlayarak her yürütme sırasında tam olarak ne olduğunu anlamanıza yardımcı olur.

  
    Araç çağrılarını, agent yollarını ve karar akışlarını zahmetsizce izleyerek agent'ınızın tamamını izleyin.

<img src='https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_agent_tracking.png'> </img>
  
  
    Desteklenen:

    - Çok aşamalı etkileşimler ve granüler iz analizi
    - Oturum Seviyesi Değerlendirmeler
    - Gerçek dünya testleri için Simülasyonlar

    Tam izler veya ayrı düğümler üzerinde ayrıntılı değerlendirmeler gerçekleştirin

  <img src='https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_trace_eval.png'> </img>

    
      ### Otomatik Değerlendirmeler Loglardan

        <p>
        Filtreler ve örnekleme ile arayüzden yakalanan günlükleri otomatik olarak değerlendirin

        </p>
      
      ### İnsan Değerlendirmeleri Loglardan

        <p>
        Günlüklerinizin kalitesini değerlendirmek ve günlüklerinizi değerlendirmek için insan değerlendirmesi veya puanlaması kullanın.

        </p>
      
      ### Düğüm Seviyesi Değerlendirmeler

        <p>
        Agent'ınızın davranışına ilişkin bilgiler edinmek için izinizdeki veya günlüğünüzdeki herhangi bir bileşeni değerlendirin.

        </p>
      
    
    ---
  
  
    **Hata**, **maliyet, belirteç kullanımı, kullanıcı geri bildirimi, gecikme** için eşikler belirleyin ve Slack veya PagerDuty üzerinden gerçek zamanlı uyarılar alın.

<img src='https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_alerts_1.png'> </img>
  
  
    İzleri, kullanım metriklerini, gecikme ve hata oranlarını kolaylıkla görselleştirin.

<img src='https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_dashboard_1.png'> </img>
  


## Başlangıç

### Önkoşullar


- Python sürümü \>=3.10
- Bir Maxim hesabı ([buradan kaydolun](https://getmaxim.ai/))
- Maxim API Anahtarını Oluşturun
- Bir CrewAI projesi

### Kurulum

Maxim SDK'sını pip ile yükleyin:

```python
pip install maxim-py
```

Veya `requirements.txt` dosyanıza ekleyin:

```
maxim-py
```
### Temel Kurulum

### 1. Ortam değişkenlerini ayarlayın

```python
### Ortam Değişkenleri Kurulumu

# Proje kökünüzde bir `.env` dosyası oluşturun:

# Maxim API Yapılandırması
MAXIM_API_KEY=your_api_key_here
MAXIM_LOG_REPO_ID=your_repo_id_here
```

### 2. Gerekli paketleri içe aktarın

```python
from crewai import Agent, Task, Crew, Process
from maxim import Maxim
from maxim.logger.crewai import instrument_crewai
```

### 3. API anahtarınızla Maxim'i başlatın


```python {8}
# CrewAI'ı sadece tek bir satırla donatın
instrument_crewai(Maxim().logger())
```

### 4. CrewAI uygulamanızı her zamanki gibi oluşturun ve çalıştırın

```python
# Agent'ınızı oluşturun
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI',
    backstory="You are an expert researcher at a tech think tank...",
    verbose=True,
    llm=llm
)

# Görevi tanımlayın
research_task = Task(
    description="Research the latest AI advancements...",
    expected_output="",
    agent=researcher
)

# Ekibi yapılandırın ve çalıştırın
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

try:
    result = crew.kickoff()
finally:
    maxim.cleanup()  # Hatalar oluşsa bile temizliğin yapıldığından emin olun
```


İşte bu kadar! Tüm CrewAI agent etkileşimleriniz şimdi Maxim kontrol panelinizde günlüğe kaydedilecek ve kullanılabilir olacaktır.

Hızlı bir referans için bu Google Colab Not Defterine bakın - [Not Defteri](https://colab.research.google.com/drive/1ZKIZWsmgQQ46n8TH9zLsT1negKkJA6K8?usp=sharing)

## İzlerinizi Görüntüleme

CrewAI uygulamanızı çalıştırdıktan sonra:

1. [Maxim Kontrol Panelinize](https://app.getmaxim.ai/login) giriş yapın
2. Deponuza gidin
3. Aşağıdakiler dahil olmak üzere ayrıntılı agent izlerini görüntüleyin:
   - Agent konuşmaları
   - Araç kullanım kalıpları
   - Performans metrikleri
   - Maliyet analizi

    <img src='https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/crewai_traces.gif'> </img>

## Sorun Giderme

### Yaygın Sorunlar

- **İzler görünmüyor**: API anahtarınızın ve depo kimliğinizin doğru olduğundan emin olun
- Doğru şekilde çalıştırmak için **`instrument_crewai()`**'ı **_önce_** çağırın. Bu, günlükleme kancalarını doğru şekilde başlatır.
- Herhangi bir dahili hatayı ortaya çıkarmak için `instrument_crewai()` çağrınızda `debug=True`'u ayarlayın:

  ```python
  instrument_crewai(logger, debug=True)
  ```
- Ayrıntılı günlükleri yakalamak için agent'larınızı `verbose=True` ile yapılandırın:

  ```python
  agent = CrewAgent(..., verbose=True)
  ```
- `instrument_crewai()`'in agent'ları oluşturmadan veya yürütmeden **önce** çağrıldığından emin olun. Bu bariz olabilir, ancak sık yapılan bir hata olabilir.

## Kaynaklar


  ### CrewAI Belgeleri

    Resmi CrewAI belgeleri
  
  ### Maxim Belgeleri

    Resmi Maxim belgeleri
  
  ### Maxim Github

    Maxim Github