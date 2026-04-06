> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Hyperbrowser Yükleme Aracı

> `HyperbrowserLoadTool`, Hyperbrowser kullanarak web scraping ve tarama işlemlerini mümkün kılar.

# `HyperbrowserLoadTool`

## Açıklama

`HyperbrowserLoadTool`, headless tarayıcıları çalıştırma ve ölçekleme platformu olan [Hyperbrowser](https://hyperbrowser.ai) aracılığıyla web scraping ve tarama yapmayı sağlar. Bu araç, tek bir sayfayı scrape etmenize veya tüm siteyi taramanıza izin verir ve içeriği düzgün biçimlendirilmiş markdown ya da HTML olarak döndürür.

Temel Özellikler:

* Anında Ölçeklenebilirlik - Altyapı sıkıntısı olmadan saniyeler içinde yüzlerce tarayıcı oturumu başlatın
* Basit Entegrasyon - Puppeteer ve Playwright gibi popüler araçlarla sorunsuz çalışır
* Güçlü API'ler - Herhangi bir siteyi scrape etmek/taramak için kullanımı kolay API'ler
* Anti-Bot Önlemlerini Aşma - Yerleşik stealth modu, reklam engelleme, otomatik CAPTCHA çözme ve dönen proxy'ler

## Kurulum

Bu aracı kullanmak için Hyperbrowser SDK'sını kurmanız gerekir:

```shell  theme={null}
uv add hyperbrowser
```

## Başlamak İçin Adımlar

`HyperbrowserLoadTool` aracını etkili şekilde kullanmak için şu adımları izleyin:

1. **Kayıt Olun**: [Hyperbrowser](https://app.hyperbrowser.ai/) adresine gidin, kaydolun ve bir API anahtarı oluşturun.
2. **API Anahtarı**: `HYPERBROWSER_API_KEY` ortam değişkenini ayarlayın veya doğrudan araç kurucusuna iletin.
3. **SDK'yı Kurun**: Yukarıdaki komutu kullanarak Hyperbrowser SDK'sını kurun.

## Örnek

Aşağıdaki örnek, aracın nasıl başlatılacağını ve bir web sitesini scrape etmek için nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai_tools import HyperbrowserLoadTool
from crewai import Agent

# Aracı API anahtarınızla başlatın
tool = HyperbrowserLoadTool(api_key="your_api_key")  # Or use environment variable

# Aracı kullanan bir ajan tanımlayın
@agent
def web_researcher(self) -> Agent:
    '''
    Bu ajan, HyperbrowserLoadTool kullanarak web sitelerini scrape eder
    ve bilgi çıkarır.
    '''
    return Agent(
        config=self.agents_config["web_researcher"],
        tools=[tool]
    )
```

## Parametreler

`HyperbrowserLoadTool` şu parametreleri kabul eder:

### Kurucu Parametreleri

* **api\_key**: İsteğe bağlı. Hyperbrowser API anahtarınız. Verilmezse `HYPERBROWSER_API_KEY` ortam değişkeninden okunur.

### Çalıştırma Parametreleri

* **url**: Gerekli. Scrape veya tarama yapılacak web sitesi URL'si.
* **operation**: İsteğe bağlı. Web sitesinde yapılacak işlem. `scrape` veya `crawl` olabilir. Varsayılan `scrape`'tir.
* **params**: İsteğe bağlı. Scrape veya tarama işlemi için ek parametreler.

## Desteklenen Parametreler

Desteklenen tüm parametreler hakkında ayrıntılı bilgi için:

* [Scrape Parameters](https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait)
* [Crawl Parameters](https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait)

## Dönüş Biçimi

Araç içeriği şu biçimde döndürür:

* **scrape** işlemleri için: Sayfa içeriği markdown veya HTML biçiminde.
* **crawl** işlemleri için: Her sayfanın içeriği, sayfa URL'siyle birlikte ayraçlarla ayrılmış şekilde.

## Sonuç

`HyperbrowserLoadTool`, anti-bot önlemleri, CAPTCHA'lar ve daha fazlası gibi karmaşık senaryoları yöneterek web sitelerini scrape etmek ve taramak için güçlü bir yol sunar. Hyperbrowser platformundan yararlanarak ajanların web içeriğine verimli biçimde erişmesini ve veri çıkarmasını sağlar.
