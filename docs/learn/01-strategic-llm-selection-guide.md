> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Stratejik LLM Seçim Kılavuzu

> CrewAI yapay zeka ajanlarınız için doğru LLM'yi seçmeye ve etkili görev ile ajan tanımları yazmaya yönelik stratejik çerçeve

## CrewAI'nin LLM Seçimine Yaklaşımı

Belirli model önerileri sunmak yerine, spesifik kullanım durumunuza, kısıtlamalarınıza ve gereksinimlerinize göre bilinçli kararlar almanıza yardımcı olan bir **düşünce çerçevesi** savunuyoruz. LLM ortamı hızla gelişmekte; düzenli aralıklarla yeni modeller çıkmakta ve mevcut olanlar sık sık güncellenmektedir. Önemli olan, hangi modellerin mevcut olduğundan bağımsız olarak geçerliliğini koruyan sistematik bir değerlendirme yaklaşımı geliştirmektir.

> **Not:** Bu kılavuz, LLM ortamı hızla değiştiğinden belirli model önerilerinden ziyade stratejik düşünceye odaklanmaktadır.

## Hızlı Karar Çerçevesi

1. **Görevlerinizi Analiz Edin** — Görevlerinizin gerçekte ne gerektirdiğini derinlemesine anlayarak başlayın. İçerdiği bilişsel karmaşıklığı, gereken akıl yürütme derinliğini, beklenen çıktıların biçimini ve modelin işlemesi gereken bağlam miktarını göz önünde bulundurun. Bu temel analiz, sonraki tüm kararlarınıza yol gösterecektir.

2. **Model Yeteneklerini Eşleştirin** — Gereksinimlerinizi anladıktan sonra bunları model güçlü yönleriyle eşleştirin. Farklı model aileleri farklı iş türlerinde üstündür; bazıları akıl yürütme ve analiz için, diğerleri yaratıcılık ve içerik üretimi için, bir kısmı ise hız ve verimlilik için optimize edilmiştir.

3. **Kısıtlamaları Göz Önünde Bulundurun** — Bütçe sınırlamaları, gecikme gereksinimleri, veri gizliliği ihtiyaçları ve altyapı kapasitesi gibi gerçek dünya operasyonel kısıtlamalarınızı hesaba katın. Teorik olarak en iyi model, durumunuz için pratikte en iyi seçenek olmayabilir.

4. **Test Edin ve Yineleyin** — Güvenilir, iyi anlaşılmış modellerle başlayın ve spesifik kullanım durumunuzdaki gerçek performansa göre optimize edin. Gerçek dünya sonuçları çoğunlukla teorik kıyaslamalardan farklı olduğundan ampirik test kritik öneme sahiptir.

## Temel Seçim Çerçevesi

### a. Önce Görev Odaklı Düşünme

LLM seçiminde en kritik adım, görevinizin gerçekte ne talep ettiğini anlamaktır. Ekipler çoğu zaman belirli gereksinimlerini dikkatle analiz etmeden genel itibar veya kıyaslama puanlarına göre model seçer. Bu yaklaşım, basit görevlerin pahalı ve karmaşık modellerle aşırı mühendislikle ele alınmasına ya da gerekli yeteneklerden yoksun modellerle sofistike çalışmaların yetersiz kalmasına yol açar.

#### Akıl Yürütme Karmaşıklığı

- **Basit Görevler**: Günlük yapay zeka işlerinin büyük çoğunluğunu oluşturur; temel talimat takibi, doğrudan veri işleme ve basit biçimlendirme işlemlerini kapsar. Bu görevler genellikle belirsizliğin az olduğu net girdi ve çıktılara sahiptir. Bilişsel yük düşüktür; model esas olarak karmaşık akıl yürütmeye girmek yerine açık talimatları takip etmek durumundadır.

- **Karmaşık Görevler**: Çok adımlı akıl yürütme, stratejik düşünme ve belirsiz ya da eksik bilgiyle başa çıkma yeteneği gerektirir. Birden fazla veri kaynağını analiz etmeyi, kapsamlı stratejiler geliştirmeyi veya daha küçük bileşenlere ayrılması gereken problemleri çözmeyi içerebilir. Modelin birden fazla akıl yürütme adımı boyunca bağlamı koruması ve çoğu zaman açıkça belirtilmemiş çıkarımlar yapması gerekir.

- **Yaratıcı Görevler**: Yeni, ilgi çekici ve bağlamsal açıdan uygun içerik üretmeye odaklanan farklı bir bilişsel kapasite gerektirir. Hikaye anlatımı, pazarlama metni oluşturma ve yaratıcı problem çözmeyi kapsar. Modelin, formüle edilmiş yerine özgün ve ilgi çekici hissettiren içerik üretirken nüansı, tonu ve hedef kitleyi anlaması gerekir.

#### Çıktı Gereksinimleri

- **Yapılandırılmış Veri**: Biçim uyumunda hassasiyet ve tutarlılık gerektirir. JSON, XML veya veritabanı biçimleriyle çalışırken model programatik olarak işlenebilecek sözdizimsel açıdan doğru çıktı üretmelidir. Bu görevler çoğunlukla katı doğrulama gereksinimlerine ve biçim hatalarına karşı düşük toleransa sahiptir; bu da yaratıcılıktan daha önemli güvenilirlik sağlar.

- **Yaratıcı İçerik**: Teknik yetkinlik ile yaratıcı özgünlük arasında denge gerektirir. Modelin, okuyucuları ilgilendiren ve belirli iletişim hedeflerine ulaşan içerik üretirken hedef kitleyi, tonu ve marka sesini anlaması gerekir.

- **Teknik İçerik**: Yapılandırılmış veri ile yaratıcı içerik arasında yer alır; hem hassasiyet hem de netlik gerektirir. Dokümantasyon, kod üretimi ve teknik analiz, hedef kitleye erişilebilir kalırken doğru ve kapsamlı olmak zorundadır.

#### Bağlam İhtiyaçları

- **Kısa Bağlam**: Modelin sınırlı bilgiyi hızla işlemesi gereken odaklı, anlık görevleri içerir. Bunlar çoğunlukla hız ve verimliliğin derin anlayıştan daha önemli olduğu işlemsel etkileşimlerdir.

- **Uzun Bağlam**: Kapsamlı belgeler, uzatılmış konuşmalar veya karmaşık çok parçalı görevlerle çalışırken ortaya çıkar. Model, önceki bilgilere doğru şekilde başvururken binlerce token boyunca tutarlılığı korumalıdır.

- **Çok Uzun Bağlam**: Mevcut olanın sınırlarını zorlayan senaryoları kapsar; devasa belge işleme, kapsamlı araştırma sentezi veya karmaşık çok oturumlu etkileşimleri içerir.

### b. Model Yetenek Eşleştirmesi

Model yeteneklerini anlamak, pazarlama iddialarının ve kıyaslama puanlarının ötesine geçerek farklı model mimarilerinin ve eğitim yaklaşımlarının temel güçlü ve zayıf yönlerini kavramayı gerektirir.

#### Akıl Yürütme Modelleri

Akıl yürütme modelleri, karmaşık ve çok adımlı düşünme görevleri için özel olarak tasarlanmış bir kategoriyi temsil eder. Bu modeller, problemlerin dikkatli analiz, stratejik planlama veya sistematik problem ayrıştırması gerektirdiği durumlarda üstündür. Genellikle karmaşık problemleri adım adım çözmek için zincir düşünce veya ağaç düşünce işleme gibi teknikler kullanır.

Akıl yürütme modellerinin gücü, uzatılmış akıl yürütme zincirlerinde mantıksal tutarlılığı koruma ve karmaşık problemleri yönetilebilir bileşenlere ayırma kapasitelerinde yatar. Stratejik planlama, karmaşık analiz ve yanıt hızından daha önemli olan akıl yürütme kalitesi için özellikle değerlidirler.

Ancak akıl yürütme modelleri çoğunlukla hız ve maliyet açısından ödünler gerektirir. Sofistike akıl yürütme yeteneklerinin gerekli olmadığı yaratıcı görevler veya basit işlemler için daha az uygun olabilirler.

#### Genel Amaçlı Modeller

Genel amaçlı modeller, belirli bir alanda aşırı uzmanlaşmadan geniş bir görev yelpazesinde sağlam performans sunarak LLM seçiminde en dengeli yaklaşımı sunar. Bu modeller çeşitli veri kümeleri üzerinde eğitilmiş ve belirli alanlarda zirve performansı yerine çok yönlülük için optimize edilmiştir.

Genel amaçlı modellerin birincil avantajı, farklı çalışma türlerinde güvenilirlik ve öngörülebilirliktir. Araştırma ve analizden içerik oluşturma ve veri işlemeye kadar çoğu standart iş görevini yetkin biçimde hallederler. Bu da onları çeşitli iş akışlarında tutarlı performansa ihtiyaç duyan ekipler için mükemmel seçenekler haline getirir.

#### Hızlı ve Verimli Modeller

Hızlı ve verimli modeller, sofistike akıl yürütme yeteneklerinden önce hız, maliyet etkinliği ve kaynak verimliliğini önceliklendirir. Bu modeller, hızlı yanıtların ve düşük operasyonel maliyetlerin nüanslı anlayış veya karmaşık akıl yürütmeden daha önemli olduğu yüksek verimli senaryolar için optimize edilmiştir.

Bu modeller rutin işlemler, basit veri işleme, fonksiyon çağırma ve bilişsel gereksinimlerin nispeten düz olduğu yüksek hacimli görevlerde üstündür. Birçok isteği hızla işlemesi gereken veya sıkı bütçe kısıtlamaları içinde çalışan uygulamalar için özellikle değerlidirler.

#### Yaratıcı Modeller

Yaratıcı modeller özellikle içerik üretimi, yazma kalitesi ve yaratıcı düşünme görevleri için optimize edilmiştir. Bu modeller genellikle nüansı, tonu ve stili anlarken doğal ve özgün hissettiren, bağlamsal açıdan uygun içerik üretmede üstündür.

Yaratıcı modellerin gücü, yazma stilini farklı kitlelere uyarlama, tutarlı ses ve tonu koruma ve okuyucuları etkili biçimde ilgilendiren içerik üretme kapasitelerinde yatar.

#### Açık Kaynak Modeller

Açık kaynak modeller maliyet kontrolü, özelleştirme potansiyeli, veri gizliliği ve dağıtım esnekliği açısından benzersiz avantajlar sunar. Bu modeller yerel olarak veya özel altyapı üzerinde çalıştırılabilir; bu da veri işleme ve model davranışı üzerinde tam kontrol sağlar.

Açık kaynak modellerin birincil faydaları arasında token başına maliyetin ortadan kalkması, belirli kullanım durumları için ince ayar yapabilme, tam veri gizliliği ve harici API sağlayıcılarından bağımsızlık sayılabilir.

Ancak açık kaynak modeller etkin şekilde dağıtılması ve sürdürülmesi için daha fazla teknik uzmanlık gerektirir. Ekiplerin altyapı maliyetlerini, model yönetim karmaşıklığını ve modelleri güncel ve optimize tutmak için gereken süregelen çabayı göz önünde bulundurması gerekir.

## Stratejik Yapılandırma Kalıpları

### a. Çoklu Model Yaklaşımı

> **İpucu:** Hem performansı hem maliyeti optimize etmek için aynı ekip içinde farklı amaçlar için farklı modeller kullanın.

En sofistike CrewAI uygulamaları çoğunlukla birden fazla modeli stratejik olarak kullanır; farklı ajanlara özel rollerine ve gereksinimlerine göre farklı modeller atar. Bu yaklaşım, her iş türü için en uygun modeli kullanarak hem performans hem de maliyet açısından optimize etmeye imkân tanır.

Planlama ajanları, karmaşık stratejik düşünme ve çok adımlı analizi kaldırabilecek akıl yürütme modellerinden yararlanır. İçerik ajanları yazma kalitesi ve hedef kitle etkileşiminde üstün yaratıcı modellerle en iyi performansı gösterir. Rutin işlemleri yürüten işleme ajanları ise hız ve maliyet etkinliğini önceliklendiren verimli modeller kullanabilir.

**Örnek: Araştırma ve Analiz Ekibi**

```python
from crewai import Agent, Task, Crew, LLM

# Stratejik planlama için yüksek kapasiteli akıl yürütme modeli
manager_llm = LLM(model="gemini-2.5-flash-preview-05-20", temperature=0.1)

# İçerik üretimi için yaratıcı model
content_llm = LLM(model="claude-3-5-sonnet-20241022", temperature=0.7)

# Veri işleme için verimli model
processing_llm = LLM(model="gpt-4o-mini", temperature=0)

research_manager = Agent(
    role="Araştırma Strateji Yöneticisi",
    goal="Kapsamlı araştırma stratejileri geliştir ve ekip çabalarını koordine et",
    backstory="Derin analitik yeteneklere sahip uzman araştırma stratejisti",
    llm=manager_llm,  # Karmaşık akıl yürütme için yüksek kapasiteli model
    verbose=True
)

content_writer = Agent(
    role="Araştırma İçerik Yazarı",
    goal="Araştırma bulgularını etkileyici ve iyi yapılandırılmış raporlara dönüştür",
    backstory="Karmaşık konuları erişilebilir kılmada üstün yetenekli yazar",
    llm=content_llm,  # İlgi çekici içerik için yaratıcı model
    verbose=True
)

data_processor = Agent(
    role="Veri Analiz Uzmanı",
    goal="Araştırma kaynaklarından temel veri noktalarını çıkar ve düzenle",
    backstory="Doğruluk ve verimliliğe odaklanan, detay odaklı analist",
    llm=processing_llm,  # Rutin görevler için hızlı ve maliyet etkin model
    verbose=True
)

crew = Crew(
    agents=[research_manager, content_writer, data_processor],
    tasks=[...],  # Spesifik görevleriniz
    manager_llm=manager_llm,  # Yönetici akıl yürütme modelini kullanır
    verbose=True
)
```

Başarılı çoklu model uygulamasının anahtarı, farklı ajanların nasıl etkileşime girdiğini anlamak ve model yeteneklerinin ajan sorumluluklarıyla örtüşmesini sağlamaktır.

### b. Bileşene Özgü Seçim

#### Yönetici LLM

Yönetici LLM, hiyerarşik CrewAI süreçlerinde kritik bir rol oynar; birden fazla ajan ve görev için koordinasyon noktası olarak hizmet eder. Bu modelin delegasyon, görev önceliklendirme ve birden fazla eş zamanlı operasyon boyunca bağlamı koruma konularında üstün olması gerekir.

Etkili yönetici LLM'ler iyi delegasyon kararları vermek için güçlü akıl yürütme, öngörülebilir koordinasyonu sağlamak için tutarlı performans ve birden fazla ajanın durumunu takip etmek için mükemmel bağlam yönetimi gerektirir.

#### Fonksiyon Çağırma LLM

Fonksiyon çağırma LLM'leri tüm ajanlarda araç kullanımını yönetir; bu da onları harici araçlara ve API'lere yoğun şekilde dayanan ekipler için kritik kılar. Bu modellerin araç yeteneklerini anlamada, parametreleri doğru şekilde çıkarmada ve araç yanıtlarını etkin biçimde işlemede üstün olması gerekir.

Fonksiyon çağırma LLM'leri için en önemli özellikler yaratıcılık veya sofistike akıl yürütmeden çok hassasiyet ve güvenilirliktir.

#### Ajana Özgü Geçersiz Kılmalar

Bireysel ajanlar, belirli ihtiyaçları ekip düzeyindeki genel gereksinimlerden önemli ölçüde farklılaştığında ekip düzeyi LLM ayarlarını geçersiz kılabilir. Bu yetenek, çoğu ajan için operasyonel basitliği korurken ince ayarlı optimizasyona imkân tanır.

## Görev Tanımı Çerçevesi

### a. Karmaşıklık Yerine Netliğe Odaklanın

Etkili görev tanımı, CrewAI çıktılarının kalitesini belirlemede çoğunlukla model seçiminden daha önemlidir. İyi tanımlanmış görevler, orta düzeydeki modellerin bile iyi performans göstermesini sağlayan net yön ve bağlam sunar; kötü tanımlanmış görevler ise sofistike modellerin bile tatmin edici olmayan sonuçlar üretmesine neden olabilir.

#### Etkili Görev Açıklamaları

En iyi görev açıklamaları yeterli ayrıntı sağlamak ile netliği korumak arasında denge kurar. Başarının nasıl göründüğü konusunda hiçbir belirsizlik kalmayacak şekilde spesifik hedefi açıkça tanımlamalı; ajanın nasıl ilerleyeceğini anlaması için yeterli ayrıntıda yaklaşım veya metodoloji açıklamalıdır.

Etkili görev açıklamaları, ajanın daha geniş amacı ve çalışması gereken sınırlamaları anlamasına yardımcı olan ilgili bağlam ve kısıtlamaları içerir. Sistematik olarak yaklaşılması zor olan bunaltıcı çok yönlü hedefler sunmak yerine sistematik biçimde yürütülebilecek odaklı adımlara böler.

#### Beklenen Çıktı Yönergeleri

Beklenen çıktı yönergeleri, görev tanımı ile ajan arasında bir sözleşme işlevi görür; teslim edilebilirin nasıl görünmesi gerektiğini ve nasıl değerlendirileceğini açıkça belirtir. Bu yönergeler hem ihtiyaç duyulan biçim ve yapıyı hem de çıktının eksiksiz sayılması için içerilmesi gereken temel unsurları tanımlamalıdır.

### b. Görev Sıralama Stratejisi

#### Sıralı Bağımlılıklar

Sıralı görev bağımlılıkları, görevlerin önceki çıktılar üzerine inşa edildiği, bilginin bir görevden diğerine aktığı veya kalitenin önkoşul çalışmasının tamamlanmasına bağlı olduğu durumlarda gereklidir. Bu yaklaşım, her görevin başarılı olmak için ihtiyaç duyduğu bilgiye ve bağlama erişmesini sağlar.

#### Paralel Yürütme

Paralel yürütme, görevler birbirinden bağımsız olduğunda, zaman verimliliği önemli olduğunda veya koordinasyon gerektirmeyen farklı uzmanlık alanları söz konusu olduğunda değerli hale gelir. Bu yaklaşım, uzman ajanların aynı anda güçlü oldukları alanlarda çalışmasına izin verirken genel yürütme süresini önemli ölçüde azaltabilir.

## LLM Performansı İçin Ajan Yapılandırmasını Optimize Etme

### a. Role Dayalı LLM Seçimi

> **Uyarı:** Genel ajan rolleri doğru LLM'yi seçmeyi imkânsız kılar. Spesifik roller, hedeflenmiş model optimizasyonunu mümkün kılar.

Ajan rollerinizin özgüllüğü, optimal performans için en önemli LLM yeteneklerini doğrudan belirler. Bu durum, model güçlü yönlerini ajan sorumluluklarıyla eşleştirmek için stratejik bir fırsat yaratır.

```python
# ✅ Spesifik rol - net LLM gereksinimleri
specific_agent = Agent(
    role="SaaS Gelir Operasyonları Analisti",  # Net alan uzmanlığı gerekli
    goal="Tekrarlayan gelir metriklerini analiz et ve büyüme fırsatlarını tespit et",
    backstory="ARR, kayıp ve genişleme geliri konusunda derin anlayışa sahip SaaS iş modeli uzmanı",
    llm=LLM(model="gpt-4o")  # Karmaşık analiz için akıl yürütme modeli haklı
)
```

**Role-Model Eşleştirme Stratejisi:**

- **"Araştırma Analisti"** → Karmaşık analiz için akıl yürütme modeli (GPT-4o, Claude Sonnet)
- **"İçerik Editörü"** → Yazma kalitesi için yaratıcı model (Claude, GPT-4o)
- **"Veri İşleyici"** → Yapılandırılmış görevler için verimli model (GPT-4o-mini, Gemini Flash)
- **"API Koordinatörü"** → Araç kullanımı için fonksiyon çağırmaya optimize edilmiş model (GPT-4o, Claude)

### b. Geçmiş Hikaye (Backstory) Model Bağlamı Güçlendiricisi Olarak

> **Bilgi:** Stratejik geçmiş hikayeler, genel istemin ulaşamadığı alana özgü bağlam sağlayarak seçtiğiniz LLM'nin etkinliğini katlar.

İyi hazırlanmış bir geçmiş hikaye, LLM seçiminizi genel kapasiteden uzmanlaşmış uzmanlığa dönüştürür. Bu özellikle maliyet optimizasyonu için kritiktir: iyi bağlamlandırılmış verimli bir model, uygun bağlam olmaksızın premium bir modelden daha iyi performans gösterebilir.

```python
# Bağlam model etkinliğini artırır
domain_expert = Agent(
    role="B2B SaaS Pazarlama Stratejisti",
    goal="Kurumsal yazılım için kapsamlı pazara giriş stratejileri geliştir",
    backstory="""
    B2B SaaS şirketlerini Seri A'dan halka arzına kadar ölçeklendirmede 10+ yıl deneyiminiz var.
    Kurumsal satış döngülerinin nüanslarını, farklı dikeylerde ürün-pazar uyumunun önemini
    ve büyüme metriklerini birim ekonomisiyle nasıl dengeleyeceğinizi anlıyorsunuz.
    Salesforce, HubSpot ve gelişmekte olan tek boynuzlu atlarla çalıştınız; bu da size
    hem köklü hem de bozucu pazara giriş stratejilerine dair perspektif kazandırdı.
    """,
    llm=LLM(model="claude-3-5-sonnet", temperature=0.3)  # Alan bilgisiyle dengeli yaratıcılık
)

# Bu bağlam Claude'un bir alan uzmanı gibi performans göstermesini sağlar
# Bağlam olmadan, genel pazarlama tavsiyeleri üretecektir
```

**LLM Performansını Artıran Geçmiş Hikaye Unsurları:**

- **Alan Deneyimi**: "Kurumsal SaaS satışında 10+ yıl"
- **Spesifik Uzmanlık**: "Seri B+ turları için teknik durum tespitinde uzmanlaşmış"
- **Çalışma Tarzı**: "Açık dokümantasyonla veri odaklı kararları tercih eder"
- **Kalite Standartları**: "Kaynakları alıntılamak ve analitik çalışmayı göstermek konusunda ısrarcıdır"

### c. Bütünsel Ajan-LLM Optimizasyonu

En etkili ajan yapılandırmaları, rol özgüllüğü, geçmiş hikaye derinliği ve LLM seçimi arasında sinerji yaratır. Her unsur diğerlerini güçlendirerek model performansını maksimize eder.

```python
# Örnek: Teknik Dokümantasyon Ajanı
tech_writer = Agent(
    role="API Dokümantasyon Uzmanı",  # Net LLM gereksinimleri için spesifik rol
    goal="Kapsamlı, geliştirici dostu API dokümantasyonu oluştur",
    backstory="""
    REST API'ları, GraphQL uç noktalarını ve SDK entegrasyon kılavuzlarını belgeleyen
    8+ yıllık teknik yazarlık deneyimine sahipsiniz. Geliştirici araçları şirketleriyle
    çalıştınız ve geliştiricilerin ne ihtiyaç duyduğunu anlıyorsunuz: net örnekler,
    kapsamlı hata yönetimi ve pratik kullanım durumları. Pazarlama jargonundan çok
    doğruluğa ve kullanılabilirliğe öncelik veriyorsunuz.
    """,
    llm=LLM(
        model="claude-3-5-sonnet",  # Teknik yazım için mükemmel
        temperature=0.1  # Doğruluk için düşük sıcaklık
    ),
    tools=[code_analyzer_tool, api_scanner_tool],
    verbose=True
)
```

**Uyum Kontrol Listesi:**

- ✅ **Rol Özgüllüğü**: Net alan ve sorumluluklar
- ✅ **LLM Eşleşmesi**: Model güçlü yönleri rol gereksinimleriyle örtüşüyor
- ✅ **Geçmiş Hikaye Derinliği**: LLM'nin yararlanabileceği alan bağlamı sağlıyor
- ✅ **Araç Entegrasyonu**: Araçlar ajanın uzmanlaşmış işlevini destekliyor
- ✅ **Parametre Ayarı**: Sıcaklık ve ayarlar rol ihtiyaçları için optimize edilmiş

## Pratik Uygulama Kontrol Listesi

### 1. Mevcut Yapınızı Denetleyin

**İncelenecekler:**

- Tüm ajanlar varsayılan olarak aynı LLM'yi mi kullanıyor?
- En karmaşık akıl yürütme görevlerini hangi ajanlar yürütüyor?
- Hangi ajanlar öncelikle veri işleme veya biçimlendirme yapıyor?
- Herhangi bir ajan yoğun şekilde araç bağımlı mı?

**Eylem**: Mevcut ajan rollerini belgelendirin ve optimizasyon fırsatlarını tespit edin.

### 2. Ekip Düzeyi Strateji Uygulayın

**Temel Düzeyinizi Belirleyin:**

```python
# Ekip için güvenilir bir varsayılanla başlayın
default_crew_llm = LLM(model="gpt-4o-mini")  # Maliyet etkin temel

crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True
)
```

**Eylem**: Bireysel ajanları optimize etmeden önce ekibinizin varsayılan LLM'sini belirleyin.

### 3. Yüksek Etkili Ajanları Optimize Edin

**Temel Ajanları Tespit Edin ve Yükseltin:**

```python
# Yönetici veya koordinasyon ajanları
manager_agent = Agent(
    role="Proje Yöneticisi",
    llm=LLM(model="gemini-2.5-flash-preview-05-20"),  # Koordinasyon için premium
    # ... geri kalan yapılandırma
)

# Yaratıcı veya müşteriyle yüz yüze ajanlar
content_agent = Agent(
    role="İçerik Oluşturucu",
    llm=LLM(model="claude-3-5-sonnet"),  # Yazım için en iyi
    # ... geri kalan yapılandırma
)
```

**Eylem**: Karmaşıklığın %80'ini yürüten %20'lik ajanlarınızı yükseltin.

### 4. Kurumsal Testlerle Doğrulayın

**Ajanlarınızı üretime aldıktan sonra:**

- Model seçimlerinizi A/B test etmek için [CrewAI AMP platformunu](https://app.crewai.com) kullanın
- Tutarlılığı ve performansı ölçmek için gerçek girdilerle birden fazla yineleme çalıştırın
- Optimize edilmiş yapınızda maliyet ve performansı karşılaştırın
- İşbirlikçi karar alma için sonuçları ekibinizle paylaşın

**Eylem**: Test platformunu kullanarak tahminleri veri odaklı doğrulamayla değiştirin.

## Farklı Model Türlerinin Ne Zaman Kullanılacağı

### Akıl Yürütme Modelleri

Akıl yürütme modelleri, görevlerin sistematik analizden yararlanan gerçek çok adımlı mantıksal düşünme, stratejik planlama veya üst düzey karar verme gerektirdiğinde vazgeçilmez hale gelir.

İş stratejisi geliştirme, birden fazla kaynaktan içgörü çıkarmayı gerektiren karmaşık veri analizi, her adımın önceki analize bağlı olduğu çok adımlı problem çözme ve birden fazla değişkeni ve bunların etkileşimlerini göz önünde bulundurmayı gerektiren stratejik planlama görevleri için akıl yürütme modellerini değerlendirin.

### Yaratıcı Modeller

Yaratıcı modeller, içerik üretiminin birincil çıktı olduğu ve o içeriğin kalitesinin, stilinin ve etkileşim düzeyinin başarıyı doğrudan etkilediği durumlarda değerli hale gelir.

Blog yazısı ve makale oluşturma, ikna etmesi ve bağ kurması gereken pazarlama metni, yaratıcı hikaye anlatımı ve anlatı geliştirme, ses ve tonun kritik olduğu marka iletişimleri için yaratıcı modeller kullanın.

### Verimli Modeller

Verimli modeller, hız ve maliyet optimizasyonunun öncelikler olduğu yüksek frekanslı, rutin operasyonlar için idealdir.

Veri işleme ve dönüştürme görevleri, basit biçimlendirme ve düzenleme işlemleri, sofistikasyondan çok hassasiyetin önemli olduğu fonksiyon çağırma ve araç kullanımı, işlem başına maliyetin önemli bir faktör olduğu yüksek hacimli operasyonlar için verimli modelleri değerlendirin.

### Açık Kaynak Modeller

Açık kaynak modeller, bütçe kısıtlamaları önemli olduğunda, veri gizliliği gereksinimleri bulunduğunda, özelleştirme ihtiyaçları kritik olduğunda veya operasyonel ya da uyumluluk nedeniyle yerel dağıtım gerektiğinde cazip hale gelir.

Veri gizliliğinin en önemli olduğu dahili şirket araçları, harici API kullanamayan gizlilik açısından hassas uygulamalar, token başına fiyatlandırmanın yasak düzeyde pahalı olduğu maliyet optimize dağıtımlar için açık kaynak modelleri değerlendirin.

## Yaygın CrewAI Model Seçimi Tuzakları

### "Tek Model Her Şeye Uyar" Tuzağı

**Sorun**: Aynı LLM'yi, spesifik rollerinden ve sorumluluklarından bağımsız olarak bir ekipteki tüm ajanlar için kullanmak.

**Gerçek Örnek**: Hem stratejik planlama yöneticisi hem de veri çıkarma ajanı için GPT-4o kullanmak. Yönetici premium maliyeti haklı kılan akıl yürütme kapasitelerine ihtiyaç duyar; ancak veri çıkarıcı GPT-4o-mini ile çok daha düşük maliyetle aynı performansı gösterebilir.

**CrewAI Çözümü**: Model yeteneklerini ajan rolleriyle eşleştirmek için ajana özgü LLM yapılandırmasını kullanın:

```python
# Stratejik ajan premium model alır
manager = Agent(role="Strateji Yöneticisi", llm=LLM(model="gpt-4o"))

# İşleme ajanı verimli model alır
processor = Agent(role="Veri İşleyici", llm=LLM(model="gpt-4o-mini"))
```

### Ekip Düzeyi ve Ajan Düzeyi LLM Hiyerarşisini Göz Ardı Etme

**Sorun**: CrewAI'nin LLM hiyerarşisinin nasıl çalıştığını anlamamak — ekip LLM, yönetici LLM ve ajan LLM ayarları çelişebilir veya kötü koordine edilebilir.

**Gerçek Örnek**: Bir ekibi Claude kullanacak şekilde ayarlamak, ancak ajanların GPT modelleriyle yapılandırılmış olması; tutarsız davranış ve gereksiz model geçiş yüküne neden olmak.

**CrewAI Çözümü**: LLM hiyerarşinizi stratejik olarak planlayın:

```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    manager_llm=LLM(model="gpt-4o"),  # Ekip koordinasyonu için
    process=Process.hierarchical  # manager_llm kullanıldığında
)

# Ajanlar, özellikle geçersiz kılınmadıkça ekip LLM'sini devralır
agent1 = Agent(llm=LLM(model="claude-3-5-sonnet"))  # Spesifik ihtiyaçlar için geçersiz kıl
```

### Fonksiyon Çağırma Modeli Uyumsuzluğu

**Sorun**: Araç yoğun CrewAI iş akışları için fonksiyon çağırma performansını göz ardı ederek genel yeteneklere göre model seçmek.

**Gerçek Örnek**: Öncelikle API çağırması, araç araması veya yapılandırılmış veri işlemesi gereken bir ajan için yaratıcılık odaklı bir model seçmek.

**CrewAI Çözümü**: Araç yoğun ajanlar için fonksiyon çağırma yeteneklerini önceliklendirin:

```python
# Birçok araç kullanan ajanlar için
tool_agent = Agent(
    role="API Entegrasyon Uzmanı",
    tools=[search_tool, api_tool, data_tool],
    llm=LLM(model="gpt-4o"),  # Mükemmel fonksiyon çağırma
    # VEYA
    # llm=LLM(model="claude-3-5-sonnet")  # Araçlarla da güçlü
)
```

### Test Etmeden Erken Optimizasyon

**Sorun**: Gerçek CrewAI iş akışları ve görevleriyle doğrulama yapmadan teorik performansa dayalı karmaşık model seçim kararları vermek.

**CrewAI Çözümü**: Basit başlayın, ardından gerçek performans verilerine göre optimize edin:

```python
# Bununla başlayın
crew = Crew(agents=[...], tasks=[...], llm=LLM(model="gpt-4o-mini"))

# Performansı test edin, ardından gerektiğinde spesifik ajanları optimize edin
# İyileştirmeleri doğrulamak için Enterprise platform testini kullanın
```

### Bağlam ve Bellek Sınırlamalarını Göz Ardı Etme

**Sorun**: Model bağlam pencerelerinin, ajanlar arasındaki CrewAI bellek ve bağlam paylaşımıyla nasıl etkileşime girdiğini göz önünde bulunduramamak.

**Gerçek Örnek**: Birden fazla görev yinelemesinde konuşma geçmişini koruması gereken ajanlar için kısa bağlamlı bir model kullanmak.

**CrewAI Çözümü**: Bağlam yeteneklerini ekip iletişim kalıplarıyla eşleştirin.

## Test ve Yineleme Stratejisi

1. **Basit Başlayın** — İyi anlaşılan ve yaygın olarak desteklenen güvenilir, genel amaçlı modellerle başlayın. Bu, uzmanlaşmış ihtiyaçlar için optimize etmeden önce spesifik gereksinimlerinizi ve performans beklentilerinizi anlamak için sağlam bir temel oluşturur.

2. **Önemli Olanı Ölçün** — Yalnızca genel kıyaslamalara güvenmek yerine spesifik kullanım durumunuz ve iş gereksinimlerinizle örtüşen metrikler geliştirin.

3. **Sonuçlara Göre Yineleyin** — Model değişikliklerini teorik değerlendirmeler veya genel önerilerden ziyade spesifik bağlamınızdaki gözlemlenen performansa dayandırın.

4. **Toplam Maliyeti Göz Önünde Bulundurun** — Model maliyetleri, geliştirme süresi, bakım yükü ve operasyonel karmaşıklık dahil olmak üzere toplam sahip olma maliyetini değerlendirin.

> **İpucu:** Önce gereksinimlerinizi anlamaya odaklanın, ardından bu ihtiyaçlarla en iyi örtüşen modelleri seçin. En iyi LLM seçimi, operasyonel kısıtlamalarınız dahilinde ihtiyaç duyduğunuz sonuçları tutarlı biçimde sunan seçimdir.

### Kurumsal Düzeyde Model Doğrulama

LLM seçimlerini optimize etme konusunda ciddi olan ekipler için **CrewAI AMP platformu**, temel CLI testinin çok ötesine geçen sofistike test yetenekleri sunar.

![Enterprise Testing Interface](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/enterprise-testing.png)

**Gelişmiş Test Özellikleri:**

- **Çoklu Model Karşılaştırması**: Aynı görevler ve girdiler üzerinde birden fazla LLM'yi eş zamanlı olarak test edin. Spesifik kullanım durumunuz için en uygun olanı belirlemek amacıyla GPT-4o, Claude, Llama, Groq, Cerebras ve diğer lider modeller arasındaki performansı paralel olarak karşılaştırın.

- **İstatistiksel Titizlik**: Güvenilirliği ve performans varyansını ölçmek için tutarlı girdilerle birden fazla yineleme yapılandırın.

- **Gerçek Dünya Doğrulaması**: Sentetik kıyaslamalar yerine gerçek ekip girdilerinizi ve senaryolarınızı kullanın.

- **Kapsamlı Analitik**: Test edilen tüm modeller genelinde ayrıntılı performans metriklerine, yürütme sürelerine ve maliyet analizine erişin.

- **Ekip İşbirliği**: Test sonuçlarını ve model performans verilerini ekibinizle paylaşarak işbirlikçi karar almayı sağlayın.

Başlamak için [app.crewai.com](https://app.crewai.com) adresine gidin!

> **Bilgi:** Enterprise platform, model seçimini tahminden veri odaklı bir sürece dönüştürerek bu kılavuzdaki ilkeleri gerçek kullanım durumlarınız ve gereksinimlerinizle doğrulamanızı sağlar.

## Temel İlkeler Özeti

- **Göreve Dayalı Seçim**: Teorik yeteneklere veya genel itibara değil, görevin gerçekte ne gerektirdiğine göre model seçin.
- **Yetenek Eşleştirme**: Optimal performans için model güçlü yönlerini ajan rolleri ve sorumluluklarıyla hizalayın.
- **Stratejik Tutarlılık**: İlgili bileşenler ve iş akışları genelinde tutarlı model seçim stratejisini koruyun.
- **Pratik Test**: Seçimleri yalnızca kıyaslamalar yerine gerçek dünya kullanımıyla doğrulayın.
- **Yinelemeli İyileştirme**: Basit başlayın ve gerçek performans ile ihtiyaçlara göre optimize edin.
- **Operasyonel Denge**: Performans gereksinimlerini maliyet ve karmaşıklık kısıtlamalarıyla dengeleyin.

> **Hatırlatma:** En iyi LLM seçimi, operasyonel kısıtlamalarınız dahilinde ihtiyaç duyduğunuz sonuçları tutarlı biçimde sunan seçimdir. Önce gereksinimlerinizi anlamaya odaklanın, ardından bu ihtiyaçlarla en iyi örtüşen modelleri seçin.

## Mevcut Model Ortamı (Haziran 2025)

> **Uyarı — Zamana Bağlı Anlık Görüntü**: Aşağıdaki model sıralamaları, Haziran 2025 itibarıyla [LMSys Arena](https://arena.lmsys.org/), [Artificial Analysis](https://artificialanalysis.ai/) ve diğer lider kıyaslamalardan derlenen mevcut sıralama listesi durumlarını yansıtmaktadır. LLM performansı, kullanılabilirliği ve fiyatlandırması hızla değişmektedir. Her zaman spesifik kullanım durumlarınız ve verilerinizle kendi değerlendirmelerinizi yapın.

### Kategoriye Göre Lider Modeller

Aşağıdaki tablolar, farklı kategorilerdeki mevcut en iyi performans gösteren modellerin temsili bir örneğini ve CrewAI ajanları için uygunluk rehberliğini göstermektedir.

> **Not:** Bu tablolar/metrikler her kategorideki seçili lider modelleri göstermekte olup kapsamlı değildir. Burada listelenenler dışında birçok mükemmel model mevcuttur.

#### Akıl Yürütme ve Planlama — Yönetici LLM ve Karmaşık Analiz İçin En İyi

| Model | Zeka Puanı | Maliyet ($/M token) | Hız | CrewAI'deki En İyi Kullanım |
| :--- | :--- | :--- | :--- | :--- |
| **o3** | 70 | $17,50 | Hızlı | Karmaşık çok ajanlı koordinasyon için Yönetici LLM |
| **Gemini 2.5 Pro** | 69 | $3,44 | Hızlı | Stratejik planlama ajanları, araştırma koordinasyonu |
| **DeepSeek R1** | 68 | $0,96 | Orta | Bütçe odaklı ekipler için maliyet etkin akıl yürütme |
| **Claude 4 Sonnet** | 53 | $6,00 | Hızlı | Nüanslı anlayış gerektiren analiz ajanları |
| **Qwen3 235B (Akıl Yürütme)** | 62 | $2,63 | Orta | Akıl yürütme görevleri için açık kaynak alternatif |

Bu modeller çok adımlı akıl yürütmede üstündür ve strateji geliştirmesi, diğer ajanları koordine etmesi veya karmaşık bilgileri analiz etmesi gereken ajanlar için idealdir.

#### Kodlama ve Teknik — Geliştirme ve Araç Yoğun İş Akışları İçin En İyi

| Model | Kodlama Performansı | Araç Kullanım Puanı | Maliyet ($/M token) | CrewAI'deki En İyi Kullanım |
| :--- | :--- | :--- | :--- | :--- |
| **Claude 4 Sonnet** | Mükemmel | %72,7 | $6,00 | Birincil kodlama ajanı, teknik dokümantasyon |
| **Claude 4 Opus** | Mükemmel | %72,5 | $30,00 | Karmaşık yazılım mimarisi, kod incelemesi |
| **DeepSeek V3** | Çok İyi | Yüksek | $0,48 | Rutin geliştirme için maliyet etkin kodlama |
| **Qwen2.5 Coder 32B** | Çok İyi | Orta | $0,15 | Bütçe dostu kodlama ajanı |
| **Llama 3.1 405B** | İyi | %81,1 | $3,50 | Araç yoğun iş akışları için fonksiyon çağırma LLM |

#### Hız ve Verimlilik — Yüksek Verimli ve Gerçek Zamanlı Uygulamalar İçin En İyi

| Model | Hız (token/sn) | Gecikme (TTFT) | Maliyet ($/M token) | CrewAI'deki En İyi Kullanım |
| :--- | :--- | :--- | :--- | :--- |
| **Llama 4 Scout** | 2.600 | 0,33 sn | $0,27 | Yüksek hacimli işleme ajanları |
| **Gemini 2.5 Flash** | 376 | 0,30 sn | $0,26 | Gerçek zamanlı yanıt ajanları |
| **DeepSeek R1 Distill** | 383 | Değişken | $0,04 | Maliyet optimize yüksek hızlı işleme |
| **Llama 3.3 70B** | 2.500 | 0,52 sn | $0,60 | Dengeli hız ve kapasite |
| **Nova Micro** | Yüksek | 0,30 sn | $0,04 | Basit, hızlı görev yürütme |

**Profesyonel İpucu**: Bu modelleri Groq gibi hızlı çıkarım sağlayıcılarıyla eşleştirmek, özellikle Llama gibi açık kaynak modeller için daha da iyi performans sağlayabilir.

#### Dengeli Performans — Genel Ekipler İçin En İyi Kapsamlı Modeller

| Model | Genel Puan | Çok Yönlülük | Maliyet ($/M token) | CrewAI'deki En İyi Kullanım |
| :--- | :--- | :--- | :--- | :--- |
| **GPT-4.1** | 53 | Mükemmel | $3,50 | Genel amaçlı ekip LLM'si |
| **Claude 3.7 Sonnet** | 48 | Çok İyi | $6,00 | Dengeli akıl yürütme ve yaratıcılık |
| **Gemini 2.0 Flash** | 48 | İyi | $0,17 | Maliyet etkin genel kullanım |
| **Llama 4 Maverick** | 51 | İyi | $0,37 | Açık kaynak genel amaçlı |
| **Qwen3 32B** | 44 | İyi | $1,23 | Bütçe dostu çok yönlülük |

### Mevcut Modeller İçin Seçim Çerçevesi

#### Yüksek Performanslı Ekipler

**Performans öncelikli olduğunda**: Yönetici LLM'ler ve kritik ajanlar için **o3**, **Gemini 2.5 Pro** veya **Claude 4 Sonnet** gibi üst düzey modeller kullanın. Bu modeller karmaşık akıl yürütme ve koordinasyonda üstündür ancak daha yüksek maliyetle gelir.

**Strateji**: Premium modellerin stratejik düşünmeyi üstlenirken verimli modellerin rutin operasyonları yürüttüğü çoklu model yaklaşımı uygulayın.

#### Maliyet Odaklı Ekipler

**Bütçe birincil kısıtlama olduğunda**: **DeepSeek R1**, **Llama 4 Scout** veya **Gemini 2.0 Flash** gibi modellere odaklanın. Bunlar önemli ölçüde düşük maliyetlerle güçlü performans sunar.

**Strateji**: Çoğu ajan için maliyet etkin modeller kullanın; premium modelleri yalnızca en kritik karar alma rolleri için ayırın.

#### Özel İş Akışları

**Belirli alan uzmanlığı için**: Birincil kullanım durumunuz için optimize edilmiş modeller seçin. Kodlama için **Claude 4** serisi, araştırma için **Gemini 2.5 Pro**, fonksiyon çağırma için **Llama 405B**.

**Strateji**: Ekibinizin birincil işlevine göre model seçin; temel yeteneğin model güçlü yönleriyle örtüşmesini sağlayın.

#### Kurumsal ve Gizlilik

**Veriye duyarlı operasyonlar için**: Veri kontrolünde potansiyel performans ödünleri kabul edilebilir biçimde yerel dağıtım sağlayan **Llama 4** serisi, **DeepSeek V3** veya **Qwen3** gibi açık kaynak modelleri değerlendirin.

**Strateji**: Açık kaynak modelleri özel altyapıda dağıtın.

### Model Seçimi İçin Temel Değerlendirmeler

- **Performans Eğilimleri**: Mevcut ortam, akıl yürütme odaklı modeller (o3, Gemini 2.5 Pro) ile dengeli modeller (Claude 4, GPT-4.1) arasında güçlü rekabet göstermektedir. DeepSeek R1 gibi özel modeller mükemmel maliyet-performans oranları sunmaktadır.

- **Hız ve Zeka Ödünleri**: Llama 4 Scout gibi modeller hızı (2.600 token/sn) makul bir zeka düzeyinde korurken önceliklendirirken, o3 gibi modeller hız ve fiyat pahasına akıl yürütme kapasitesini maksimize eder.

- **Açık Kaynağın Uygulanabilirliği**: Açık kaynak ve tescilli modeller arasındaki fark daralmaya devam etmektedir. Hızlı çıkarım sağlayıcıları özellikle açık kaynak modellerle parlıyor; çoğu zaman tescilli alternatiflere göre daha iyi hız/maliyet oranı sunuyor.

> **Bilgi — Test Zorunludur:** Sıralama listesi sıralamaları genel rehberlik sağlar ancak spesifik kullanım durumunuz, istem tarzınız ve değerlendirme kriterleriniz farklı sonuçlar üretebilir. Nihai kararları vermeden önce her zaman aday modelleri gerçek görevleriniz ve verilerinizle test edin.

### Pratik Uygulama Stratejisi

1. **Kanıtlanmış Modellerle Başlayın** — Birden fazla boyutta iyi performans sunan ve kapsamlı gerçek dünya doğrulamasına sahip **GPT-4.1**, **Claude 3.7 Sonnet** veya **Gemini 2.0 Flash** gibi köklü modellerle başlayın.

2. **Özel İhtiyaçları Belirleyin** — Ekibinizin geliştirme için **Claude 4 Sonnet** veya karmaşık analiz için **o3** gibi özel modellerden yararlanacak spesifik gereksinimleri (kodlama, akıl yürütme, hız) olup olmadığını belirleyin. Hıza duyarlı uygulamalar için model seçimiyle birlikte **Groq** gibi hızlı çıkarım sağlayıcılarını değerlendirin.

3. **Çoklu Model Stratejisi Uygulayın** — Farklı ajanlar için rollerine göre farklı modeller kullanın. Yöneticiler ve karmaşık görevler için yüksek kapasiteli modeller, rutin operasyonlar için verimli modeller.

4. **İzleyin ve Optimize Edin** — Kullanım durumunuzla ilgili performans metriklerini takip edin ve yeni modeller yayınlandıkça veya fiyatlandırma değiştikçe model seçimlerini ayarlamaya hazır olun.