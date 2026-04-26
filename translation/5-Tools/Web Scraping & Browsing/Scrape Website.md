> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Web Sitesi Scrape Etme

> `ScrapeWebsiteTool`, belirtilen bir web sitesinin içeriğini çıkarmak ve okumak için tasarlanmıştır.

# `ScrapeWebsiteTool`

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

Belirtilen bir web sitesinin içeriğini çıkarmak ve okumak için tasarlanmış bir araçtır. HTTP istekleri yaparak ve alınan HTML içeriğini ayrıştırarak çeşitli türde web sayfalarını işleyebilir.
Bu araç özellikle web scraping görevleri, veri toplama veya web sitelerinden belirli bilgileri çıkarma için kullanışlı olabilir.

## Kurulum

crewai\_tools paketini kurun

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

```python  theme={null}
from crewai_tools import ScrapeWebsiteTool

# Çalışması sırasında bulduğu herhangi bir web sitesini scrape etmesini sağlamak için
tool = ScrapeWebsiteTool()

# Aracı web sitesi URL'si ile başlat;
# böylece ajan yalnızca belirtilen web sitesinin içeriğini scrape edebilsin
tool = ScrapeWebsiteTool(website_url='https://www.example.com')

# Siteden metni çıkar
text = tool.run()
print(text)
```

## Argümanlar

| Argument         | Type     | Description                                                                                                                                        |
| :--------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **website\_url** | `string` | Dosyayı okumak için **zorunlu** web sitesi URL'si. Bu, hangi web sitesi içeriğinin scrape edilip okunacağını belirleyen aracın temel girdisidir. |
