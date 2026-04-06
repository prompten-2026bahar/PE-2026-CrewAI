> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Databricks SQL Sorgu Aracı

> `DatabricksQueryTool`, Databricks çalışma alanı tablolarına karşı SQL sorguları yürütür.

# `DatabricksQueryTool`

## Açıklama

CLI profili veya doğrudan host/token kimlik doğrulaması ile Databricks çalışma alanı tablolarına karşı SQL çalıştırın.

## Kurulum

```shell  theme={null}
uv add crewai-tools[databricks-sdk]
```

## Ortam Değişkenleri

* `DATABRICKS_CONFIG_PROFILE` veya (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`)

Kişisel bir erişim jetonu oluşturun ve Databricks çalışma alanında Kullanıcı Ayarları → Geliştirici altında ana bilgisayar ayrıntılarını bulun.
Dokümanlar: [https://docs.databricks.com/en/dev-tools/auth/pat.html](https://docs.databricks.com/en/dev-tools/auth/pat.html)

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import DatabricksQueryTool

tool = DatabricksQueryTool(
    default_catalog="main", 
    default_schema="default",
)

agent = Agent(
    role="Data Analyst",
    goal="Query Databricks",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="SELECT * FROM my_table LIMIT 10",
    expected_output="10 rows", 
    agent=agent,
)

crew = Crew(
    agents=[agent], 
    tasks=[task],
    verbose=True,
)
result = crew.kickoff()

print(result)
```

## Parametreler

* `query` (gerekli): Yürütülecek SQL sorgusu
* `catalog` (isteğe bağlı): Varsayılan kataloğu geçersiz kıl
* `db_schema` (isteğe bağlı): Varsayılan şemayı geçersiz kıl
* `warehouse_id` (isteğe bağlı): Varsayılan SQL ambarını geçersiz kıl
* `row_limit` (isteğe bağlı): Döndürülecek maksimum satırlar (varsayılan: 1000)

## Başlangıçtaki Varsayılanlar

* `default_catalog`
* `default_schema`
* `default_warehouse_id`

### Hata işleme ve ipuçları

* Kimlik doğrulama hataları: `DATABRICKS_HOST` öğesinin `https://` ile başladığını ve jetonun geçerli olduğunu doğrulayın.
* İzinler: SQL ambarınız ve şemanız jetonunuz tarafından erişilebilir olduğundan emin olun.
* Limitler: uzun süreli sorguların ajan döngülerinde kaçınılması gerekir; filtreler/limitler ekleyin.
