# Dosyalar
 Görüntü, PDF, ses, video ve metin dosyalarını çoklu modal işleme için agent'larınıza iletin.


## Genel Bakış

CrewAI, yerel çoklu modal dosya girişlerini destekler, bu sayede görüntü, PDF, ses, video ve metin dosyalarını doğrudan agent'larınıza iletebilirsiniz. Dosyalar, LLM sağlayıcısının API gereksinimleri için otomatik olarak biçimlendirilir.


Dosya işleme desteği, isteğe bağlı `crewai-files` paketini gerektirir. Bunu şu şekilde yükleyin:

```bash
uv add 'crewai[file-processing]'
```



Dosya işleme API'si şu anda erken erişimdedir.


## Dosya Türleri

CrewAI, otomatik tür algılama özelliğine sahip genel bir `File` sınıfı ile birlikte beş belirli dosya türünü destekler:

| Tür | Sınıf | Kullanım Alanları |
|:-----|:------|:----------|
| **Görüntü** | `ImageFile` | Fotoğraflar, ekran görüntüleri, şemalar, grafikler |
| **PDF** | `PDFFile` | Belgeler, raporlar, makaleler |
| **Ses** | `AudioFile` | Ses kayıtları, podcast'ler, toplantılar |
| **Video** | `VideoFile` | Ekran kayıtları, sunumlar |
| **Metin** | `TextFile` | Kod dosyaları, günlükler, veri dosyaları |
| **Genel** | `File` | İçerikten türü otomatik algılar |

```python
from crewai_files import File, ImageFile, PDFFile, AudioFile, VideoFile, TextFile

image = ImageFile(source="screenshot.png")
pdf = PDFFile(source="report.pdf")
audio = AudioFile(source="meeting.mp3")
video = VideoFile(source="demo.mp4")
text = TextFile(source="data.csv")

file = File(source="document.pdf")
```

## Dosya Kaynakları

`source` parametresi, uygun işleyiciyi otomatik olarak algılayan çoklu giriş türlerini kabul eder:

### Yoldan

```python
from crewai_files import ImageFile

image = ImageFile(source="./images/chart.png")
```

### URL'den

```python
from crewai_files import ImageFile

image = ImageFile(source="https://example.com/image.png")
```

### Baytlardan

```python
from crewai_files import ImageFile, FileBytes

image_bytes = download_image_from_api()
image = ImageFile(source=FileBytes(data=image_bytes, filename="downloaded.png"))
image = ImageFile(source=image_bytes)
```

## Dosyaları Kullanma

Dosyalar, daha özel seviyelerin daha üstün öncelikli olacak şekilde, birden çok seviyede geçirilebilir.

### Crew'larla

Crew'u başlattığınızda dosyaları iletin:

```python
from crewai import Crew
from crewai_files import ImageFile

crew = Crew(agents=[analyst], tasks=[analysis_task])

result = crew.kickoff(
    inputs={"topic": "Q4 Sales"},
    input_files={
        "chart": ImageFile(source="sales_chart.png"),
        "report": PDFFile(source="quarterly_report.pdf"),
    }
)
```

### Görevlerle

Dosyaları belirli görevlere ekleyin:

```python
from crewai import Task
from crewai_files import ImageFile

task = Task(
    description="Satış grafiğini analiz edin ve {chart} içindeki eğilimleri belirleyin",
    expected_output="Temel eğilimlerin özeti",
    input_files={
        "chart": ImageFile(source="sales_chart.png"),
    }
)
```

### Akışlarla

Dosyaları, crew'lara otomatik olarak devredilen akışlara iletin:

```python
from crewai.flow.flow import Flow, start
from crewai_files import ImageFile

class AnalysisFlow(Flow):
    @start()
    def analyze(self):
        return self.analysis_crew.kickoff()

flow = AnalysisFlow()
result = flow.kickoff(
    input_files={"image": ImageFile(source="data.png")}
)
```

### Bağımsız Agent'larla

Dosyaları doğrudan agent kickoff'a iletin:

```python
from crewai import Agent
from crewai_files import ImageFile

agent = Agent(
    role="Görüntü Analisti",
    goal="Görüntüleri analiz et",
    backstory="Görsel analizde uzman",
    llm="gpt-4o",
)

result = agent.kickoff(
    messages="Bu görüntüde neler var?",
    input_files={"photo": ImageFile(source="photo.jpg")},
)
```

## Dosya Önceliği

Dosyalar birden çok seviyede geçirildiğinde, daha geniş olanları geçersiz kılacak daha özel seviyeler geçerli olur:

```
Flow input_files < Crew input_files < Task input_files
```

Örneğin, hem Flow hem de Task bir `"chart"` dosyası tanımlarsa, Task'ın sürümü kullanılır.

## Sağlayıcı Desteği

Farklı sağlayıcılar farklı dosya türlerini destekler. CrewAI, dosya türlerini her sağlayıcının API'si için otomatik olarak biçimlendirir.

| Sağlayıcı | Görüntü | PDF | Ses | Video | Metin |
|:---------|:-----:|:---:|:-----:|:-----:|:----:|
| **OpenAI** (completions API) | ✓ | | | | |
| **OpenAI** (responses API) | ✓ | ✓ | ✓ | | |
| **Anthropic** (claude-3.x) | ✓ | ✓ | | | |
| **Google Gemini** (gemini-1.5, 2.0, 2.5) | ✓ | ✓ | ✓ | ✓ | ✓ |
| **AWS Bedrock** (claude-3) | ✓ | ✓ | | | |
| **Azure OpenAI** (gpt-4o) | ✓ | | ✓ | | |


Google Gemini modelleri, 1 saate kadar ve 2 GB'a kadar video dahil tüm dosya türlerini destekler. Video içeriğini işlemeniz gerekiyorsa Gemini'yi kullanın.



Sağlayıcının desteklemediği bir dosya türünü (örneğin OpenAI'ya video) ilettiğinizde, `UnsupportedFileTypeError` alırsınız. İşlemeniz gereken dosya türlerine göre sağlayıcıyı seçin.


## Dosyaların Gönderilmesi

CrewAI, sağlayıcılara dosyaları göndermek için en uygun yöntemi otomatik olarak seçer:

| Yöntem | Açıklama | Ne Zaman Kullanılır |
|:-------|:------------|:----------|
| **Inline Base64** | Dosya, istekte doğrudan gömülüdür | Küçük dosyalar (< 5MB tipik olarak) |
| **Dosya Yükleme API'si** | Dosya ayrı ayrı yüklenir ve bir ID tarafından referans gösterilir | Eşik değerini aşan büyük dosyalar |
| **URL Referansı** | Modele doğrudan URL geçirilir | Dosya kaynağı zaten bir URL'dir |

### Sağlayıcı İletim Yöntemleri

| Sağlayıcı | Inline Base64 | Dosya Yükleme API'si | URL Referansları |
|:---------|:-------------:|:---------------:|:--------------:|
| **OpenAI** | ✓ | ✓ (> 5 MB) | ✓ |
| **Anthropic** | ✓ | ✓ (> 5 MB) | ✓ |
| **Google Gemini** | ✓ | ✓ (> 20 MB) | ✓ |
| **AWS Bedrock** | ✓ | | ✓ (S3 URIs) |
| **Azure OpenAI** | ✓ | | ✓ |


Bunu kendiniz yönetmenize gerek yoktur. CrewAI, dosya boyutu ve sağlayıcı yeteneklerine göre en verimli yöntemi otomatik olarak kullanır. Dosya yükleme API'si olmayan sağlayıcılar, tüm dosyalar için inline base64 kullanır.


## Dosya İşleme Modları

Dosyalar sağlayıcı limitlerini aştığında dosyaların nasıl işleneceğini kontrol edin:

```python
from crewai_files import ImageFile, PDFFile

image = ImageFile(source="large.png", mode="strict")
image = ImageFile(source="large.png", mode="auto")
image = ImageFile(source="large.png", mode="warn")
pdf = PDFFile(source="large.pdf", mode="chunk")
```

## Sağlayıcı Kısıtlamaları

Her sağlayıcının dosya boyutları ve boyutları için belirli limitleri vardır:

### OpenAI
- **Görüntüler**: Maksimum 20 MB, istek başına maksimum 10 görüntü
- **PDF'ler**: Maksimum 32 MB, maksimum 100 sayfa
- **Ses**: Maksimum 25 MB, maksimum 25 dakika

### Anthropic
- **Görüntüler**: Maksimum 5 MB, maksimum 8000x8000 piksel, maksimum 100 görüntü
- **PDF'ler**: Maksimum 32 MB, maksimum 100 sayfa

### Google Gemini
- **Görüntüler**: Maksimum 100 MB
- **PDF'ler**: Maksimum 50 MB
- **Ses**: Maksimum 100 MB, maksimum 9,5 saat
- **Video**: Maksimum 2 GB, maksimum 1 saat

### AWS Bedrock
- **Görüntüler**: Maksimum 4,5 MB, maksimum 8000x8000 piksel
- **PDF'ler**: Maksimum 3,75 MB, maksimum 100 sayfa

## Komut İsteklerinde Dosyalara Referans Verme

Dosyaya referans vermek için görev açıklamalarınızda dosyanın anahtar adını kullanın:

```python
task = Task(
    description="""
    Sağlanan materyalleri inceleyin:
    1. {sales_chart} içindeki grafiği gözden geçirin
    2. {quarterly_report} içindeki verilerle çapraz referans alın
    3. Temel bulguların özetini çıkarın
    """,
    expected_output="Temel içgörülerle analiz özeti",
    input_files={
        "sales_chart": ImageFile(source="chart.png"),
        "quarterly_report": PDFFile(source="report.pdf"),
    }
)
```