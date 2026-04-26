> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# JSON RAG Arama

> `JSONSearchTool`, JSON dosyalarında arama yapmak ve en ilgili sonuçları döndürmek için tasarlanmıştır.

# `JSONSearchTool`

<Note>
  JSONSearchTool şu anda deneysel aşamadadır. Bu, aracın aktif olarak geliştirildiği
  ve kullanıcıların beklenmeyen davranışlar ya da değişikliklerle
  karşılaşabileceği anlamına gelir. Her türlü sorun veya iyileştirme
  önerisine dair geri bildirimi güçlü şekilde teşvik ediyoruz.
</Note>

## Açıklama

JSONSearchTool, JSON dosya içeriklerinde verimli ve hassas aramalar yapılmasını kolaylaştırmak için tasarlanmıştır. Belirli bir JSON dosyasında hedefli aramalar için kullanıcıların bir JSON yolu belirtmesine izin veren bir RAG (Retrieve and Generate) arama mekanizması kullanır. Bu yetenek, arama sonuçlarının doğruluğunu ve ilgililiğini önemli ölçüde artırır.

## Kurulum

JSONSearchTool'u kurmak için aşağıdaki pip komutunu kullanın:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Kullanım Örnekleri

Burada JSONSearchTool'u JSON dosyalarında arama yapmak için etkili şekilde nasıl kullanacağınızı gösteren güncellenmiş örnekler bulunmaktadır. Bu örnekler, kod tabanında belirlenen mevcut uygulama ve kullanım kalıplarını dikkate alır.

```python Code theme={null}
from crewai_tools import JSONSearchTool

# Genel JSON içerik araması
# Bu yaklaşım, JSON yolu önceden biliniyorsa veya dinamik olarak belirlenebiliyorsa uygundur.
tool = JSONSearchTool()

# Aramayı belirli bir JSON dosyasıyla sınırlandırma
# Arama kapsamını belirli bir JSON dosyasıyla kısıtlamak istediğinizde bu başlatma yöntemini kullanın.
tool = JSONSearchTool(json_path='./path/to/your/file.json')
```

## Argümanlar

* `json_path` (str, isteğe bağlı): Aranacak JSON dosyasının yolunu belirtir. Araç genel arama için başlatıldıysa bu argüman gerekli değildir. Verildiğinde aramayı belirtilen JSON dosyasıyla sınırlar.

## Yapılandırma Seçenekleri

JSONSearchTool, bir yapılandırma sözlüğü aracılığıyla kapsamlı özelleştirmeyi destekler. Bu, kullanıcıların gereksinimlerine göre embedding ve özetleme için farklı modeller seçmesine olanak tanır.

```python Code theme={null}
tool = JSONSearchTool(
    config={
        "llm": {
            "provider": "ollama",  # Other options include google, openai, anthropic, llama2, etc.
            "config": {
                "model": "llama2",
                # Additional optional configurations can be specified here.
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            },
        },
        "embedding_model": {
            "provider": "google-generativeai", # or openai, ollama, ...
            "config": {
                "model_name": "gemini-embedding-001",
                "task_type": "RETRIEVAL_DOCUMENT",
                # Further customization options can be added here.
            },
        },
    }
)
```
