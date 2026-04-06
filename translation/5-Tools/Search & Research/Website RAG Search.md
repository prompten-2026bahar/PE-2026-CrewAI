> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Web Sitesi RAG Arama

> `WebsiteSearchTool`, bir web sitesinin içeriğinde RAG (Retrieval-Augmented Generation) araması yapmak için tasarlanmıştır.

# `WebsiteSearchTool`

<Note>
  WebsiteSearchTool şu anda deneysel aşamadadır. Bu aracı araç setimize dahil etmek için aktif olarak çalışıyoruz ve dokümantasyonu buna göre güncelleyeceğiz.
</Note>

## Açıklama

WebsiteSearchTool, web sitelerinin içeriğinde anlamsal aramalar yapmak için bir kavram olarak tasarlanmıştır.
Belirtilen URL’lerden verimli şekilde gezinmek ve bilgi çıkarmak için Retrieval-Augmented Generation (RAG) gibi gelişmiş makine öğrenimi modellerinden yararlanmayı amaçlar.
Bu araç, kullanıcıların herhangi bir web sitesinde arama yapmasına veya ilgilenilen belirli web sitelerine odaklanmasına olanak tanıyarak esneklik sunmayı hedefler.
Lütfen WebsiteSearchTool’un mevcut uygulama ayrıntılarının geliştirme aşamasında olduğunu ve burada açıklanan işlevlerin henüz erişilebilir olmayabileceğini unutmayın.

## Kurulum

WebsiteSearchTool kullanılabilir hale geldiğinde ortamınızı hazırlamak için temel paketi şu komutla kurabilirsiniz:

```shell  theme={null}
pip install 'crewai[tools]'
```

Bu komut, araç tam olarak entegre edildiğinde kullanıcıların hemen kullanmaya başlayabilmesi için gerekli bağımlılıkları kurar.

## Kullanım Örneği

Aşağıda WebsiteSearchTool’un farklı senaryolarda nasıl kullanılabileceğini gösteren örnekler yer almaktadır. Lütfen bu örneklerin açıklayıcı olduğunu ve planlanan işlevselliği temsil ettiğini unutmayın:

```python Code theme={null}
from crewai_tools import WebsiteSearchTool

# Ajanların keşfettikleri herhangi bir web sitesinde
# arama yapabilmesi için aracı başlatma örneği
tool = WebsiteSearchTool()

# Aramayı belirli bir web sitesinin içeriğiyle sınırlama örneği;
# böylece ajanlar yalnızca o web sitesinde arama yapabilir
tool = WebsiteSearchTool(website='https://example.com')
```

## Argümanlar

* `website`: Odaklı aramalar için web sitesi URL’sini belirtmeyi amaçlayan isteğe bağlı argüman. Bu argüman, gerektiğinde hedefli aramaya izin vererek aracın esnekliğini artırmak üzere tasarlanmıştır.

## Özelleştirme Seçenekleri

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code theme={null}
tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google-generativeai", # or openai, ollama, ...
            config=dict(
                model_name="gemini-embedding-001",
                task_type="RETRIEVAL_DOCUMENT",
                # title="Embeddings",
            ),
        ),
    )
)
```
