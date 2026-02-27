# Parmak İzi
CrewAI'nin parmak izi sistemini kullanarak bileşenleri yaşam döngüleri boyunca benzersiz olarak tanımlamayı ve izlemeyi öğrenin.


## Genel Bakış

CrewAI'deki parmak izleri, bileşenleri yaşam döngüleri boyunca benzersiz olarak tanımlamanın ve izlemenin bir yolunu sağlar. Her `Agent`, `Crew` ve `Task` oluşturulduğunda otomatik olarak benzersiz bir parmak izi alır ve bu parmak izi manuel olarak geçersiz kılınamaz.

Bu parmak izleri şunlar için kullanılabilir:
- Bileşen kullanımını denetleme ve izleme
- Bileşen kimlik bütünlüğünü sağlama
- Bileşenlere meta veri ekleme
- İzlenebilir bir işlem zinciri oluşturma

## Parmak İzleri Nasıl Çalışır

Bir parmak izi, `crewai.security` modülündeki `Fingerprint` sınıfının bir örneğidir. Her parmak izi şunları içerir:

- Bir UUID dizesi: Otomatik olarak oluşturulan ve manuel olarak ayarlanamayan bileşen için benzersiz bir tanımlayıcı
- Oluşturma zaman damgası: Parmak izinin oluşturulduğu zaman, otomatik olarak ayarlanır ve manuel olarak değiştirilemez
- Meta veri: Özelleştirilebilen ek bilgiler sözlüğü

Parmak izleri, bir bileşen oluşturulduğunda otomatik olarak oluşturulur ve atanır. Her bileşen, salt okunur bir özellik aracılığıyla parmak izini açığa çıkarır.

## Temel Kullanım

### Parmak İzlerine Erişme

```python
from crewai import Agent, Crew, Task

# Bileşenleri oluşturun - parmak izleri otomatik olarak oluşturulur
agent = Agent(
    role="Veri Bilimcisi",
    goal="Veriyi analiz et",
    backstory="Veri analizinde uzman"
)

crew = Crew(
    agents=[agent],
    tasks=[]
)

task = Task(
    description="Müşteri verisini analiz et",
    expected_output="Veri analizinden elde edilen bilgiler",
    agent=agent
)

# Parmak izlerine erişin
agent_fingerprint = agent.fingerprint
crew_fingerprint = crew.fingerprint
task_fingerprint = task.fingerprint

# UUID dizesini yazdırın
print(f"Agent parmak izi: {agent_fingerprint.uuid_str}")
print(f"Crew parmak izi: {crew_fingerprint.uuid_str}")
print(f"Task parmak izi: {task_fingerprint.uuid_str}")
```

### Parmak İzi Meta Verileriyle Çalışma

Ek bağlam için parmak izlerine meta veri ekleyebilirsiniz:

```python
# Agent'ın parmak izine meta veri ekleyin
agent.security_config.fingerprint.metadata = {
    "version": "1.0",
    "department": "Veri Bilimi",
    "project": "Müşteri Analizi"
}

# Meta verilere erişin
print(f"Agent meta verisi: {agent.fingerprint.metadata}")
```

## Parmak İzi Kalıcılığı

Parmak izleri, bir bileşenin yaşam döngüsü boyunca kalıcı olacak ve değişmemek üzere tasarlanmıştır. Bir bileşeni değiştirdiğinizde, parmak izi aynı kalır:

```python
original_fingerprint = agent.fingerprint.uuid_str

# Agent'ı değiştirin
agent.goal = "Analiz için yeni hedef"

# Parmak izi aynı kalır
assert agent.fingerprint.uuid_str == original_fingerprint
```

## Belirli Parmak İzleri

UUID ve oluşturma zaman damgasını doğrudan ayarlayamazsanız, bir tohum kullanarak deterministik parmak izleri oluşturabilirsiniz:

```python
from crewai.security import Fingerprint

# Bir tohum dizesi kullanarak deterministik bir parmak izi oluşturun
deterministic_fingerprint = Fingerprint.generate(seed="my-agent-id")

# Aynı tohum her zaman aynı parmak izini üretir
same_fingerprint = Fingerprint.generate(seed="my-agent-id")
assert deterministic_fingerprint.uuid_str == same_fingerprint.uuid_str

# Ayrıca meta veriyi ayarlayabilirsiniz
custom_fingerprint = Fingerprint.generate(
    seed="my-agent-id",
    metadata={"version": "1.0"}
)
```

## Gelişmiş Kullanım

### Parmak İzi Yapısı

Her parmak izinin aşağıdaki yapıya sahip olması:

```python
from crewai.security import Fingerprint

fingerprint = agent.fingerprint

# UUID dizesi - benzersiz tanımlayıcı (otomatik olarak oluşturulur)
uuid_str = fingerprint.uuid_str  # örn., "123e4567-e89b-12d3-a456-426614174000"

# Oluşturma zaman damgası (otomatik olarak oluşturulur)
created_at = fingerprint.created_at  # Bir datetime nesnesi

# Meta veri - ek bilgiler için (özelleştirilebilir)
metadata = fingerprint.metadata  # Bir sözlük, varsayılan olarak {}
```