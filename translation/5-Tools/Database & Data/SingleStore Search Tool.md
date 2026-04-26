> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# SingleStore Arama Aracı

> `SingleStoreSearchTool`, havuzlama desteğiyle SingleStore üzerinde SELECT/SHOW sorgularını güvenli şekilde çalıştırır.

# `SingleStoreSearchTool`

## Açıklama

Bağlantı havuzlama ve girdi doğrulama ile SingleStore üzerinde salt okunur (`SELECT`/`SHOW`) sorguları çalıştırır.

## Kurulum

```shell  theme={null}
uv add crewai-tools[singlestore]
```

## Ortam Değişkenleri

`SINGLESTOREDB_HOST`, `SINGLESTOREDB_USER`, `SINGLESTOREDB_PASSWORD` gibi değişkenler kullanılabilir; alternatif olarak tek bir DSN olarak `SINGLESTOREDB_URL` de kullanılabilir.

API anahtarını SingleStore panelinden oluşturun; [dokümantasyon burada](https://docs.singlestore.com/cloud/reference/management-api/#generate-an-api-key).

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import SingleStoreSearchTool

tool = SingleStoreSearchTool(
    tables=["products"], 
    host="host", 
    user="user", 
    password="pass", 
    database="db",
)

agent = Agent(
    role="Analist", 
    goal="SingleStore sorgula", 
    tools=[tool], 
    verbose=True,
)

task = Task(
    description="5 ürün listele", 
    expected_output="JSON/metin olarak 5 satır", 
    agent=agent,
)

crew = Crew(
    agents=[agent], 
    tasks=[task],
    verbose=True,
)

result = crew.kickoff()
```
