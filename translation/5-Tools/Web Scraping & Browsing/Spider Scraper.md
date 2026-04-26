> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Spider Scraper

> `SpiderTool`, Spider kullanarak belirtilen bir web sitesinin içeriğini çıkarmak ve okumak için tasarlanmıştır.

# `SpiderTool`

## Açıklama

[Spider](https://spider.cloud/?ref=crewai) is the [fastest](https://github.com/spider-rs/spider/blob/main/benches/BENCHMARKS.md#benchmark-results)
açık kaynak scraper ve crawler'dır ve LLM'e hazır veri döndürür.
Herhangi bir web sitesini saf HTML, markdown, metadata veya metne dönüştürürken yapay zeka kullanarak özel eylemlerle tarama yapmanıza olanak tanır.

## Kurulum

`SpiderTool` kullanmak için [Spider SDK](https://pypi.org/project/spider-client/)
ve ayrıca `crewai[tools]` SDK'sını indirmeniz gerekir:

```shell  theme={null}
pip install spider-client 'crewai[tools]'
```

## Örnek

Bu örnek, `SpiderTool` kullanarak ajanınızın web sitelerini scrape etmesini ve taramasını nasıl sağlayabileceğinizi gösterir.
Spider API'den dönen veri zaten LLM'e hazırdır; bu nedenle ayrıca temizleme yapmanıza gerek yoktur.

```python Code theme={null}
from crewai_tools import SpiderTool

def main():
    spider_tool = SpiderTool()

    searcher = Agent(
        role="Web Araştırma Uzmanı",
        goal="Belirli URL'lerden ilgili bilgileri bul",
        backstory="Web'i son derece iyi kullanan uzman bir web araştırmacısı",
        tools=[spider_tool],
        verbose=True,
    )

    return_metadata = Task(
        description="https://spider.cloud adresini 1 sınırıyla scrape et ve metadata'yı etkinleştir",
        expected_output="spider.cloud için metadata ve 10 kelimelik özet",
        agent=searcher
    )

    crew = Crew(
        agents=[searcher],
        tasks=[
            return_metadata,
        ],
        verbose=2
    )

    crew.kickoff()

if __name__ == "__main__":
    main()
```

## Argümanlar

| Argument                | Type     | Description                                                                                                                       |
| :---------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **api\_key**            | `string` | Spider API anahtarını belirtir. Belirtilmezse ortam değişkenlerindeki `SPIDER_API_KEY` aranır.                               |
| **params**              | `object` | İstek için isteğe bağlı parametreler. Varsayılan olarak içeriği LLM'ler için optimize etmek amacıyla `{"return_format": "markdown"}` kullanılır.                    |
| **request**             | `string` | Gerçekleştirilecek istek türü (`http`, `chrome`, `smart`). `smart` varsayılan olarak HTTP kullanır, gerekirse JavaScript render etmeye geçer.    |
| **limit**               | `int`    | Web sitesi başına taranacak maksimum sayfa sayısı. Sınırsız için `0` yapın veya boş bırakın.                                                                 |
| **depth**               | `int`    | Maksimum tarama derinliği. Sınırsız için `0` yapın.                                                                                         |
| **cache**               | `bool`   | Tekrarlanan çalıştırmaları hızlandırmak için HTTP önbelleğini etkinleştirir. Varsayılan `true`.                                                                |
| **budget**              | `object` | Taranan sayfalar için yol tabanlı sınırlar belirler; ör. yalnızca kök sayfa için `{"*":1}`.                                                     |
| **locale**              | `string` | İstek için yerel ayar; ör. `en-US`.                                                                                            |
| **cookies**             | `string` | İstek için HTTP çerezleri.                                                                                                     |
| **stealth**             | `bool`   | Tespit edilmemek için Chrome isteklerinde stealth modunu etkinleştirir. Varsayılan `true`.                                                   |
| **headers**             | `object` | Tüm istekler için anahtar-değer eşlemeli HTTP başlıkları.                                                                        |
| **metadata**            | `bool`   | Sayfalar ve içerik hakkında metadata saklar; yapay zeka birlikte çalışabilirliğine yardımcı olur. Varsayılan `false`.                                         |
| **viewport**            | `object` | Chrome viewport boyutlarını ayarlar. Varsayılan `800x600`.                                                                            |
| **encoding**            | `string` | Kodlama türünü belirtir; ör. `UTF-8`, `SHIFT_JIS`.                                                                              |
| **subdomains**          | `bool`   | Alt alan adlarını taramaya dahil eder. Varsayılan `false`.                                                                             |
| **user\_agent**         | `string` | Özel HTTP user agent. Varsayılan olarak rastgele bir agent kullanılır.                                                                               |
| **store\_data**         | `bool`   | İstek için veri depolamayı etkinleştirir. Ayarlandığında `storageless` değerini geçersiz kılar. Varsayılan `false`.                                       |
| **gpt\_config**         | `object` | Yapay zekanın tarama eylemleri üretmesine izin verir; `"prompt"` için dizi yoluyla isteğe bağlı zincirleme adımlar desteklenir.                                    |
| **fingerprint**         | `bool`   | Chrome için gelişmiş parmak izi özelliklerini etkinleştirir.                                                                                       |
| **storageless**         | `bool`   | Yapay zeka embedding'leri dahil tüm veri depolamayı engeller. Varsayılan `false`.                                                           |
| **readability**         | `bool`   | İçeriği [Mozilla’s readability](https://github.com/mozilla/readability) ile okumaya uygun hale getirmek için ön işler. LLM'ler için içeriği iyileştirir. |
| **return\_format**      | `string` | Verinin döneceği biçim: `markdown`, `raw`, `text`, `html2text`. Varsayılan sayfa biçimi için `raw` kullanın.                                 |
| **proxy\_enabled**      | `bool`   | Ağ düzeyindeki engellemeleri önlemek için yüksek performanslı proxy'leri etkinleştirir.                                                                 |
| **query\_selector**     | `string` | İşaretlemeden içerik çıkarmak için CSS sorgu seçicisi.                                                                            |
| **full\_resources**     | `bool`   | Web sitesine bağlı tüm kaynakları indirir.                                                                                    |
| **request\_timeout**    | `int`    | İstekler için saniye cinsinden zaman aşımı (5-60). Varsayılan `30`.                                                                          |
| **run\_in\_background** | `bool`   | İsteği arka planda çalıştırır; veri depolama ve pano üzerinden tarama tetikleme için kullanışlıdır. `storageless` ayarlıysa etkisi yoktur.   |
