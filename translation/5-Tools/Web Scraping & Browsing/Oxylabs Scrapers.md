> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Oxylabs Scraper'ları

> Oxylabs Scrapers, ilgili kaynaklardaki bilgilere kolayca erişmeyi sağlar. Kullanılabilir kaynakların listesi aşağıdadır:
  - `Amazon Product`
  - `Amazon Search`
  - `Google Seach`
  - `Universal`


## Kurulum

[buradan](https://oxylabs.io) bir Oxylabs hesabı oluşturarak kimlik bilgilerini edinin.

```shell  theme={null}
pip install 'crewai[tools]' oxylabs
```

[Oxylabs Documentation](https://developers.oxylabs.io/scraping-solutions/web-scraper-api/targets) üzerinden API parametreleri hakkında daha fazla bilgi alabilirsiniz.

# `OxylabsAmazonProductScraperTool`

### Örnek

```python  theme={null}
from crewai_tools import OxylabsAmazonProductScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsAmazonProductScraperTool()

result = tool.run(query="AAAAABBBBCC")

print(result)
```

### Parametreler

* `query` - 10 karakterli ASIN kodu.
* `domain` - Amazon için alan adı yerelleştirmesi.
* `geo_location` - *Deliver to* konumu.
* `user_agent_type` - cihaz türü ve tarayıcı.
* `render` - `html` olarak ayarlandığında JavaScript render özelliğini etkinleştirir.
* `callback_url` - callback uç noktanızın URL'si.
* `context` - Özel gereksinimler için ek gelişmiş ayarlar ve kontroller.
* `parse` - `true` olduğunda ayrıştırılmış veriyi döndürür.
* `parsing_instructions` - HTML scraping sonucu üzerinde çalıştırılacak kendi ayrıştırma ve veri dönüştürme mantığınızı tanımlar.

### Gelişmiş örnek

```python  theme={null}
from crewai_tools import OxylabsAmazonProductScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsAmazonProductScraperTool(
    config={
        "domain": "com",
        "parse": True,
        "context": [
            {
                "key": "autoselect_variant",
                "value": True
            }
        ]
    }
)

result = tool.run(query="AAAAABBBBCC")

print(result)
```

# `OxylabsAmazonSearchScraperTool`

### Örnek

```python  theme={null}
from crewai_tools import OxylabsAmazonSearchScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsAmazonSearchScraperTool()

result = tool.run(query="headsets")

print(result)
```

### Parametreler

* `query` - Amazon arama terimi.
* `domain` - Bestbuy için alan adı yerelleştirmesi.
* `start_page` - başlangıç sayfa numarası.
* `pages` - getirilecek sayfa sayısı.
* `geo_location` - *Deliver to* konumu.
* `user_agent_type` - cihaz türü ve tarayıcı.
* `render` - `html` olarak ayarlandığında JavaScript render özelliğini etkinleştirir.
* `callback_url` - callback uç noktanızın URL'si.
* `context` - Özel gereksinimler için ek gelişmiş ayarlar ve kontroller.
* `parse` - `true` olduğunda ayrıştırılmış veriyi döndürür.
* `parsing_instructions` - HTML scraping sonucu üzerinde çalıştırılacak kendi ayrıştırma ve veri dönüştürme mantığınızı tanımlar.

### Gelişmiş örnek

```python  theme={null}
from crewai_tools import OxylabsAmazonSearchScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsAmazonSearchScraperTool(
    config={
        "domain": 'nl',
        "start_page": 2,
        "pages": 2,
        "parse": True,
        "context": [
            {'key': 'category_id', 'value': 16391693031}
        ],
    }
)

result = tool.run(query='nirvana tshirt')

print(result)
```

# `OxylabsGoogleSearchScraperTool`

### Örnek

```python  theme={null}
from crewai_tools import OxylabsGoogleSearchScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsGoogleSearchScraperTool()

result = tool.run(query="iPhone 16")

print(result)
```

### Parametreler

* `query` - arama anahtar kelimesi.
* `domain` - Google için alan adı yerelleştirmesi.
* `start_page` - başlangıç sayfa numarası.
* `pages` - getirilecek sayfa sayısı.
* `limit` - her sayfada getirilecek sonuç sayısı.
* `locale` - Google arama sayfası arayüz dilini değiştiren `Accept-Language` başlık değeri.
* `geo_location` - sonucun uyarlanacağı coğrafi konum. Doğru veriyi almak için bu parametrenin doğru kullanılması son derece önemlidir.
* `user_agent_type` - cihaz türü ve tarayıcı.
* `render` - `html` olarak ayarlandığında JavaScript render özelliğini etkinleştirir.
* `callback_url` - callback uç noktanızın URL'si.
* `context` - Özel gereksinimler için ek gelişmiş ayarlar ve kontroller.
* `parse` - `true` olduğunda ayrıştırılmış veriyi döndürür.
* `parsing_instructions` - HTML scraping sonucu üzerinde çalıştırılacak kendi ayrıştırma ve veri dönüştürme mantığınızı tanımlar.

### Gelişmiş örnek

```python  theme={null}
from crewai_tools import OxylabsGoogleSearchScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsGoogleSearchScraperTool(
    config={
        "parse": True,
        "geo_location": "Paris, France",
        "user_agent_type": "tablet",
    }
)

result = tool.run(query="iPhone 16")

print(result)
```

# `OxylabsUniversalScraperTool`

### Örnek

```python  theme={null}
from crewai_tools import OxylabsUniversalScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsUniversalScraperTool()

result = tool.run(url="https://ip.oxylabs.io")

print(result)
```

### Parametreler

* `url` - scrape edilecek web sitesi URL'si.
* `user_agent_type` - cihaz türü ve tarayıcı.
* `geo_location` - veriyi almak için proxy'nin coğrafi konumunu ayarlar.
* `render` - `html` olarak ayarlandığında JavaScript render özelliğini etkinleştirir.
* `callback_url` - callback uç noktanızın URL'si.
* `context` - Özel gereksinimler için ek gelişmiş ayarlar ve kontroller.
* `parse` - gönderilen URL'nin sayfa türü için özel bir ayrıştırıcı mevcut olduğu sürece `true` olarak ayarlandığında ayrıştırılmış veriyi döndürür.
* `parsing_instructions` - HTML scraping sonucu üzerinde çalıştırılacak kendi ayrıştırma ve veri dönüştürme mantığınızı tanımlar.

### Gelişmiş örnek

```python  theme={null}
from crewai_tools import OxylabsUniversalScraperTool

# OXYLABS_USERNAME ve OXYLABS_PASSWORD değişkenlerinin ayarlı olduğundan emin olun
tool = OxylabsUniversalScraperTool(
    config={
        "render": "html",
        "user_agent_type": "mobile",
        "context": [
            {"key": "force_headers", "value": True},
            {"key": "force_cookies", "value": True},
            {
                "key": "headers",
                "value": {
                    "Custom-Header-Name": "custom header content",
                },
            },
            {
                "key": "cookies",
                "value": [
                    {"key": "NID", "value": "1234567890"},
                    {"key": "1P JAR", "value": "0987654321"},
                ],
            },
            {"key": "http_method", "value": "get"},
            {"key": "follow_redirects", "value": True},
            {"key": "successful_status_codes", "value": [808, 909]},
        ],
    }
)

result = tool.run(url="https://ip.oxylabs.io")

print(result)
```
