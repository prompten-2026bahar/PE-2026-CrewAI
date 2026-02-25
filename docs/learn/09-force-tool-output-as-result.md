> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Araç Çıktısını Sonuç Olarak Zorla

> CrewAI'de bir Ajanın görevinde araç çıktısını sonuç olarak nasıl zorlayacağınızı öğrenin.

## Giriş

CrewAI'de bir aracın çıktısını ajanın görev sonucu olarak zorlamanız mümkündür. Bu özellik, görev yürütme sırasında ajan tarafından herhangi bir değişiklik yapılmadan araç çıktısının yakalanıp sonuç olarak döndürülmesini garantilemek istediğinizde kullanışlıdır.

## Araç Çıktısını Sonuç Olarak Zorlama

Araç çıktısını ajanın görev sonucu olarak zorlamak için, araca ajana eklerken `result_as_answer` parametresini `True` olarak ayarlamanız gerekir. Bu parametre, araç çıktısının ajan tarafından herhangi bir değişikliğe uğramadan yakalanıp görev sonucu olarak döndürülmesini sağlar.

Araç çıktısını bir ajanın görev sonucu olarak nasıl zorlayacağınıza dair bir örnek:

```python
from crewai.agent import Agent
from my_tool import MyCustomTool

# Özel araçla bir kodlama ajanı oluşturun
coding_agent = Agent(
        role="Data Scientist",
        goal="Yapay zeka hakkında etkileyici raporlar üret",
        backstory="Veri ve yapay zeka ile çalışıyorsunuz",
        tools=[MyCustomTool(result_as_answer=True)],
    )

# Aracın yürütülmesi ve sonucun sistem içinde oluşturulduğu varsayılır
task_result = coding_agent.execute_task(task)
```

## İşleyişin Adımları

1. **Görev Yürütme** — Ajan, sağlanan aracı kullanarak görevi yürütür.
2. **Araç Çıktısı** — Araç, görev sonucu olarak yakalanan çıktıyı üretir.
3. **Ajan Etkileşimi** — Ajan araçtan çıkarımlar yapabilir ancak çıktı değiştirilmez.
4. **Sonuç Döndürme** — Araç çıktısı, herhangi bir değişiklik yapılmadan görev sonucu olarak döndürülür.
