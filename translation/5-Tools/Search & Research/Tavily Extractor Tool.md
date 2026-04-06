> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Tavily Çıkarıcı Aracı

> Tavily API kullanarak web sayfalarından yapılandırılmış içerik çıkarın

`TavilyExtractorTool`, CrewAI ajanlarının Tavily API kullanarak web sayfalarından yapılandırılmış içerik çıkarmasını sağlar. Tekil URL'leri veya URL listelerini işleyebilir ve çıkarım derinliğini kontrol etme ile görselleri dahil etme seçenekleri sunar.

## Kurulum

`TavilyExtractorTool` kullanmak için `tavily-python` kütüphanesini kurmanız gerekir:

```shell  theme={null}
pip install 'crewai[tools]' tavily-python
```

Ayrıca Tavily API anahtarınızı bir ortam değişkeni olarak ayarlamanız gerekir:

```bash  theme={null}
export TAVILY_API_KEY='your-tavily-api-key'
```

## Kullanım Örneği

`TavilyExtractorTool` aracını bir CrewAI ajanı içinde başlatmak ve kullanmak için şu örneği izleyebilirsiniz:

```python  theme={null}
import os
from crewai import Agent, Task, Crew
from crewai_tools import TavilyExtractorTool

# TAVILY_API_KEY'in ortamınızda ayarlı olduğundan emin olun
# os.environ["TAVILY_API_KEY"] = "YOUR_API_KEY"

# Aracı başlat
tavily_tool = TavilyExtractorTool()

# Aracı kullanan bir ajan oluştur
extractor_agent = Agent(
    role='Web İçerik Çıkarıcı',
    goal='Belirtilen web sayfalarından temel bilgileri çıkar',
    backstory='Tavily API kullanarak web sitelerinden ilgili içerikleri çıkarma konusunda uzmansın.',
    tools=[tavily_tool],
    verbose=True
)

# Ajan için bir görev tanımla
extract_task = Task(
    description='https://example.com URL’sinden temel çıkarım derinliğini kullanarak ana içeriği çıkar.',
    expected_output='URL’den çıkarılan içeriği içeren bir JSON dizesi.',
    agent=extractor_agent
)

# Ekibi oluştur ve çalıştır
crew = Crew(
    agents=[extractor_agent],
    tasks=[extract_task],
    verbose=2
)

result = crew.kickoff()
print(result)
```

## Yapılandırma Seçenekleri

`TavilyExtractorTool` şu argümanları kabul eder:

* `urls` (Union\[List\[str], str]): **Gerekli**. Veri çıkarılacak tek bir URL dizesi veya URL dizeleri listesi.
* `include_images` (Optional\[bool]): Çıkarım sonuçlarına görsellerin dahil edilip edilmeyeceği. Varsayılan `False`.
* `extract_depth` (Literal\["basic", "advanced"]): Çıkarım derinliği. Daha hızlı, yüzeysel çıkarım için `"basic"`, daha kapsamlı çıkarım için `"advanced"` kullanın. Varsayılan `"basic"`.
* `timeout` (int): Çıkarım isteğinin tamamlanması için beklenecek maksimum süre (saniye). Varsayılan `60`.

## Gelişmiş Kullanım

### Gelişmiş Çıkarımla Birden Fazla URL

```python  theme={null}
# Birden fazla URL ve gelişmiş çıkarım ile örnek
multi_extract_task = Task(
    description='https://example.com ve https://anotherexample.org adreslerinden gelişmiş çıkarım kullanarak içerik çıkar.',
    expected_output='Her iki URL’den çıkarılan içeriği içeren bir JSON dizesi.',
    agent=extractor_agent
)

# Aracı özel parametrelerle yapılandır
custom_extractor = TavilyExtractorTool(
    extract_depth='advanced',
    include_images=True,
    timeout=120
)

agent_with_custom_tool = Agent(
    role="Gelişmiş İçerik Çıkarıcı",
    goal="Görsellerle birlikte kapsamlı içerik çıkar",
    tools=[custom_extractor]
)
```

### Araç Parametreleri

Aracın davranışını, başlatma sırasında parametreler vererek özelleştirebilirsiniz:

```python  theme={null}
# Özel yapılandırma ile başlat
extractor_tool = TavilyExtractorTool(
    extract_depth='advanced',  # Daha kapsamlı çıkarım
    include_images=True,       # Görsel sonuçlarını dahil et
    timeout=90                 # Özel zaman aşımı
)
```

## Özellikler

* **Tekil veya Çoklu URL**: Bir URL’den içerik çıkarın veya tek bir istekte birden fazla URL’yi işleyin
* **Yapılandırılabilir Derinlik**: Temel (hızlı) ve gelişmiş (kapsamlı) çıkarım modları arasında seçim yapın
* **Görsel Desteği**: Çıkarım sonuçlarına isteğe bağlı olarak görselleri dahil edin
* **Yapılandırılmış Çıktı**: Çıkarılan içeriği içeren iyi biçimlendirilmiş JSON döndürür
* **Hata Yönetimi**: Ağ zaman aşımları ve çıkarım hataları için sağlam yönetim

## Yanıt Biçimi

Araç, sağlanan URL(ler)den çıkarılan yapılandırılmış veriyi temsil eden bir JSON dizesi döndürür. Tam yapı, sayfaların içeriğine ve kullanılan `extract_depth` değerine bağlıdır.

Yaygın yanıt öğeleri şunları içerir:

* **Title**: Sayfa başlığı
* **Content**: Sayfanın ana metin içeriği
* **Images**: Görsel URL’leri ve meta verileri (`include_images=True` olduğunda)
* **Metadata**: Yazar, açıklama vb. ek sayfa bilgileri

## Kullanım Senaryoları

* **İçerik Analizi**: Rakip web sitelerinden içerik çıkarın ve analiz edin
* **Araştırma**: Analiz için birden fazla kaynaktan yapılandırılmış veri toplayın
* **İçerik Taşıma**: Mevcut web sitelerinden taşıma için içerik çıkarın
* **İzleme**: Değişiklik tespiti için düzenli içerik çıkarımı yapın
* **Veri Toplama**: Web kaynaklarından sistematik bilgi çıkarımı gerçekleştirin

Yanıt yapısı ve mevcut seçenekler hakkında ayrıntılı bilgi için [Tavily API documentation](https://docs.tavily.com/docs/tavily-api/python-sdk#extract) sayfasına bakın.
