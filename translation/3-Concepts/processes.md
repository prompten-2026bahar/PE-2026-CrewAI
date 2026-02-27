# Süreçler
CrewAI'deki iş akışı yönetimini süreçler aracılığıyla ayrıntılı olarak anlatan kılavuz, güncellenmiş uygulama detaylarıyla.


## Genel Bakış


  Süreçler, agent'ların görevleri yürütmesini orkestre eder, insan ekiplerdeki proje yönetimine benzer şekilde. 
  Bu süreçler, önceden tanımlanmış bir stratejiyle uyumlu olarak görevlerin verimli bir şekilde dağıtılmasını ve yürütülmesini sağlar.


## Süreç Uygulamaları

- **Sıralı**: Görevleri sırayla yürütür, görevlerin düzenli bir ilerleme ile tamamlanmasını sağlar.
- **Hiyerarşik**: Görevleri bir yönetim hiyerarşisi içinde düzenler, görevlerin yapılandırılmış bir komuta zinciri üzerinde delege edildiği ve yürütüldüğü bir sistemdir. Hiyerarşik sürecin etkinleşmesi ve manager agent'ın görevleri oluşturmasını ve yönetmesini kolaylaştırmak için, ekibe bir manager language model (`manager_llm`) veya özel bir manager agent (`manager_agent`) belirtilmesi gerekir.
- **Konsensüel Süreç (Planlı)**: Görev yürütme konusunda agent'lar arasında işbirlikçi karar alma hedefleyen bu süreç türü, CrewAI içindeki görev yönetiminde demokratik bir yaklaşım sunar. Gelecekteki geliştirmeler için planlanmıştır ve şu anda kod tabanında uygulanmamıştır.

## Takım Çalışmasındaki Süreçlerin Rolü
Süreçler, bireysel agent'lerin uyumlu bir birim olarak çalışmasını sağlayarak, ortak hedeflere verimlilik ve tutarlılıkla ulaşmak için çabalarını kolaylaştırır.

## Bir Ekipe Süreç Atama
Bir süreci bir ekibe atamak için, yürütme stratejisini ayarlamak için ekip oluşturulurken süreç türünü belirtin. Hiyerarşik bir süreç için, manager agent için `manager_llm` veya `manager_agent` tanımladığınızdan emin olun.

```python
from crewai import Crew, Process

# Örnek: Sıralı bir süreçle bir ekip oluşturma
crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.sequential
)

# Örnek: Hiyerarşik bir süreçle bir ekip oluşturma
# Lütfen bir manager_llm veya manager_agent sağlayın
crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.hierarchical,
    manager_llm="gpt-4o"
    # veya
    # manager_agent=my_manager_agent
)
```
**Not:** `Crew` nesnesi oluşturulmadan önce `my_agents` ve `my_tasks`'in tanımlandığından ve hiyerarşik süreç için `manager_llm` veya `manager_agent`'in de belirtilmesi gerektiğinden emin olun.

## Sıralı Süreç

Bu yöntem, dinamik ekip iş akışlarını yansıtarak, düşünceli ve sistematik bir şekilde görevlerden geçer. Görev yürütme, görev listesindeki önceden tanımlanmış sırayı izler ve bir görevin çıktısı bir sonraki görev için bağlam görevi görür.

Görev bağlamını özelleştirmek için, bir sonraki görevler için bağlam olarak kullanılacak çıktıları belirtmek üzere `Task` sınıfındaki `context` parametresini kullanın.

## Hiyerarşik Süreç

Bir şirket hiyerarşisini taklit eder, CrewAI özel bir manager agent belirtmenize olanak tanır veya otomatik olarak bir tane oluşturur ve bunun için bir manager language model (`manager_llm`) belirtilmesi gerekir. Bu agent, görev yürütmesini, planlamayı, delege etmeyi ve doğrulamayı denetler. Görevler önceden atanmaz; manager, agent'ların yeteneklerine göre görevleri atar, çıktıları gözden geçirir ve görev tamamlama durumunu değerlendirir.

## Süreç Sınıfı: Ayrıntılı Genel Bakış

`Process` sınıfı, tür güvenliğini sağlamak ve süreç değerlerini tanımlanmış türlere (`sıralı`, `hiyerarşik`) kısıtlamak için bir numaralandırma (`Enum`) olarak uygulanmıştır. Konsensüel süreç, sürekli gelişim ve yeniliğe olan bağlılığımızı vurgulayarak gelecekteki eklemeler için planlanmıştır.

## Sonuç

CrewAI içindeki süreçler tarafından kolaylaştırılan yapılandırılmış işbirliği, agent'lar arasında sistematik takım çalışmasını etkinleştirmek için çok önemlidir. 
Bu dokümantasyon, en son özelliklere, geliştirmelere ve Konsensüel Sürecin planlanan entegrasyonuna yansıtılarak güncellenmiştir ve kullanıcıların en güncel ve kapsamlı bilgilere erişebilmelerini sağlamaktadır.