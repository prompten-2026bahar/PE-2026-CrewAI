> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Stagehand Aracı

> Tarayıcı etkileşimi ve otomasyonu için Stagehand'i CrewAI ile entegre eden web otomasyon aracı

# Genel Bakış

`StagehandTool`, [Stagehand](https://docs.stagehand.dev/get_started/introduction) çatısını CrewAI ile entegre ederek ajanların doğal dil komutları kullanarak web siteleriyle etkileşime girmesini ve tarayıcı görevlerini otomatikleştirmesini sağlar.

## Genel Bakış

Stagehand, Browserbase tarafından geliştirilmiş güçlü bir tarayıcı otomasyon çatısıdır ve yapay zeka ajanlarının şunları yapmasına olanak tanır:

* Web sitelerinde gezinme
* Düğmelere, bağlantılara ve diğer öğelere tıklama
* Form doldurma
* Web sayfalarından veri çıkarma
* Öğeleri gözlemleme ve tanımlama
* Karmaşık iş akışlarını yürütme

StagehandTool, CrewAI ajanlarına üç temel ilkel üzerinden tarayıcı kontrol yetenekleri sağlamak için Stagehand Python SDK'sını sarmalar:

1. **Act**: Tıklama, yazma veya gezinme gibi eylemleri gerçekleştirme
2. **Extract**: Web sayfalarından yapılandırılmış veri çıkarma
3. **Observe**: Sayfadaki öğeleri tanımlama ve analiz etme

## Ön Koşullar

Bu aracı kullanmadan önce şunlara sahip olduğunuzdan emin olun:

1. API anahtarı ve proje kimliğine sahip bir [Browserbase](https://www.browserbase.com/) hesabı
2. Bir LLM için API anahtarı (OpenAI veya Anthropic Claude)
3. Kurulu Stagehand Python SDK

Gerekli bağımlılığı kurun:

```bash  theme={null}
pip install stagehand-py
```

## Kullanım

### Temel Uygulama

StagehandTool iki şekilde kullanılabilir:

#### 1. Bağlam Yöneticisi Kullanımı (Önerilen)

<Tip>
  Bağlam yöneticisi yaklaşımı, istisna oluşsa bile kaynakların düzgün şekilde temizlenmesini garanti ettiği için önerilir.
</Tip>

```python  theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import StagehandTool
from stagehand.schemas import AvailableModel

# Aracı API anahtarlarınızla bir bağlam yöneticisi kullanarak başlatın
with StagehandTool(
    api_key="your-browserbase-api-key",
    project_id="your-browserbase-project-id",
    model_api_key="your-llm-api-key",  # OpenAI or Anthropic API key
    model_name=AvailableModel.CLAUDE_3_7_SONNET_LATEST,  # Optional: specify which model to use
) as stagehand_tool:
    # Araç ile bir ajan oluştur
    researcher = Agent(
            role="Web Araştırmacısı",
            goal="Web sitelerinden bilgi bul ve özetle",
            backstory="Çevrimiçi bilgi bulma konusunda uzmanım.",
        verbose=True,
        tools=[stagehand_tool],
    )

    # Aracı kullanan bir görev oluştur
    research_task = Task(
        description="https://www.example.com adresine git ve ana sayfada ne gördüğünü söyle.",
        agent=researcher,
    )

    # Ekibi çalıştır
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True,
    )

    result = crew.kickoff()
    print(result)
```

#### 2. Manuel Kaynak Yönetimi

```python  theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import StagehandTool
from stagehand.schemas import AvailableModel

# Aracı API anahtarlarınızla başlatın
stagehand_tool = StagehandTool(
    api_key="your-browserbase-api-key",
    project_id="your-browserbase-project-id",
    model_api_key="your-llm-api-key",
    model_name=AvailableModel.CLAUDE_3_7_SONNET_LATEST,
)

try:
    # Araç ile bir ajan oluştur
    researcher = Agent(
            role="Web Araştırmacısı",
            goal="Web sitelerinden bilgi bul ve özetle",
            backstory="Çevrimiçi bilgi bulma konusunda uzmanım.",
        verbose=True,
        tools=[stagehand_tool],
    )

    # Aracı kullanan bir görev oluştur
    research_task = Task(
        description="https://www.example.com adresine git ve ana sayfada ne gördüğünü söyle.",
        agent=researcher,
    )

    # Ekibi çalıştır
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True,
    )

    result = crew.kickoff()
    print(result)
finally:
    # Kaynakları açıkça temizle
    stagehand_tool.close()
```

## Komut Türleri

StagehandTool, belirli web otomasyon görevleri için üç farklı komut türünü destekler:

### 1. Act Komutu

`act` komut türü (varsayılan), düğmelere tıklama, form doldurma ve gezinme gibi web sayfası etkileşimlerini sağlar.

```python  theme={null}
# Bir eylem gerçekleştir (varsayılan davranış)
result = stagehand_tool.run(
    instruction="Click the login button", 
    url="https://example.com",
    command_type="act"  # Default, so can be omitted
)

# Bir form doldur
result = stagehand_tool.run(
    instruction="Fill the contact form with name 'John Doe', email 'john@example.com', and message 'Hello world'", 
    url="https://example.com/contact"
)
```

### 2. Extract Komutu

`extract` komut türü, web sayfalarından yapılandırılmış veri alır.

```python  theme={null}
# Tüm ürün bilgilerini çıkar
result = stagehand_tool.run(
    instruction="Extract all product names, prices, and descriptions", 
    url="https://example.com/products",
    command_type="extract"
)

# Bir seçici ile belirli bilgileri çıkar
result = stagehand_tool.run(
    instruction="Extract the main article title and content", 
    url="https://example.com/blog/article",
    command_type="extract",
    selector=".article-container"  # İsteğe bağlı CSS seçici
)
```

### 3. Observe Komutu

`observe` komut türü, web sayfası öğelerini tanımlar ve analiz eder.

```python  theme={null}
# Etkileşimli öğeleri bul
result = stagehand_tool.run(
    instruction="Find all interactive elements in the navigation menu", 
    url="https://example.com",
    command_type="observe"
)

# Form alanlarını tanımla
result = stagehand_tool.run(
    instruction="Identify all the input fields in the registration form", 
    url="https://example.com/register",
    command_type="observe",
    selector="#registration-form"
)
```

## Yapılandırma Seçenekleri

StagehandTool davranışını şu parametrelerle özelleştirin:

```python  theme={null}
stagehand_tool = StagehandTool(
    api_key="your-browserbase-api-key",
    project_id="your-browserbase-project-id",
    model_api_key="your-llm-api-key",
    model_name=AvailableModel.CLAUDE_3_7_SONNET_LATEST,
    dom_settle_timeout_ms=5000,  # DOM'un oturması için daha uzun bekle
    headless=True,  # Tarayıcıyı headless modda çalıştır
    self_heal=True,  # Hatalardan kurtulmayı dene
    wait_for_captcha_solves=True,  # CAPTCHA çözümünü bekle
    verbose=1,  # Günlük ayrıntı düzeyini kontrol et (0-3)
)
```

## En İyi Uygulamalar

1. **Spesifik Olun**: Daha iyi sonuçlar için ayrıntılı talimatlar verin
2. **Uygun Komut Türünü Seçin**: Göreviniz için doğru komut türünü seçin
3. **Seçiciler Kullanın**: Doğruluğu artırmak için CSS seçicilerden yararlanın
4. **Karmaşık Görevleri Bölün**: Karmaşık iş akışlarını birden fazla araç çağrısına ayırın
5. **Hata Yönetimi Uygulayın**: Olası sorunlar için hata yönetimi ekleyin

## Sorun Giderme

Yaygın sorunlar ve çözümleri:

* **Oturum Sorunları**: Hem Browserbase hem LLM sağlayıcısı için API anahtarlarını doğrulayın
* **Öğe Bulunamadı**: Yavaş sayfalar için `dom_settle_timeout_ms` değerini artırın
* **Eylem Başarısızlıkları**: Önce doğru öğeleri tanımlamak için `observe` kullanın
* **Eksik Veri**: Talimatları iyileştirin veya belirli seçiciler verin

## Ek Kaynaklar

CrewAI entegrasyonu hakkındaki sorular için:

* Stagehand'in [Slack topluluğuna](https://stagehand.dev/slack) katılın
* [Stagehand deposunda](https://github.com/browserbase/stagehand) bir issue açın
* [Stagehand dokümantasyonunu](https://docs.stagehand.dev/) ziyaret edin
