> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Hiyerarşik Süreç

> CrewAI projelerinizde hiyerarşik süreci anlamaya ve uygulamaya yönelik kapsamlı kılavuz; en güncel kodlama pratikleri ve işlevler yansıtılacak şekilde güncellenmiştir.

## Giriş

CrewAI'deki hiyerarşik süreç, verimli görev delegasyonu ve yürütme için geleneksel organizasyonel hiyerarşileri simüle eden yapılandırılmış bir görev yönetimi yaklaşımı sunar. Bu sistematik iş akışı, görevlerin optimal verimlilik ve doğrulukla ele alınmasını sağlayarak proje sonuçlarını iyileştirir.

> **İpucu:** Hiyerarşik süreç, GPT-4 gibi gelişmiş modellerden yararlanacak şekilde tasarlanmıştır; token kullanımını optimize ederken karmaşık görevleri daha yüksek verimlilikle yönetir.

## Hiyerarşik Sürece Genel Bakış

CrewAI'de görevler varsayılan olarak sıralı bir süreçle yönetilir. Ancak hiyerarşik yaklaşım benimsemek, görev yönetiminde net bir hiyerarşiye imkân tanır: bir 'yönetici' ajan iş akışını koordine eder, görevleri delege eder ve sonuçları doğrular. Bu yönetici ajan artık CrewAI tarafından otomatik olarak oluşturulabilir ya da kullanıcı tarafından açıkça belirlenebilir.

### Temel Özellikler

- **Görev Delegasyonu**: Yönetici ajan, görevleri ekip üyelerinin rolleri ve yeteneklerine göre dağıtır.
- **Sonuç Doğrulama**: Yönetici, sonuçların gerekli standartları karşıladığından emin olmak için değerlendirir.
- **Verimli İş Akışı**: Kurumsal yapıları taklit ederek görev yönetimine düzenli bir yaklaşım sağlar.
- **Sistem İstemi Yönetimi**: Sistemin önceden tanımlanmış istemleri kullanıp kullanmayacağını isteğe bağlı olarak belirleyin.
- **Durdurma Sözcükleri Kontrolü**: o1 modelleri dahil çeşitli modelleri destekleyecek şekilde durdurma sözcüklerinin kullanılıp kullanılmayacağını isteğe bağlı olarak belirleyin.
- **Bağlam Penceresi Uyumu**: Bağlam penceresine saygıyı etkinleştirerek önemli bağlamı önceliklendirin; bu artık varsayılan davranıştır.
- **Delegasyon Kontrolü**: Kullanıcılara açık kontrol sağlamak amacıyla delegasyon artık varsayılan olarak devre dışıdır.
- **Dakika Başına Maksimum İstek**: Dakika başına maksimum istek sayısını ayarlamak için yapılandırılabilir seçenek.
- **Maksimum Yineleme**: Nihai yanıt elde etmek için maksimum yineleme sayısını sınırlayın.

## Hiyerarşik Süreci Uygulama

Hiyerarşik süreci kullanmak için, varsayılan davranış `Process.sequential` olduğundan process niteliğini açıkça `Process.hierarchical` olarak ayarlamak zorunludur. Belirlenmiş bir yöneticiyle bir ekip tanımlayın ve açık bir komuta zinciri oluşturun.

> **İpucu:** Yöneticinin rehberliği altında belirlenen ajanlarca görev delegasyonu ve yürütmeyi kolaylaştırmak için araçları ajan düzeyinde atayın. Araçlar, görev yürütme sırasında araç kullanılabilirliği üzerinde hassas kontrol için görev düzeyinde de belirtilebilir.

> **İpucu:** Hiyerarşik süreç için `manager_llm` parametresini yapılandırmak kritik öneme sahiptir. Sistem, uygun işleyiş ve özelleştirilmiş karar alma için bir yönetici LLM ayarlanmasını gerektirir.

```python
from crewai import Crew, Process, Agent

# Ajanlar geçmiş hikaye, önbellek ve ayrıntılı mod nitelikleriyle tanımlanır
researcher = Agent(
    role='Researcher',
    goal='Derinlemesine analiz yap',
    backstory='Gizli trendleri ortaya çıkarma yeteneğine sahip deneyimli veri analisti.',
)
writer = Agent(
    role='Writer',
    goal='İlgi çekici içerikler oluştur',
    backstory='Teknik alanlarda hikaye anlatımına tutkulu yaratıcı yazar.',
)

# Hiyerarşik süreç ve ek yapılandırmalarla ekibi kurma
project_crew = Crew(
    tasks=[...],  # Yöneticinin gözetiminde delege edilip yürütülecek görevler
    agents=[researcher, writer],
    manager_llm="gpt-4o",  # Yöneticinin hangi LLM'i kullanacağını belirtin
    process=Process.hierarchical,
    planning=True,
)
```

### Özel Yönetici Ajan Kullanma

Alternatif olarak, projenizin yönetim ihtiyaçlarına göre uyarlanmış özel niteliklere sahip bir yönetici ajan oluşturabilirsiniz. Bu yaklaşım, yöneticinin davranışı ve yetenekleri üzerinde daha fazla kontrol sağlar.

```python
# Özel bir yönetici ajan tanımlayın
manager = Agent(
    role="Project Manager",
    goal="Ekibi verimli şekilde yönet ve yüksek kaliteli görev tamamlanmasını sağla",
    backstory="Karmaşık projeleri yönetme ve ekipleri başarıya yönlendirme konusunda deneyimli bir proje yöneticisisiniz.",
    allow_delegation=True,
)

# Özel yöneticiyi ekibinizde kullanın
project_crew = Crew(
    tasks=[...],
    agents=[researcher, writer],
    manager_agent=manager,  # Özel yönetici ajanınızı kullanın
    process=Process.hierarchical,
    planning=True,
)
```

> **İpucu:** Yönetici ajan oluşturma ve özelleştirme hakkında daha fazla ayrıntı için [Özel Yönetici Ajan dokümantasyonunu](/en/learn/custom-manager-agent) inceleyin.

### İşleyişin Adımları

1. **Görev Atama**: Yönetici, her ajanın yeteneklerini ve mevcut araçları göz önünde bulundurarak görevleri stratejik biçimde atar.
2. **Yürütme ve İnceleme**: Ajanlar, kolaylaştırılmış iş akışları için asenkron yürütme ve geri çağırma fonksiyonları seçeneğiyle görevlerini tamamlar.
3. **Sıralı Görev İlerlemesi**: Hiyerarşik bir süreç olmasına karşın görevler, yöneticinin gözetiminde sorunsuz ilerleme için mantıksal bir sırayı takip eder.

## Sonuç

CrewAI'de hiyerarşik süreci doğru yapılandırmalar ve sistemin yeteneklerine ilişkin anlayışla benimsemek, proje yönetimine düzenli ve verimli bir yaklaşım sağlar. İş akışını özel ihtiyaçlarınıza göre uyarlamak, optimal görev yürütmesi ve proje başarısını garantilemek için gelişmiş özellikler ve özelleştirmelerden yararlanın.
