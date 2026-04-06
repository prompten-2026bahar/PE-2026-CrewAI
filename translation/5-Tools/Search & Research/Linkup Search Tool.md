> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Linkup Arama Aracı

> `LinkupSearchTool`, bağlamsal bilgi için Linkup API'sini sorgulama olanağı sağlar.

# `LinkupSearchTool`

## Açıklama

`LinkupSearchTool`, Linkup API'sini bağlamsal bilgi ve yapılandırılmış sonuçlar için sorgulama olanağı sağlar. Bu araç, iş akışlarını Linkup'tan güncel ve güvenilir bilgilerle zenginleştirmek için idealdir ve ajanların görevleri sırasında ilgili veriye erişmesini sağlar.

## Kurulum

Bu aracı kullanmak için Linkup SDK'yı yüklemeniz gerekir:

```shell  theme={null}
uv add linkup-sdk
```

## Başlamak İçin Adımlar

`LinkupSearchTool`'u etkili bir şekilde kullanmak için aşağıdaki adımları izleyin:

1. **API Anahtarı**: Linkup API anahtarı alın.
2. **Ortam Kurulumu**: API anahtarı ile ortamınızı ayarlayın.
3. **SDK Kurulumu**: Yukarıdaki komutu kullanarak Linkup SDK'yı yükleyin.

## Örnek

Aşağıdaki örnek, aracı başlatmanız ve bir ajan içinde kullanmanızın nasıl yapılacağını göstermektedir:

```python Code theme={null}
from crewai_tools import LinkupSearchTool
from crewai import Agent
import os

# Aracı API anahtarınız ile başlat
linkup_tool = LinkupSearchTool(api_key=os.getenv("LINKUP_API_KEY"))

# Aracı kullanan bir ajan tanımla
@agent
def researcher(self) -> Agent:
    '''
    Bu ajan, Linkup API'sinden bağlamsal bilgiler almak için LinkupSearchTool'u kullanır.
    '''
    return Agent(
        config=self.agents_config["researcher"],
        tools=[linkup_tool]
    )
```

## Parametreler

`LinkupSearchTool` aşağıdaki parametreleri kabul eder:

### Oluşturucu Parametreleri

* **api\_key**: Gerekli. Linkup API anahtarınız.

### Çalıştırma Parametreleri

* **query**: Gerekli. Arama terimi veya ifadesi.
* **depth**: İsteğe bağlı. Arama derinliği. Varsayılan "standard" olarak ayarlanmıştır.
* **output\_type**: İsteğe bağlı. Çıkış türü. Varsayılan "searchResults" olarak ayarlanmıştır.

## Gelişmiş Kullanım

Daha spesifik sonuçlar için arama parametrelerini özelleştirebilirsiniz:

```python Code theme={null}
# Özel parametrelerle bir arama yap
results = linkup_tool.run(
    query="Women Nobel Prize Physics",
    depth="deep",
    output_type="searchResults"
)
```

## Dönüş Biçimi

Araç sonuçları aşağıdaki biçimde döndürür:

```json  theme={null}
{
  "success": true,
  "results": [
    {
      "name": "Sonuç Başlığı",
      "url": "https://example.com/result",
      "content": "Sonucun içeriği..."
    },
    // Ek sonuçlar...
  ]
}
```

Bir hata oluşursa, yanıt şu şekilde olacaktır:

```json  theme={null}
{
  "success": false,
  "error": "Hata mesajı"
}
```

## Hata İşleme

Araç API hatalarını zarif bir şekilde işler ve yapılandırılmış geri bildirim sağlar. API isteği başarısız olursa, araç `success: false` ve bir hata mesajı içeren bir sözlük döndürür.

## Sonuç

`LinkupSearchTool`, Linkup'ın bağlamsal bilgi alma yeteneklerini CrewAI ajanlarınıza entegre etmek için sorunsuz bir yol sağlar. Bu aracı kullanarak, ajanlar karar verme ve görev yürütmelerini iyileştirmek için ilgili ve güncel bilgilere erişebilirler.

