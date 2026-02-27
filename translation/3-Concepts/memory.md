## Bellek

Bellek, CrewAI’nin birleşik bellek sistemini kullanarak aracılarının yeteneklerini geliştirmektedir.

### Genel Bakış

CrewAI, **birleşik bir bellek sistemi** sunar – ayrı kısa süreli, uzun süreli, varlık ve dış bellek türlerini tek bir akıllı API ile değiştiren tek bir `Memory` sınıfı. Bellek, içeriği kaydederken LLM kullanarak içeriği analiz eder (kapsamı, kategorileri ve önemi çıkarır) ve semantik benzerliği, yakınlığı ve önemi birleştiren bileşik puanlama ile uyarlanabilir derinlikte hatırlamayı destekler.

Belleği dört şekilde kullanabilirsiniz: **bağımsız** (betikler, not defterleri), **Crew’lar ile**, **aracılar ile** veya **Akışlar içinde**.

## Hızlı Başlangıç

```python
from crewai import Memory

memory = Memory()

# Sakla -- LLM kapsamı, kategorileri ve önemi çıkarır
memory.remember("Kullanıcı veritabanı için PostgreSQL kullanmaya karar verdik.")

# Geri çağırma -- bileşik puan (semantik + yakınlık + önem) tarafından sıralanmış sonuçlar
eşleşmeler = memory.recall("Hangi veritabanını seçtik?")
for m in eşleşmeler:
    print(f"[{m.score:.2f}] {m.record.content}")

# Proje için yakınlık ağırlığını ayarlayın
memory = Memory(yakınlık_ağırlığı=0.5, yakınlık_yarım_ömrü_gün=7)

# Unut
memory.forget(kapsam="/proje/eski")

# Kendi kendini organize eden kapsam ağacını inceleyin
print(memory.tree())
print(memory.info("/"))
```

## Belleği Kullanmanın Dört Yolu

### Bağımsız

Belleği betikler, not defterleri, CLI araçları veya ayrı bir bilgi tabanı olarak kullanın -- araca veya Crew'a gerek yok.

```python
from crewai import Memory

memory = Memory()

# Bilgi oluşturun
memory.remember("API hız sınırı dakika başına 1000 istek.)
memory.remember("Staging ortamımız 8080 portunu kullanır.")
memory.remember("Ekip, tüm yeni sürümler için özellik bayraklarını kullanmayı kabul etti.")

# Daha sonra ihtiyacınız olanı geri alın
eşleşmeler = memory.recall("API sınırları nelerdir?", limit=5)
for m in eşleşmeler:
    print(f"[{m.score:.2f}] {m.record.content}")

# Daha uzun bir metinden atomik gerçekleri çıkarın
ham = """Toplantı notları: MySQL'den PostgreSQL'e geçmeyi
bir sonraki çeyrekte planladık. Bütçe 50 bin dolardır. Sarah geçişi yönetecek."""

gerçekler = memory.extract_memories(ham)
# ["MySQL'den PostgreSQL'e geçiş bir sonraki çeyrekte planlandı",
#  "Veritabanı geçişi bütçesi 50 bin dolardır",
#  "Sarah veritabanı geçişini yönetecek"]

for fact in gerçekler:
    memory.remember(fact)
```

### Crew’lar ile

Varsayılan ayarlar için `memory=True` veya özel davranış için yapılandırılmış bir `Memory` örneği geçirin.

```python
from crewai import Crew, Agent, Task, Process, Memory

# Seçenek 1: Varsayılan bellek
crew = Crew(
    agents=[araştırmacı, yazar],
    tasks=[araştırma_görevi, yazma_görevi],
    process=Process.sıralı,
    memory=True,
    verbose=True,
)

# Seçenek 2: Ayarlanmış puanlama ile özel bellek
memory = Memory(
    yakınlık_ağırlığı=0.4,
    semantik_ağırlığı=0.4,
    önem_ağırlığı=0.2,
    yakınlık_yarım_ömrü_gün=14,
)
crew = Crew(
    agents=[araştırmacı, yazar],
    tasks=[araştırma_görevi, yazma_görevi],
    memory=memory,
)
```

`memory=True` olduğunda, Crew varsayılan bir `Memory()` oluşturur ve Crew'un `embedder` yapılandırmasını otomatik olarak geçirir. Crew'un belleğini kendi belleği olmayan bir aracının aksine, Crew'daki tüm aracılar Crew'un belleğini paylaşır.

Her görevin ardından, Crew otomatik olarak görev çıktısından ayrı gerçekleri çıkarır ve depolar. Her görevden önce, araç belleğinden ilgili bağlamı geri çağırır ve görevin komut istemine enjekte eder.

### Aracılar ile

Aracılar, paylaşılan Crew belleğini (varsayılan) kullanabilir veya özel bağlam için kapsamlı bir görünüm alabilir.

```python
from crewai import Agent, Memory

memory = Memory()

# Araştırmacı özel bir kapsam alır -- yalnızca /agent/araştırmacı'yı görür
araştırmacı = Agent(
    role="Araştırmacı",
    goal="Bilgi bulun ve analiz edin",
    backstory="Ayrıntıya dikkat eden uzman araştırmacı",
    memory=memory.scope("/agent/araştırmacı"),
)

# Yazar Crew'un paylaşılan belleğini kullanır (araca özel bellek ayarlanmamıştır)
writer = Agent(
    role="Yazar",
    goal="Açık, iyi yapılandırılmış içerik üretin",
    backstory="Deneyimli teknik yazar",
    # memory ayarlanmamıştır -- Crew'un belleğini kullanır.
)
```

Bu desen, araştırmacının özel bulgularını korurken yazarın paylaşılan Crew belleğinden okumasını sağlar.

### Akışlar ile

Her Akış yerleşik belleğe sahiptir. Herhangi bir akış metodu içinde `self.remember()`, `self.recall()` ve `self.extract_memories()`'i kullanın.

```python
from crewai.flow.flow import Flow, listen, start

class ResearchFlow(Flow):
    @start()
    def gather_data(self):
        findings = "PostgreSQL 10 bin eşzamanlı bağlantı işleyebilir. MySQL 5 bin ile sınırlıdır."
        self.remember(findings, kapsam="/araştırma/veritabanları")
        return findings

    @listen(gather_data)
    def write_report(self, findings):
        # Geçmiş araştırmalardan bağlam sağlamak için geri alın
        past = self.recall("veritabanı performans kıyaslamaları")
        context = "\n".join(f"- {m.record.content}" for m in past)
        return f"Rapor:\nYeni bulgular: {findings}\nÖnceki bağlam:\n{context}"
```

Daha fazla bilgi için [Akışlar dokümantasyonuna](/concepts/flows) bakın.

## Hiyerarşik Kapsamlar

### Kapsamlar Nedir

Bellekler, bir dosya sistemine benzer bir kapsamlar hiyerarşik ağacında düzenlenir. Her kapsam `/`, `/proje/alfa` veya `/agent/araştırmacı/bulgular` gibi bir yoldur.

```
/
  /şirket
    /şirket/mühendislik
    /şirket/ürün
  /proje
    /proje/alfa
    /proje/beta
  /agent
    /agent/araştırmacı
    /agent/yazar
```

Kapsamlar **bağlamla ilgili belleği** sağlar -- bir kapsam içinde geri çağırdığınızda, yalnızca ağacın o dalını ararsınız, bu da hem hassasiyeti hem de performansı artırır.

### Kapsam Çıkarımı Nasıl Çalışır

Bir kapsam belirtmeden `remember()`'i çağırdığınızda, LLM içeriği ve mevcut kapsam ağacını analiz eder, ardından en iyi yerleşimi önerir. Mevcut bir kapsam uygun değilse, yeni bir tane oluşturur. Zamanla, kapsam ağacı içeriğinden organik olarak büyür -- önceden bir şema tasarlamanıza gerek yoktur.

```python
memory = Memory()

# LLM, içerikten kapsamı çıkarır
memory.remember("Kullanıcı veritabanı için PostgreSQL kullanmaya karar verdik.")
# -> /proje/kararları veya /mühendislik/veritabanı altında yerleştirilebilir

# Kapsamı açıkça da belirtebilirsiniz
memory.remember("Sprint hızı 42 puandır", kapsam="/ekip/metrikler")
```

### Kapsam Ağacını Görselleştirme

```python
print(memory.tree())
# / (15 kayıt)
#   /proje (8 kayıt)
#     /proje/alfa (5 kayıt)
#     /proje/beta (3 kayıt)
#   /agent (7 kayıt)
#     /agent/araştırmacı (4 kayıt)
#     /agent/yazar (3 kayıt)

print(memory.info("/proje/alfa"))
# KapsamInfo(path='/proje/alfa', kayıt_sayısı=5,
#           kategoriler=['mimari', 'veritabanı'],
#           en_eski_kayıt=datetime(...), en_yeni_kayıt=datetime(...),
#           çocuk_kapsamlar=[])
```

### MemoryScope: Alt Ağaç Görünimleri

Bir `MemoryScope`, ağacın bir dalına kısıtlar. Aracın veya bunun kullandığı kodun yalnızca bu alt ağaç içinde görebilmesi ve yazabilmesi.

```python
memory = Memory()

# Belirli bir araca yönelik bir kapsam oluşturun
agent_memory = memory.scope("/agent/araştırmacı")

# Her şey /agent/araştırmacı'ya göredir
agent_memory.remember("LLM belleği üzerine üç ilgili makale bulundu.")
# -> /agent/araştırmacı altında depolanır

agent_memory.recall("ilgili makaleler")
# -> yalnızca /agent/araştırmacı altında arama yapar

# Alt kapsam ile daha da daraltın
project_memory = agent_memory.subscope("proje-alfa")
# -> /agent/araştırmacı/proje-alfa
```

### Kapsam Tasarımı İçin En İyi Uygulamalar

- **Düz başlayın, LLM'nin düzenlemesine izin verin.** Önceden kapsam hiyerarşinizi aşırı mühendislemeyin. `memory.remember(içerik)` ile başlayın ve LLM'nin kapsam çıkarımı içeriğin birikmesiyle yapı oluşturmasına izin verin.
- **`/{varlık_türü}/{tanımlayıcı}` desenlerini kullanın.** Doğal hiyerarşiler `/proje/alfa`, `/agent/araştırmacı`, `/şirket/mühendislik`, `/müşteri/acme-corp` gibi desenlerden ortaya çıkar.
- **Endişeye göre değil, veri türüne göre kapsamlayın.** `/proje/alfa/kararlar` yerine `/kararlar/proje/alfa` kullanın. Bu, ilgili içeriği bir arada tutar.
- **Derinliği sığ tutun (2-3 seviye).** Derinlemesine yerleşik kapsamlar çok seyrekleşir. `/proje/alfa/mimari` iyidir; `/proje/alfa/mimari/kararlar/veritabanları/postgresql` çok derindir.
- **Bildiğinizde açık kapsamlar kullanın, bilmediğinizde LLM'nin çıkarım yapmasına izin verin.** Bir proje kararını depoluyorsanız, `scope="/proje/alfa/kararlar"` geçirin. Serbest biçimli aracı çıktısını depoluyorsanız, kapsamı atlayın ve LLM'nin bunu anlamasına izin verin.

### Kullanım Örnekleri

**Çoklu proje ekibi:**
```python
memory = Memory()
# Her proje kendi dalına sahip
memory.remember("mikro hizmetler mimarisi kullanılıyor", kapsam="/proje/alfa/mimari")
memory.remember("İstemci uygulamaları için GraphQL API'si", kapsam="/proje/beta/api")

# Tüm projelerde geri çağırma
memory.recall("API tasarım kararları")

# Veya belirli bir projede
memory.recall("API tasarım", kapsam="/proje/beta")
```

**Paylaşılan bilgi ile per-aracın özel bağlamı:**
```python
memory = Memory()

# Araştırmacı özel bulgulara sahip
araştırmacı_belleği = memory.scope("/agent/araştırmacı")

# Yazar kendi kapsamından ve paylaşılan şirket bilgisinden okuyabilir
yazar_görünümü = memory.dilim(
    kapsamlar=["/agent/yazar", "/şirket/bilgisi"],
    sadece_okuma=True,
)
```

**Müşteri desteği (müşteri başına bağlam):**
```python
memory = Memory()

# Her müşteri izole bir bağlama sahip
memory.remember("E-posta iletişimi tercih eder", kapsam="/müşteri/acme-corp")
memory.remember("Kurumsal plan, 50 koltuk", kapsam="/müşteri/acme-corp")

# Paylaşılan ürün belgelerine herkes erişebilir
memory.remember("Hız sınırı, kurumsal plan için dakika başına 1000 istek", kapsam="/ürün/belgeleri")
```

## Bellek Dilimleri

### Dilimler Nedir

Bir `MemorySlice`, birden fazla, olası olarak kopuk kapsamdan bir bakıştır. Bir kapsam (tek bir alt ağacı kısıtlar) aksine, bir dilim aynı anda birden fazla daldan bağlamı birleştirmenize olanak tanır.

### Dilimleri mi Kapsamları mı Kullanmalı

- **Kapsam**: Bir aracın veya kod bloğunun tek bir alt ağaca kısıtlanması gerektiğinde kullanın. Örnek: yalnızca `/agent/araştırmacı`'yı gören bir araç.
- **Dilim**: Birden fazla daldan bağlamı birleştirmek gerektiğinde kullanın. Örnek: kendi kapsamı ve paylaşılan şirket bilgisi okuyan bir araç.

### Sadece Okuma Dilimleri

En yaygın desen: bir aracın birden fazla dalı okumasına izin verilirken, paylaşılan alanlara yazmasını engellemek.

```python
memory = Memory()

# Aracın kendi kapsamına VE şirket bilgisine erişebileceği,
# ancak şirket bilgisine yazamadığı bir dilim
agent_view = memory.dilim(
    kapsamlar=["/agent/araştırmacı", "/şirket/bilgisi"],
    sadece_okuma=True,
)

# Şirket bilgileri ile eşleştiği için özel belleği görür
eşleşmeler = agent_view.recall("şirket güvenlik politikaları", limit=5)

# Sadece okuma olduğu için bu geri çağırma özel belleği görmez (farklı bir kaynak)
eşleşmeler = agent_view.recall("API anahtarı", kaynak="user:bob")

# Yönetici erişimi: kaynağı ne olursa olsun tüm özel kayıtları görebilir
eşleşmeler = memory.recall("API anahtarı", include_private=True)
```

### Okuma-Yazma Dilimleri

Sadece okuma devre dışı bırakıldığında, dahil edilen herhangi bir kapsamda yazabilirsiniz, ancak bunu açıkça belirtmeniz gerekir.

```python
view = memory.dilim(kapsamlar=["/ekip/alfa", "/ekip/beta"], sadece_okuma=False)

# Kapsamı belirtmek zorundasınız
view.remember("Çapraz ekip kararı", kapsam="/ekip/alfa", kategoriler=["kararlar"])
```

## Bileşik Puanlama

Geri çağırma sonuçları, üç sinyalin ağırlıklı bir kombinasyonuyla sıralanır:

```
bileşik = semantik_ağırlığı * benzerlik + yakınlık_ağırlığı * bozunma + önem_ağırlığı * önem
```

Burada:
- **benzerlik** = vektör dizininden `1 / (1 + mesafe)` (0 ile 1 arasında)
- **bozunma** = `0.5^(yaş_günleri / yarım_ömür_günleri)` -- üstel bozunma (bugün 1.0, yarım ömürde 0.5)
- **önem** = kayda koyma zamanında kaydın önem puanı (0 ile 1 arasında)

Bunlar, `Memory` yapıcıya doğrudan anahtar kelime argümanları olarak yapılandırılabilir:

```python
# Sprint geriye dönük görüşmesi: son bellekleri tercih edin, kısa yarım ömür
memory = Memory(
    yakınlık_ağırlığı=0.5,
    semantik_ağırlığı=0.3,
    önem_ağırlığı=0.2,
    yakınlık_yarım_ömrü_gün=7,
)

# Mimari bilgi tabanı: önemli bellekleri tercih edin, uzun yarım ömür
memory = Memory(
    yakınlık_ağırlığı=0.1,
    semantik_ağırlığı=0.5,
    önem_ağırlığı=0.4,
    yakınlık_yarım_ömrü_gün=180,
)
```

Her `MemoryMatch`, bir `match_reasons` listesi içerir, böylece bir sonucun neden nerede sıralandığını görebilirsiniz (örneğin `["semantik", "yakınlık", "önem"]`).

## LLM Analiz Katmanı

Bellek, LLM'yi üç şekilde kullanır:

1. **Kaydetme sırasında** -- kapsam, kategoriler veya önem belirtilmediğinde, LLM içeriği analiz eder (kapsamı, kategorileri ve önemi çıkarır).
2. **Geri çağırma sırasında** -- derin/otomatik geri çağırma için, LLM sorguyu (anahtar kelimeler, zaman ipuçları, önerilen kapsamlardır) geri getirmeyi yönlendirmek için analiz eder.
3. **Bellekleri ayıklama** -- `extract_memories(içerik)` ham metni (örneğin, görev çıktısı) atomik bellek ifadelerine ayırır. Aracılar, her bir ifadeyi `remember()`'i çağırmadan önce kullanır, böylece tek bir büyük blok yerine atomik gerçekler depolanır.

Tüm analiz, LLM başarısız olsa bile zarif bir şekilde bozulur – yalnızca depolama veya gömmeler başarısızlıkları bir istisna yükseltir.

## Bellek Birleştirme

Yeni içeriği kaydederken, kodlama boru hattı otomatik olarak depolamadaki benzer mevcut kayıtları kontrol eder. Benzerlik `consolidation_threshold` (varsayılan 0.85) aşarsa, LLM ne yapacağına karar verir:

- **sakla** -- Mevcut kayıt hala doğrudur ve gereksiz değildir.
- **güncelle** -- Mevcut kaydın yeni bilgilerle güncellenmesi gerekir (LLM birleştirilmiş içeriği sağlar).
- **sil** -- Mevcut kayıt eskidir, geçersizdir veya çelişkilidir.
- **yeni_ekle** -- Yeni içeriğin ayrı bir kayıt olarak eklenip eklenmeyeceği.

Bu, yinelenenlerin birikmesini önler. Örneğin, "CrewAI güvenilir çalıştırmayı sağlar" üç kez kaydederseniz, birleştirme yinelenenleri tanır ve yalnızca bir kayıt tutar.

### Yığın İçi Yinelenme

`remember_many()` kullanıldığında, aynı yığındaki öğeler depolanmadan önce birbirine göre karşılaştırılır. İki öğenin kosinüs benzerliği >= `batch_dedup_threshold` (varsayılan 0.98) ise, daha sonraki öğe sessizce bırakılır. Bu, tek bir yığında kesin veya yakın kesin yinelenmeleri yakalar ve herhangi bir LLM çağrısı yapmadan (saf vektör matematiği) gerçekleştirilir.

```python
# Sadece 2 kayıt depolanır (üçüncüsü birincisinin yakın bir kopyasıdır)
memory.remember_many([
    "CrewAI karmaşık iş akışlarını destekler.",
    "Python harika bir dildir.",
    "CrewAI karmaşık iş akışlarını destekler.",  # yığın içi yinelenme tarafından bırakılır
])
```

## Engellemesiz Kaydetmeler

`remember_many()` **engellemesizdir** -- kodlama boru hattını arka plan bir iş parçacığına gönderir ve hemen geri döner. Bu, aracın arka plan işlemleri kaydedilirken bir sonraki göreve devam etmesini sağlar.

```python
# Hemen geri döner -- kaydetme arka planda olur
memory.remember_many(["Gerçek A.", "Gerçek B.", "Gerçek C."])

# recall() arama yapmadan önce bekleyen kaydetmeleri otomatik olarak bekler
eşleşmeler = memory.recall("gerçekler")  # tüm 3 kaydı görür
```

### Okuma Bariyeri

Her `recall()` çağrısı, arama yapmadan önce `drain_writes()`'ı çağırır ve sorgunun her zaman en son depolanan kayıtları gördüğünden emin olur. Bu, şeffaftır – bunun hakkında düşünmenize gerek yoktur.

### Crew Kapatma

Bir Crew tamamlandığında, `kickoff()`'unun `finally` bloğunda tüm bekleyen bellek kaydetmelerini boşaltır, böylece Crew tamamlarken arka plan kaydetmeleri uçuşta olsa bile kayıpları önler.

### Bağımsız Kullanım

Çerçeve yaşam döngüsü olmayan komut dosyalarında veya not defterlerinde, açıkça `drain_writes()` veya `close()`'u çağırın:

```python
memory = Memory()
memory.remember_many(["Gerçek A.", "Gerçek B."])

# Seçenek 1: Bekleyen kaydetmeler için bekleyin
memory.drain_writes()

# Seçenek 2: Arka plan havuzunu boşaltın ve kapatın
memory.close()
```

## Kaynak ve Gizlilik

Her bellek kaydı, köken izleme için bir `kaynak` etiketi ve erişim kontrolü için bir `özel` bayrağı taşıyabilir.

### Kaynak İzleme

`kaynak` parametresi, belleğin nereden geldiğini belirler:

```python
# Bellekleri kökenleriyle etiketleyin
memory.remember("Alice e-posta iletişimini tercih ediyor", kaynak="user:alice")
memory.remember("Sistem yapılandırması güncellendi", kaynak="admin")
memory.remember("Aracı bir hata buldu", kaynak="agent:debug")

# Belirli bir kaynaktan gelen bellekleri geri alın
eşleşmeler = memory.recall("kullanıcı tercihleri", kaynak="user:alice")
```

### Özel Bellekler

Özel bellekler yalnızca kaynak eşleştiğinde geri çağırmaya açıktır:

```python
# Özel bir bellek depolayın
memory.remember("Alice'in API anahtarı sk-...", kaynak="user:alice", özel=True)

# Bu geri çağırma özel belleği görür (kaynak eşleşir)
eşleşmeler = memory.recall("API anahtarı", kaynak="user:alice")

# Bu geri çağırma onu görmez (farklı kaynak)
eşleşmeler = memory.recall("API anahtarı", kaynak="user:bob")

# Yönetici erişimi: kaynağı ne olursa olsun tüm özel kayıtları görebilir
eşleşmeler = memory.recall("API anahtarı", include_private=True)
```

Bu, farklı kullanıcıların belleklerinin izole edilmesi gereken çok kullanıcılı veya kurumsal dağıtımlarda özellikle yararlıdır.

## Derin Geri Çağırma

`recall()` iki derinlikte desteklenir:

- **`derinlik="sığ"`** -- Kompozit puanlamayla doğrudan vektör araması. Hızlıdır (~200 ms), herhangi bir LLM çağrısı yoktur.
- **`derinlik="derin"` (varsayılan)** -- Çok aşamalı bir RecallFlow'u çalıştırır: sorgu analizi, kapsam seçimi, paralel vektör araması, güvene dayalı yönlendirme ve güven düşük olduğunda isteğe bağlı yinelemeli keşif.

**Akıllı LLM atlama**: `query_analysis_threshold` (varsayılan 200 karakter) değerinden daha kısa sorgular LLM sorgu analizi aşamasını tamamen atlar, derin modda bile. Kısa sorgular gibi "Hangi veritabanını kullandık?" zaten iyi arama ifadeleridir – LLM analizi çok fazla değer katmaz. Bu, tipik kısa sorgular için ~1-3 saniyelik tasarruf sağlar. Sadece daha uzun sorgular (örneğin, tam görev açıklamaları) LLM damıtma yoluyla hedeflenmiş alt sorgulara gider.

```python
# Sığ: saf vektör arama, LLM yok
eşleşmeler = memory.recall("Ne karar verdik?", limit=10, derinlik="sığ")

# Derin (varsayılan): uzun sorgular için LLM analiziyle akıllı geri getirme
eşleşmeler = memory.recall(
    "Bu çeyrekteki tüm mimari kararlarını özetleyin",
    limit=10,
    derinlik="derin",
)
```

RecallFlow yönlendiricisini kontrol eden güven eşiklerinin yapılandırılabilir olduğunu unutmayın:

```python
memory = Memory(
    yüksek_güven_eşik_değeri=0.9,   # Sadece çok güvenli olduğunda sentezleyin
    düşük_güven_eşik_değeri=0.4,    # Daha agresif olarak daha derin keşfedin
    keşif_bütçesi=2,            # En fazla 2 keşif turuna izin verin
    sorgu_analiz_eşik_değeri=200,    # Bu değerden daha kısa sorgular için LLM'yi atlayın
)
```

## Kodlayıcı Yapılandırması

Bellek, metni semantik arama için vektörlere dönüştürmek için bir gömme modeline ihtiyaç duyar. Bu, üç şekilde yapılandırılabilir:

### Belleğe Doğrudan Geçirme

```python
from crewai import Memory

# Bir yapılandırma sözlüğü olarak
memory = Memory(embedder={"sağlayıcı": "openai", "yapılandırma": {"model_adı": "metin-gömme-3-küçük"}})

# Önceden oluşturulmuş bir çağırma fonksiyonu olarak
from crewai.rag.embeddings.factory import build_embedder
embedder = build_embedder({"sağlayıcı": "ollama", "yapılandırma": {"model_adı": "mxbai-embed-büyük"}})
memory = Memory(embedder=embedder)
```

### Crew Gömme Yapılandırması Aracılığıyla

`memory=True` kullanıldığında, Crew'un `embedder` yapılandırması geçirilir:

```python
from crewai import Crew

crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,
    embedder={"sağlayıcı": "openai", "yapılandırma": {"model_adı": "metin-gömme-3-küçük"}},
)
```

### Sağlayıcı Örnekleri

```python
memory = Memory(embedder={
    "sağlayıcı": "openai",
    "yapılandırma": {
        "model_adı": "metin-gömme-3-küçük",
        # "api_anahtarı": "sk-...",  # veya OPENAI_API_KEY ortam değişkenini ayarlayın
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "ollama",
    "yapılandırma": {
        "model_adı": "mxbai-embed-büyük",
        "url": "http://localhost:11434/api/embeddings",
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "azure",
    "yapılandırma": {
        "yerleşim_id": "yerleşim_gömme",
        "api_anahtarı": "azure_api_anahtarınız",
        "api_temeli": "https://your-resource.openai.azure.com",
        "api_sürümü": "2024-02-01",
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "google-generativeai",
    "yapılandırma": {
        "model_adı": "gemini-gömme-001",
        # "api_anahtarı": "...",  # veya GOOGLE_API_KEY ortam değişkenini ayarlayın
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "google-vertex",
    "yapılandırma": {
        "model_adı": "gemini-gömme-001",
        "proje_id": "gcp_proje_kimliğiniz",
        "konum": "us-central1",
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "cohere",
    "yapılandırma": {
        "model_adı": "göm-ingilizce-v3.0",
        # "api_anahtarı": "...",  # veya COHERE_API_KEY ortam değişkenini ayarlayın
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "voyageai",
    "yapılandırma": {
        "model": "seyahat-3",
        # "api_anahtarı": "...",  # veya VOYAGE_API_KEY ortam değişkenini ayarlayın
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "amazon-bedrock",
    "yapılandırma": {
        "model_adı": "amazon.titan-embed-text-v1",
        # boto3 kimlik bilgilerini varsayılan olarak kullanır
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "huggingface",
    "yapılandırma": {
        "model_adı": "sentence-transformers/all-MiniLM-L6-v2",
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "jina",
    "yapılandırma": {
        "model_adı": "jina-embeddings-v2-base-en",
        # "api_anahtarı": "...",  # veya JINA_API_KEY ortam değişkenini ayarlayın
    },
})
```

```python
memory = Memory(embedder={
    "sağlayıcı": "watsonx",
    "yapılandırma": {
        "model_id": "ibm/slate-30m-ingilizce-rtrvr",
        "api_anahtarı": "watsonx_api_anahtarınız",
        "proje_id": "proje_kimliğiniz",
        "url": "https://us-south.ml.cloud.ibm.com",
    },
})
```

```python
# Bir liste dize alır ve vektör listesi döndüren herhangi bir çağırma fonksiyonunu geçin
def özel_gömme(metinler: list[str]) -> list[list[float]]:
    # Gömme mantığınız burada
    return [[0.1, 0.2, ...] for _ in metinler]

memory = Memory(embedder=özel_gömme)
```

### Sağlayıcı Referansı

| Sağlayıcı | Anahtar | Tipik Model | Notlar |
| :--- | :--- | :--- | :--- |
| OpenAI | `openai` | `metin-gömme-3-küçük` | Varsayılan. `OPENAI_API_KEY`'i ayarlayın. |
| Ollama | `ollama` | `mxbai-embed-büyük` | Yerel, API anahtarı gerekli değildir. |
| Azure OpenAI | `azure` | `metin-gömme-ada-002` | `yerleşim_id` gerektirir. |
| Google AI | `google-generativeai` | `gemini-gömme-001` | `GOOGLE_API_KEY`'i ayarlayın. |
| Google Vertex | `google-vertex` | `gemini-gömme-001` | `proje_id` gerektirir. |
| Cohere | `cohere` | `göm-ingilizce-v3.0` | Güçlü çoklu dil desteği. |
| VoyageAI | `voyageai` | `seyahat-3` | Geri getirme için optimize edilmiştir. |
| AWS Bedrock | `amazon-bedrock` | `amazon.titan-embed-text-v1` | boto3 kimlik bilgilerini kullanır. |
| Hugging Face | `huggingface` | `all-MiniLM-L6-v2` | Yerel cümle dönüştürücüler. |
| Jina | `jina` | `jina-embeddings-v2-base-en` | `JINA_API_KEY`'i ayarlayın. |
| IBM WatsonX | `watsonx` | `ibm/slate-30m-ingilizce-rtrvr` | `proje_id` gerektirir. |
| Cümle Dönüştürücü | `sentence-transformer` | `all-MiniLM-L6-v2` | Yerel, API anahtarı gerekli değildir. |
| Özel | `özel` | -- | `embedding_callable` gerektirir. |

## LLM Yapılandırması

Bellek, kaydedilecek analiz (kapsam, kategoriler, önem çıkarımı), birleştirme kararları ve derin geri çağırma sorgusu analizi için bir LLM kullanır. Bu modelin nasıl yapılandırılacağını aşağıda gösteririz.

```python
from crewai import Memory, LLM

# Varsayılan: gpt-4o-mini
memory = Memory()

# Farklı bir OpenAI modeli kullanın
memory = Memory(llm="gpt-4o")

# Anthropic kullanın
memory = Memory(llm="anthropic/claude-3-haiku-20240307")

# Tamamen yerel/özel işlem için Ollama kullanın
memory = Memory(llm="ollama/llama3.2")

# Google Gemini kullanın
memory = Memory(llm="gemini/gemini-2.0-flash")

# Özel ayarlar içeren önceden yapılandırılmış bir LLM örneği geçirin
llm = LLM(model="gpt-4o", sıcaklık=0)
memory = Memory(llm=llm)
```

LLM, yalnızca ihtiyaç duyulduğunda **tembelce** başlatılır – bu, API anahtarları ayarlanmamış olsa bile `Memory()` oluşturma zamanında başarısız olmaz. Hatalar yalnızca LLM aslında çağrıldığında ortaya çıkar (örneğin, açık kapsam/kategoriler olmadan kaydetme veya derin geri çağırma sırasında).

Tamamen çevrimdışı/özel işlem için hem LLM hem de gömmeci için yerel bir model kullanın:

```python
memory = Memory(
    llm="ollama/llama3.2",
    embedder={"sağlayıcı": "ollama", "yapılandırma": {"model_adı": "mxbai-embed-büyük"}},
)
```

## Depolama Arka Ucu

- **Varsayılan**: LanceDB, `./.crewai/bellek`'te depolanır (veya `CREWAI_STORAGE_DIR` ortam değişkeni ayarlanmışsa `$CREWAI_STORAGE_DIR/bellek` veya `storage="dizin/yolu"` olarak geçirdiğiniz yol).
- **Özel arka uç**: `StorageBackend` protokolunu uygulayın (bkz. `crewai.memory.storage.backend`) ve `Memory(storage=arka_uç_örneğiniz)` ile bir örnek geçirin.

## Keşif

Kapsam hiyerarşisini, kategorileri ve kayıtları inceleyin:

```python
memory.tree()                        # Biçimlendirilmiş kapsamlar ağacı ve kayıt sayıları
memory.tree("/proje", max_depth=2) # Alt ağaç görünümü
memory.info("/proje")              # KapsamInfo: kayıt_sayısı, kategoriler, en_eski/en_yeni
memory.list_scopes("/")              # Anında çocuk kapsamlar
memory.list_categories()             # Kategori adları ve sayıları
memory.list_records(kapsam="/proje/alfa", limit=20)  # Bir kapsamdaki kayıtlar, en yeni ile başlar
```

## Hata Davranışı

LLM analiz sırasında başarısız olursa (ağ hatası, hız sınırı, geçersiz yanıt), bellek zarifçe bozulur:

- **Kaydetme analizi** -- Bir uyarı günlüğe kaydedilir ve bellek varsayılan kapsam `/`, boş kategoriler ve önem `0.5` ile depolanır.
- **Ayıklama bellekleri** -- Tam içerik tek bir bellek olarak depolanır, böylece hiçbir şey düşmez.
- **Sorgu analizi** -- Geri çağırma basit kapsam seçimi ve vektör aramasında geri döner, böylece yine de sonuçlar alırsınız.

Bu analiz başarısızlıkları için istisna yükseltilmez; yalnızca depolama veya gömmeler başarısızlıkları bir istisna yükseltir.