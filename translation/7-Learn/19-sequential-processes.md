# Ardışık Süreçler (Sequential Processes)

> CrewAI projelerinde görev yürütme için ardışık süreçlerin kullanılmasına yönelik kapsamlı bir rehber.

## Giriş

CrewAI, hem ardışık hem de hiyerarşik süreçleri destekleyerek görevlerin yapılandırılmış bir şekilde yürütülmesi için esnek bir çerçeve sunar.
Bu kılavuz, verimli görev yürütme ve proje tamamlamayı sağlamak için bu süreçlerin nasıl etkili bir şekilde uygulanacağını ana hatlarıyla belirtmektedir.

## Ardışık Süreç Genel Bakış

Ardışık süreç, görevlerin doğrusal bir ilerlemeyi takip ederek birbiri ardına yürütülmesini sağlar.
Bu yaklaşım, görevlerin belirli bir sırayla tamamlanmasını gerektiren projeler için idealdir.

### Temel Özellikler

* **Doğrusal Görev Akışı**: Görevleri önceden belirlenmiş bir sırayla işleyerek düzenli bir ilerleme sağlar.
* **Basitlik**: Adım adım ilerleyen, net görevleri olan projeler için en uygunudur.
* **Kolay İzleme**: Görev tamamlanmasının ve proje ilerlemesinin kolayca takip edilmesini sağlar.

## Ardışık Süreci Uygulama

Ardışık süreci kullanmak için ekibinizi oluşturun ve görevleri yürütülmeleri gereken sıraya göre tanımlayın.

```python
from crewai import Crew, Process, Agent, Task, TaskOutput, CrewOutput

# Temsilcilerinizi tanımlayın
researcher = Agent(
  role='Araştırmacı',
  goal='Temel araştırmalar yürütmek',
  backstory='İçgörüleri ortaya çıkarma tutkusu olan deneyimli bir araştırmacı'
)
analyst = Agent(
  role='Veri Analisti',
  goal='Araştırma bulgularını analiz etmek',
  backstory='Kalıpları ortaya çıkarma becerisine sahip titiz bir analist'
)
writer = Agent(
  role='Yazar',
  goal='Final raporunu taslak haline getirmek',
  backstory='Etkileyici anlatılar oluşturma yeteneğine sahip yetenekli bir yazar'
)

# Görevlerinizi tanımlayın
research_task = Task(
  description='İlgili verileri topla...', 
  agent=researcher, 
  expected_output='Ham Veri'
)
analysis_task = Task(
  description='Verileri analiz et...', 
  agent=analyst, 
  expected_output='Veri İçgörüleri'
)
writing_task = Task(
  description='Raporu oluştur...', 
  agent=writer, 
  expected_output='Final Raporu'
)

# Ardışık bir süreçle ekibi (crew) oluşturun
report_crew = Crew(
  agents=[researcher, analyst, writer],
  tasks=[research_task, analysis_task, writing_task],
  process=Process.sequential
)

# Ekibi çalıştırın
result = report_crew.kickoff()

# Tip güvenli çıktıya erişim
task_output: TaskOutput = result.tasks[0].output
crew_output: CrewOutput = result.output
```

### Not:

Ardışık bir süreçteki her görevin atanmış bir temsilcisi **olmalıdır**. Her `Task`ın bir `agent` parametresi içerdiğinden emin olun.

### İş Akışı Başında

1. **İlk Görev**: Ardışık bir süreçte, ilk temsilci görevini tamamlar ve tamamlandığını bildirir.
2. **Sonraki Görevler**: Temsilciler, süreç türüne göre görevlerini üstlenirler; önceki görevlerin çıktıları veya yönergeler yürütmelerine rehberlik eder.
3. **Tamamlama**: Süreç, son görev yürütüldüğünde sona erer ve projenin tamamlanmasına yol açar.

## Gelişmiş Özellikler

### Görev Delegasyonu

Ardışık süreçlerde, bir temsilcinin `allow_delegation` ayarı `True` ise, görevleri ekipteki diğer temsilcilere devredebilir.
Bu özellik, ekipte birden fazla temsilci olduğunda otomatik olarak kurulur.

### Asenkron Yürütme

Görevler asenkron olarak yürütülebilir ve uygun olduğunda paralel işlemeye olanak tanır.
Asenkron bir görev oluşturmak için görevi tanımlarken `async_execution=True` ayarını yapın.

### Bellek ve Önbelleğe Alma

CrewAI hem bellek hem de önbelleğe alma özelliklerini destekler:

* **Bellek**: Ekibi (Crew) oluştururken `memory=True` ayarını yaparak etkinleştirin. Bu, temsilcilerin görevler arasında bilgileri tutmasına olanak tanır.
* **Önbelleğe Alma**: Varsayılan olarak önbelleğe alma etkindir. Devre dışı bırakmak için `cache=False` ayarını yapın.

### Geri Çağırmalar (Callbacks)

Hem görev hem de adım seviyesinde geri çağırmalar ayarlayabilirsiniz:

* `task_callback`: Her görev tamamlandıktan sonra yürütülür.
* `step_callback`: Bir temsilcinin yürütmesindeki her adımdan sonra yürütülür.

### Kullanım Metrikleri

CrewAI, tüm görevler ve temsilciler genelinde token kullanımını takip eder. Yürütmeden sonra bu metriklere erişebilirsiniz.

## Ardışık Süreçler İçin En İyi Uygulamalar

1. **Sıralama Önemlidir**: Görevleri, her görevin bir öncekine dayandığı mantıklı bir dizide düzenleyin.
2. **Net Görev Açıklamaları**: Temsilcileri etkili bir şekilde yönlendirmek için her görev için ayrıntılı açıklamalar sağlayın.
3. **Uygun Temsilci Seçimi**: Temsilcilerin becerilerini ve rollerini her görevin gereksinimleriyle eşleştirin.
4. **Bağlamı (Context) Kullanın**: Sonraki görevleri bilgilendirmek için önceki görevlerden gelen bağlamdan yararlanın.

Bu güncellenen dokümantasyon, ayrıntıların kod tabanındaki en son değişiklikleri doğru bir şekilde yansıtmasını sağlar ve yeni özelliklerin ve yapılandırmaların nasıl kullanılacağını açıkça tanımlar.
İçerik, kolay anlaşılmasını sağlamak için basit ve doğrudan tutulmuştur.
