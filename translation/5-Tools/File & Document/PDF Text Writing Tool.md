> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# PDF Metin Yazma Aracı

> `PDFTextWritingTool`, özel yazı tiplerini destekleyerek PDF içinde belirli konumlara metin yazar.

# `PDFTextWritingTool`

## Açıklama

Bir PDF sayfasında hassas koordinatlara metin yazar; isteğe bağlı olarak özel bir TrueType yazı tipi gömebilir.

## Parametreler

### Çalıştırma Parametreleri

* `pdf_path` (str, gerekli): Girdi PDF dosyasının yolu.
* `text` (str, gerekli): Eklenecek metin.
* `position` (tuple\[int, int], gerekli): `(x, y)` koordinatları.
* `font_size` (int, default `12`)
* `font_color` (str, default `"0 0 0 rg"`)
* `font_name` (str, default `"F1"`)
* `font_file` (str, isteğe bağlı): `.ttf` dosyasının yolu.
* `page_number` (int, default `0`)

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import PDFTextWritingTool

tool = PDFTextWritingTool()

agent = Agent(
    role="PDF Düzenleyici",
    goal="PDF'leri açıklama notlarıyla işaretle",
    backstory="Dokümantasyon uzmanı",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="./sample.pdf dosyasının 1. sayfasında (72, 720) konumuna 'CONFIDENTIAL' yaz",
    expected_output="Onay mesajı",
    agent=agent,
)

crew = Crew(
    agents=[agent], 
    tasks=[task],
    verbose=True,
)

result = crew.kickoff()
```

### Doğrudan kullanım

```python Code theme={null}
from crewai_tools import PDFTextWritingTool

PDFTextWritingTool().run(
  pdf_path="./input.pdf",
  text="CONFIDENTIAL",
  position=(72, 720),
  font_size=18,
  page_number=0,
)
```

## İpuçları

* Koordinat başlangıç noktası sol alt köşedir.
* Özel bir yazı tipi (`font_file`) kullanıyorsanız geçerli bir `.ttf` dosyası olduğundan emin olun.
