# AI Mind Aracı

> `AIMindTool`, veri kaynaklarını doğal dilde sorgulamak için tasarlanmıştır.

# `AIMindTool`

## Açıklama

`AIMindTool`, [MindsDB](https://mindsdb.com/) tarafından sağlanan [AI-Minds](https://mindsdb.com/minds) için bir sarmalayıcıdır (wrapper). Sadece bağlantı parametrelerini yapılandırarak veri kaynaklarını doğal dilde sorgulamanıza olanak tanır. Bu araç; PostgreSQL, MySQL, MariaDB, ClickHouse, Snowflake ve Google BigQuery dahil olmak üzere çeşitli veri kaynaklarında depolanan verilerinizden sorulara yanıt almanız gerektiğinde kullanışlıdır.

Zihinler (Minds), Büyük Dil Modellerine (LLM'ler) benzer şekilde çalışan ancak herhangi bir veriden herhangi bir soruyu yanıtlayarak daha ileri giden yapay zeka sistemleridir. Bu, şu şekilde gerçekleştirilir:

* Parametrik arama kullanarak bir cevap için en ilgili verileri seçmek
* Anlamsal (semantic) arama yoluyla anlamı anlamak ve doğru bağlam içinde yanıtlar sağlamak
* Verileri analiz ederek ve makine öğrenimi (ML) modellerini kullanarak kesin yanıtlar sunmak

## Kurulum

Bu aracı projenize dahil etmek için Minds SDK'yı yüklemeniz gerekir:

```shell  theme={null}
uv add minds-sdk
```

## Başlangıç Adımları

`AIMindTool`'u etkili bir şekilde kullanmak için şu adımları izleyin:

1. **Paket Kurulumu**: `crewai[tools]` ve `minds-sdk` paketlerinin Python ortamınızda kurulu olduğundan emin olun.
2. **API Anahtarı Edinme**: [Buradan](https://mdb.ai/register) bir Minds hesabı oluşturun ve bir API anahtarı alın.
3. **Ortam Yapılandırması**: Aldığınız API anahtarını, aracın kullanımı kolaylaştırmak için `MINDS_API_KEY` adlı bir ortam değişkeninde saklayın.

## Örnek

Aşağıdaki örnek, aracın nasıl başlatılacağını ve bir sorgunun nasıl yürütüleceğini gösterir:

```python Code theme={null}
from crewai_tools import AIMindTool

# AIMindTool'u başlatın
aimind_tool = AIMindTool(
    datasources=[
        {
            "description": "ev satış verileri",
            "engine": "postgres",
            "connection_data": {
                "user": "demo_user",
                "password": "demo_password",
                "host": "samples.mindsdb.com",
                "port": 5432,
                "database": "demo",
                "schema": "demo_data"
            },
            "tables": ["house_sales"]
        }
    ]
)

# Doğal dilde bir sorgu çalıştırın
result = aimind_tool.run("2008 yılında kaç tane 3 yatak odalı ev satıldı?")
print(result)
```

## Parametreler

`AIMindTool` aşağıdaki parametreleri kabul eder:

* **api\_key**: Opsiyonel. Minds API anahtarınız. Sağlanmazsa, `MINDS_API_KEY` ortam değişkeninden okunacaktır.
* **datasources**: Her biri aşağıdaki anahtarları içeren bir sözlük listesi:
  * **description**: Veri kaynağında bulunan verilerin açıklaması.
  * **engine**: Veri kaynağının motoru (veya türü).
  * **connection\_data**: Veri kaynağı için bağlantı parametrelerini içeren bir sözlük.
  * **tables**: Veri kaynağının kullanacağı tabloların listesi. Bu opsiyoneldir ve veri kaynağındaki tüm tablolar kullanılacaksa atlanabilir.

Desteklenen veri kaynaklarının ve bağlantı parametrelerinin listesine [buradan](https://docs.mdb.ai/docs/data_sources) ulaşabilirsiniz.

## Ajan Entegrasyon Örneği

`AIMindTool`'u bir CrewAI ajanıyla nasıl entegre edeceğiniz aşağıda açıklanmıştır:

```python Code theme={null}
from crewai import Agent
from crewai.project import agent
from crewai_tools import AIMindTool

# Aracı başlatın
aimind_tool = AIMindTool(
    datasources=[
        {
            "description": "satış verileri",
            "engine": "postgres",
            "connection_data": {
                "user": "your_user",
                "password": "your_password",
                "host": "your_host",
                "port": 5432,
                "database": "your_db",
                "schema": "your_schema"
            },
            "tables": ["sales"]
        }
    ]
)

# AIMindTool ile bir ajan tanımlayın
@agent
def data_analyst(self) -> Agent:
    return Agent(
        config=self.agents_config["data_analyst"],
        allow_delegation=False,
        tools=[aimind_tool]
    )
```

## Sonuç

`AIMindTool`, karmaşık SQL sorguları yazmaya gerek kalmadan içgörüleri ayıklamayı kolaylaştırarak veri kaynaklarınızı doğal dilde sorgulamanın güçlü bir yolunu sunar. Çeşitli veri kaynaklarına bağlanarak ve AI-Minds teknolojisinden yararlanarak, bu araç ajanların verilere verimli bir şekilde erişmesini ve bunları analiz etmesini sağlar.
