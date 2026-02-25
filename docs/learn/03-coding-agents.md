> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Kodlama Ajanları

> CrewAI Ajanlarınızın kod yazıp çalıştırmasını nasıl etkinleştireceğinizi ve gelişmiş işlevler için ek özellikleri nasıl kullanacağınızı öğrenin.

## Giriş

CrewAI Ajanları artık kod yazma ve çalıştırma gibi güçlü bir yeteneğe sahiptir; bu durum problem çözme kapasitelerini önemli ölçüde artırmaktadır. Bu özellik, hesaplamalı veya programatik çözümler gerektiren görevler için özellikle kullanışlıdır.

## Kod Çalıştırmayı Etkinleştirme

Bir ajan için kod çalıştırmayı etkinleştirmek amacıyla, ajanı oluştururken `allow_code_execution` parametresini `True` olarak ayarlayın.

İşte bir örnek:

```python
from crewai import Agent

coding_agent = Agent(
    role="Senior Python Developer",
    goal="İyi tasarlanmış ve düşünülmüş kod yaz",
    backstory="Yazılım mimarisi ve en iyi uygulamalar konusunda geniş deneyime sahip kıdemli bir Python geliştiricisisiniz.",
    allow_code_execution=True
)
```

> **Not:** `allow_code_execution` parametresi varsayılan olarak `False` değerindedir.

## Önemli Konular

1. **Model Seçimi**: Kod çalıştırma etkinleştirildiğinde Claude 3.5 Sonnet ve GPT-4 gibi daha yetenekli modellerin kullanılması şiddetle tavsiye edilir. Bu modeller programlama kavramlarını daha iyi anlar ve doğru ile verimli kod üretme olasılıkları daha yüksektir.

2. **Hata Yönetimi**: Kod çalıştırma özelliği hata yönetimi içerir. Çalıştırılan kod bir istisna fırlatırsa ajan hata mesajını alır ve kodu düzeltmeye ya da alternatif çözümler sunmaya çalışabilir. Varsayılan değeri 2 olan `max_retry_limit` parametresi, bir görev için maksimum yeniden deneme sayısını kontrol eder.

3. **Bağımlılıklar**: Kod çalıştırma özelliğini kullanmak için `crewai_tools` paketini yüklemeniz gerekmektedir. Yüklü değilse ajan şu bilgi mesajını kaydeder: "Coding tools not available. Install crewai\_tools."

## Kod Çalıştırma Süreci

Kod çalıştırma etkinleştirilmiş bir ajan programlama gerektiren bir görevle karşılaştığında:

1. **Görev Analizi** — Ajan görevi analiz eder ve kod çalıştırmanın gerekli olduğunu belirler.
2. **Kod Oluşturma** — Problemi çözmek için gereken Python kodunu oluşturur.
3. **Kod Çalıştırma** — Kod dahili kod çalıştırma aracına (`CodeInterpreterTool`) gönderilir.
4. **Sonuç Yorumlama** — Ajan sonucu yorumlar ve yanıtına dahil eder ya da daha ileri problem çözme için kullanır.

## Kullanım Örneği

Kod çalıştırma yeteneğine sahip bir ajan oluşturma ve bunu bir görevde kullanmaya ilişkin ayrıntılı bir örnek:

```python
from crewai import Agent, Task, Crew

# Kod çalıştırma etkinleştirilmiş bir ajan oluşturun
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Python kullanarak veri analizi yap ve içgörüler sun",
    backstory="Güçlü Python becerilerine sahip deneyimli bir veri analistisiniz.",
    allow_code_execution=True
)

# Kod çalıştırma gerektiren bir görev oluşturun
data_analysis_task = Task(
    description="Verilen veri kümesini analiz edin ve katılımcıların ortalama yaşını hesaplayın.",
    agent=coding_agent
)

# Bir ekip oluşturun ve görevi ekleyin
analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

# Ekibi çalıştırın
result = analysis_crew.kickoff()

print(result)
```

Bu örnekte `coding_agent`, veri analizi görevlerini gerçekleştirmek için Python kodu yazıp çalıştırabilmektedir.
