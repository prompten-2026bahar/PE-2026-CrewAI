# Portkey Entegrasyonu
CrewAI ile Portkey'i kullanma şekli


<img src="https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/main/Portkey-CrewAI.png" alt="Portkey CrewAI Başlık Resmi" width="70%" />



## Giriş

Portkey, CrewAI'ye üretim-hazırlık özelliklerini ekleyerek, deneysel agent gruplarınızı, her adımda, araç kullanımında ve etkileşimde tamamıyla gözlemlenebilir, yerleşik güvenilirlik, maliyet takibi ve optimizasyonu, 200'den fazla LLM'ye tek bir entegrasyon yoluyla erişim, agent davranışını güvende ve uyumlu tutan koruyucu önlemler ve tutarlı agent performansı için sürüm kontrollü istemler sağlayarak sağlam sistemlere dönüştürür.

### Kurulum & Yapılandırma

```bash
pip install -U crewai portkey-ai
```

[Portkey dashboard](https://app.portkey.ai/) adresinden isteğe bağlı bütçe/hız sınırlarıyla Portkey API anahtarı oluşturun. Daha sonra bununla ilgili olarak güvenilirlik, önbellekleme ve daha fazlası için yapılandırmalar da ekleyebilirsiniz. Daha fazlasını daha sonra öğreneceksiniz.

Entegrasyon basittir – sadece CrewAI kurulumunuzdaki LLM yapılandırmanızı güncellemeniz gerekir:

```python
from crewai import LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Portkey entegrasyonlu bir LLM örneği oluşturun
gpt_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",  # Sanal bir anahtar kullandığımız için bu bir yer tutucudur
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_LLM_VIRTUAL_KEY",
        trace_id="unique-trace-id",               # İsteğe bağlı olarak, istek takibi için
    )
)

# Agent'larınızda şu şekilde kullanın:

	@agent
	def lead_market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_market_analyst'],
			verbose=True,
			memory=False,
			llm=gpt_llm
		)
```

**Sanal Anahtarlar Nelerdir?** Sanal anahtarlar, Portkey'de LLM sağlayıcı API anahtarlarınızı (OpenAI, Anthropic vb.) şifreli bir kasada güvenli bir şekilde saklar. Daha kolay anahtar rotasyonu ve bütçe yönetimi sağlar. [Sanal anahtarlar hakkında daha fazla bilgi edinin](https://portkey.ai/docs/product/ai-gateway/virtual-keys).




## Üretim Özellikleri

### 1. Gelişmiş Gözlemlenebilirlik

Portkey, CrewAI agent'larınız için kapsamlı gözlemlenebilirlik sağlayarak, her çalıştırma sırasında tam olarak neler olduğunu anlamanıza yardımcı olur.

  

<img src="https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Product%2011.1.webp"/>


İzlemeler, mürettebatınızın yürütmesinin hiyerarşik bir görünümünü sağlayarak LLM çağrıları, araç çağrıları ve durum geçişlerinin dizisini gösterir.

```python
# Hiyerarşik izlemeyi Portkey'de etkinleştirmek için trace_id ekleyin
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        trace_id="unique-session-id"  # Benzersiz bir iz süresi kimliği ekleyin
    )
)
```
  

<img src="https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Portkey%20Docs%20Metadata.png"/>


Portkey, LLM'lerle her etkileşimi kaydeder, buna:

- Tam istek ve yanıt yükleri
- Gecikme ve jeton kullanımı metrikleri
- Maliyet hesaplamaları
- Araç çağrıları ve fonksiyon yürütmeleri

Tüm günlükler, özel metadata, iz süresi kimlikleri, modeller ve daha fazlasıyla filtrelenebilir ve bu da belirli mürettebat çalıştırmalarını hata ayıklamayı kolaylaştırır.
  

  

<img src="https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Dashboard.png"/>


Portkey, size şunları yapmanıza yardımcı olan yerleşik panolar sağlar:

- Tüm mürettebat çalıştırmalarında maliyet ve jeton kullanımını takip etme
- Gecikme ve başarı oranları gibi performans metriklerini analiz etme
- Agent iş akışlarınızdaki darboğazları belirleme
- Farklı mürettebat yapılandırmalarını ve LLM'leri karşılaştırma

Tüm metrikleri özel metadata ile filtreleyip bölümlendirebilir, bu da belirli mürettebat türlerini, kullanıcı gruplarını veya kullanım durumlarını analiz etmenizi sağlar.
  

  

  <img src="https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/Metadata%20Filters%20from%20CrewAI.png" alt="Metadata filtreleriyle analizler" />


Portkey panosunda güçlü filtreleme ve bölümlendirme sağlamak için CrewAI LLM yapılandırmanıza özel metadata ekleyin:

```python
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        metadata={
            "crew_type": "research_crew",
            "environment": "production",
            "_user": "user_123",   # Kullanıcı analizi için özel _user alanı
            "request_source": "mobile_app"
        }
    )
)
```

Bu metadata, Portkey panosundaki günlükleri, izlemeleri ve metrikleri filtrelemek için kullanılabilir, bu da belirli mürettebat çalıştırmalarını, kullanıcıları veya ortamları analiz etmenizi sağlar.
  


### 2. Güvenilirlik - Mürettebatınızı Sürekli Çalışır Durumda Tutun

Mürettebatı üretime alırken, API hız sınırları, ağ sorunları veya sağlayıcı kesintileri gibi şeyler ters gidebilir. Portkey'nin güvenilirlik özellikleri, sorunlar ortaya çıktığında bile agent'larınızın sorunsuz bir şekilde çalışmaya devam etmesini sağlar.

Geri düşmeyi etkinleştirmek, Portkey Yapılandırması kullanarak CrewAI kurulumunuzda kolaydır:

```python
from crewai import LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Geri düşürme yapılandırmasına sahip LLM oluşturun
portkey_llm = LLM(
    model="gpt-4o",
    max_tokens=1000,
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        config={
            "strategy": {
                "mode": "fallback"
            },
            "targets": [
                {
                    "provider": "openai",
                    "api_key": "YOUR_OPENAI_API_KEY",
                    "override_params": {"model": "gpt-4o"}
                },
                {
                    "provider": "anthropic",
                    "api_key": "YOUR_ANTHROPIC_API_KEY",
                    "override_params": {"model": "claude-3-opus-20240229"}
                }
            ]
        }
    )
)

# Bu LLM yapılandırmasını agent'larınızla kullanın
```

Bu yapılandırma, GPT-4o isteği başarısız olduğunda Claude'yi otomatik olarak deneyecek ve mürettebatınızın çalışmaya devam etmesini sağlayacaktır.


  ### Otomatik Yeniden Denemeler

    Geçici hataları otomatik olarak ele alır. Bir LLM çağrısı başarısız olursa, Portkey aynı isteği belirtilen sayıda kez yeniden deneyecektir - hız sınırları veya ağ sorunları için mükemmeldir.
  
  ### İstek Zaman Aşımı

    Agent'larınızın askıda kalmasını önleyin. Gerekli zaman çerçeveleriniz dahilinde yanıtlar aldığınızdan (veya zarif bir şekilde başarısız olduğunuzdan) emin olmak için zaman aşımlarını ayarlayın.
  
  ### Koşullu Yönlendirme

    Farklı sağlayıcılara farklı istekler gönderin. Karmaşık muhakemeyi GPT-4'e, yaratıcı görevleri Claude'a ve hızlı yanıtları Gemini'ye ihtiyaçlarınıza göre yönlendirin.
  
  ### Geri Düşürmeler

    Birincil sağlayıcınız başarısız olsa bile çalışmaya devam edin. Otomatik olarak yedek sağlayıcılara geçerek kullanılabilirliği koruyun.
  
  ### Yük Dengeleme

    İstekleri çoklu API anahtarlarına veya sağlayıcılara yayın. Yüksek hacimli mürettebat operasyonları için ve hız sınırları dahilinde kalmak için harikadır.
  


### 3. CrewAI'de İstemleme

Portkey'nin İstem Mühendisliği Stüdyosu, CrewAI agent'larınızda kullanılan istemleri oluşturmanıza, yönetmenize ve optimize etmenize yardımcı olur. İstemleri kodlayarak sabit kodlamak yerine, sürüm kontrollü istemlerinizi dinamik olarak almak ve uygulamak için Portkey'nin istem oluşturma API'sini kullanın.

![İstem Oynatma Arayüzü](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Portkey%20Docs.webp)

Prompt Playground, istemleri karşılaştırmanız, test etmeniz ve dağıtmanız için bir yerdir. İstemi uygulamadan önce farklı modellerle ve değişkenlerle deney yapabilirsiniz. Aşağıdakileri yapmanıza olanak tanır:

1. Agent'larınızda kullanmadan önce istemleri yinelemeli olarak geliştirin
2. Farklı değişkenler ve modellerle istemleri test edin
3. Farklı istem sürümü arasındaki çıktıları karşılaştırın
4. Ekip üyelerinizle istem geliştirme konusunda işbirliği yapın

Bu görsel ortam, CrewAI agent'larınızın iş akışındaki her adım için etkili istemler oluşturmayı kolaylaştırır.
  

  
İstem Oluşturma API'si, tüm parametreler yapılandırılmış istem şablonlarınızı alır:

```python
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL, Portkey

# Portkey yönetici istemciyi başlatın
portkey_admin = Portkey(api_key="YOUR_PORTKEY_API_KEY")

# Oluşturma API'sini kullanarak istemi alın
prompt_data = portkey_client.prompts.render(
    prompt_id="YOUR_PROMPT_ID",
    variables={
        "agent_role": "Senior Research Scientist",
    }
)

backstory_agent_prompt=prompt_data.data.messages[0]["content"]


# Portkey entegrasyonlu LLM ile kurulum
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY"
    )
)

# Agent'larınızı aşağıdaki gibi kullanın:

	@agent
	def lead_market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_market_analyst'],
			verbose=True,
			memory=False,
			llm=portkey_llm
		)
```
  

  
İstem Playground, istemlerin farklı versiyonlarını karşılaştırmanıza, test etmenize ve dağıtmanıza olanak tanır. Bu, istemleri oluşturma, test etme ve iyileştirme için görsel bir ortam sağlar.

İstemler, değişkenlerin kolayca yerleştirilebilmesi için bıyık stili şablonlama kullanır:

```
Siz bir {{agent_role}}'siniz ve {{domain}} konusunda uzmanlığa sahipsiniz.

Göreviniz {{agent_goal}}'ı bilgi ve deneyiminizi kullanarak yerine getirmektir.

Her zaman {{tone}} tonunda kalın ve {{focus_area}}'ya odaklanın.
```

Yazdırırken, yalnızca değişkenleri geçirin:

```python
prompt_data = portkey_admin.prompts.render(
    prompt_id="YOUR_PROMPT_ID",
    variables={
        "agent_role": "Senior Research Scientist",
        "domain": "artificial intelligence",
        "agent_goal": "çığır açan içgörüler keşfetmek",
        "tone": "profesyonel",
        "focus_area": "pratik uygulamalar"
    }
)
```
  

  
Portkey istemleri, aynı istemin farklı versiyonlarını oluşturmanıza, versiyonlar arasında performansı karşılaştırmanıza, gerektiğinde önceki versiyonlara geri dönmenize ve kodunuzda kullanılacak versiyonu belirtmenize olanak tanır:

```python
# Belirli bir istem versiyonunu kullanın
prompt_data = portkey_admin.prompts.render(
    prompt_id="YOUR_PROMPT_ID@version_number",
    variables={
        "agent_role": "Senior Research Scientist",
        "agent_goal": "çığır açan içgörüler keşfetmek"
    }
)
```
  

  
Portkey, istemleriniz için değişken yerleştirme için bıyık stili şablonlama kullanır:

```
Siz bir {{agent_role}}'siniz ve {{domain}} konusunda uzmanlığa sahipsiniz.

Göreviniz {{agent_goal}}'ı bilgi ve deneyiminizi kullanarak yerine getirmektir.

Her zaman {{tone}} tonunda kalın ve {{focus_area}}'ya odaklanın.
```

Yazdırma sırasında değişkenleri geçirin:

```python
prompt_data = portkey_admin.prompts.render(
    prompt_id="YOUR_PROMPT_ID",
    variables={
        "agent_role": "Senior Research Scientist",
        "domain": "artificial intelligence",
        "agent_goal": "çığır açan içgörüler keşfetmek",
        "tone": "profesyonel",
        "focus_area": "pratik uygulamalar"
    }
)
```
  


### İstem Mühendisliği Stüdyosu

  Portkey'in istem yönetimi özelliklerini öğrenin

### 4. Güvenli Mürettebatlar için Koruyucu Önlemler

Koruyucu önlemler, CrewAI agent'larınızın her durumda güvenli ve uygun şekilde yanıt vermesini sağlar.

**Neden Koruyucu Önlemler Kullanmalı?**

CrewAI agent'ları çeşitli başarısızlık modları yaşayabilir:
- Zararlı veya uygunsuz içerik üretme
- Kişisel tanımlanabilir bilgilere sızdırma
- Yanlış bilgi uydurma
- Yanlış formatlarda çıktılar üretme

Portkey'nin koruyucu önlemleri, hem girişler hem de çıktılar için koruma sağlar.

**Koruyucu Önlemleri Uygulama**

```python
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Portkey koruyucu önlemleriyle LLM oluşturun
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        config={
            "input_guardrails": ["guardrails-id-xxx", "guardrails-id-yyy"],
            "output_guardrails": ["guardrails-id-zzz"]
        }
    )
)

# Koruyucu önlemli LLM ile agent oluşturun
researcher = Agent(
    role="Senior Research Scientist",
    goal="Devrim niteliğinde içgörüler keşfetmek",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

Portkey'nin koruyucu önlemleri şunları yapabilir:

- Hem girişlerde hem de çıktılarda PII'yi algılayıp sansürleme
- Uygunsuz veya zararlı içeriği filtreleme
- Yanıt formatlarını şemalara göre doğrulama
- Uydurma içerikleri temel gerçeklere göre kontrol etme
- Özel iş kurallarını ve kurallarını uygulama

### Koruyucu Önlemler hakkında daha fazla bilgi edinin

  Agent güvenliğini artırmak için Portkey'in koruyucu önlem özellikleri hakkında daha fazla bilgi edinin

### 5. Kullanıcı İzleme Metadata ile

Portkey'nin metadata sistemi, CrewAI agent'larınız aracılığıyla bireysel kullanıcıları izlemenizi sağlar.

**Portkey'de Metadata Nedir?**

Metadata, her istekle özel veri ilişkilendirmenizi sağlayarak filtrelemeyi, bölümlendirmeyi ve analizi mümkün kılar. Özel `_user` alanı, kullanıcı izleme için özel olarak tasarlanmıştır.

```python
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Kullanıcı izleme ile LLM'yi yapılandırın
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        metadata={
            "_user": "user_123",  # Kullanıcı analizi için özel _user alanı
            "user_tier": "premium",
            "user_company": "Acme Corp",
            "session_id": "abc-123"
        }
    )
)

# İzli LLM ile agent oluşturun
researcher = Agent(
    role="Senior Research Scientist",
    goal="Devrim niteliğinde içgörüler keşfetmek",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

**Kullanıcıya göre filtreleme Analizi**

Metadata yerinde, kullanıcı başına performans metriklerini analiz etmek için kullanıcıya göre filtreleme yapabilirsiniz:

  

  
### 6. Verimlilik için Önbellekleme

Agent'larınızın verimliliğini ve maliyet etkinliğini artırmak için önbellekleme uygulayın:

  

```python
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Basit bir önbellekleme ile LLM yapılandırın
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        config={
            "cache": {
                "mode": "simple"
            }
        }
    )
)

# Önbelleğe alınmış LLM ile agent oluşturun
researcher = Agent(
    role="Senior Research Scientist",
    goal="Devrim niteliğinde içgörüler keşfetmek",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

Basit önbellekleme, girdi istemlerinin tam eşleşmelerine dayanır ve aynı istemleri tekrar tekrar çalıştırılmasını önleyerek aynı istemler için yanıtları önbelleğe alır.
  

  

```python
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Anlamlı bir önbellekleme ile LLM yapılandırın
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        config={
            "cache": {
                "mode": "semantic"
            }
        }
    )
)

# Anlamlı olarak önbelleğe alınmış LLM ile agent oluşturun
researcher = Agent(
    role="Senior Research Scientist",
    goal="Devrim niteliğinde içgörüler keşfetmek",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

Anlamlı önbellekleme, girdi istekleri arasındaki bağlamsal benzerliği dikkate alarak benzer bağlamsal girdiler için yanıtları önbelleğe alır.
  


### 7. Model Etkileşimi

CrewAI çoklu LLM sağlayıcısını destekler ve Portkey bu yeteneği, tek bir arayüz aracılığıyla 200'den fazla LLM'ye erişerek genişletir. Kodunuzdaki büyük değişiklikleri yapmadan farklı modellere kolayca geçiş yapabilirsiniz:

```python
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Farklı sağlayıcılara sahip LLM'ler oluşturun
openai_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY"
    )
)

anthropic_llm = LLM(
    model="claude-3-5-sonnet-latest",
    max_tokens=1000,
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_ANTHROPIC_VIRTUAL_KEY"
    )
)

# Her agent için hangi LLM'nin kullanılacağını ihtiyaçlarınıza göre seçin
researcher = Agent(
    role="Senior Research Scientist",
    goal="Devrim niteliğinde içgörüler keşfetmek",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=openai_llm  # Anthropic için anthropic_llm kullanın
)
```

Portkey, aşağıdakiler dahil sağlayıcılardan LLM'lere erişim sağlar:

- OpenAI (GPT-4o, GPT-4 Turbo vb.)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus vb.)
- Mistral AI (Mistral Large, Mistral Medium vb.)
- Google Vertex AI (Gemini 1.5 Pro vb.)
- Cohere (Command, Command-R vb.)
- AWS Bedrock (Claude, Titan vb.)
- Yerel/Özel Modeller

### Desteklenen Sağlayıcılar

  Desteklenen LLM sağlayıcılarının eksiksiz listesini burada bulabilirsiniz

## Kurumsal Yönetişim için CrewAI'yi Kurun

**Kurumsal Yönetişim Neden?**
CrewAI'yi kuruluşunuz içinde kullanıyorsanız, aşağıdaki yönetişim yönlerini dikkate almanız gerekir:
- **Maliyet Yönetimi**: Takımlar arasında yapay zeka harcamalarını kontrol etme ve izleme
- **Erişim Kontrolü**: Hangi takımların belirli modelleri kullanabileceğini yönetme
- **Kullanım Analizi**: Yapay zekanın kuruluş genelinde nasıl kullanıldığını anlama
- **Güvenlik ve Uyumluluk**: Kurumsal güvenlik standartlarını sürdürme
- **Güvenilirlik**: Tüm kullanıcılar için tutarlı hizmet sağlamak

Portkey, bu kurumsal ihtiyaçları ele alan kapsamlı bir yönetişim katmanı ekler. Adım adım bu kontrolleri uygulayalım.

Sanal Anahtarlar, LLM sağlayıcı API anahtarlarınızı yönetmek için Portkey'in güvenli bir yoludur. Aşağıdakiler gibi temel kontroller sağlar:
- API kullanımına yönelik bütçe sınırları
- Hız sınırlama yetenekleri
- Güvenli API anahtarı depolama

Sanal anahtar oluşturmak için:
Portkey Uygulamasındaki [Sanal Anahtarlar](https://app.portkey.ai/virtual-keys) bölümüne gidin. İsteğe bağlı bütçe/hız sınırlarıyla sanal anahtar oluşturun. Daha fazlasını daha sonra öğreneceksiniz.

Yapılandırmalar, isteklerin nasıl yönlendirildiği (gelişmiş yönlendirme, geri dönüş ve yeniden denemeler gibi özellikler) tanımlamak için Portkey Yapılandırmaları aracılığıyla kontrol katmanını sağlar.

Yapılandırmanızı oluşturmak için:
1. Portkey panosundaki [Yapılandırmalar](https://app.portkey.ai/configs) bölümüne gidin
2. Yeni bir yapılandırma oluşturun:
    ```json
    {
        "virtual_key": "YOUR_VIRTUAL_KEY_FROM_STEP1",
       	"override_params": {
          "model": "gpt-4o" // Tercih ettiğiniz model adı
        }
    }
    ```
3. Sonraki adım için Yapılandırma adını kaydedin ve not edin

<img src="https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Portkey%20Docs%20Config.png" width="500"/>

Şimdi Portkey API anahtarınızı eklediğiniz yapılandırmayla oluşturun:

1. Portkey'deki [API Anahtarları](https://app.portkey.ai/api-keys) bölümüne gidin ve yeni bir API anahtarı oluşturun
2. 2. Adımda oluşturduğunuz yapılandırmayı seçin
3. API anahtarınızı oluşturun ve kaydedin

<img src="https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20API%20Key.png" width="500"/>

Portkey API anahtarınızı eklediğiniz yapılandırmayla kurduktan sonra, onu CrewAI agent'larınızla entegre edin:

```python
from crewai import Agent, LLM
from portkey_ai import PORTKEY_GATEWAY_URL

# API anahtarınızla LLM'yi yapılandırın
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="YOUR_PORTKEY_API_KEY"
)

# Portkey'li LLM ile agent oluşturun
researcher = Agent(
    role="Senior Research Scientist",
    goal="Devrim niteliğinde içgörüler keşfetmek",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

### 1. Bütçe Kontrollerini ve Hız Limitlerini Uygulayın

Sanal Anahtarlar, ekip/departman düzeyinde LLM erişimi üzerinde kapsamlı bir kontrol sağlar. Bu, aşağıdakileri yapmanıza yardımcı olur:
- [Bütçe limitleri](https://portkey.ai/docs/product/ai-gateway/virtual-keys/budget-limits) ayarlama
- Beklenmedik kullanım artışlarını hız limitleri kullanarak önleme
- Departmanlar arasında harcamaları izleme

#### Departman Özelinde Kontrolleri Kurma:
1. Portkey panosundaki [Sanal Anahtarlar](https://app.portkey.ai/virtual-keys) bölümüne gidin
2. Her departman için bütçe limitleri ve hız limitleriyle yeni bir Sanal Anahtar oluşturun
3. Departman özelinde limitleri yapılandırın

  

  
### 2. Model Erişim Kurallarını Tanımlama

Yapay zeka kullanımınız ölçeklenirken, hangi takımların hangi modellere erişebileceğini kontrol etmek çok önemli hale gelir. Portkey Yapılandırmaları, bu kontrol katmanını model kısıtlamaları ve veri koruma gibi özelliklerle sağlar.

#### Erişim Kontrolü Özellikleri:
- **Model Kısıtlamaları**: Belirli modellere erişimi sınırlayın
- **Veri Koruması**: Hassas veriler için koruyucu önlemleri uygulayın
- **Güvenilirlik Kontrolleri**: Geri dönüş ve yeniden deneme mantığını ekleyin

#### Örnek Yapılandırma:
İşte OpenAI'yi kullanmaya yönelik temel bir yapılandırma:

```json
{
	"strategy": {
		"mode": "single"
	},
	"targets": [
		{
			"virtual_key": "YOUR_OPENAI_VIRTUAL_KEY",
			"override_params": {
				"model": "gpt-4o"
			}
		}
	]
}
```

Yapılandırmanızı Portkey panosundaki [Yapılandırmalar](https://app.portkey.ai/configs) sayfasında oluşturun.

    
Yapılandırmalar, çalışan uygulamaları etkilemeden herhangi bir zamanda güncellenebilir.
    
  

  
### 3. Erişim Kontrollerini Uygulama

Otomatik olarak:
- Kullanıcı/ekip başına kullanım takibi için sanal anahtarları kullanarak
- Uygun erişim seviyeleri ve bütçe kontrolleriyle yapılandırmaları yönlendirme
- İlgili metadata'yı toplayarak filtrelemeyi sağlamak
- Erişim izinlerini zorunlu kılmak için Kullanıcıya özel API anahtarları oluşturun

Portkey Uygulamasındaki [Portkey App](https://app.portkey.ai/) aracılığıyla API anahtarlarını oluşturun

Python SDK'sını kullanarak bir örnek:
```python
from portkey_ai import Portkey

portkey = Portkey(api_key="YOUR_ADMIN_API_KEY")

api_key = portkey.api_keys.create(
    name="engineering-team",
    type="organisation",
    workspace_id="YOUR_WORKSPACE_ID",
    defaults={
        "config_id": "your-config-id",
        "metadata": {
            "environment": "production",
            "department": "engineering"
        }
    },
    scopes=["logs.view", "configs.read"]
)
```

Ayrıntılı anahtar yönetimi talimatları için [Portkey belgelerine](https://portkey.ai/docs) bakın.
  

  
### 4. Dağıt ve İzle
API anahtarlarını dağıttıktan sonra, kurumsal hazır CrewAI kurulumunuz kullanıma hazır. Her ekip üyesi, uygun erişim seviyeleri ve bütçe kontrolleri ile kendi özel API anahtarlarını kullanabilir.

Portkey panosunda kullanımı izleyin:
- Departman başına maliyet takibi
- Model kullanım kalıpları
- İstek hacimleri
- Hata oranları  

### Kurumsal Özellikler Şimdi Kullanımda
**CrewAI entegrasyonunuz artık şunlara sahip:**
- Departmanlar arası bütçe kontrolleri
- Model erişim yönetimi
- Kullanım takibi ve ataması
- Güvenlik koruyucu önlemleri
- Güvenilirlik özellikleri


## Sıkça Sorulan Sorular

  
    Portkey, kapsamlı gözlemlenebilirlik (izlemeler, günlükler, metrikler), güvenilirlik özellikleri (geri dönüş, yeniden deneme, önbellekleme) ve tek bir arayüz aracılığıyla 200'den fazla LLM'ye erişim sağlayarak CrewAI'ye üretim-hazırlık özellikleri ekler. Bu, agent uygulamalarınızı hata ayıklamayı, optimize etmeyi ve ölçeklendirmeyi kolaylaştırır.
  

  
    Evet! Portkey, mevcut CrewAI uygulamalarıyla kusursuz bir şekilde entegre olur. Sadece Portkey'li sürümüyle LLM yapılandırma kodunuzu güncellemeniz gerekir. Kalan agent ve mürettebat kodunuz değişmeden kalır.
  

  
    Portkey, agent'lar, araçlar, insan-dahil iş akışları ve tüm görev süreci türleri (sıralı, hiyerarşik vb.) dahil olmak üzere tüm CrewAI özelliklerini destekler. Kısıtlamadan tüm çerçeve işlevselliğini ekleyerek gözlemlenebilirlik ve güvenilirlik katmanı ekler.
  

  
    Evet, Portkey, mürettebatınızdaki tüm iş akışını izlemek için birden çok agent'ta tutarlı bir `trace_id` kullanmanıza olanak tanır. Bu, özellikle birden çok agent içeren karmaşık mürettebatlarda tam yürütme yolunu anlamak istediğinizde özellikle yararlıdır.
  

  
    Portkey, LLM yapılandırmanıza özel metadata eklemenize olanak tanır, böylece filtreleme için kullanabilirsiniz. Belirli mürettebat çalıştırmalarını bulmayı ve analiz etmeyi kolaylaştırmak için `crew_name`, `crew_type` veya `session_id` gibi alanlar ekleyebilirsiniz.
  

  
    Evet, Portkey kendi LLM sağlayıcılarınıza ait API anahtarlarını güvenli bir şekilde depolayan sanal anahtarlar kullanarak çalışır ve anahtarlarınızı kodunuzu değiştirmeden kolayca döndürmenizi sağlar.
  



## Kaynaklar


  ### CrewAI Belgeleri

    <p>Resmi CrewAI belgeleri</p>
  
  ### Bir Demoyu Ayarlayın

    <p>Bu entegrasyonu uygulama konusunda kişiselleştirilmiş rehberlik alın</p>