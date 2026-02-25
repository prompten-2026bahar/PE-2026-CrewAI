# Çalışma Hook'larına (Execution Hooks) Genel Bakış

> Temsilci işlemleri üzerinde ince ayarlı kontrol için CrewAI'daki çalışma hook'larını anlama ve kullanma

Çalışma Hook'ları (Execution Hooks), CrewAI temsilcilerinizin çalışma zamanı davranışı üzerinde ince ayarlı kontrol sağlar. Ekip yürütmesinden önce ve sonra çalışan kickoff hook'larının aksine, çalışma hook'ları temsilci yürütmesi sırasında belirli işlemleri yakalar; bu da davranışı değiştirmenize, güvenlik kontrolleri uygulamanıza ve kapsamlı izleme eklemenize olanak tanır.

## Çalışma Hook'larının Türleri

CrewAI, çalışma hook'ları için iki ana kategori sunar:

### 1. [LLM Çağrı Hook'ları (LLM Call Hooks)](/learn/llm-hooks)

Dil modeli etkileşimlerini kontrol edin ve izleyin:

* **LLM Çağrısından Önce**: İstemleri (prompts) değiştirin, girişleri doğrulayın, onay geçitleri uygulayın
* **LLM Çağrısından Sonra**: Yanıtları dönüştürün, çıktıları temizleyin, konuşma geçmişini güncelleyin

**Kullanım Durumları:**

* Tekrar (iteration) sınırlama
* Maliyet takibi ve token kullanımı izleme
* Yanıt temizleme ve içerik filtreleme
* LLM çağrıları için insan onaylı (human-in-the-loop) sistemler
* Güvenlik yönergeleri veya bağlam ekleme
* Hata ayıklama günlükleri ve istek/yanıt inceleme

[LLM Hook Dokümantasyonunu Görüntüle →](/learn/llm-hooks)

### 2. [Araç Çağrı Hook'ları (Tool Call Hooks)](/learn/tool-hooks)

Araç yürütmesini kontrol edin ve izleyin:

* **Araç Çağrısından Önce**: Girişleri değiştirin, parametreleri doğrulayın, tehlikeli işlemleri engelleyin
* **Araç Çağrısından Sonra**: Sonuçları dönüştürün, çıktıları temizleyin, yürütme ayrıntılarını günlüğe kaydedin

**Kullanım Durumları:**

* Yıkıcı işlemler için güvenlik önlemleri
* Hassas eylemler için insan onayı
* Giriş doğrulama ve temizleme
* Sonuç önbelleğe alma ve hız sınırlama
* Araç kullanım analitiği
* Hata ayıklama günlükleri ve izleme

[Araç Hook Dokümantasyonunu Görüntüle →](/learn/tool-hooks)

## Hook Kayıt Yöntemleri

### 1. Dekoratör Tabanlı Hook'lar (Önerilen)

Hook'ları kaydetmenin en temiz ve en "Pythonic" yolu:

```python
from crewai.hooks import before_llm_call, after_llm_call, before_tool_call, after_tool_call

@before_llm_call
def limit_iterations(context):
    """Tekrarları sınırlayarak sonsuz döngüleri önleyin."""
    if context.iterations > 10:
        return False  # Yürütmeyi engelle
    return None

@after_llm_call
def sanitize_response(context):
    """LLM yanıtlarından hassas verileri kaldırın."""
    if "API_KEY" in context.response:
        return context.response.replace("API_KEY", "[GİZLENDİ]")
    return None

@before_tool_call
def block_dangerous_tools(context):
    """Yıkıcı işlemleri engelleyin."""
    if context.tool_name == "delete_database":
        return False  # Yürütmeyi engelle
    return None

@after_tool_call
def log_tool_result(context):
    """Araç yürütmesini günlüğe kaydedin."""
    print(f"Araç {context.tool_name} tamamlandı")
    return None
```

### 2. Ekip Kapsamlı (Crew-Scoped) Hook'lar

Hook'ları yalnızca belirli ekip örneklerine uygulayın:

```python
from crewai import CrewBase
from crewai.project import crew
from crewai.hooks import before_llm_call_crew, after_tool_call_crew

@CrewBase
class MyProjCrew:
    @before_llm_call_crew
    def validate_inputs(self, context):
        # Yalnızca bu ekip için geçerlidir
        print(f"{self.__class__.__name__} içinde LLM çağrısı")
        return None

    @after_tool_call_crew
    def log_results(self, context):
        # Ekibe özel günlüğe kaydetme
        print(f"Araç sonucu: {context.tool_result[:50]}...")
        return None

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

## Hook Yürütme Akışı

### LLM Çağrı Akışı

```
Temsilcinin LLM'i çağırması gerekiyor
    ↓
[LLM Çağrısı Öncesi Hook'lar Yürütülür]
    ├→ Hook 1: Tekrar sayısını doğrula
    ├→ Hook 2: Güvenlik bağlamı ekle
    └→ Hook 3: İsteği günlüğe kaydet
    ↓
Herhangi bir hook False dönerse:
    ├→ LLM çağrısını engelle
    └→ ValueError fırlat
    ↓
Tüm hook'lar True/None dönerse:
    ├→ LLM çağrısı devam eder
    └→ Yanıt oluşturulur
    ↓
[LLM Çağrısı Sonrası Hook'lar Yürütülür]
    ├→ Hook 1: Yanıtı temizle
    ├→ Hook 2: Yanıtı günlüğe kaydet
    └→ Hook 3: Metrikleri güncelle
    ↓
Final yanıtı döndürülür
```

### Araç Çağrı Akışı

```
Temsilcinin aracı yürütmesi gerekiyor
    ↓
[Araç Çağrısı Öncesi Hook'lar Yürütülür]
    ├→ Hook 1: Aracın izinli olup olmadığını kontrol et
    ├→ Hook 2: Girişleri doğrula
    └→ Hook 3: Gerekiyorsa onay iste
    ↓
Herhangi bir hook False dönerse:
    ├→ Araç yürütmesini engelle
    └→ Hata mesajı döndür
    ↓
Tüm hook'lar True/None dönerse:
    ├→ Araç yürütmesi devam eder
    └→ Sonuç oluşturulur
    ↓
[Araç Çağrısı Sonrası Hook'lar Yürütülür]
    ├→ Hook 1: Sonucu temizle
    ├→ Hook 2: Sonucu önbelleğe al
    └→ Hook 3: Metrikleri günlüğe kaydet
    ↓
Final sonucu döndürülür
```

## Hook Bağlam (Context) Nesneleri

### LLMCallHookContext

LLM yürütme durumuna erişim sağlar:

```python
class LLMCallHookContext:
    executor: CrewAgentExecutor  # Tam yürütücü erişimi
    messages: list               # Değiştirilebilir mesaj listesi
    agent: Agent                 # Mevcut temsilci
    task: Task                   # Mevcut görev
    crew: Crew                   # Ekip örneği
    llm: BaseLLM                 # LLM örneği
    iterations: int              # Mevcut tekrar sayısı
    response: str | None         # LLM yanıtı (after hooklarından sonra)
```

### ToolCallHookContext

Araç yürütme durumuna erişim sağlar:

```python
class ToolCallHookContext:
    tool_name: str               # Çağrılan aracın adı
    tool_input: dict             # Değiştirilebilir giriş parametreleri
    tool: CrewStructuredTool     # Araç örneği
    agent: Agent | None          # Yürüten temsilci
    task: Task | None            # Mevcut görev
    crew: Crew | None            # Ekip örneği
    tool_result: str | None      # Araç sonucu (after hooklarından sonra)
```

## Yaygın Kalıplar (Common Patterns)

### Güvenlik ve Doğrulama

```python
@before_tool_call
def safety_check(context):
    """Yıkıcı işlemleri engelleyin."""
    dangerous = ['delete_file', 'drop_table', 'system_shutdown']
    if context.tool_name in dangerous:
        print(f"🛑 Engellendi: {context.tool_name}")
        return False
    return None

@before_llm_call
def iteration_limit(context):
    """Sonsuz döngüleri önleyin."""
    if context.iterations > 15:
        print("⛔ Maksimum tekrar sayısına ulaşıldı")
        return False
    return None
```

### İnsan Onayı (Human-in-the-Loop)

```python
@before_tool_call
def require_approval(context):
    """Hassas işlemler için onay isteyin."""
    sensitive = ['send_email', 'make_payment', 'post_message']

    if context.tool_name in sensitive:
        response = context.request_human_input(
            prompt=f"{context.tool_name} işlemini onayla?",
            default_message="Onaylamak için 'evet' yazın:"
        )

        if response.lower() != 'evet':
            return False

    return None
```

### İzleme ve Analitik

```python
from collections import defaultdict
import time

metrics = defaultdict(lambda: {'count': 0, 'total_time': 0})

@before_tool_call
def start_timer(context):
    context.tool_input['_start'] = time.time()
    return None

@after_tool_call
def track_metrics(context):
    start = context.tool_input.get('_start', time.time())
    duration = time.time() - start

    metrics[context.tool_name]['count'] += 1
    metrics[context.tool_name]['total_time'] += duration

    return None

# Metrikleri görüntüle
def print_metrics():
    for tool, data in metrics.items():
        avg = data['total_time'] / data['count']
        print(f"{tool}: {data['count']} çağrı, ortalama {avg:.2f}sn")
```

### Yanıt Temizleme (Response Sanitization)

```python
import re

@after_llm_call
def sanitize_llm_response(context):
    """LLM yanıtlarından hassas verileri kaldırın."""
    if not context.response:
        return None

    result = context.response
    result = re.sub(r'(api[_-]?key)["\']?\s*[:=]\s*["\']?[\w-]+',
                   r'\1: [GİZLENDİ]', result, flags=re.IGNORECASE)
    return result

@after_tool_call
def sanitize_tool_result(context):
    """Araç sonuçlarından hassas verileri kaldırın."""
    if not context.tool_result:
        return None

    result = context.tool_result
    result = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                   '[EPOSTA-GİZLENDİ]', result)
    return result
```

## Hook Yönetimi

### Tüm Hook'ları Temizleme

```python
from crewai.hooks import clear_all_global_hooks

# Tüm hook'ları tek seferde temizle
result = clear_all_global_hooks()
print(f"{result['total']} hook temizlendi")
# Çıktı Örneği: {'llm_hooks': (2, 1), 'tool_hooks': (1, 2), 'total': (3, 3)}
```

### Belirli Hook Türlerini Temizleme

```python
from crewai.hooks import (
    clear_before_llm_call_hooks,
    clear_after_llm_call_hooks,
    clear_before_tool_call_hooks,
    clear_after_tool_call_hooks
)

# Belirli türleri temizle
llm_before_count = clear_before_llm_call_hooks()
tool_after_count = clear_after_tool_call_hooks()
```

### Münferit Hook'ların Kaydını Silme

```python
from crewai.hooks import (
    unregister_before_llm_call_hook,
    unregister_after_tool_call_hook
)

def my_hook(context):
    ...

# Kaydet
register_before_llm_call_hook(my_hook)

# Daha sonra kaydı sil
success = unregister_before_llm_call_hook(my_hook)
print(f"Kayıt silindi: {success}")
```

## En İyi Uygulamalar

### 1. Hook'ları Odaklanmış Tutun

Her hook tek bir net sorumluluğa sahip olmalıdır:

```python
# ✅ İyi - odaklanmış sorumluluk
@before_tool_call
def validate_file_path(context):
    if context.tool_name == 'read_file':
        if '..' in context.tool_input.get('path', ''):
            return False
    return None

# ❌ Kötü - çok fazla sorumluluk
@before_tool_call
def do_everything(context):
    # Doğrulama + günlükleme + metrikler + onay...
    ...
```

### 2. Hataları Zarif Bir Şekilde Yönetin

```python
@before_llm_call
def safe_hook(context):
    try:
        # Mantığınız
        if some_condition:
            return False
    except Exception as e:
        print(f"Hook hatası: {e}")
        return None  # Hataya rağmen yürütmeye izin ver
```

### 3. Bağlamı Yerinde Değiştirin (Modify Context In-Place)

```python
# ✅ Doğru - yerinde değiştir
@before_llm_call
def add_context(context):
    context.messages.append({"role": "system", "content": "Kısa ve öz ol"})

# ❌ Yanlış - referansı değiştirir
@before_llm_call
def wrong_approach(context):
    context.messages = [{"role": "system", "content": "Kısa ve öz ol"}]
```

### 4. Tip İpuçlarını (Type Hints) Kullanın

```python
from crewai.hooks import LLMCallHookContext, ToolCallHookContext

def my_llm_hook(context: LLMCallHookContext) -> bool | None:
    # IDE otomatik tamamlama ve tip kontrolü
    return None

def my_tool_hook(context: ToolCallHookContext) -> str | None:
    return None
```

### 5. Testlerde Temizlik Yapın

```python
import pytest
from crewai.hooks import clear_all_global_hooks

@pytest.fixture(autouse=True)
def clean_hooks():
    """Her testten önce hook'ları sıfırla."""
    yield
    clear_all_global_hooks()
```

## Hangi Hook Ne Zaman Kullanılmalı?

### Şu Durumlarda LLM Hook'larını Kullanın:

* Tekrar sınırları uygularken
* İsteme bağlam veya güvenlik yönergeleri eklerken
* Token kullanımını ve maliyetleri takip ederken
* Yanıtları temizlerken veya dönüştürürken
* LLM çağrıları için onay geçitleri uygularken
* İstem/yanıt etkileşimlerinde hata ayıklarken

### Şu Durumlarda Araç Hook'larını Kullanın:

* Tehlikeli veya yıkıcı işlemleri engellerken
* Yürütmeden önce araç girişlerini doğrularken
* Hassas eylemler için onay geçitleri uygularken
* Araç sonuçlarını önbelleğe alırken
* Araç kullanımını ve performansını takip ederken
* Araç çıktılarını temizlerken
* Araç çağrılarına hız sınırı (rate limit) koyarken

### Şu Durumlarda Her İkisini de Kullanın:

Tüm temsilci işlemlerini izlemesi gereken kapsamlı gözlemlenebilirlik, güvenlik veya onay sistemleri oluştururken.

## Alternatif Kayıt Yöntemleri

### Programatik Kayıt (Gelişmiş)

Dinamik hook kaydı için veya hook'ları programatik olarak kaydetmeniz gerektiğinde:

```python
from crewai.hooks import (
    register_before_llm_call_hook,
    register_after_tool_call_hook
)

def my_hook(context):
    return None

# Programatik olarak kaydet
register_before_llm_call_hook(my_hook)

# Şunlar için kullanışlıdır:
# - Yapılandırmadan hook yükleme
# - Koşullu hook kaydı
# - Eklenti (plugin) sistemleri
```

**Not:** Çoğu kullanım durumu için dekoratörler daha temiz ve bakımı daha kolaydır.

## Performans Değerlendirmeleri

1. **Hook'ları Hızlı Tutun**: Hook'lar her çağrıda çalışır - ağır hesaplamalardan kaçının
2. **Mümkünse Önbelleğe Alın**: Pahalı doğrulamaları veya aramaları saklayın
3. **Seçici Olun**: Global hook'lara ihtiyaç duyulmadığında ekibe özel hook'ları kullanın
4. **Hook Yükünü İzleyin**: Üretim ortamında hook yürütme süresini profilleme yaparak izleyin
5. **Geç Yükleme (Lazy Import)**: Ağır bağımlılıkları yalnızca ihtiyaç duyulduğunda içe aktarın

## Hook'larda Hata Ayıklama

### Hata Ayıklama Günlüğünü Etkinleştir

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@before_llm_call
def debug_hook(context):
    logger.debug(f"LLM çağrısı: {context.agent.role}, tekrar {context.iterations}")
    return None
```

### Hook Yürütme Sırası

Hook'lar kayıt sırasına göre yürütülür. Eğer bir `before` hook'u `False` dönerse, sonraki hook'lar yürütülmez:

```python
# Kayıt sırası önemlidir!
register_before_tool_call_hook(hook1)  # İlk önce yürütülür
register_before_tool_call_hook(hook2)  # İkinci olarak yürütülür
register_before_tool_call_hook(hook3)  # Üçüncü olarak yürütülür

# Eğer hook2, False dönerse:
# - hook1 yürütüldü
# - hook2 yürütüldü ve False döndü
# - hook3 YÜRÜTÜLMEDİ
# - Araç çağrısı engellendi
```

## İlgili Dokümantasyon

* [LLM Çağrı Hook'ları →](/learn/llm-hooks) - Ayrıntılı LLM hook dokümantasyonu
* [Araç Çağrı Hook'ları →](/learn/tool-hooks) - Ayrıntılı araç hook dokümantasyonu
* [Kickoff Öncesi ve Sonrası Hook'ları →](/learn/before-and-after-kickoff-hooks) - Ekip yaşam döngüsü hook'ları
* [İnsan Onaylı Sistemler (Human-in-the-Loop) →](/learn/human-in-the-loop) - İnsan girişi modelleri

## Sonuç

Çalışma hook'ları, temsilci çalışma zamanı davranışı üzerinde güçlü bir kontrol sağlar. Bunları güvenlik önemleri, onay iş akışları, kapsamlı izleme ve özel iş mantığı uygulamak için kullanın. Düzgün hata yönetimi, tip güvenliği ve performans değerlendirmeleriyle birleştiğinde, hook'lar üretim için hazır, güvenli ve gözlemlenebilir temsilci sistemleri oluşturulmasına olanak tanır.
