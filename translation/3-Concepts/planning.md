## Genel Bakış

CrewAI'daki planlama özelliği, mürettebatınıza planlama yeteneği eklemenize olanak tanır. Etkinleştirildiğinde, her Crew yinelemesinden önce, tüm Crew bilgileri, adım adım görevleri planlayacak bir AgentPlanner'a gönderilir ve bu plan, her görev tanımına eklenir.

### Planlama Özelliğini Kullanma

Planlama özelliğini kullanmaya başlamak çok kolaydır, gerekli tek adım `planning=True`'yu Crew'unuza eklemektir:

```python Code
from crewai import Crew, Agent, Task, Process

# Planlama yetenekleriyle mürettebatınızı bir araya getirin
my_crew = Crew(
    agents=self.agents,
    tasks=self.tasks,
    process=Process.sequential,
    planning=True,
)
```

Buradan itibaren mürettebatınızda planlama etkinleştirilecektir ve görevler her yinelemeden önce planlanacaktır.

Planlama etkinleştirildiğinde, crewAI planlama için varsayılan olarak `gpt-4o-mini` LLM'sini kullanacaktır ve bunun için geçerli bir OpenAI API anahtarı gerekir. Aracınız farklı LLM'leri kullanıyorsa, bu durum bir OpenAI API anahtarına sahip değilseniz veya LLM API çağrılarıyla ilgili beklenmedik davranışlar yaşıyorsanız kafa karışıklığına neden olabilir.

#### Planlama LLM

Şimdi görevleri planlamak için kullanılacak LLM'yi tanımlayabilirsiniz.

Temel örnek çalıştırmayı çalıştırırken, `AgentPlanner`'ın adım adım mantığı oluşturmaktan sorumlu olduğu çıktının altındaki örneğe benzer bir çıktı göreceksiniz.

```python Code
from crewai import Crew, Agent, Task, Process

# Planlama yetenekleri ve özel LLM ile mürettebatınızı bir araya getirin
my_crew = Crew(
    agents=self.agents,
    tasks=self.tasks,
    process=Process.sequential,
    planning=True,
    planning_llm="gpt-4o"
)

# Mürettebatı çalıştırın
my_crew.kickoff()
```

```markdown Result
[2024-07-15 16:49:11][INFO]: Mürettebat yürütülmesinin planlanması
**Görev Yürütme için Adım Adım Plan**

**Görev Numarası 1: AI LLM'ler hakkında kapsamlı bir araştırma yapın**

**Aracı:** AI LLM'ler Kıdemli Veri Araştırmacısı

**Aracı Hedefi:** AI LLM'lerdeki son gelişmeleri ortaya çıkarın

**Beklenen Görev Çıktısı:** AI LLM'ler hakkında en alakalı bilgileri içeren 10 madde işaretli bir liste

**Görev Araçları:** Belirtilmedi

**Aracı Araçları:** Belirtilmedi

**Adım Adım Plan:**

1. **Araştırma Kapsamını Tanımlayın:**

   - Odaklanılacak AI LLM'lerin özel alanlarını belirleyin; mimari, kullanım alanları, etik hususlar ve performans ölçütleri gibi.

2. **Güvenilir Kaynakları Belirleyin:**

   - Akademik dergiler, sektör raporları, konferanslar (örn. NeurIPS, ACL), AI araştırma laboratuvarları (örn. OpenAI, Google AI) ve çevrimiçi veritabanları (örn. IEEE Xplore, arXiv) dahil olmak üzere AI araştırması için güvenilir kaynakların bir listesini oluşturun.

3. **Veri Toplayın:**

   - 2024 ve ilk 2025'te yayınlanan en son makaleler, makaleler ve raporlar için arama yapın.
   - "Büyük Dil Modelleri 2025", "AI LLM gelişmeleri", "AI etiği 2025" gibi anahtar kelimeler kullanın.

4. **Bulguları Analiz Edin:**

   - Her kaynaktan ana noktaları okuyun ve özetleyin.
   - Geçtiğimiz yılda tanıtılan yeni teknikleri, modelleri ve uygulamaları vurgulayın.

5. **Bilgileri Düzenleyin:**

   - Bilgileri ilgili konulara göre (örn. yeni mimariler, etik etkiler, gerçek dünya uygulamaları) kategorilere ayırın.
   - Her madde işaretinin özlü ancak bilgilendirici olduğundan emin olun.

6. **Listeyi Oluşturun:**

   - En alakalı 10 bilgiyi bir madde işaretli listeye derleyin.
   - Açıklık ve alaka düzeyini sağlamak için listeyi gözden geçirin.

**Beklenen Çıktı:**

AI LLM'ler hakkında en alakalı bilgileri içeren 10 madde işaretli bir liste.

---

**Görev Numarası 2: Aldığınız bağlamı gözden geçirin ve her konuyu bir rapor için ayrı bir bölüme genişletin**

**Aracı:** AI LLM'ler Raporlama Analisti

**Aracı Hedefi:** AI LLM veri analizleri ve araştırma bulgularına göre ayrıntılı raporlar oluşturun

**Beklenen Görev Çıktısı:** Ana konuları içeren, her biri bilgi dolu ayrı bir bölüme sahip tam teşekküllü bir rapor. '```' olmadan markdown olarak biçimlendirilmiş

**Görev Araçları:** Belirtilmedi

**Aracı Araçları:** Belirtilmedi

**Adım Adım Plan:**

1. **Madde İşaretlerini Gözden Geçirin:**
   - AI LLM'ler Kıdemli Veri Araştırmacısı tarafından sağlanan 10 madde işaretli listenin dikkatlice okunması.

2. **Raporu Taslaklayın:**
   - Her madde işaretini ana bölüm başlığı olarak kullanarak bir taslak oluşturun.
   - Konunun farklı yönlerini kapsamak için her ana başlık altında alt başlıklar planlayın.

3. **Daha Fazla Ayrıntı Araştırın:**
   - Her madde işareti için, her bölüm için daha ayrıntılı bilgi toplamak için gerektiğinde ek araştırma yapın.
   - Her bölümü desteklemek için vaka çalışmaları, örnekler ve istatistiksel veriler arayın.

4. **Ayrıntılı Bölümler Yazın:**
   - Her madde işaretini kapsamlı bir bölüme genişletin.
   - Her bölümün bir giriş, ayrıntılı bir açıklama, örnekler ve bir sonuç içerdiğinden emin olun.
   - Başlıklar, alt başlıklar, listeler ve vurgu için markdown biçimlendirmesi kullanın.

5. **Gözden Geçirin ve Düzenleyin:**
   - Açıklık, tutarlılık ve doğruluk için raporu okuyun.
   - Raporun mantıksal olarak bir bölümden diğerine aktığını sağlayın.
   - Raporu markdown standartlarına göre biçimlendirin.

6. **Raporu Sonlandırın:**
   - Tüm bölümlerin genişletilmiş ve ayrıntılı olduğundan emin olun.
   - Biçimlendirmeyi iki kez kontrol edin ve gerekli ayarlamaları yapın.

**Beklenen Çıktı:**
Ana konuları içeren, her biri bilgi dolu ayrı bir bölüme sahip tam teşekküllü bir rapor. '```' olmadan markdown olarak biçimlendirilmiş.
