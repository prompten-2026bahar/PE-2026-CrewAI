> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# MySQL RAG Arama

> `MySQLSearchTool`, MySQL veritabanlarında arama yapmak ve en ilgili sonuçları döndürmek için tasarlanmıştır.

## Genel Bakış

Bu araç, MySQL veritabanı tabloları içinde anlamsal aramaları kolaylaştırmak için tasarlanmıştır. RAG (Retrieve and Generate) teknolojisinden yararlanarak,
MySQLSearchTool kullanıcılara, özellikle MySQL veritabanları için uyarlanmış veritabanı tablo içeriğini sorgulamanın verimli bir yolunu sunar.
Anlamsal arama sorguları aracılığıyla ilgili veriyi bulma sürecini basitleştirir; bu da onu MySQL veritabanı içindeki geniş veri kümeleri üzerinde
gelişmiş sorgular yapması gereken kullanıcılar için çok değerli bir kaynak haline getirir.

## Kurulum

`crewai_tools` paketini kurmak ve MySQLSearchTool'u kullanmak için terminalinizde aşağıdaki komutu çalıştırın:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

Aşağıda, MySQLSearchTool'un bir MySQL veritabanındaki tablo üzerinde anlamsal arama yapmak için nasıl kullanılacağını gösteren bir örnek bulunmaktadır:

```python Code theme={null}
from crewai_tools import MySQLSearchTool

# Aracı veritabanı URI'si ve hedef tablo adı ile başlat
tool = MySQLSearchTool(
    db_uri='mysql://user:password@localhost:3306/mydatabase',
    table_name='employees'
)
```

## Argümanlar

MySQLSearchTool, çalışması için aşağıdaki argümanları gerektirir:

* `db_uri`: Sorgulanacak MySQL veritabanının URI'sini temsil eden string. Bu argüman zorunludur ve gerekli kimlik doğrulama ayrıntılarını ve veritabanının konumunu içermelidir.
* `table_name`: Anlamsal aramanın yapılacağı veritabanı içindeki tablonun adını belirten string. Bu argüman zorunludur.

## Özel model ve embedding'ler

Varsayılan olarak araç hem embedding hem özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code theme={null}
tool = MySQLSearchTool(
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
            provider="google-generativeai",
            config=dict(
                model_name="gemini-embedding-001",
                task_type="RETRIEVAL_DOCUMENT",
                # title="Embeddings",
            ),
        ),
    )
)
```
