# S3 Yazma Aracı (S3 Writer Tool)

> `S3WriterTool`, CrewAI ajanlarının Amazon S3 bucket'larındaki dosyalara içerik yazmasını sağlar.

# `S3WriterTool`

## Açıklama

`S3WriterTool`, Amazon S3 bucket'larındaki dosyalara içerik yazmak için tasarlanmıştır. Bu araç, CrewAI ajanlarının S3'te dosyalar oluşturmasına veya güncellemesine olanak tanıyarak; veri depolama, yapılandırma dosyalarını kaydetme veya AWS S3 depolama biriminde içerik kalıcılığı sağlama gerektiren iş akışları için ideal bir çözüm sunar.

## Kurulum

Bu aracı kullanmak için gerekli bağımlılıkları yüklemeniz gerekir:

```shell  theme={null}
uv add boto3
```

## Başlangıç Adımları

`S3WriterTool`'u etkili bir şekilde kullanmak için şu adımları izleyin:

1. **Bağımlılıkları Kurun**: Yukarıdaki komutu kullanarak gerekli paketleri yükleyin.
2. **AWS Kimlik Bilgilerini Yapılandırın**: AWS kimlik bilgilerinizi ortam değişkeni (environment variable) olarak ayarlayın.
3. **Aracı Başlatın**: Aracın bir örneğini oluşturun.
4. **S3 Yolunu ve İçeriği Belirtin**: Dosyayı yazmak istediğiniz S3 yolunu ve yazılacak içeriği sağlayın.

## Örnek

Aşağıdaki örnek, bir S3 bucket'ındaki dosyaya içerik yazmak için `S3WriterTool`'un nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.s3 import S3WriterTool

# Aracı başlatın
s3_writer_tool = S3WriterTool()

# Aracı kullanan bir ajan tanımlayın
file_writer_agent = Agent(
    role="Dosya Yazıcı",
    goal="S3 bucket'larındaki dosyalara içerik yaz",
    backstory="Bulut depolama birimlerinde dosya saklama ve yönetme konusunda uzman.",
    tools=[s3_writer_tool],
    verbose=True,
)

# Rapor yazma görevi örneği
write_task = Task(
    description="Üç aylık satış verilerinin bir özet raporunu oluştur ve {my_bucket} adresine kaydet.",
    expected_output="Raporun S3'e başarıyla kaydedildiğine dair onay.",
    agent=file_writer_agent,
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(agents=[file_writer_agent], tasks=[write_task])
result = crew.kickoff(inputs={"my_bucket": "s3://bucket-adim/reports/quarterly-summary.txt"})
```

## Parametreler

`S3WriterTool`, bir ajan tarafından kullanıldığında şu parametreleri kabul eder:

* **file\_path**: Zorunlu. `s3://bucket-adi/dosya-adi` formatındaki S3 dosya yolu.
* **content**: Zorunlu. Dosyaya yazılacak içerik.

## AWS Kimlik Bilgileri

Aracın S3 bucket'larına erişmesi için AWS kimlik bilgileri gereklidir. Bu bilgileri ortam değişkenlerini kullanarak yapılandırabilirsiniz:

* **CREW\_AWS\_REGION**: S3 bucket'ınızın bulunduğu AWS bölgesi (region). Varsayılan: `us-east-1`.
* **CREW\_AWS\_ACCESS\_KEY\_ID**: AWS erişim anahtarı ID'niz (access key ID).
* **CREW\_AWS\_SEC\_ACCESS\_KEY**: AWS gizli erişim anahtarınız (secret access key).

## Kullanım

`S3WriterTool` bir ajanla kullanıldığında, ajanın hem S3 dosya yolunu hem de yazılacak içeriği sağlaması gerekecektir:

```python Code theme={null}
# Aracın bir ajanla kullanım örneği
file_writer_agent = Agent(
    role="Dosya Yazıcı",
    goal="S3 bucket'larındaki dosyalara içerik yaz",
    backstory="Bulut depolama birimlerinde dosya saklama ve yönetme konusunda uzman.",
    tools=[s3_writer_tool],
    verbose=True,
)

# Ajan için belirli bir dosyayı yazma görevi oluşturun
write_config_task = Task(
    description="""
    Aşağıdaki veritabanı ayarlarına sahip bir yapılandırma dosyası oluştur:
    - host: db.example.com
    - port: 5432
    - username: app_user
    - password: secure_password
    
    Bu yapılandırmayı JSON olarak {my_bucket} adresine kaydet.
    """,
    expected_output="Yapılandırma dosyasının S3'e başarıyla kaydedildiğine dair onay.",
    agent=file_writer_agent,
)

# Görevi çalıştırın
crew = Crew(agents=[file_writer_agent], tasks=[write_config_task])
result = crew.kickoff(inputs={"my_bucket": "s3://bucket-adim/config/db-config.json"})
```

## Hata Yönetimi

`S3WriterTool`, yaygın S3 sorunları için hata yönetimi içerir:

* Geçersiz S3 yolu formatı
* İzin sorunları (örn. bucket'a yazma erişiminin olmaması)
* AWS kimlik bilgisi sorunları
* Bucket'ın mevcut olmaması

Bir hata oluştuğunda araç, sorunla ilgili ayrıntıları içeren bir hata mesajı döndürür.

## Uygulama Detayları

`S3WriterTool`, S3 ile etkileşim kurmak için Python için AWS SDK'sını (boto3) kullanır:

```python Code theme={null}
class S3WriterTool(BaseTool):
    name: str = "S3 Writer Tool"
    description: str = "Verilen S3 dosya yoluna göre Amazon S3'teki bir dosyaya içerik yazar"
    
    def _run(self, file_path: str, content: str) -> str:
        try:
            bucket_name, object_key = self._parse_s3_path(file_path)

            s3 = boto3.client(
                's3',
                region_name=os.getenv('CREW_AWS_REGION', 'us-east-1'),
                aws_access_key_id=os.getenv('CREW_AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('CREW_AWS_SEC_ACCESS_KEY')
            )

            s3.put_object(Bucket=bucket_name, Key=object_key, Body=content.encode('utf-8'))
            return f"İçerik başarıyla {file_path} adresine yazıldı."
        except ClientError as e:
            return f"S3'e dosya yazılırken hata oluştu: {str(e)}"
```

## Sonuç

`S3WriterTool`, Amazon S3 bucket'larındaki dosyalara içerik yazmak için basit bir yol sunar. Ajanların S3'te dosyalar oluşturmasını ve güncellemesini sağlayarak, bulut tabanlı dosya depolama gerektiren iş akışlarını kolaylaştırır. Bu araç; veri kalıcılığı, yapılandırma yönetimi, rapor oluşturma ve AWS S3 depolama biriminde bilgi saklamayı içeren her türlü görev için özellikle yararlıdır.
