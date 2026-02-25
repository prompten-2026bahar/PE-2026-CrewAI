> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Özel Yönetici Ajan

> CrewAI'de özel bir ajanı yönetici olarak nasıl atayacağınızı ve görev yönetimi ile koordinasyon üzerinde daha fazla kontrol sahibi olacağınızı öğrenin.

# CrewAI'de Belirli Bir Ajanı Yönetici Olarak Atama

CrewAI, kullanıcıların belirli bir ajanı ekibin yöneticisi olarak atamasına imkân tanıyarak görevlerin yönetimi ve koordinasyonu üzerinde daha fazla kontrol sağlar.
Bu özellik, yönetici rolünün projenizin gereksinimlerine daha iyi uyacak şekilde özelleştirilmesini mümkün kılar.

## `manager_agent` Niteliğini Kullanma

### Özel Yönetici Ajan

`manager_agent` niteliği, ekibi yönetecek özel bir ajan tanımlamanızı sağlar. Bu ajan, görevlerin verimli biçimde ve en yüksek standartta tamamlanmasını sağlayarak tüm süreci denetler.

### Örnek

```python
import os
from crewai import Agent, Task, Crew, Process

# Ajanlarınızı tanımlayın
researcher = Agent(
    role="Researcher",
    goal="Yapay zeka ve yapay zeka ajanları üzerine kapsamlı araştırma ve analiz yap",
    backstory="Teknoloji, yazılım mühendisliği, yapay zeka ve girişimler konusunda uzmanlaşmış bir araştırmacısınız. Serbest çalışıyorsunuz ve şu anda yeni bir müşteri için araştırma yapıyorsunuz.",
    allow_delegation=False,
)

writer = Agent(
    role="Senior Writer",
    goal="Yapay zeka ve yapay zeka ajanları hakkında etkileyici içerikler oluştur",
    backstory="Teknoloji, yazılım mühendisliği, yapay zeka ve girişimler konusunda uzmanlaşmış kıdemli bir yazarsınız. Serbest çalışıyorsunuz ve şu anda yeni bir müşteri için içerik yazıyorsunuz.",
    allow_delegation=False,
)

# Görevinizi tanımlayın
task = Task(
    description="Bir makale için 5 ilginç fikir listesi oluşturun, ardından bu konuda tam bir makalenin potansiyelini ortaya koyan her fikir için bir etkileyici paragraf yazın. Fikirlerin notlarla birlikte paragraflarını içeren listeyi döndürün.",
    expected_output="Her biri bir paragraf ve ilgili notlar içeren 5 madde işareti.",
)

# Yönetici ajanı tanımlayın
manager = Agent(
    role="Project Manager",
    goal="Ekibi verimli şekilde yönet ve yüksek kaliteli görev tamamlanmasını sağla",
    backstory="Karmaşık projeleri yönetme ve ekipleri başarıya yönlendirme konusunda deneyimli bir proje yöneticisisiniz. Rolünüz, ekip üyelerinin çabalarını koordine etmek; her görevin zamanında ve en yüksek standartta tamamlanmasını sağlamaktır.",
    allow_delegation=True,
)

# Özel yöneticiyle ekibinizi oluşturun
crew = Crew(
    agents=[researcher, writer],
    tasks=[task],
    manager_agent=manager,
    process=Process.hierarchical,
)

# Ekibin çalışmasını başlatın
result = crew.kickoff()
```

## Özel Yönetici Ajanın Faydaları

- **Gelişmiş Kontrol**: Yönetim yaklaşımını projenizin özel ihtiyaçlarına göre uyarlayın.
- **İyileştirilmiş Koordinasyon**: Deneyimli bir ajan aracılığıyla verimli görev koordinasyonu ve yönetimi sağlayın.
- **Özelleştirilebilir Yönetim**: Projenizin hedefleriyle örtüşen yönetici rol ve sorumlulukları tanımlayın.

## Yönetici LLM Ayarlama

Hiyerarşik süreci kullanıyor ancak özel bir yönetici ajan atamak istemiyorsanız, yönetici için dil modelini belirtebilirsiniz:

```python
from crewai import LLM

manager_llm = LLM(model="gpt-4o")

crew = Crew(
    agents=[researcher, writer],
    tasks=[task],
    process=Process.hierarchical,
    manager_llm=manager_llm
)
```

> **Not:** Hiyerarşik süreç kullanıldığında `manager_agent` veya `manager_llm`'den biri mutlaka ayarlanmalıdır.
