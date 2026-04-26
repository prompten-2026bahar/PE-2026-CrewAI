> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# PG RAG Arama

> `PGSearchTool`, PostgreSQL veritabanlarında arama yapmak ve en ilgili sonuçları döndürmek için tasarlanmıştır.

## Genel Bakış

<Note>
  PGSearchTool şu anda geliştirme aşamasındadır. Bu belge amaçlanan işlevselliği ve arayüzü özetler.
  Geliştirme ilerledikçe bazı özelliklerin mevcut olmayabileceğini veya değişebileceğini lütfen göz önünde bulundurun.
</Note>

## Açıklama

PGSearchTool, PostgreSQL veritabanı tabloları içinde anlamsal aramaları kolaylaştırmak için güçlü bir araç olarak tasarlanmıştır. Gelişmiş Retrieve and Generate (RAG) teknolojisinden yararlanarak,
özellikle PostgreSQL veritabanları için uyarlanmış, tablo içeriğini sorgulamanın verimli bir yolunu sunmayı amaçlar.
Aracın hedefi, anlamsal arama sorguları aracılığıyla ilgili veriyi bulma sürecini basitleştirmek ve PostgreSQL ortamında geniş veri kümeleri üzerinde gelişmiş sorgular yapması gereken kullanıcılar için
değerli bir kaynak sunmaktır.

## Kurulum

Yayınlandığında PGSearchTool'u içerecek olan `crewai_tools` paketi aşağıdaki komutla kurulabilir:

```shell  theme={null}
pip install 'crewai[tools]'
```

<Note>
  PGSearchTool, `crewai_tools` paketinin mevcut sürümünde henüz mevcut değildir. Araç yayınlandığında bu kurulum komutu güncellenecektir.
</Note>

## Kullanım Örneği

Aşağıda, PGSearchTool'un bir PostgreSQL veritabanındaki bir tablo üzerinde anlamsal arama yapmak için nasıl kullanılacağını gösteren öneri niteliğinde bir örnek yer almaktadır:

```python Code theme={null}
from crewai_tools import PGSearchTool

# Aracı veritabanı URI'si ve hedef tablo adı ile başlat
tool = PGSearchTool(
    db_uri='postgresql://user:password@localhost:5432/mydatabase', 
    table_name='employees'
)
```

## Argümanlar

PGSearchTool'un çalışması için aşağıdaki argümanları gerektirmesi amaçlanmaktadır:

| Argument        | Type     | Description                                                                                                                                                                                                    |
| :-------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **db\_uri**     | `string` | **Zorunlu**. Sorgulanacak PostgreSQL veritabanının URI'sini temsil eden string. Bu argüman zorunlu olacaktır ve gerekli kimlik doğrulama ayrıntılarını ve veritabanının konumunu içermelidir. |
| **table\_name** | `string` | **Zorunlu**. Anlamsal aramanın yapılacağı veritabanı içindeki tablonun adını belirten string. Bu argüman da zorunlu olacaktır.                                             |

## Özel Model ve Embedding'ler

Araç, varsayılan olarak hem embedding hem de özetleme için OpenAI kullanmayı amaçlamaktadır. Kullanıcılar, modeli aşağıdaki gibi bir config sözlüğü ile özelleştirebilecektir:

```python Code theme={null}
tool = PGSearchTool(
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
