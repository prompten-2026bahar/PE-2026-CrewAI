# Muhakeme Yeteneği

Agent'ların görev yürütmesini iyileştirmek için agent muhakemesini nasıl etkinleştireceğinizi ve kullanacağınızı öğrenin.

## Genel Bakış

Agent muhakemesi, agent'ların bir görev üzerinde düşünmesini ve yürütmeden önce bir plan oluşturmasını sağlayan bir özelliktir. Bu, agent'ların görevlere daha metodik bir şekilde yaklaşmasına ve atanan işi yapmaya hazır olmasını sağlamasına yardımcı olur.

## Kullanım

Bir agent için muhakemeyi etkinleştirmek için, agent oluştururken `reasoning=True` değerini ayarlamanız yeterlidir:

```python
from crewai import Agent

agent = Agent(
    role="Veri Analisti",
    goal="Karmaşık veri kümelerini analiz et ve içgörüler sağla",
    backstory="You are an experienced data analyst with expertise in finding patterns in complex data.",
    reasoning=True,  # Muhakemeyi etkinleştir
    max_reasoning_attempts=3  # İsteğe bağlı: Muhakeme denemelerinin maksimum sayısını ayarla
)
```

## Nasıl Çalışır

Muhakeme etkinleştirildiğinde, bir görevi yürütmeden önce agent aşağıdaki adımları izleyecektir:

1. Görevi değerlendirir ve ayrıntılı bir plan oluşturur
2. Görevi yürütmeye hazır olup olmadığını değerlendirir
3. Planı hazır olana veya `max_reasoning_attempts` değerine ulaşılana kadar gerekli görüldüğü şekilde iyileştirir
4. Yürütmeden önce muhakeme planını görev tanımına enjekte eder

Bu süreç, agent'ların karmaşık görevleri yönetilebilir adımlara ayırarak ve başlamadan önce olası zorlukları belirlemelerine yardımcı olur.

## Yapılandırma Seçenekleri

 
    Muhakemeyi etkinleştirin veya devre dışı bırakın 


 
    Yürütmeyle devam etmeden önce planın iyileştirilmesi için maksimum deneme sayısı. None (varsayılan) ise, agent hazır olana kadar iyileştirmeye devam eder. 


## Örnek

İşte eksiksiz bir örnek:

```python
from crewai import Agent, Task, Crew

# Muhakemesi etkinleştirilmiş bir agent oluştur
analyst = Agent(
    role="Veri Analisti",
    goal="Veri analiz et ve içgörüler sağla",
    backstory="You are an expert data analyst.",
    reasoning=True,
    max_reasoning_attempts=3  # İsteğe bağlı: Muhakeme denemelerinin sayısını sınırlayın
)

# Bir görev oluştur
analysis_task = Task(
    description="Sağlanan satış verilerini analiz et ve önemli eğilimleri belirle.",
    expected_output="En iyi 3 satış eğilimini vurgulayan bir rapor.",
    agent=analyst
)

# Bir ekip oluştur ve görevi çalıştır
crew = Crew(agents=[analyst], tasks=[analysis_task])
result = crew.kickoff()

print(result)
```

## Hata Yönetimi

Muhakeme süreci, yerleşik hata yönetimi ile sağlam bir şekilde tasarlanmıştır. Muhakeme sırasında bir hata oluşursa, agent muhakeme planı olmaksızın görevi yürütmeye devam eder. Bu, muhakeme süreci başarısız olsa bile görevlerin hala yürütülebilmesini sağlar.

Potansiyel hataları kodunuzda nasıl ele alacağınız aşağıda açıklanmıştır:

```python
from crewai import Agent, Task

# Herhangi bir muhakeme hatasını yakalamak için günlük kaydetmeyi ayarlayın
import logging
logging.basicConfig(level=logging.INFO)

# Muhakemesi etkinleştirilmiş bir agent oluştur
agent = Agent(
    role="Veri Analisti",
    goal="Veri analiz et ve içgörüler sağla",
    reasoning=True,
    max_reasoning_attempts=3
)

# Bir görev oluştur
task = Task(
    description="Sağlanan satış verilerini analiz et ve önemli eğilimleri belirle.",
    expected_output="En iyi 3 satış eğilimini vurgulayan bir rapor.",
    agent=agent
)

# Görevi yürüt
# Muhakeme sırasında bir hata oluşursa, günlüğe kaydedilir ve yürütme devam eder
result = agent.execute_task(task)
```

## Örnek Muhakeme Çıktısı

İşte bir veri analizi görevi için bir muhakeme planının nasıl görünmesine dair bir örnek:

```
Görev: Sağlanan satış verilerini analiz et ve önemli eğilimleri belirle.

Muhakeme Planı:
Satış verilerini analiz ederek en iyi 3 eğilimi belirleyeceğim.

1. Görev Anlayışı:
   İşletme karar alma süreçleri için değerli olabilecek satış verilerini analiz ederek temel eğilimleri belirlemem gerekiyor.

2. İzleyeceğim temel adımlar:
   - Öncelikle, hangi alanların mevcut olduğunu anlamak için veri yapısını inceleyeceğim.
   - Daha sonra desenleri belirlemek için keşif amaçlı veri analizi yapacağım.
   - Ardından satışları zaman dilimlerine göre analiz ederek zamansal eğilimleri belirleyeceğim.
   - Ayrıca satışları ürün kategorilerine ve müşteri segmentlerine göre analiz edeceğim.
   - Son olarak en önemli 3 eğilimi belirleyeceğim.

3. Zorluklara Yaklaşım:
   - Veride eksik değerler varsa, bunları doldurup filtreleyeceğim mi karar vereceğim.
   - Veride aykırı değerler varsa, bunların geçerli veri noktaları mı yoksa hatalar mı olduğunu araştıracağım.
   - Eğilimler hemen belirgin olmazsa, desenleri ortaya çıkarmak için istatistiksel yöntemler uygulayacağım.

4. Mevcut araçların kullanımı:
   - Veriyi keşfetmek ve görselleştirmek için veri analiz araçlarını kullanacağım.
   - Desenleri belirlemek için istatistiksel araçları kullanacağım.
   - Satış analizi ile ilgili ilgili bilgilere erişmek için bilgi alma becerisini kullanacağım.

5. Beklenen sonuç:
   Verilerden elde edilen kanıtlarla en iyi 3 satış eğilimini vurgulayan özlü bir rapor.

HAZIR: Görevi yürütmeye hazırım.
```

Bu muhakeme planı, agent'ın göreve yaklaşımını düzenlemesine, olası zorlukları göz önünde bulundurmasına ve beklenen çıktıyı sunmasını sağlamasına yardımcı olur.
