> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Firecrawl ile Web Sitesi Tarama

> `FirecrawlCrawlWebsiteTool`, web sitelerini taramak ve bunları temiz markdown ya da yapılandırılmış veriye dönüştürmek için tasarlanmıştır.

# `FirecrawlCrawlWebsiteTool`

## Açıklama

[Firecrawl](https://firecrawl.dev), herhangi bir web sitesini taramak ve temiz markdown ya da yapılandırılmış veriye dönüştürmek için kullanılan bir platformdur.

## Kurulum

* [firecrawl.dev](https://firecrawl.dev) üzerinden bir API anahtarı alın ve bunu ortam değişkenlerine (`FIRECRAWL_API_KEY`) ayarlayın.
* [Firecrawl SDK](https://github.com/mendableai/firecrawl) ile birlikte `crewai[tools]` paketini kurun:

```shell  theme={null}
pip install firecrawl-py 'crewai[tools]'
```

## Örnek

Ajanınızın web sitelerini yükleyebilmesi için FirecrawlScrapeFromWebsiteTool'u aşağıdaki gibi kullanın:

```python Code theme={null}
from crewai_tools import FirecrawlCrawlWebsiteTool

tool = FirecrawlCrawlWebsiteTool(url='firecrawl.dev')
```

## Argümanlar

* `api_key`: İsteğe bağlı. Firecrawl API anahtarını belirtir. Varsayılan olarak `FIRECRAWL_API_KEY` ortam değişkeni kullanılır.
* `url`: Taramaya başlanacak temel URL.
* `page_options`: İsteğe bağlı.
  * `onlyMainContent`: İsteğe bağlı. Header, nav, footer vb. hariç yalnızca sayfanın ana içeriğini döndürür.
  * `includeHtml`: İsteğe bağlı. Sayfanın ham HTML içeriğini dahil eder. Yanıtta bir `html` anahtarı üretir.
* `crawler_options`: İsteğe bağlı. Tarama davranışını kontrol etmeye yönelik seçenekler.
  * `includes`: İsteğe bağlı. Taramaya dahil edilecek URL desenleri.
  * `exclude`: İsteğe bağlı. Taramadan hariç tutulacak URL desenleri.
  * `generateImgAltText`: İsteğe bağlı. Görseller için LLM'ler kullanarak alt metin üretir (ücretli plan gerekir).
  * `returnOnlyUrls`: İsteğe bağlı. `true` ise tarama durumunda yalnızca URL'leri bir liste olarak döndürür. Not: yanıt, belgeler listesi değil `data` içinde URL listesi olacaktır.
  * `maxDepth`: İsteğe bağlı. Maksimum tarama derinliği. Derinlik 1 temel URL'dir; derinlik 2, temel URL ve doğrudan alt sayfalarını içerir; bu şekilde devam eder.
  * `mode`: İsteğe bağlı. Kullanılacak tarama modu. Hızlı mod, site haritası olmayan sitelerde 4 kat daha hızlı tarar; ancak o kadar doğru olmayabilir ve yoğun JavaScript render edilen web sitelerinde kullanılmamalıdır.
  * `limit`: İsteğe bağlı. Taranacak maksimum sayfa sayısı.
  * `timeout`: İsteğe bağlı. Tarama işlemi için milisaniye cinsinden zaman aşımı.
