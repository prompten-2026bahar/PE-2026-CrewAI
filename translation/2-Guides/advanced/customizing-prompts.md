# Komutları Özelleştirme
 CrewAI için düşük seviyeli komut özelleştirmesinin derinliklerine inin ve farklı modeller ve diller için süper özel ve karmaşık kullanım durumları sağlayın.


## Neden Komutları Özelleştirin?

CrewAI'nin varsayılan komutları birçok senaryo için iyi çalışsa da, düşük seviyeli özelleştirme, çok daha esnek ve güçlü bir ajan davranışına kapı açar. Bu daha derin kontrolü kullanmanın nedenleri şunlardır:

1. **Belirli LLM'ler için optimize edin** - Farklı modeller (örneğin GPT-4, Claude veya Llama) benzersiz mimarilerine göre uyarlanmış komut formatlarıyla daha iyi performans gösterir.
2. **Dili değiştirin** - Yalnızca İngilizce olmayan dillerde çalışan ajanlar oluşturun ve nüansları kesinlikle işleyin.
3. **Karmaşık alanlar için uzmanlaşın** - Sağlık, finans veya hukuk gibi son derece uzmanlaşmış sektörler için komutları uyarlayın.
4. **Ton ve stili ayarlayın** - Ajanları daha resmi, gayri resmi, yaratıcı veya analitik yapın.
5. **Süper özel kullanım durumlarını destekleyin** - Gelişmiş komut yapılarını ve biçimlendirmeyi kullanarak karmaşık, proje özel gereksinimleri karşılayın.

Bu kılavuz, CrewAI'nin komutlarına daha düşük bir seviyede nasıl erişilebileceğini ve ajanların düşünme ve etkileşim şekli üzerinde ince ayar kontrolü sağlayarak size açıklayacaktır.

## CrewAI'nin Komut Sistemini Anlamak

Temelde, CrewAI, kapsamlı bir şekilde özelleştirilebilen modüler bir komut sistemi kullanır:

- **Ajan şablonları** - Her ajanın atanmış rolüne yaklaşımını yönetir.
- **Komut dilimleri** - Görevler, araç kullanımı ve çıktı yapısı gibi uzmanlaşmış davranışları kontrol eder.
- **Hata işleme** - Ajanların hatalara, istisnalara veya zaman aşımına nasıl yanıt vereceğini yönlendirir.
- **Araç-spesifik komutlar** - Araçların nasıl çağrıldığı veya kullanıldığına dair ayrıntılı talimatları tanımlar.

[CrewAI deposundaki orijinal komut şablonlarına](https://github.com/crewAIInc/crewAI/blob/main/src/crewai/translations/en.json) göz atarak bu öğelerin nasıl düzenlendiğini görün. Oradan, gelişmiş davranışları ortaya çıkarmak için bunları gerektiği gibi geçersiz kılabilir veya uyarlayabilirsiniz.

## Varsayılan Sistem Talimatlarını Anlamak

**Üretim Şeffaflığı Sorunu**: CrewAI, siz farkında olmayabileceğiniz komutlarınıza varsayılan talimatları otomatik olarak enjekte eder. Bu bölüm, sahne arkasındaki durumu açıklar ve tam kontrole nasıl ulaşacağınızı gösterir.

`role`, `goal` ve `backstory` ile bir ajan tanımladığınızda, CrewAI, biçimlendirmeyi ve davranışı kontrol eden ek sistem talimatları otomatik olarak ekler. Üretim sistemlerinde tam komut şeffaflığı gerektirdiğinizde, bu varsayılan enjeksiyonları anlamak çok önemlidir.

### CrewAI Otomatik Olarak Enjekte Ettikleri

Ajan yapılandırmanıza göre CrewAI farklı varsayılan talimatlar ekler:

#### Araçsız Ajanlar İçin
```text
"Bu formatları KULLANMALISIN, bu işime bağlı!"
```

#### Araçlı Ajanlar İçin
```text
"ÖNEMLİ: Yanıtınızda aşağıdaki formatı kullanın:

Thought: ne yapılması gerektiği hakkında düşünmelisin
Action: yapılacak eylem, yalnızca [tool_names] isimlerinden bir tanesi
Action Input: eyleme girdisi, basit bir JSON nesnesi..."
```

#### Yapılandırılmış Çıktılar (JSON/Pydantic) İçin
```text
"Son yanıtınızın yalnızca aşağıdaki biçimde içerik içerdiğinden emin olun: {output_format}
Son çıktının ```json veya ```python gibi kod blokları işaretçileri içermediğinden emin olun."
```

### Tam Sistem Komutunu Görüntüleme

LLM'e gönderilen komutu görmek için oluşturulan komutu inceleyebilirsiniz:

```python
from crewai import Agent, Crew, Task
from crewai.utilities.prompts import Prompts

# Ajanınızı oluşturun
agent = Agent(
    role="Veri Analisti",
    goal="Verileri analiz et ve içgörüler sağla",
    backstory="10 yıllık deneyime sahip bir veri analisti uzmanısınız.",
    verbose=True
)

# Örnek bir görev oluşturun
task = Task(
    description="Satış verilerini analiz et ve eğilimleri belirle",
    expected_output="Temel içgörüler ve eğilimlerle ayrıntılı bir analiz",
    agent=agent
)

# Komut oluşturucu oluşturun
prompt_generator = Prompts(
    agent=agent,
    has_tools=len(agent.tools) > 0,
    use_system_prompt=agent.use_system_prompt
)

# Oluşturulan komutu oluşturun ve inceleyin
generated_prompt = prompt_generator.task_execution()

# LLM'ye gönderilecek tam sistem komutunu yazdırın
if "system" in generated_prompt:
    print("=== SİSTEM KOMUTU ===")
    print(generated_prompt["system"])
    print("\n=== KULLANICI KOMUTU ===")
    print(generated_prompt["user"])
else:
    print("=== TAM KOMUT ===")
    print(generated_prompt["prompt"])

# Görev açıklığının nasıl biçimlendirildiğini de görebilirsiniz
print("\n=== GÖREV BAĞLAMI ===")
print(f"Görev Açıklaması: {task.description}")
print(f"Beklenen Çıktı: {task.expected_output}")
```

### Varsayılan Talimatları Geçersiz Kılma

Tam kontrolü elde etmek için birkaç seçeneğiniz var:

#### Seçenek 1: Özel Şablonlar (Önerilen)
```python
from crewai import Agent

# Varsayılan talimatlar olmadan kendi sistem şablonunuzu tanımlayın
custom_system_template = """{role} rolündesiniz. {backstory}
Amacınız şudur: {goal}

Doğal ve konuşma tarzında yanıt verin. Yardımcı, doğru bilgi sağlamaya odaklanın."""

custom_prompt_template = """Görev: {input}

Lütfen bu görevi düşünerek tamamlayın."""

agent = Agent(
    role="Araştırma Asistanı",
    goal="Kullanıcıların doğru bilgi bulmasına yardımcı olun",
    backstory="Yardımcı bir araştırma asistanısınız.",
    system_template=custom_system_template,
    prompt_template=custom_prompt_template,
    use_system_prompt=True  # Ayrı sistem/kullanıcı mesajlarını kullanın
)
```

#### Seçenek 2: Özel Komut Dosyası
Belirli komut dilimlerini geçersiz kılmak için `custom_prompts.json` adlı bir dosya oluşturun:

```json
{
  "slices": {
    "no_tools": "\nEn iyi cevabınızı doğal, konuşma tarzında verin.",
    "tools": "\nBu araçlara erişiminiz var: {tools}\n\nYardımlı olduğunda bunları kullanın, ancak doğal olarak yanıt verin.",
    "formatted_task_instructions": "Yanıtınızı şu biçimde biçimlendirin: {output_format}"
  }
}
```

Ardından onu mürettebatınızda kullanın:

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    prompt_file="custom_prompts.json",
    verbose=True
)
```

#### Seçenek 3: o1 Modelleri İçin Sistem Komutlarını Devre Dışı Bırakma
```python
agent = Agent(
    role="Analist",
    goal="Verileri analiz et",
    backstory="Uzman analist",
    use_system_prompt=False  # Sistem istemini devre dışı bırakır
)
```

### Gözlemlenebilirlik Araçlarıyla Hata Ayıklama

Üretim şeffaflığı için, tüm komutları ve LLM etkileşimlerini izlemek için gözlemlenebilirlik platformlarıyla entegre olun. Bu, LLM'lerinize gönderilen komutları (varsayılan talimatlar dahil) tam olarak görmenizi sağlar.

Ayrıntılı entegrasyon kılavuzları için [Gözlemlenebilirlik belgelerimizi](/en/observability/overview) inceleyin, Langfuse, MLflow, Weights & Biases ve özel kayıt çözümleri gibi çeşitli platformları içerir.

### Üretim İçin En İyi Uygulamalar

1. **Üretim ortamına dağıtmadan önce oluşturulan komutları her zaman inceleyin**
2. **Komut içeriği üzerinde tam kontrole ihtiyacınız olduğunda özel şablonlar kullanın**
3. **Devam eden komut izleme için gözlemlenebilirlik araçlarını entegre edin** (bkz. [Gözlemlenebilirlik dokümanları](/en/observability/overview))
4. **Varsayılan talimatların farklı modeller arasında farklı şekilde çalışabileceği için farklı LLM'lerle test edin**
5. **Ekip şeffaflığı için komut özelleştirmelerinizi belgeleyin**

Varsayılan talimatlar, tutarlı ajan davranışı sağlamak için mevcuttur, ancak etki alanına özgü gereksinimlerle çakışabilir. Ajan davranışınız üzerinde tam kontrolü korumak için yukarıdaki özelleştirme seçeneklerini kullanın.

## Komut Dosyalarını Yönetmek İçin En İyi Uygulamalar

Düşük seviyeli komut özelleştirmesine dahil olurken, bunları düzenli ve bakımı kolay tutmak için aşağıdaki yönergelere uyun:

1. **Dosyaları ayrı tutun** - Özel komutlarınızı ana kod tabanınızın dışında ayrı JSON dosyalarında saklayın.
2. **Sürüm kontrolü** - Zaman içinde komut ayarlamalarının net bir dokümantasyonunu sağlayarak deponuzda değişiklikleri izleyin.
3. **Model veya dile göre düzenleyin** - `prompts_llama.json` veya `prompts_es.json` gibi adlandırma şemalarını kullanarak özel yapılandırmaları hızla tanımlayın.
4. **Değişiklikleri belgeleyin** - Amacını ve özelleştirmelerinizin kapsamını ayrıntılı olarak açıklayan yorumlar veya bir README bulundurun.
5. **Düzeltmeleri en aza indirin** - Sadece gerçekten ayarlamanız gereken belirli dilimleri geçersiz kılın ve geri kalan her şey için varsayılan işlevselliği sağlam tutun.

## Komutları Özelleştirmenin En Basit Yolu

Düz ve kolay bir yaklaşım, özelleştirmek istediğiniz komutlar için bir JSON dosyası oluşturmak ve ardından mürettebatınızın bu dosyaya işaret etmesini sağlamaktır:

1. Güncellemek istediğiniz komutlarla bir JSON dosyası oluşturun.
2. Bu dosyaya `prompt_file` parametresi aracılığıyla referans verin.

CrewAI daha sonra özel alanlarınızı varsayılanlarla birleştirir, böylece her komutu yeniden tanımlamanız gerekmez. İşte nasıl:

### Örnek: Temel Komut Özelleştirmesi

```json
{
  "slices": {
    "format": "Yanıt verirken şu yapıyı izleyin:\n\nTHOUGHTS: Adım adım düşünceniz\nACTION: Kullandığınız araç\nRESULT: Son cevabınız veya sonucunuz"
  }
}
```

Sonra şöyle entegre edin:

```python
from crewai import Agent, Crew, Task, Process

# Ajanları ve görevleri normal şekilde oluşturun
researcher = Agent(
    role="Araştırma Uzmanı",
    goal="Kuantum bilişim hakkında bilgi bulun",
    backstory="Kuantum fiziği uzmanısınız",
    verbose=True
)

research_task = Task(
    description="Kuantum bilişim uygulamalarını araştırın",
    expected_output="Pratik uygulamaların bir özeti",
    agent=researcher
)

# Özel komut dosyanızla bir mürettebat oluşturun
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    prompt_file="path/to/custom_prompts.json",
    verbose=True
)

# Mürettebatı çalıştırın
result = crew.kickoff()
```

Bu birkaç düzenleme ile ajanlarınızın nasıl iletişim kurduğunu ve görevleri nasıl çözdüğünü kontrol etmek için düşük seviyeli bir kontrol elde edersiniz.

## Belirli Modeller İçin Optimizasyon

Farklı modeller, farklı yapılandırılmış komutlar üzerinde daha iyi performans gösterir. Daha derin ayarlamalar yapmak, komutlarınızı bir modelin nüanslarıyla uyumlu hale getirerek performansı önemli ölçüde artırabilir.

### Örnek: Llama 3.3 Komut Şablonu

Örneğin, Meta'nın Llama 3.3'ü ile uğraşırken, daha derin seviyeli özelleştirmeler, https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/#prompt-template adresinde tanımlanan önerilen yapıya yansıtılabilir:

İşte nasıl ince ayar yapabileceğinizi vurgulamak için bir örnek:

```python
from crewai import Agent, Crew, Task, Process
from crewai_tools import DirectoryReadTool, FileReadTool

# Sistem, kullanıcı (komut) ve asistan (yanıt) mesajları için şablonları tanımlayın
system_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>{{ .System }}<|eot_id|>"""
prompt_template = """<|start_header_id|>user<|end_header_id|>{{ .Prompt }}<|eot_id|>"""
response_template = """<|start_header_id|>assistant<|end_header_id|>{{ .Response }}<|eot_id|>"""

# Llama-spesifik düzenleri kullanan bir Ajan oluşturun
principal_engineer = Agent(
    role="Baş Mühendis",
    goal="AI mimarisi üzerinde gözetim ve yüksek seviyeli kararlar alın",
    backstory="Kritik AI sistemlerinden sorumlu baş mühendissiniz",
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",  # Llama 3 modelini kullanma
    system_template=system_template,
    prompt_template=prompt_template,
    response_template=response_template,
    tools=[DirectoryReadTool(), FileReadTool()]
)

# Örnek bir görev tanımlayın
engineering_task = Task(
    description="Potansiyel iyileştirmeler için AI uygulama dosyalarını inceleyin",
    expected_output="Temel bulguların ve önerilerin bir özeti",
    agent=principal_engineer
)

# Görev için bir mürettebat oluşturun
llama_crew = Crew(
    agents=[principal_engineer],
    tasks=[engineering_task],
    process=Process.sequential,
    verbose=True
)

# Mürettebatı çalıştırın
result = llama_crew.kickoff()
print(result.raw)
```

Bu daha derin yapılandırmayla, ayrı bir JSON dosyasına ihtiyaç duymadan Llama tabanlı iş akışlarınızı kapsamlı ve düşük seviyeli olarak kontrol edebilirsiniz.

## Sonuç

CrewAI'de düşük seviyeli komut özelleştirmesi, süper özel, karmaşık kullanım durumları için kapıları açar. İyi organize edilmiş komut dosyaları (veya doğrudan yerleşik şablonlar) oluşturarak, çeşitli modelleri, dilleri ve uzmanlaşmış alanları barındırabilirsiniz. Bu düzeyde esneklik, ihtiyaç duyduğunuz AI davranışını şekillendirirken CrewAI'nin hala güvenilir varsayılanlar sağladığından emin olmanızı sağlar.

Şimdi CrewAI'da gelişmiş komut özelleştirmesi için temeli aldınız. Alan verilerine özgü kısıtlamalar veya model özel yapıları olup olmadığına bakılmaksızın, bu düşük seviyeli yaklaşım, ajan etkileşimlerini son derece uzmanlaşmış şekillerde şekillendirmenizi sağlar.