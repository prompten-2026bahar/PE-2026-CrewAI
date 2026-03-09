# S3 Okuma Aracı (S3 Reader Tool)

> `S3ReaderTool`, CrewAI ajanlarının Amazon S3 bucket'larından dosya okumasını sağlar.

# `S3ReaderTool`

## Açıklama

`S3ReaderTool`, Amazon S3 bucket'larından dosya okumak için tasarlanmıştır. Bu araç, CrewAI ajanlarının S3'te depolanan içeriğe erişmesine ve geri çağırmasına olanak tanıyarak; veri okuma, yapılandırma dosyaları veya AWS S3 depolama biriminde saklanan diğer içeriklerin okunmasını gerektiren iş akışları için ideal bir çözüm sunar.

## Kurulum

Bu aracı kullanmak için gerekli bağımlılıkları yüklemeniz gerekir:

```shell  theme={null}
uv add boto3
```

## Başlangıç Adımları

`S3ReaderTool`'u etkili bir şekilde kullanmak için şu adımları izleyin:

1. **Bağımlılıkları Kurun**: Yukarıdaki komutu kullanarak gerekli paketleri yükleyin.
2. **AWS Kimlik Bilgilerini Yapılandırın**: AWS kimlik bilgilerinizi ortam değişkeni (environment variable) olarak ayarlayın.
3. **Aracı Başlatın**: Aracın bir örneğini oluşturun.
4. **S3 Yolunu Belirtin**: Okumak istediğiniz dosyanın S3 yolunu sağlayın.

## Örnek

Aşağıdaki örnek, bir S3 bucket'ından dosya okumak için `S3ReaderTool`'un nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.s3 import S3ReaderTool

# Aracı başlatın
s3_reader_tool = S3ReaderTool()

# Aracı kullanan bir ajan tanımlayın
file_reader_agent = Agent(
    role="Dosya Okuyucu",
    goal="S3 bucket'larından dosya oku",
    backstory="Bulut depolama birimlerinden dosya getirme ve işleme konusunda uzman.",
    tools=[s3_reader_tool],
    verbose=True,
)

# Yapılandırma dosyasını okuma görevi örneği
read_task = Task(
    description="{my_bucket} içindeki yapılandırma dosyasını oku ve içeriğini özetle.",
    expected_output="Yapılandırma dosyası içeriğinin bir özeti.",
    agent=file_reader_agent,
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(agents=[file_reader_agent], tasks=[read_task])
result = crew.kickoff(inputs={"my_bucket": "s3://bucket-adim/config/app-config.json"})
```

## Parametreler

`S3ReaderTool`, bir ajan tarafından kullanıldığında şu parametreyi kabul eder:

* **file\_path**: Zorunlu. `s3://bucket-adi/dosya-adi` formatındaki S3 dosya yolu.

## AWS Kimlik Bilgileri

Aracın S3 bucket'larına erişmesi için AWS kimlik bilgileri gereklidir. Bu bilgileri ortam değişkenlerini kullanarak yapılandırabilirsiniz:

* **CREW\_AWS\_REGION**: S3 bucket'ınızın bulunduğu AWS bölgesi (region). Varsayılan: `us-east-1`.
* **CREW\_AWS\_ACCESS\_KEY\_ID**: AWS erişim anahtarı ID'niz (access key ID).
* **CREW\_AWS\_SEC\_ACCESS\_KEY**: AWS gizli erişim anahtarınız (secret access key).

## Kullanım

`S3ReaderTool` bir ajanla kullanıldığında, ajanın S3 dosya yolunu sağlaması gerekecektir:

```python Code theme={null}
# Aracın bir ajanla kullanım örneği
file_reader_agent = Agent(
    role="Dosya Okuyucu",
    goal="S3 bucket'larından dosya oku",
    backstory="Bulut depolama birimlerinden dosya getirme ve işleme konusunda uzman.",
    tools=[s3_reader_tool],
    verbose=True,
)

# Ajan için belirli bir dosyayı okuma görevi oluşturun
read_config_task = Task(
    description="{my_bucket} adresindeki uygulama yapılandırma dosyasını oku ve veritabanı bağlantı ayarlarını ayıkla.",
    expected_output="Yapılandırma dosyasındaki veritabanı bağlantı ayarları.",
    agent=file_reader_agent,
)

# Görevi çalıştırın
crew = Crew(agents=[file_reader_agent], tasks=[read_config_task])
result = crew.kickoff(inputs={"my_bucket": "s3://bucket-adim/config/app-config.json"})
```

## Hata Yönetimi

`S3ReaderTool`, yaygın S3 sorunları için hata yönetimi içerir:

* Geçersiz S3 yolu formatı
* Eksik veya erişilemeyen dosyalar
* İzin (permission) sorunları
* AWS kimlik bilgisi sorunları

Bir hata oluştuğunda araç, sorunla ilgili ayrıntıları içeren bir hata mesajı döndürür.

## Uygulama Detayları

`S3ReaderTool`, S3 ile etkileşim kurmak için Python için AWS SDK'sını (boto3) kullanır:

```python Code theme={null}
class S3ReaderTool(BaseTool):
    name: str = "S3 Reader Tool"
    description: str = "Verilen S3 dosya yoluna göre Amazon S3'ten bir dosya okur"
    
    def _run(self, file_path: str) -> str:
        try:
            bucket_name, object_key = self._parse_s3_path(file_path)

            s3 = boto3.client(
                's3',
                region_name=os.getenv('CREW_AWS_REGION', 'us-east-1'),
                aws_access_key_id=os.getenv('CREW_AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('CREW_AWS_SEC_ACCESS_KEY')
            )

            # S3'ten dosya içeriğini oku
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            file_content = response['Body'].read().decode('utf-8')

            return file_content
        except ClientError as e:
            return f"S3'ten dosya okunurken hata oluştu: {str(e)}"
```

## Sonuç

`S3ReaderTool`, Amazon S3 bucket'larından dosya okumak için basit bir yol sunar. Ajanların S3'te depolanan içeriğe erişmesini sağlayarak, bulut tabanlı dosya erişimi gerektiren iş akışlarını kolaylaştırır. Bu araç; veri işleme, yapılandırma yönetimi ve AWS S3 depolama biriminden bilgi getirmeyi içeren her türlü görev için özellikle yararlıdır.
