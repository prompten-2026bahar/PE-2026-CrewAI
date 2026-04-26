> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Snowflake Arama Aracı

> `SnowflakeSearchTool`, CrewAI ajanlarının SQL sorguları çalıştırmasını ve Snowflake veri ambarlarında anlamsal arama yapmasını sağlar.

# `SnowflakeSearchTool`

## Açıklama

`SnowflakeSearchTool`, Snowflake veri ambarlarına bağlanmak ve bağlantı havuzlama, yeniden deneme mantığı ve eşzamansız çalıştırma gibi gelişmiş özelliklerle SQL sorguları yürütmek için tasarlanmıştır. Bu araç, CrewAI ajanlarının Snowflake veritabanlarıyla etkileşime girmesine olanak tanır; bu da onu Snowflake'te saklanan kurumsal verilere erişim gerektiren veri analizi, raporlama ve iş zekası görevleri için ideal hale getirir.

## Kurulum

Bu aracı kullanmak için gerekli bağımlılıkları kurmanız gerekir:

```shell  theme={null}
uv add cryptography snowflake-connector-python snowflake-sqlalchemy
```

Alternatif olarak:

```shell  theme={null}
uv sync --extra snowflake
```

## Başlamak İçin Adımlar

`SnowflakeSearchTool` aracını etkili şekilde kullanmak için şu adımları izleyin:

1. **Bağımlılıkları Kurun**: Gerekli paketleri yukarıdaki komutlardan biriyle kurun.
2. **Snowflake Bağlantısını Yapılandırın**: Snowflake kimlik bilgilerinizle bir `SnowflakeConfig` nesnesi oluşturun.
3. **Aracı Başlatın**: Gerekli yapılandırmayla aracın bir örneğini oluşturun.
4. **Sorguları Çalıştırın**: Aracı kullanarak Snowflake veritabanınıza karşı SQL sorguları çalıştırın.

## Örnek

Aşağıdaki örnek, `SnowflakeSearchTool` aracının bir Snowflake veritabanından veri sorgulamak için nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import SnowflakeSearchTool, SnowflakeConfig

# Snowflake yapılandırması oluştur
config = SnowflakeConfig(
    account="your_account",
    user="your_username",
    password="your_password",
    warehouse="COMPUTE_WH",
    database="your_database",
    snowflake_schema="your_schema"
)

# Aracı başlat
snowflake_tool = SnowflakeSearchTool(config=config)

# Aracı kullanan bir ajan tanımla
data_analyst_agent = Agent(
    role="Veri Analisti",
    goal="Snowflake veritabanındaki verileri analiz et",
    backstory="Kurumsal verilerden içgörü çıkarabilen uzman bir veri analisti.",
    tools=[snowflake_tool],
    verbose=True,
)

# Satış verisini sorgulamak için örnek görev
query_task = Task(
    description="Son çeyreğe ait satış verisini sorgula ve gelire göre ilk 5 ürünü özetle.",
    expected_output="Son çeyrekte gelire göre ilk 5 ürünün özeti.",
    agent=data_analyst_agent,
)

# Ekibi oluştur ve çalıştır
crew = Crew(agents=[data_analyst_agent], 
            tasks=[query_task])
result = crew.kickoff()
```

Aracı ek parametrelerle de özelleştirebilirsiniz:

```python Code theme={null}
# Aracı özel parametrelerle başlat
snowflake_tool = SnowflakeSearchTool(
    config=config,
    pool_size=10,
    max_retries=5,
    retry_delay=2.0,
    enable_caching=True
)
```

## Parametreler

### SnowflakeConfig Parametreleri

`SnowflakeConfig` sınıfı şu parametreleri kabul eder:

* **account**: Gerekli. Snowflake hesap tanımlayıcısı.
* **user**: Gerekli. Snowflake kullanıcı adı.
* **password**: İsteğe bağlı\*. Snowflake parolası.
* **private\_key\_path**: İsteğe bağlı\*. Özel anahtar dosyasının yolu (parolaya alternatif).
* **warehouse**: Gerekli. Snowflake warehouse adı.
* **database**: Gerekli. Varsayılan veritabanı.
* **snowflake\_schema**: Gerekli. Varsayılan şema.
* **role**: İsteğe bağlı. Snowflake rolü.
* **session\_parameters**: İsteğe bağlı. Sözlük olarak özel oturum parametreleri.

\*`password` veya `private_key_path` değerlerinden biri mutlaka verilmelidir.

### SnowflakeSearchTool Parametreleri

`SnowflakeSearchTool`, başlatma sırasında şu parametreleri kabul eder:

* **config**: Gerekli. Bağlantı ayrıntılarını içeren bir `SnowflakeConfig` nesnesi.
* **pool\_size**: İsteğe bağlı. Havuzdaki bağlantı sayısı. Varsayılan 5.
* **max\_retries**: İsteğe bağlı. Başarısız sorgular için maksimum yeniden deneme sayısı. Varsayılan 3.
* **retry\_delay**: İsteğe bağlı. Yeniden denemeler arasındaki saniye cinsinden gecikme. Varsayılan 1.0.
* **enable\_caching**: İsteğe bağlı. Sorgu sonuç önbelleğinin etkinleştirilip etkinleştirilmeyeceği. Varsayılan True.

## Kullanım

`SnowflakeSearchTool` kullanılırken aşağıdaki parametreleri sağlamanız gerekir:

* **query**: Gerekli. Çalıştırılacak SQL sorgusu.
* **database**: İsteğe bağlı. Yapılandırmada belirtilen varsayılan veritabanını geçersiz kılar.
* **snowflake\_schema**: İsteğe bağlı. Yapılandırmada belirtilen varsayılan şemayı geçersiz kılar.
* **timeout**: İsteğe bağlı. Sorgu zaman aşımı, saniye cinsinden. Varsayılan 300.

Araç, sorgu sonuçlarını; her sözlüğün sütun adlarını anahtar olarak kullanan bir satırı temsil ettiği sözlükler listesi olarak döndürür.

```python Code theme={null}
# Aracın bir ajan ile kullanım örneği
data_analyst = Agent(
    role="Veri Analisti",
    goal="Snowflake üzerindeki satış verisini analiz et",
    backstory="SQL ve veri görselleştirme deneyimine sahip uzman veri analisti.",
    tools=[snowflake_tool],
    verbose=True
)

# Ajan aracı şu tür parametrelerle kullanacaktır:
# query="SELECT product_name, SUM(revenue) as total_revenue FROM sales GROUP BY product_name ORDER BY total_revenue DESC LIMIT 5"
# timeout=600

# Ajan için bir görev oluştur
analysis_task = Task(
    description="Satış veritabanını sorgula ve son çeyrekte gelire göre ilk 5 ürünü belirle.",
    expected_output="Gelire göre ilk 5 ürünün ayrıntılı analizi.",
    agent=data_analyst
)

# Görevi çalıştır
crew = Crew(
    agents=[data_analyst], 
    tasks=[analysis_task]
)
result = crew.kickoff()
```

## Gelişmiş Özellikler

### Bağlantı Havuzlama

`SnowflakeSearchTool`, veritabanı bağlantılarını yeniden kullanarak performansı artırmak için bağlantı havuzlama uygular. Havuz boyutunu `pool_size` parametresi ile kontrol edebilirsiniz.

### Otomatik Yeniden Denemeler

Araç, başarısız sorguları exponential backoff ile otomatik olarak yeniden dener. Yeniden deneme davranışını `max_retries` ve `retry_delay` parametreleriyle yapılandırabilirsiniz.

### Sorgu Sonucu Önbellekleme

Yinelenen sorgular için performansı artırmak amacıyla araç sorgu sonuçlarını önbelleğe alabilir. Bu özellik varsayılan olarak etkindir ancak `enable_caching=False` ayarlanarak kapatılabilir.

### Anahtar Çifti ile Kimlik Doğrulama

Parola ile kimlik doğrulamaya ek olarak araç, artırılmış güvenlik için anahtar çifti ile kimlik doğrulamayı destekler:

```python Code theme={null}
config = SnowflakeConfig(
    account="your_account",
    user="your_username",
    private_key_path="/path/to/your/private/key.p8",
    warehouse="COMPUTE_WH",
    database="your_database",
    snowflake_schema="your_schema"
)
```

## Hata Yönetimi

`SnowflakeSearchTool`, yaygın Snowflake sorunları için kapsamlı hata yönetimi içerir:

* Bağlantı hataları
* Sorgu zaman aşımı
* Kimlik doğrulama hataları
* Veritabanı ve şema hataları

Bir hata oluştuğunda araç işlemi yeniden denemeye çalışır (yapılandırılmışsa) ve ayrıntılı hata bilgisi sağlar.

## Sonuç

`SnowflakeSearchTool`, Snowflake veri ambarlarını CrewAI ajanlarıyla entegre etmek için güçlü bir yol sunar. Bağlantı havuzlama, otomatik yeniden deneme ve sorgu önbellekleme gibi özelliklerle kurumsal verilere verimli ve güvenilir erişim sağlar. Bu araç, özellikle Snowflake'te saklanan yapılandırılmış verilere erişim gerektiren veri analizi, raporlama ve iş zekası görevlerinde kullanışlıdır.
