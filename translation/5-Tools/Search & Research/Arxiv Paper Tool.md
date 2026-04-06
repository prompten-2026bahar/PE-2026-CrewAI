> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Arxiv Makale Aracı

> `ArxivPaperTool`, bir sorguyla eşleşen arXiv makalelerini arar ve isteğe bağlı olarak PDF'leri indirir.

# `ArxivPaperTool`

## Açıklama

`ArxivPaperTool`, akademik makaleler için arXiv API'sini sorgular ve kompakt, okunabilir sonuçlar döndürür. Ayrıca isteğe bağlı olarak PDF'leri diske indirebilir.

## Kurulum

Bu araç `crewai-tools` dışında özel kuruluma ihtiyaç duymaz.

```shell  theme={null}
uv add crewai-tools
```

API anahtarı gerekli değildir. Bu araç herkese açık arXiv Atom API'sini kullanır.

## Başlamak İçin Adımlar

1. Aracı başlatın.
2. Bir `search_query` sağlayın (ör. "transformer neural network").
3. İsteğe bağlı olarak `max_results` (1–100) ayarlayın ve yapıcıda PDF indirmelerini etkinleştirin.

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import ArxivPaperTool

tool = ArxivPaperTool(
    download_pdfs=False,
    save_dir="./arxiv_pdfs",
    use_title_as_filename=True,
)

agent = Agent(
    role="Researcher",
    goal="Find relevant arXiv papers",
    backstory="Expert at literature discovery",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="Search arXiv for 'transformer neural network' and list top 5 results.",
    expected_output="A concise list of 5 relevant papers with titles, links, and summaries.",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

### Doğrudan kullanım (Ajan olmadan)

```python Code theme={null}
from crewai_tools import ArxivPaperTool

tool = ArxivPaperTool(
    download_pdfs=True, 
    save_dir="./arxiv_pdfs",
)
print(tool.run(search_query="mixture of experts", max_results=3))
```

## Parametreler

### Başlangıç Parametreleri

* `download_pdfs` (bool, varsayılan `False`): PDF'leri indirip indirmeyeceği.
* `save_dir` (str, varsayılan `./arxiv_pdfs`): PDF'lerin kaydedileceği dizin.
* `use_title_as_filename` (bool, varsayılan `False`): Dosya adları için makale başlıklarını kullanın.

### Çalıştırma Parametreleri

* `search_query` (str, gerekli): arXiv arama sorgusu.
* `max_results` (int, varsayılan `5`, aralık 1–100): Sonuç sayısı.

## Çıktı formatı

Araç, aşağıdakilerle insan tarafından okunabilir bir makale listesi döndürür:

* Başlık
* Bağlantı (abs sayfası)
* Snippet/özet (kesik)

`download_pdfs=True` olduğunda, PDF'ler diske kaydedilir ve özet kaydedilen dosyaları söyler.

## Kullanım Notları

* Araç, anahtar meta veriler ve bağlantılarla biçimlendirilmiş metni döndürür.
* `download_pdfs=True` olduğunda, PDF'ler `save_dir` dizinine depolanacaktır.

## Sorun Giderme

* Ağ zaman aşımı aldıysanız, `max_results` değerini azaltın veya yeniden deneyin.
* Geçersiz XML hataları, arXiv yanıt ayrıştırma sorunu belirtir; daha basit bir sorgu deneyin.
* Dosya sistemi hataları (ör. izin reddedildi) PDF'ler kaydedilirken oluşabilir; `save_dir` yazılabilir olduğundan emin olun.

## İlişkili bağlantılar

* arXiv API dokümanları: [https://info.arxiv.org/help/api/index.html](https://info.arxiv.org/help/api/index.html)

## Hata İşleme

* Ağ sorunları, geçersiz XML ve OS hataları bilgilendirici mesajlarla işlenir.

