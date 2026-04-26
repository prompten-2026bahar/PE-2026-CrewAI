> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Google Serper Araması

> `SerperDevTool`, interneti araştırmak ve en alakalı sonuçları döndürmek için tasarlanmıştır.

# `SerperDevTool`

## Açıklama

Bu araç, metindeki içerikten belirli bir sorgu için anlamsal arama yapmak ve internet genelinde en alakalı arama sonuçlarını getirmek ve göstermek için tasarlanmıştır. [serper.dev](https://serper.dev) API'sini kullanarak, kullanıcı tarafından sağlanan sorguya göre en alakalı arama sonuçlarını getirir ve gösterir.

## Kurulum

`SerperDevTool`'u etkili bir şekilde kullanmak için aşağıdaki adımları izleyin:

1. **Paket Kurulumu**: `crewai[tools]` paketinin Python ortamınızda yüklü olduğundan emin olun.
2. **API Anahtarı Alma**: [https://serper.dev/](https://serper.dev/) adresinde `serper.dev` API anahtarı alın (ücretsiz katman mevcut).
3. **Ortam Yapılandırması**: Elde ettiğiniz API anahtarını `SERPER_API_KEY` adlı bir ortam değişkeninde saklayın.

Bu aracı projenize dahil etmek için, aşağıdaki kurulum talimatlarını izleyin:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

Aşağıdaki örnek, aracı başlatmanız ve verilen bir sorgu ile bir arama yürütmenüzün nasıl yapılacağını göstermektedir:

```python Code theme={null}
from crewai_tools import SerperDevTool

# İnternet arama yetenekleri için aracı başlat
tool = SerperDevTool()
```

## Parametreler

`SerperDevTool` API'ye iletilecek birkaç parametreye sahiptir:

* **search\_url**: Arama API'si için URL uç noktası. (Varsayılan `https://google.serper.dev/search` olarak ayarlanmıştır)

* **country**: İsteğe bağlı. Arama sonuçları için ülkeyi belirtin.

* **location**: İsteğe bağlı. Arama sonuçları için konumu belirtin.

* **locale**: İsteğe bağlı. Arama sonuçları için yerel ayarları belirtin.

* **n\_results**: Döndürülecek arama sonuçlarının sayısı. Varsayılan `10` olarak ayarlanmıştır.

`country`, `location`, `locale` ve `search_url` değerleri [Serper Playground](https://serper.dev/playground) adresinde bulunabilir.

## Parametrelerle Örnek

Aşağıda aracını ek parametrelerle kullanmanın bir örneği bulunmaktadır:

```python Code theme={null}
from crewai_tools import SerperDevTool

tool = SerperDevTool(
    search_url="https://google.serper.dev/scholar",
    n_results=2,
)

print(tool.run(search_query="ChatGPT"))

# Araç Kullanılıyor: İnternette Ara

# Arama sonuçları: Başlık: Halk sağlığında sohbet GPT'nin rolü
# Bağlantı: https://link.springer.com/article/10.1007/s10439-023-03172-7
# Snippet: … halk sağlığında ChatGPT. Bu genel bakışta, ChatGPT'nin olası kullanımlarını inceleyeceğiz
# ---
# Başlık: Küresel ısınmada sohbet GPT potansiyel kullanımı
# Bağlantı: https://link.springer.com/article/10.1007/s10439-023-03171-8
# Snippet: … ChatGPT gibi, iklim değişikliğimizi anlamamızda kritik bir rol oynama potansiyeline sahiptir
# ---

```

```python Code theme={null}
from crewai_tools import SerperDevTool

tool = SerperDevTool(
    country="fr",
    locale="fr",
    location="Paris, Paris, Ile-de-France, France",
    n_results=2,
)

print(tool.run(search_query="Jeux Olympiques"))

# Araç Kullanılıyor: İnternette Ara

# Arama sonuçları: Başlık: Jeux Olympiques de Paris 2024 - Actualités, calendriers, résultats
# Bağlantı: https://olympics.com/fr/paris-2024
# Snippet: Quels sont les sports présents aux Jeux Olympiques de Paris 2024 ? · Athlétisme · Aviron · Badminton · Basketball · Basketball 3x3 · Boxe · Breaking · Canoë ...
# ---
# Başlık: Billetterie Officielle de Paris 2024 - Jeux Olympiques et Paralympiques
# Bağlantı: https://tickets.paris2024.org/
# Snippet: Achetez vos billets exclusivement sur le site officiel de la billetterie de Paris 2024 pour participer au plus grand événement sportif au monde.
# ---
```

## Sonuç

`SerperDevTool`'u Python projelerine entegre ederek, kullanıcılar uygulamalarından doğrudan internet genelinde gerçek zamanlı, ilgili aramalar yapabilme yeteneği elde ederler.
Güncellenen parametreler daha özelleştirilmiş ve yerelleştirilmiş arama sonuçlarına izin verir. Sağlanan kurulum ve kullanım yönergeleri takip ederek, bu aracını projelere dahil etmek basit ve doğrudandır.

