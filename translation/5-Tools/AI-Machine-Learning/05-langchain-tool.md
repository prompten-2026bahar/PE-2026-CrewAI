# LangChain Aracı

> `LangChainTool`, LangChain araçları ve sorgu motorları için bir sarmalayıcıdır (wrapper).

## `LangChainTool`

CrewAI, LangChain'in kapsamlı [araç listesi](https://python.langchain.com/docs/integrations/tools/) ile sorunsuz bir şekilde entegre olur ve bunların tümü CrewAI ile kullanılabilir.

```python Code theme={null}
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import GoogleSerperAPIWrapper

# .env dosyanıza SERPER_API_KEY anahtarınızı ayarlayın, örneğin:
# SERPER_API_KEY=<api anahtarınız>
load_dotenv()

search = GoogleSerperAPIWrapper()

class SearchTool(BaseTool):
    name: str = "Arama"
    description: str = "Arama tabanlı sorgular için kullanışlıdır. Pazarlar, şirketler ve trendler hakkında güncel bilgileri bulmak için bunu kullanın."
    search: GoogleSerperAPIWrapper = Field(default_factory=GoogleSerperAPIWrapper)

    def _run(self, query: str) -> str:
        """Arama sorgusunu yürütür ve sonuçları döndürür"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Arama yapılırken hata oluştu: {str(e)}"

# Ajanları Oluşturun
researcher = Agent(
    role='Araştırma Analisti',
    goal='Güncel pazar verilerini ve trendlerini topla',
    backstory="""Pazar istihbaratı toplama konusunda yılların deneyimine sahip uzman bir araştırma analistisiniz. 
    İlgili ve güncel pazar bilgilerini bulma ve bunları net, eyleme dönüştürülebilir bir formatta sunma 
    yeteneğinizle tanınırsınız.""",
    tools=[SearchTool()],
    verbose=True
)

# kodun geri kalanı ...
```

## Sonuç

Araçlar, CrewAI ajanlarının yeteneklerini genişletmede, geniş bir görev yelpazesini üstlenmelerini ve etkili bir şekilde işbirliği yapmalarını sağlamada kritik öneme sahiptir. CrewAI ile çözümler üretirken, ajanlarınızı güçlendirmek ve yapay zeka ekosistemini geliştirmek için hem özel hem de mevcut araçlardan yararlanın. Ajanlarınızın performansını ve yeteneklerini optimize etmek için hata giderme, önbelleğe alma (caching) mekanizmaları ve araç argümanlarının esnekliğini kullanmayı düşünün.
