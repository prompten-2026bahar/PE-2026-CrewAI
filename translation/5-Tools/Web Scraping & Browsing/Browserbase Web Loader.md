> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Browserbase Web Yükleyici

> Browserbase, headless tarayıcıları güvenilir şekilde çalıştırmak, yönetmek ve izlemek için geliştirici platformudur.

# `BrowserbaseLoadTool`

## Açıklama

[Browserbase](https://browserbase.com), headless tarayıcıları güvenilir şekilde çalıştırmak, yönetmek ve izlemek için geliştirici platformudur.

Yapay zeka veri toplama işlerinizi şu özelliklerle güçlendirin:

* Karmaşık arayüzlerden veri çıkarmak için güvenilir tarayıcılar sağlayan [Serverless Infrastructure](https://docs.browserbase.com/under-the-hood)
* Parmak izi taktikleri ve otomatik captcha çözümü içeren [Stealth Mode](https://docs.browserbase.com/features/stealth-mode)
* Ağ zaman çizelgesi ve günlüklerle tarayıcı oturumunuzu incelemek için [Session Debugger](https://docs.browserbase.com/features/sessions)
* Otomasyonunuzu hızlıca hata ayıklamak için [Live Debug](https://docs.browserbase.com/guides/session-debug-connection/browser-remote-control)

## Kurulum

* [browserbase.com](https://browserbase.com) üzerinden bir API anahtarı ve Proje Kimliği alın ve bunları ortam değişkenlerine (`BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID`) ayarlayın.
* [Browserbase SDK](http://github.com/browserbase/python-sdk) ile birlikte `crewai[tools]` paketini kurun:

```shell  theme={null}
pip install browserbase 'crewai[tools]'
```

## Örnek

Ajanınızın web sitelerini yükleyebilmesi için BrowserbaseLoadTool'u aşağıdaki gibi kullanın:

```python Code theme={null}
from crewai_tools import BrowserbaseLoadTool

# Aracı Browserbase API anahtarı ve Proje Kimliği ile başlatın
tool = BrowserbaseLoadTool()
```

## Argümanlar

`BrowserbaseLoadTool` davranışını özelleştirmek için aşağıdaki parametreler kullanılabilir:

| Argument          | Type     | Description                                                                           |
| :---------------- | :------- | :------------------------------------------------------------------------------------ |
| **api\_key**      | `string` | *İsteğe bağlı*. Browserbase API anahtarı. Varsayılan `BROWSERBASE_API_KEY` ortam değişkenidir.       |
| **project\_id**   | `string` | *İsteğe bağlı*. Browserbase Proje Kimliği. Varsayılan `BROWSERBASE_PROJECT_ID` ortam değişkenidir. |
| **text\_content** | `bool`   | *İsteğe bağlı*. Yalnızca metin içeriğini getirir. Varsayılan `False`.                           |
| **session\_id**   | `string` | *İsteğe bağlı*. Mevcut bir Oturum Kimliği sağlayın.                                           |
| **proxy**         | `bool`   | *İsteğe bağlı*. Proxy'leri etkinleştirir/devre dışı bırakır. Varsayılan `False`.                               |
