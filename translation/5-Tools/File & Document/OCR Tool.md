> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# OCR Aracı

> `OCRTool`, görsel anlayışına sahip bir LLM kullanarak yerel görsellerden veya görsel URL'lerinden metin çıkarır.

# `OCRTool`

## Açıklama

Görsellerden (yerel yol veya URL) metin çıkarır. CrewAI'nin LLM arayüzü üzerinden görsel yetenekli bir LLM kullanır.

## Kurulum

`crewai-tools` dışında ek kurulum gerekmez. Seçtiğiniz LLM'in görsel desteğine sahip olduğundan emin olun.

## Parametreler

### Çalıştırma Parametreleri

* `image_path_url` (str, gerekli): Yerel görsel yolu veya HTTP(S) URL'si.

## Örnekler

### Doğrudan kullanım

```python Code theme={null}
from crewai_tools import OCRTool

print(OCRTool().run(image_path_url="/tmp/receipt.png"))
```

### Bir ajan ile

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import OCRTool

ocr = OCRTool()

agent = Agent(
    role="OCR", 
    goal="Metni çıkar", 
    tools=[ocr],
)

task = Task(
    description="https://example.com/invoice.jpg görselinden metni çıkar", 
    expected_output="Algılanan tüm metin düz metin olarak",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

## Notlar

* Seçilen LLM'in görsel girdilerini desteklediğinden emin olun.
* Büyük görseller için token kullanımını azaltmak amacıyla küçültme yapmayı değerlendirin.
* Gerekirse README yönergelerine uygun şekilde araca belirli bir LLM örneği (ör. `LLM(model="gpt-4o")`) verebilirsiniz.

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import OCRTool

tool = OCRTool()

agent = Agent(
    role="OCR Uzmanı",
    goal="Görsellerden metin çıkar",
    backstory="Görsel yetenekli analist",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="https://example.com/receipt.png görselinden metni çıkar",
    expected_output="Algılanan tüm metin düz metin olarak",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```
