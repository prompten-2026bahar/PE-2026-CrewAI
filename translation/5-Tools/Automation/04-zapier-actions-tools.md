# Zapier Actions Aracı

> `ZapierActionsAdapter`, Zapier eylemlerini otomasyon için CrewAI araçları olarak sunar.

# `ZapierActionsAdapter`

## Açıklama

Zapier eylemlerini CrewAI araçları olarak listelemek ve çağırmak için Zapier adaptörünü kullanın. Bu, ajanların binlerce uygulama genelinde otomasyonları tetiklemesini sağlar.

## Kurulum

Bu adaptör `crewai-tools` paketine dahildir. Ek bir kurulum gerektirmez.

## Ortam Değişkenleri

* `ZAPIER_API_KEY` (gerekli): Zapier API anahtarı. [https://actions.zapier.com/](https://actions.zapier.com/) adresindeki Zapier Actions panelinden alın (hesap oluşturun, ardından bir API anahtarı oluşturun). Adaptörü kurarken `zapier_api_key` parametresini doğrudan da geçirebilirsiniz.

## Örnek

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.adapters.zapier_adapter import ZapierActionsAdapter

adapter = ZapierActionsAdapter(api_key="zapier_api_anahtarınız")
tools = adapter.tools()

agent = Agent(
    role="Otomasyoncu",
    goal="Zapier eylemlerini yürüt",
    backstory="Otomasyon uzmanı",
    tools=tools,
    verbose=True,
)

task = Task(
    description="Zapier eylemlerini kullanarak yeni bir Google E-Tablo oluştur ve bir satır ekle",
    expected_output="Oluşturulan kaynak ID'leriyle onay",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

## Notlar ve Sınırlar

* Adaptör, anahtarınız için mevcut eylemleri listeler ve dinamik olarak `BaseTool` sarmalayıcıları oluşturur.
* Eyleme özel zorunlu alanları görev talimatlarınızda veya araç çağrınızda yönetin.
* İstek limitleri (rate limits) Zapier planınıza bağlıdır; Zapier Actions dökümantasyonuna bakın.
