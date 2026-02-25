# Özel LLM Uygulaması

> CrewAI'de özel LLM uygulamalarının nasıl oluşturulacağını öğrenin.

## Genel Bakış

CrewAI, `BaseLLM` soyut temel sınıfı aracılığıyla özel LLM uygulamalarını destekler. Bu özellik, LiteLLM'de yerleşik desteği bulunmayan herhangi bir LLM sağlayıcısını entegre etmenizi veya özel kimlik doğrulama mekanizmaları uygulamanızı sağlar.

## Hızlı Başlangıç

Asgari düzeyde bir özel LLM uygulaması:

```python
from crewai import BaseLLM
from typing import Any, Dict, List, Optional, Union
import requests

class CustomLLM(BaseLLM):
    def __init__(self, model: str, api_key: str, endpoint: str, temperature: Optional[float] = None):
        # ÖNEMLİ: super().__init__()'i gerekli parametrelerle çağırın
        super().__init__(model=model, temperature=temperature)
        
        self.api_key = api_key
        self.endpoint = endpoint
        
    def call(
        self,
        messages: Union[str, List[Dict[str, str]]],
        tools: Optional[List[dict]] = None,
        callbacks: Optional[List[Any]] = None,
        available_functions: Optional[Dict[str, Any]] = None,
    ) -> Union[str, Any]:
        """LLM'i verilen mesajlarla çağırır."""
        # Gerekirse string'i mesaj formatına dönüştürün
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        # İsteği hazırlayın
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        
        # Sağlanmışsa ve destekleniyorsa araçları ekleyin
        if tools and self.supports_function_calling():
            payload["tools"] = tools
        
        # API çağrısı yapın
        response = requests.post(
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    def supports_function_calling(self) -> bool:
        """LLM'iniz fonksiyon çağırmayı destekliyorsa geçersiz kılın."""
        return True  # LLM'iniz araçları desteklemiyorsa False olarak değiştirin
        
    def get_context_window_size(self) -> int:
        """LLM'inizin bağlam penceresi boyutunu döndürür."""
        return 8192  # Modelinizin gerçek bağlam penceresine göre ayarlayın
```

## Özel LLM'inizi Kullanma

```python
from crewai import Agent, Task, Crew

# Yukarıda tanımlanmış CustomLLM sınıfına sahip olduğunuzu varsayarak
# Özel LLM'inizi oluşturun
custom_llm = CustomLLM(
    model="my-custom-model",
    api_key="your-api-key",
    endpoint="https://api.example.com/v1/chat/completions",
    temperature=0.7
)

# Bir ajanla kullanın
agent = Agent(
    role="Research Assistant",
    goal="Bilgi bul ve analiz et",
    backstory="Bir araştırma asistanısınız.",
    llm=custom_llm
)

# Görevler oluşturun ve çalıştırın
task = Task(
    description="Yapay zekadaki son gelişmeleri araştır",
    expected_output="Kapsamlı bir özet",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

## Gerekli Yöntemler

### Yapıcı: `__init__()`

**Kritik**: `super().__init__(model, temperature)`'ı gerekli parametrelerle çağırmanız zorunludur:

```python
def __init__(self, model: str, api_key: str, temperature: Optional[float] = None):
    # ZORUNLU: Üst yapıcıyı model ve temperature ile çağırın
    super().__init__(model=model, temperature=temperature)
    
    # Özel başlatma işleminiz
    self.api_key = api_key
```

### Soyut Yöntem: `call()`

`call()` yöntemi, LLM uygulamanızın kalbidir. Şunları yapması gerekir:

- Mesajları kabul etmek (string veya 'role' ve 'content' içeren sözlük listesi)
- String bir yanıt döndürmek
- Destekleniyorsa araçları ve fonksiyon çağırmayı yönetmek
- Hatalar için uygun istisnalar fırlatmak

### İsteğe Bağlı Yöntemler

```python
def supports_function_calling(self) -> bool:
    """LLM'iniz fonksiyon çağırmayı destekliyorsa True döndürür."""
    return True  # Varsayılan True'dur

def supports_stop_words(self) -> bool:
    """LLM'iniz durdurma dizilerini destekliyorsa True döndürür."""
    return True  # Varsayılan True'dur

def get_context_window_size(self) -> int:
    """Bağlam penceresi boyutunu döndürür."""
    return 4096  # Varsayılan 4096'dır
```

## Yaygın Kalıplar

### Hata Yönetimi

```python
import requests

def call(self, messages, tools=None, callbacks=None, available_functions=None):
    try:
        response = requests.post(
            self.endpoint,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
        
    except requests.Timeout:
        raise TimeoutError("LLM isteği zaman aşımına uğradı")
    except requests.RequestException as e:
        raise RuntimeError(f"LLM isteği başarısız oldu: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Geçersiz yanıt formatı: {str(e)}")
```

### Özel Kimlik Doğrulama

```python
from crewai import BaseLLM
from typing import Optional

class CustomAuthLLM(BaseLLM):
    def __init__(self, model: str, auth_token: str, endpoint: str, temperature: Optional[float] = None):
        super().__init__(model=model, temperature=temperature)
        self.auth_token = auth_token
        self.endpoint = endpoint
    
    def call(self, messages, tools=None, callbacks=None, available_functions=None):
        headers = {
            "Authorization": f"Custom {self.auth_token}",  # Özel kimlik doğrulama formatı
            "Content-Type": "application/json"
        }
        # Uygulamanın geri kalanı...
```

### Durdurma Sözcükleri Desteği

CrewAI, ajan davranışını kontrol etmek için otomatik olarak `"\nObservation:"` değerini durdurma sözcüğü olarak ekler. LLM'iniz durdurma sözcüklerini destekliyorsa:

```python
def call(self, messages, tools=None, callbacks=None, available_functions=None):
    payload = {
        "model": self.model,
        "messages": messages,
        "stop": self.stop  # API çağrısına durdurma sözcüklerini dahil edin
    }
    # API çağrısı yapın...

def supports_stop_words(self) -> bool:
    return True  # LLM'iniz durdurma dizilerini destekliyor
```

LLM'iniz durdurma sözcüklerini doğal olarak desteklemiyorsa:

```python
def call(self, messages, tools=None, callbacks=None, available_functions=None):
    response = self._make_api_call(messages, tools)
    content = response["choices"][0]["message"]["content"]
    
    # Durdurma sözcüklerinde manuel olarak kırpın
    if self.stop:
        for stop_word in self.stop:
            if stop_word in content:
                content = content.split(stop_word)[0]
                break
    
    return content

def supports_stop_words(self) -> bool:
    return False  # CrewAI'ye durdurma sözcüklerini manuel olarak yönettiğimizi bildirin
```

## Fonksiyon Çağırma

LLM'iniz fonksiyon çağırmayı destekliyorsa tam akışı uygulayın:

```python
import json

def call(self, messages, tools=None, callbacks=None, available_functions=None):
    # String'i mesaj formatına dönüştürün
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    # API çağrısı yapın
    response = self._make_api_call(messages, tools)
    message = response["choices"][0]["message"]
    
    # Fonksiyon çağrılarını kontrol edin
    if "tool_calls" in message and available_functions:
        return self._handle_function_calls(
            message["tool_calls"], messages, tools, available_functions
        )
    
    return message["content"]

def _handle_function_calls(self, tool_calls, messages, tools, available_functions):
    """Fonksiyon çağırmayı uygun mesaj akışıyla yönetir."""
    for tool_call in tool_calls:
        function_name = tool_call["function"]["name"]
        
        if function_name in available_functions:
            # Fonksiyonu ayrıştırın ve çalıştırın
            function_args = json.loads(tool_call["function"]["arguments"])
            function_result = available_functions[function_name](**function_args)
            
            # Fonksiyon çağrısını ve sonucunu mesaj geçmişine ekleyin
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": str(function_result)
            })
            
            # Güncellenmiş bağlamla LLM'i tekrar çağırın
            return self.call(messages, tools, None, available_functions)
    
    return "Fonksiyon çağrısı başarısız oldu"
```

## Sorun Giderme

### Yaygın Sorunlar

**Yapıcı Hataları**

```python
# ❌ Yanlış - gerekli parametreler eksik
def __init__(self, api_key: str):
    super().__init__()

# ✅ Doğru
def __init__(self, model: str, api_key: str, temperature: Optional[float] = None):
    super().__init__(model=model, temperature=temperature)
```

**Fonksiyon Çağırma Çalışmıyor**

- `supports_function_calling()`'in `True` döndürdüğünden emin olun
- Yanıtta `tool_calls`'u yönettiğinizi kontrol edin
- `available_functions` parametresinin doğru kullanıldığını doğrulayın

**Kimlik Doğrulama Hataları**

- API anahtarı formatını ve izinlerini doğrulayın
- Kimlik doğrulama başlığı formatını kontrol edin
- Uç nokta URL'lerinin doğru olduğundan emin olun

**Yanıt Ayrıştırma Hataları**

- İç içe alanlara erişmeden önce yanıt yapısını doğrulayın
- İçeriğin None olabileceği durumları yönetin
- Hatalı biçimlendirilmiş yanıtlar için uygun hata yönetimi ekleyin

## Özel LLM'inizi Test Etme

```python
from crewai import Agent, Task, Crew

def test_custom_llm():
    llm = CustomLLM(
        model="test-model",
        api_key="test-key",
        endpoint="https://api.test.com"
    )
    
    # Temel çağrıyı test edin
    result = llm.call("Merhaba, dünya!")
    assert isinstance(result, str)
    assert len(result) > 0
    
    # CrewAI ajanıyla test edin
    agent = Agent(
        role="Test Agent",
        goal="Özel LLM'i test et",
        backstory="Bir test ajanı.",
        llm=llm
    )
    
    task = Task(
        description="Merhaba de",
        expected_output="Bir selamlama",
        agent=agent
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    assert "hello" in result.raw.lower()
```

Bu kılavuz, CrewAI'de özel LLM uygulamasının temellerini kapsamaktadır.
