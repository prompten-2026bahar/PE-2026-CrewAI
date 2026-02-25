> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları bulmak için bu dosyayı kullanın.

# Özel Araçlar Oluşturma

> CrewAI çerçevesi içinde özel araçlar oluşturma, kullanma ve yönetme konusunda yeni işlevler ve hata yönetimi dahil kapsamlı kılavuz.

## CrewAI'de Araç Oluşturma ve Kullanma

Bu kılavuz, CrewAI çerçevesi için özel araçlar oluşturma ve bu araçları verimli biçimde yönetme ile kullanmaya dair ayrıntılı talimatlar sunar;
araç delegasyonu, hata yönetimi ve dinamik araç çağırma gibi en güncel işlevleri kapsar. Ayrıca iş birliği araçlarının önemini vurgulayarak
ajanların geniş bir eylem yelpazesi gerçekleştirmesine olanak tanır.

### `BaseTool` Alt Sınıfını Oluşturma

Kişiselleştirilmiş bir araç oluşturmak için `BaseTool`'dan türetin ve girdi doğrulaması için `args_schema` ile `_run` yöntemi dahil gerekli nitelikleri tanımlayın.

```python
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """MyCustomTool için girdi şeması."""
    argument: str = Field(..., description="Argümanın açıklaması.")

class MyCustomTool(BaseTool):
    name: str = "Aracımın adı"
    description: str = "Bu aracın ne yaptığı. Etkin kullanım için hayati önem taşır."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, argument: str) -> str:
        # Aracınızın mantığı buraya gelir
        return "Aracın sonucu"
```

### `tool` Dekoratörünü Kullanma

Alternatif olarak `@tool` dekoratörünü kullanabilirsiniz. Bu yaklaşım, aracın niteliklerini ve işlevselliğini doğrudan bir fonksiyon içinde tanımlamanıza imkân tanır;
ihtiyaçlarınıza göre uyarlanmış özel araçlar oluşturmak için özlü ve verimli bir yol sunar.

```python
from crewai.tools import tool

@tool("Araç Adı")
def my_simple_tool(question: str) -> str:
    """Netlik için araç açıklaması."""
    # Araç mantığı buraya gelir
    return "Araç çıktısı"
```

### Araç için Önbellek Fonksiyonu Tanımlama

Önbellekleme ile araç performansını optimize etmek için `cache_function` niteliğini kullanarak özel önbellekleme stratejileri tanımlayın.

```python
@tool("Önbellekli Araç")
def cached_tool(argument: str) -> str:
    """Araç işlevselliği açıklaması."""
    return "Önbelleklenebilir sonuç"

def my_cache_strategy(arguments: dict, result: str) -> bool:
    # Özel önbellekleme mantığını tanımlayın
    return True if some_condition else False

cached_tool.cache_function = my_cache_strategy
```

### Asenkron Araçlar Oluşturma

CrewAI, bloklamayan G/Ç işlemleri için asenkron araçları destekler. Bu özellik, aracınızın HTTP istekleri, veritabanı sorguları veya diğer G/Ç bağlı işlemler yapması gerektiğinde kullanışlıdır.

#### Asenkron Fonksiyonlarla `@tool` Dekoratörünü Kullanma

Asenkron araç oluşturmanın en basit yolu, `@tool` dekoratörünü asenkron bir fonksiyonla kullanmaktır:

```python
import aiohttp
from crewai.tools import tool

@tool("Async Web Fetcher")
async def fetch_webpage(url: str) -> str:
    """Bir web sayfasından içeriği asenkron olarak çeker."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

#### Asenkron Destekli `BaseTool` Alt Sınıfı Oluşturma

Daha fazla kontrol için `BaseTool`'dan türetin ve hem `_run` (senkron) hem de `_arun` (asenkron) yöntemlerini uygulayın:

```python
import requests
import aiohttp
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class WebFetcherInput(BaseModel):
    """WebFetcher için girdi şeması."""
    url: str = Field(..., description="Çekilecek URL")

class WebFetcherTool(BaseTool):
    name: str = "Web Fetcher"
    description: str = "Bir URL'den içerik çeker"
    args_schema: type[BaseModel] = WebFetcherInput

    def _run(self, url: str) -> str:
        """Senkron uygulama."""
        return requests.get(url).text

    async def _arun(self, url: str) -> str:
        """Bloklamayan G/Ç için asenkron uygulama."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
```

Bu yönergelere uyarak ve araç oluşturma ile yönetim süreçlerinize yeni işlevleri ve iş birliği araçlarını dahil ederek
CrewAI çerçevesinin tüm kapasitesinden yararlanabilir; hem geliştirme deneyimini hem de yapay zeka ajanlarınızın verimliliğini artırabilirsiniz.
