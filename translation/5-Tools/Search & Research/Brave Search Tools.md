> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Brave Search Araçları

> Brave Search API'sini sorgulamak için araçlar - web, haber, görüntü ve video araması kapsayan.

# Brave Search Araçları

## Açıklama

CrewAI, belirli bir [Brave Search API](https://brave.com/search/api/) uç noktasını hedefleyen bir Brave Search araçları ailesi sunmaktadır.
Tek bir genel araç yerine, ajanınızın ihtiyaç duyduğu sonuç türüne tam olarak eşleşen aracı seçebilirsiniz:

| Araç                            | Uç Nokta       | Kullanım Alanı                                                                             |
| ------------------------------- | ------------ | ------------------------------------------------------------------------------------ |
| `BraveWebSearchTool`            | Web Araması   | Genel web sonuçları, snippet'ler ve URL'ler                                              |
| `BraveNewsSearchTool`           | Haber Araması  | Son haber makaleleri ve başlıklar                                                   |
| `BraveImageSearchTool`          | Görüntü Araması | Görüntü sonuçları boyutlar ve kaynak URL'leri ile                                        |
| `BraveVideoSearchTool`          | Video Araması | Web'den video sonuçları                                                    |
| `BraveLocalPOIsTool`            | Yerel POI'lar   | İlgi alanlarını bulma (ör. restoranlar)                                          |
| `BraveLocalPOIsDescriptionTool` | Yerel POI'lar   | Yapay zeka tarafından oluşturulan konum açıklamalarını alma                                          |
| `BraveLLMContextTool`           | LLM Bağlamı  | AI ajanları, LLM temeli ve RAG boru hatları için optimize edilmiş önceden çıkarılmış web içeriği. |

Tüm araçlar ortak bir temel sınıf (`BraveSearchToolBase`) paylaşır - hız sınırlaması, `429` yanıtlarında otomatik yeniden denemeler, başlık ve parametre doğrulaması ve isteğe bağlı dosya kaydetme sağlayan.

<Note>
  Eski `BraveSearchTool` sınıfı hala geriye dönük uyumluluk için mevcuttur, ancak **eski** olarak kabul edilir ve ileriye dönük aynı düzeyde dikkati almayacaktır. Yukarıda listelenen belirli araçlara geçişi öneririz, bu araçlar daha zengin yapılandırma ve daha odaklanmış bir arayüz sunarlar.
</Note>

<Note>
  Birçok araç (ör. *BraveWebSearchTool*, *BraveNewsSearchTool*, *BraveImageSearchTool* ve *BraveVideoSearchTool*) ücretsiz bir Brave Search API aboneliği/planıyla kullanılabilirken, bazı parametreler (ör. `enable_snippets`) ve araçlar (ör. *BraveLocalPOIsTool* ve *BraveLocalPOIsDescriptionTool*) ücretli bir plan gerektirir. Açıklama için abonelik planınızın yeteneklerine bakın.
</Note>

## Kurulum

```shell  theme={null}
pip install 'crewai[tools]'
```

## Başlangıç

1. **Paketi yükleyin** — `crewai[tools]` öğesinin Python ortamınızda yüklü olduğundan emin olun.
2. **Bir API anahtarı alın** — [api-dashboard.search.brave.com/login](https://api-dashboard.search.brave.com/login) adresinde kaydolun ve bir anahtar oluşturun.
3. **Ortam değişkenini ayarlayın** — anahtarınızı `BRAVE_API_KEY` olarak saklayın veya doğrudan `api_key` parametresi aracılığıyla geçin.

## Hızlı Örnekler

### Web Araması

```python Code theme={null}
from crewai_tools import BraveWebSearchTool

tool = BraveWebSearchTool()
results = tool.run(q="CrewAI agent framework")
print(results)
```

### Haber Araması

```python Code theme={null}
from crewai_tools import BraveNewsSearchTool

tool = BraveNewsSearchTool()
results = tool.run(q="latest AI breakthroughs")
print(results)
```

### Görüntü Araması

```python Code theme={null}
from crewai_tools import BraveImageSearchTool

tool = BraveImageSearchTool()
results = tool.run(q="northern lights photography")
print(results)
```

### Video Araması

```python Code theme={null}
from crewai_tools import BraveVideoSearchTool

tool = BraveVideoSearchTool()
results = tool.run(q="how to build AI agents")
print(results)
```

### Konum POI Açıklamaları

```python Code theme={null}
from crewai_tools import (
    BraveWebSearchTool,
    BraveLocalPOIsDescriptionTool,
)

web_search = BraveWebSearchTool(raw=True)
poi_details = BraveLocalPOIsDescriptionTool()

results = web_search.run(q="italian restaurants in pensacola, florida")

if "locations" in results:
    location_ids = [ loc["id"] for loc in results["locations"]["results"] ]
    if location_ids:
        descriptions = poi_details.run(ids=location_ids)
        print(descriptions)
```

## Ortak Oluşturucu Parametreleri

Her Brave Search aracı, başlatma sırasında aşağıdaki parametreleri kabul eder:

| Parametre             | Tür            | Varsayılan | Açıklama                                                                                             |
| --------------------- | -------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| `api_key`             | `str \| None`  | `None`  | Brave API anahtarı. `BRAVE_API_KEY` ortam değişkenine geri döner.                                  |
| `headers`             | `dict \| None` | `None`  | Her istekle gönderilecek ek HTTP başlıkları (ör. `api-version`, yer bilgisi başlıkları).          |
| `requests_per_second` | `float`        | `1.0`   | Maksimum istek hızı. Araç bu sınırda kalmak için çağrılar arasında uyku moduna geçecektir.                      |
| `save_file`           | `bool`         | `False` | `True` olduğunda, her yanıt zaman damgalı bir `.txt` dosyasına yazılır.                                     |
| `raw`                 | `bool`         | `False` | `True` olduğunda, tam API JSON yanıtı herhangi bir iyileştirme olmadan döndürülür.                             |
| `timeout`             | `int`          | `30`    | HTTP istek zaman aşımı (saniye cinsinden).                                                                        |
| `country`             | `str \| None`  | `None`  | Yer hedeflemesi için eski kısaltma (ör. `"US"`). Bunun yerine `country` sorgu parametresini doğrudan kullanmayı tercih edin. |
| `n_results`           | `int`          | `10`    | Sonuç sayısı için eski kısaltma. Bunun yerine `count` sorgu parametresini doğrudan kullanmayı tercih edin.                   |

<Warning>
  `country` ve `n_results` oluşturucu parametreleri geriye dönük uyumluluk için mevcuttur. Çağrı sırasında karşılık gelen sorgu parametreleri (`country`, `count`) sağlanmadığında varsayılan olarak uygulanırlar. Yeni kod için, bunun yerine `country` ve `count` öğelerini doğrudan sorgu parametreleri olarak geçmenizi öneririz.
</Warning>

## Sorgu Parametreleri

Her araç, isteği göndermeden önce sorgu parametrelerini bir Pydantic şemasına karşı doğrular.
Parametreler her uç nokta için biraz farklılık gösterir - en yaygın olarak kullanılanların bir özeti burada verilmiştir:

### BraveWebSearchTool

| Parametre        | Açıklama                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `q`              | **(gerekli)** Arama sorgusu dizesi (maks 400 karakter).                                                                                              |
| `country`        | Yer hedeflemesi için iki harfli ülke kodu (ör. `"US"`).                                                                                        |
| `search_lang`    | Sonuçlar için iki harfli dil kodu (ör. `"en"`).                                                                                             |
| `count`          | Döndürülecek maksimum sonuç sayısı (1–20).                                                                                                          |
| `offset`         | Sonuçların ilk N sayfasını atla (0–9).                                                                                                         |
| `safesearch`     | İçerik filtresi: `"off"`, `"moderate"` veya `"strict"`.                                                                                            |
| `freshness`      | Yenilik filtresi: `"pd"` (son gün), `"pw"` (son hafta), `"pm"` (son ay), `"py"` (son yıl) veya tarih aralığı `"2025-01-01to2025-06-01"`. |
| `extra_snippets` | Sonuç başına 5 ek metin snippet'ine kadar ekle.                                                                                             |
| `goggles`        | Özel yeniden sıralama için Brave Goggles URL'si ve/veya kaynağı.                                                                                        |

Tam parametre ve başlık referansı için bkz. [Brave Web Araması API'si belgeleri](https://api-dashboard.search.brave.com/api-reference/web/search/get).

### BraveNewsSearchTool

| Parametre     | Açıklama                                               |
| ------------- | --------------------------------------------------------- |
| `q`           | **(gerekli)** Arama sorgusu dizesi (maks 400 karakter).       |
| `country`     | Yer hedeflemesi için iki harfli ülke kodu.                |
| `search_lang` | Sonuçlar için iki harfli dil kodu.                     |
| `count`       | Döndürülecek maksimum sonuç sayısı (1–50).                   |
| `offset`      | Sonuçların ilk N sayfasını atla (0–9).                  |
| `safesearch`  | İçerik filtresi: `"off"`, `"moderate"` veya `"strict"`.     |
| `freshness`   | Yenilik filtresi (Web Araması ile aynı seçenekler).              |
| `goggles`     | Özel yeniden sıralama için Brave Goggles URL'si ve/veya kaynağı. |

Tam parametre ve başlık referansı için bkz. [Brave Haber Araması API'si belgeleri](https://api-dashboard.search.brave.com/api-reference/news/news_search/get).

### BraveImageSearchTool

| Parametre     | Açıklama                                         |
| ------------- | --------------------------------------------------- |
| `q`           | **(gerekli)** Arama sorgusu dizesi (maks 400 karakter). |
| `country`     | Yer hedeflemesi için iki harfli ülke kodu.          |
| `search_lang` | Sonuçlar için iki harfli dil kodu.               |
| `count`       | Döndürülecek maksimum sonuç sayısı (1–200).            |
| `safesearch`  | İçerik filtresi: `"off"` veya `"strict"`.              |
| `spellcheck`  | Sorguda yazım hatalarını düzeltmeyi dene.    |

Tam parametre ve başlık referansı için bkz. [Brave Görüntü Araması API'si belgeleri](https://api-dashboard.search.brave.com/api-reference/images/image_search).

### BraveVideoSearchTool

| Parametre     | Açıklama                                           |
| ------------- | ----------------------------------------------------- |
| `q`           | **(gerekli)** Arama sorgusu dizesi (maks 400 karakter).   |
| `country`     | Yer hedeflemesi için iki harfli ülke kodu.            |
| `search_lang` | Sonuçlar için iki harfli dil kodu.                 |
| `count`       | Döndürülecek maksimum sonuç sayısı (1–50).               |
| `offset`      | Sonuçların ilk N sayfasını atla (0–9).              |
| `safesearch`  | İçerik filtresi: `"off"`, `"moderate"` veya `"strict"`. |
| `freshness`   | Yenilik filtresi (Web Araması ile aynı seçenekler).          |

Tam parametre ve başlık referansı için bkz. [Brave Video Araması API'si belgeleri](https://api-dashboard.search.brave.com/api-reference/videos/video_search/get).

### BraveLocalPOIsTool

| Parametre     | Açıklama                                                            |
| ------------- | ---------------------------------------------------------------------- |
| `ids`         | **(gerekli)** İstenen konum için benzersiz tanımlayıcıların listesi. |
| `search_lang` | Sonuçlar için iki harfli dil kodu.                                  |

For the complete parameter and header reference, see [Brave Local POIs API documentation](https://api-dashboard.search.brave.com/api-reference/web/local_pois).

### BraveLocalPOIsDescriptionTool

| Parameter | Description                                                            |
| --------- | ---------------------------------------------------------------------- |
| `ids`     | **(required)** A list of unique identifiers for the desired locations. |

Tam parametre ve başlık referansı için bkz. [Brave POI Açıklamaları API'si belgeleri](https://api-dashboard.search.brave.com/api-reference/web/poi_descriptions).

## Özel Başlıklar

Tüm araçlar özel HTTP istek başlıklarını destekler. Örneğin Web Araması aracı, konum açısından farkında sonuçlar için yer bilgisi başlıklarını kabul eder:

```python Code theme={null}
from crewai_tools import BraveWebSearchTool

tool = BraveWebSearchTool(
    headers={
        "x-loc-lat": "37.7749",
        "x-loc-long": "-122.4194",
        "x-loc-city": "San Francisco",
        "x-loc-state": "CA",
        "x-loc-country": "US",
    }
)

results = tool.run(q="best coffee shops nearby")
```

Ayrıca `set_headers()` yöntemini kullanarak başlatmadan sonra başlıkları güncelleyebilirsiniz:

```python Code theme={null}
tool.set_headers({"api-version": "2025-01-01"})
```

## Ham Mod

Varsayılan olarak, her araç API yanıtını kısa bir sonuç listesine dönüştürür. Tam, işlenmemiş API yanıtına ihtiyacınız varsa, ham modu etkinleştirin:

```python Code theme={null}
from crewai_tools import BraveWebSearchTool

tool = BraveWebSearchTool(raw=True)
full_response = tool.run(q="Brave Search API")
```

## Ajan Entegrasyonu Örneği

CrewAI ajanını birden fazla Brave Search aracıyla nasıl donatılacağını şöyle gösterilmiştir:

```python Code theme={null}
from crewai import Agent
from crewai.project import agent
from crewai_tools import BraveWebSearchTool, BraveNewsSearchTool

web_search = BraveWebSearchTool()
news_search = BraveNewsSearchTool()

@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config["researcher"],
        tools=[web_search, news_search],
    )
```

## Gelişmiş Örnek

Hedeflenen bir arama için birden fazla parametreyi birleştirme:

```python Code theme={null}
from crewai_tools import BraveWebSearchTool

tool = BraveWebSearchTool(
    requests_per_second=0.5,  # conservative rate limit
    save_file=True,
)

results = tool.run(
    q="artificial intelligence news",
    country="US",
    search_lang="en",
    count=5,
    freshness="pm",           # sadece geçen ay
    extra_snippets=True,
)
print(results)
```

## `BraveSearchTool` (Eski) Sürümünden Geçiş

Şu anda `BraveSearchTool` kullanıyorsanız, yeni araçlara geçiş kolaydır:

```python Code theme={null}
# Öncesi (eski)
from crewai_tools import BraveSearchTool

tool = BraveSearchTool(country="US", n_results=5, save_file=True)
results = tool.run(search_query="AI agents")

# Sonrası (önerilen)
from crewai_tools import BraveWebSearchTool

tool = BraveWebSearchTool(save_file=True)
results = tool.run(q="AI agents", country="US", count=5)
```

Temel farklılıklar:

* **İçe Aktarma**: `BraveSearchTool` yerine `BraveWebSearchTool` (veya haber/görüntü/video varyantı) kullanın.
* **Sorgu parametresi**: `search_query` yerine `q` kullanın. (Kolaylık için hem `search_query` hem de `query` hala kabul edilir, ancak `q` tercih edilen parametredir.)
* **Sonuç sayısı**: `n_results` yerine `count` öğesini sorgu parametresi olarak geçin.
* **Ülke**: `country`'yi başlatma sırası yerine sorgu parametresi olarak geçin.
* **API anahtarı**: `BRAVE_API_KEY` ortam değişkenine ek olarak artık `api_key=` aracılığıyla doğrudan geçilebilir.
* **Hız sınırlama**: `requests_per_second` aracılığıyla yapılandırılabilir, `429` yanıtlarında otomatik yeniden deneme.

## Sonuç

Brave Search araç paketi, CrewAI ajanlarınıza Brave Search API'sine esnek, uç nokta özgü erişim sağlar. Web sayfalarına, son dakika haberlerine, görüntülere veya videolara ihtiyacınız olsun, doğrulanmış parametreler ve yerleşik dayanıklılığa sahip adanmış bir araç vardır. Kullanım durumunuza uygun aracı seçin ve kullanılabilir parametreler ve yanıt biçimleri hakkında tam ayrıntılar için [Brave Search API belgeleri](https://brave.com/search/api/) öğesine bakın.

