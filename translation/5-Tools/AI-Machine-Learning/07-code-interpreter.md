# Kod Yorumlayıcı (Code Interpreter)

> `CodeInterpreterTool`, Python 3 kodlarını güvenli ve izole bir ortamda yürütmek için tasarlanmış güçlü bir araçtır.

# `CodeInterpreterTool`

## Açıklama

`CodeInterpreterTool`, CrewAI ajanlarının otonom olarak oluşturdukları Python 3 kodlarını yürütmelerini sağlar. Bu işlevsellik; ajanların kod yazmasına, yürütmesine, sonuçları almasına ve bu bilgileri sonraki kararlarını ve eylemlerini şekillendirmek için kullanmasına olanak tanıdığı için özellikle değerlidir.

Bu aracı kullanmanın birkaç yolu vardır:

### Docker Konteyneri (Önerilen)

Birincil seçenektir. Kod, içeriğinden bağımsız olarak güvenliği sağlayan izole bir Docker konteynerinde çalışır. Sisteminizde Docker'ın kurulu ve çalışıyor olduğundan emin olun. Kurulu değilse [buradan](https://docs.docker.com/get-docker/) yükleyebilirsiniz.

### Sandbox Ortamı

Docker mevcut değilse (kurulu değilse veya herhangi bir nedenle erişilemiyorsa), kod "sandbox" adı verilen kısıtlı bir Python ortamında yürütülecektir. Bu ortam, birçok modül ve yerleşik işlev üzerinde katı kısıtlamalarla oldukça sınırlıdır.

### Güvensiz Yürütme (Unsafe Execution)

**ÜRETİM ORTAMLARI İÇİN ÖNERİLMEZ**
Bu mod, `sys`, `os` ve benzeri modüllere yönelik tehlikeli çağrılar dahil olmak üzere herhangi bir Python kodunun yürütülmesine izin verir. [Buradan](/en/tools/ai-ml/codeinterpretertool#enabling-unsafe-mode) bu modun nasıl etkinleştirileceğini kontrol edebilirsiniz.

## Günlüklendirme (Logging)

`CodeInterpreterTool`, seçilen yürütme stratejisini standart çıktıya (STDOUT) kaydeder.

## Kurulum

Bu aracı kullanmak için CrewAI araçları paketini yüklemeniz gerekir:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

Aşağıdaki örnek, `CodeInterpreterTool`'un bir CrewAI ajanıyla nasıl kullanılacağını gösterir:

```python Code theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeInterpreterTool

# Aracı başlatın
code_interpreter = CodeInterpreterTool()

# Aracı kullanan bir ajan tanımlayın
programmer_agent = Agent(
    role="Python Programcısı",
    goal="Sorunları çözmek için Python kodu yaz ve yürüt",
    backstory="Karmaşık sorunları çözmek için verimli kodlar yazabilen uzman bir Python programcısı.",
    tools=[code_interpreter],
    verbose=True,
)

# Kod oluşturma ve yürütme görevi örneği
coding_task = Task(
    description="Fibonacci dizisini 10. sayıya kadar hesaplayan ve sonucu yazdıran bir Python fonksiyonu yaz.",
    expected_output="10. sayıya kadar Fibonacci dizisi.",
    agent=programmer_agent,
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(
    agents=[programmer_agent],
    tasks=[coding_task],
    verbose=True,
    process=Process.sequential,
)
result = crew.kickoff()
```

Bir ajan oluştururken kod yürütmeyi doğrudan da etkinleştirebilirsiniz:

```python Code theme={null}
from crewai import Agent

# Kod yürütme yeteneği etkinleştirilmiş bir ajan oluşturun
programmer_agent = Agent(
    role="Python Programcısı",
    goal="Sorunları çözmek için Python kodu yaz ve yürüt",
    backstory="Karmaşık sorunları çözmek için verimli kodlar yazabilen uzman bir Python programcısı.",
    allow_code_execution=True,  # Bu, otomatik olarak CodeInterpreterTool'u ekler
    verbose=True,
)
```

### `unsafe_mode` Etkinleştirme

```python Code theme={null}
from crewai_tools import CodeInterpreterTool

code = """
import os
os.system("ls -la")
"""

CodeInterpreterTool(unsafe_mode=True).run(code=code)
```

## Parametreler

`CodeInterpreterTool`, başlatma sırasında aşağıdaki parametreleri kabul eder:

* **user\_dockerfile\_path**: Opsiyonel. Kod yorumlayıcı konteyneri için kullanılacak özel bir Dockerfile yolu.
* **user\_docker\_base\_url**: Opsiyonel. Konteyneri çalıştırmak için kullanılacak Docker daemon URL'si.
* **unsafe\_mode**: Opsiyonel. Kodun bir Docker konteyneri veya sandbox yerine doğrudan ana makinede çalıştırılıp çalıştırılmayacağı. Varsayılan: `False`. Dikkatli kullanın!
* **default\_image\_tag**: Opsiyonel. Varsayılan Docker imaj etiketi. Varsayılan: `code-interpreter:latest`

Aracı bir ajanla kullanırken, ajanın şunları sağlaması gerekir:

* **code**: Zorunlu. Yürütülecek Python 3 kodu.
* **libraries\_used**: Opsiyonel. Kodda kullanılan ve yüklenmesi gereken kütüphanelerin listesi. Varsayılan: `[]`

## Ajan Entegrasyon Örneği

`CodeInterpreterTool`'un bir CrewAI ajanıyla nasıl entegre edileceğine dair daha ayrıntılı bir örnek:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import CodeInterpreterTool

# Aracı başlatın
code_interpreter = CodeInterpreterTool()

# Aracı kullanan bir ajan tanımlayın
data_analyst = Agent(
    role="Veri Analisti",
    goal="Python kodu kullanarak verileri analiz et",
    backstory="""Verileri analiz etmek ve görselleştirmek için Python kullanma konusunda uzman bir veri analistisiniz. 
    Büyük veri setlerini işlemek ve anlamlı içgörüler ayıklamak için verimli kodlar yazabilirsiniz.""",
    tools=[code_interpreter],
    verbose=True,
)

# Ajan için bir görev oluşturun
analysis_task = Task(
    description="""
    Şu işlemleri yapan Python kodunu yaz:
    1. x ve y koordinatlarına sahip 100 noktadan oluşan rastgele bir veri seti oluştur.
    2. x ve y arasındaki korelasyon katsayısını hesapla.
    3. Verilerin saçılım grafiğini (scatter plot) oluştur.
    4. Korelasyon katsayısını yazdır ve grafiği 'scatter.png' olarak kaydet.

    Gerekli içe aktarmaları (imports) yaptığından ve sonuçları yazdırdığından emin ol.
    """,
    expected_output="Korelasyon katsayısı ve saçılım grafiğinin kaydedildiğine dair onay.",
    agent=data_analyst,
)

# Görevi çalıştırın
crew = Crew(
    agents=[data_analyst],
    tasks=[analysis_task],
    verbose=True,
    process=Process.sequential,
)
result = crew.kickoff()
```

## Uygulama Detayları

`CodeInterpreterTool`, kod yürütme için güvenli bir ortam oluşturmak üzere Docker kullanır:

```python Code theme={null}
class CodeInterpreterTool(BaseTool):
    name: str = "Code Interpreter"
    description: str = "Sonunda bir print ifadesi bulunan Python3 kod dizelerini yorumlar."
    args_schema: Type[BaseModel] = CodeInterpreterSchema
    default_image_tag: str = "code-interpreter:latest"

    def _run(self, **kwargs) -> str:
        code = kwargs.get("code", self.code)
        libraries_used = kwargs.get("libraries_used", [])

        if self.unsafe_mode:
            return self.run_code_unsafe(code, libraries_used)
        else:
            return self.run_code_safety(code, libraries_used)
```

Araç şu adımları gerçekleştirir:

1. Docker imajının var olduğunu doğrular veya gerekirse oluşturur.
2. Mevcut çalışma dizininin bağlı (mounted) olduğu bir Docker konteyneri oluşturur.
3. Ajan tarafından belirtilen gerekli kütüphaneleri yükler.
4. Python kodunu konteyner içinde yürütür.
5. Kod yürütme çıktısını döndürür.
6. Konteyneri durdurup kaldırarak temizlik yapar.

## Güvenlik Hususları

Varsayılan olarak `CodeInterpreterTool`, bir güvenlik katmanı sağlayan izole bir Docker konteynerinde kod çalıştırır. Ancak yine de akılda tutulması gereken bazı güvenlik hususları vardır:

1. Docker konteyneri mevcut çalışma dizinine erişebilir, bu nedenle hassas dosyalara potansiyel olarak erişilebilir.
2. Docker konteyneri mevcut değilse ve kodun güvenli bir şekilde çalışması gerekiyorsa, sandbox ortamında yürütülecektir. Güvenlik nedenleriyle, rastgele kütüphanelerin yüklenmesine izin verilmez.
3. `unsafe_mode` parametresi, kodun doğrudan ana makinede yürütülmesine izin verir; bu sadece güvenilir ortamlarda kullanılmalıdır.
4. Ajanların rastgele kütüphaneler yüklemesine izin verirken dikkatli olun; bunlar potansiyel olarak kötü amaçlı kodlar içerebilir.

## Sonuç

`CodeInterpreterTool`, CrewAI ajanlarının Python kodlarını nispeten güvenli bir ortamda yürütmeleri için güçlü bir yol sunar. Ajanların kod yazıp çalıştırmasını sağlayarak, özellikle veri analizi, hesaplamalar veya diğer sayısal çalışmaları içeren görevler için problem çözme yeteneklerini önemli ölçüde genişletir. Bu araç, doğal dilden ziyade kodla daha verimli şekilde ifade edilebilen karmaşık işlemleri gerçekleştirmesi gereken ajanlar için özellikle yararlıdır.
