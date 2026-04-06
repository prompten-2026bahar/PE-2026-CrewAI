> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Firecrawl ile Web Sitesi Scrape Etme

> `FirecrawlScrapeWebsiteTool`, web sitelerini scrape etmek ve bunları temiz markdown ya da yapılandırılmış veriye dönüştürmek için tasarlanmıştır.

# `FirecrawlScrapeWebsiteTool`

## Açıklama

[Firecrawl](https://firecrawl.dev), herhangi bir web sitesini taramak ve temiz markdown ya da yapılandırılmış veriye dönüştürmek için kullanılan bir platformdur.

## Kurulum

* [firecrawl.dev](https://firecrawl.dev) üzerinden bir API anahtarı alın ve bunu ortam değişkenlerine (`FIRECRAWL_API_KEY`) ayarlayın.
* [Firecrawl SDK](https://github.com/mendableai/firecrawl) ile birlikte `crewai[tools]` paketini kurun:

```shell  theme={null}
pip install firecrawl-py 'crewai[tools]'
```

## Örnek

Ajanınızın web sitelerini yükleyebilmesi için FirecrawlScrapeWebsiteTool'u aşağıdaki gibi kullanın:

```python Code theme={null}
from crewai_tools import FirecrawlScrapeWebsiteTool

tool = FirecrawlScrapeWebsiteTool(url='firecrawl.dev')
```

## Argümanlar

* `api_key`: İsteğe bağlı. Firecrawl API anahtarını belirtir. Varsayılan olarak `FIRECRAWL_API_KEY` ortam değişkeni kullanılır.
* `url`: Scrape edilecek URL.
* `page_options`: İsteğe bağlı.
  * `onlyMainContent`: İsteğe bağlı. Header, nav, footer vb. hariç yalnızca sayfanın ana içeriğini döndürür.
  * `includeHtml`: İsteğe bağlı. Sayfanın ham HTML içeriğini dahil eder. Yanıtta bir `html` anahtarı üretir.
* `extractor_options`: İsteğe bağlı. Sayfa içeriğinden yapılandırılmış bilgi çıkarmaya yönelik LLM tabanlı seçenekler
  * `mode`: Kullanılacak çıkarım modu; şu anda `llm-extraction` desteklenir
  * `extractionPrompt`: İsteğe bağlı. Sayfadan hangi bilginin çıkarılacağını açıklayan prompt
  * `extractionSchema`: İsteğe bağlı. Çıkarılacak verinin şeması
* `timeout`: İsteğe bağlı. İstek için milisaniye cinsinden zaman aşımı
