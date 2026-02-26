# Araç Çağrı Hook'ları (Tool Call Hooks)

> CrewAI'da araç yürütmesini yakalamayı, değiştirmeyi ve kontrol etmeyi öğrenin.

Araç Çağrı Hook'ları, temsilci işlemleri sırasında araç yürütmesi üzerinde ince ayarlı kontrol sağlar. Bu hook'lar araç çağrılarını yakalamanıza, girişleri değiştirmenize, çıktıları dönüştürmenize, güvenlik kontrolleri uygulamanıza ve kapsamlı günlükleme veya izleme eklemenize olanak tanır.

## Genel Bakış

Araç hook'ları iki kritik noktada yürütülür:

* **Araç Çağrısından Önce**: Girişleri değiştirin, parametreleri doğrulayın veya yürütmeyi engelleyin
* **Araç Çağrısından Sonra**: Sonuçları dönüştürün, çıktıları temizleyin veya yürütme ayrıntılarını günlüğe kaydedin

## Hook Türleri

### Araç Çağrısı Öncesi Hook'lar (Before Tool Call Hooks)

Her araç yürütülmeden önce çalıştırılır, bu hook'lar şunları yapabilir:

* Araç girişlerini inceleyebilir ve değiştirebilir
* Koşullara bağlı olarak araç yürütmesini engelleyebilir
* Tehlikeli işlemler için onay geçitleri uygulayabilir
* Parametreleri doğrulayabilir
* Araç çağrılarını günlüğe kaydedebilir

**İmza:**

```python
def before_hook(context: ToolCallHookContext) -> bool | None:
    # Yürütmeyi engellemek için False döndürün
    # Yürütmeye izin vermek için True veya None döndürün
    ...
```

### Araç Çağrısı Sonrası Hook'lar (After Tool Call Hooks)

Her araç yürütüldükten sonra çalıştırılır, bu hook'lar şunları yapabilir:

* Araç sonuçlarını değiştirebilir veya temizleyebilir
* Meta veri veya biçimlendirme ekleyebilir
* Yürütme sonuçlarını günlüğe kaydedebilir
* Sonuç doğrulaması uygulayabilir
* Çıktı formatlarını dönüştürebilir

**İmza:**

```python
def after_hook(context: ToolCallHookContext) -> str | None:
    # Değiştirilmiş sonuç dizisini döndürün
    # Orijinal sonucu korumak için None döndürün
    ...
```

## Araç Hook Bağlamı (Context)

`ToolCallHookContext` nesnesi araç yürütme durumuna kapsamlı bir erişim sağlar:

```python
class ToolCallHookContext:
    tool_name: str                    # Çağrılan aracın adı
    tool_input: dict[str, Any]        # Değiştirilebilir araç giriş parametreleri
    tool: CrewStructuredTool          # Araç örneği referansı
    agent: Agent | BaseAgent | None   # Aracı yürüten temsilci
    task: Task | None                 # Mevcut görev
    crew: Crew | None                 # Ekip örneği
    tool_result: str | None           # Araç sonucu (yalnızca after hook'larından sonra)
```

### Araç Girişlerini Değiştirme

**Önemli:** Araç girişlerini her zaman yerinde (in-place) değiştirin:

```python
# ✅ Doğru - yerinde değiştir
def sanitize_input(context: ToolCallHookContext) -> None:
    context.tool_input['query'] = context.tool_input['query'].lower()

# ❌ Yanlış - sözlük referansını değiştirir
def wrong_approach(context: ToolCallHookContext) -> None:
    context.tool_input = {'query': 'yeni sorgu'}
```

## Kayıt Yöntemleri

### 1. Global Hook Kaydı

Tüm ekiplerdeki tüm araç çağrılarına uygulanan hook'ları kaydedin:

```python
from crewai.hooks import register_before_tool_call_hook, register_after_tool_call_hook

def log_tool_call(context):
    print(f"Araç: {context.tool_name}")
    print(f"Giriş: {context.tool_input}")
    return None  # Yürütmeye izin ver

register_before_tool_call_hook(log_tool_call)
```

### 2. Dekoratör Tabanlı Kayıt

Daha temiz bir yazım için dekoratörleri kullanın:

```python
from crewai.hooks import before_tool_call, after_tool_call

@before_tool_call
def block_dangerous_tools(context):
    dangerous_tools = ['delete_database', 'drop_table', 'rm_rf']
    if context.tool_name in dangerous_tools:
        print(f"⛔ Tehlikeli araç engellendi: {context.tool_name}")
        return False  # Yürütmeyi engelle
    return None

@after_tool_call
def sanitize_results(context):
    if context.tool_result and "parola" in context.tool_result.lower():
        return context.tool_result.replace("parola", "[GİZLENDİ]")
    return None
```

### 3. Ekip Kapsamlı (Crew-Scoped) Hook'lar

Belirli bir ekip örneği için hook'ları kaydedin:

```python
@CrewBase
class MyProjCrew:
    @before_tool_call_crew
    def validate_tool_inputs(self, context):
        # Yalnızca bu ekip için geçerlidir
        if context.tool_name == "web_search":
            if not context.tool_input.get('query'):
                print("❌ Geçersiz arama sorgusu")
                return False
        return None

    @after_tool_call_crew
    def log_tool_results(self, context):
        # Ekibe özel araç günlüğe kaydetme
        print(f"✅ {context.tool_name} tamamlandı")
        return None

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

## Yaygın Kullanım Durumları

### 1. Güvenlik Önlemleri (Safety Guardrails)

```python
@before_tool_call
def safety_check(context: ToolCallHookContext) -> bool | None:
    # Zarar verebilecek araçları engelleyin
    destructive_tools = [
        'delete_file',
        'drop_table',
        'remove_user',
        'system_shutdown'
    ]

    if context.tool_name in destructive_tools:
        print(f"🛑 Yıkıcı araç engellendi: {context.tool_name}")
        return False

    # Hassas işlemler için uyarın
    sensitive_tools = ['send_email', 'post_to_social_media', 'charge_payment']
    if context.tool_name in sensitive_tools:
        print(f"⚠️  Hassas araç yürütülüyor: {context.tool_name}")

    return None
```

### 2. İnsan Onay Geçidi

```python
@before_tool_call
def require_approval_for_actions(context: ToolCallHookContext) -> bool | None:
    approval_required = [
        'send_email',
        'make_purchase',
        'delete_file',
        'post_message'
    ]

    if context.tool_name in approval_required:
        response = context.request_human_input(
            prompt=f"{context.tool_name} onaylansın mı?",
            default_message=f"Giriş: {context.tool_input}\nOnaylamak için 'evet' yazın:"
        )

        if response.lower() != 'evet':
            print(f"❌ Araç yürütme reddedildi: {context.tool_name}")
            return False

    return None
```

### 3. Giriş Doğrulama ve Temizleme

```python
@before_tool_call
def validate_and_sanitize_inputs(context: ToolCallHookContext) -> bool | None:
    # Arama sorgularını doğrula
    if context.tool_name == 'web_search':
        query = context.tool_input.get('query', '')
        if len(query) < 3:
            print("❌ Arama sorgusu çok kısa")
            return False

        # Sorguyu temizle
        context.tool_input['query'] = query.strip().lower()

    # Dosya yollarını doğrula
    if context.tool_name == 'read_file':
        path = context.tool_input.get('path', '')
        if '..' in path or path.startswith('/'):
            print("❌ Geçersiz dosya yolu")
            return False

    return None
```

### 4. Sonuç Temizleme (Result Sanitization)

```python
@after_tool_call
def sanitize_sensitive_data(context: ToolCallHookContext) -> str | None:
    if not context.tool_result:
        return None

    import re
    result = context.tool_result

    # API anahtarlarını kaldır
    result = re.sub(
        r'(api[_-]?key|token)["\']?\s*[:=]\s*["\']?[\w-]+',
        r'\1: [GİZLENDİ]',
        result,
        flags=re.IGNORECASE
    )

    # E-posta adreslerini kaldır
    result = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EPOSTA-GİZLENDİ]',
        result
    )

    # Kredi kartı numaralarını kaldır
    result = re.sub(
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        '[KART-GİZLENDİ]',
        result
    )

    return result
```

### 5. Araç Kullanım Analitiği

```python
import time
from collections import defaultdict

tool_stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'failures': 0})

@before_tool_call
def start_timer(context: ToolCallHookContext) -> None:
    context.tool_input['_start_time'] = time.time()
    return None

@after_tool_call
def track_tool_usage(context: ToolCallHookContext) -> None:
    start_time = context.tool_input.get('_start_time', time.time())
    duration = time.time() - start_time

    tool_stats[context.tool_name]['count'] += 1
    tool_stats[context.tool_name]['total_time'] += duration

    if not context.tool_result or 'hata' in context.tool_result.lower():
        tool_stats[context.tool_name]['failures'] += 1

    print(f"""
    📊 {context.tool_name} için Araç İstatistikleri:
    - Yürütme Sayısı: {tool_stats[context.tool_name]['count']}
    - Ortalama Süre: {tool_stats[context.tool_name]['total_time'] / tool_stats[context.tool_name]['count']:.2f}sn
    - Hata Sayısı: {tool_stats[context.tool_name]['failures']}
    """)

    return None
```

### 6. Hız Sınırlama (Rate Limiting)

```python
from collections import defaultdict
from datetime import datetime, timedelta

tool_call_history = defaultdict(list)

@before_tool_call
def rate_limit_tools(context: ToolCallHookContext) -> bool | None:
    tool_name = context.tool_name
    now = datetime.now()

    # Eski kayıtları temizle (1 dakikadan eski olanlar)
    tool_call_history[tool_name] = [
        call_time for call_time in tool_call_history[tool_name]
        if now - call_time < timedelta(minutes=1)
    ]

    # Hız sınırını kontrol et (dakikada maksimum 10 çağrı)
    if len(tool_call_history[tool_name]) >= 10:
        print(f"🚫 {tool_name} için hız sınırı aşıldı")
        return False

    # Bu çağrıyı kaydet
    tool_call_history[tool_name].append(now)
    return None
```

### 7. Araç Sonuçlarını Önbelleğe Alma

```python
import hashlib
import json

tool_cache = {}

def cache_key(tool_name: str, tool_input: dict) -> str:
    """Araç adı ve girişinden bir önbellek anahtarı oluşturur."""
    input_str = json.dumps(tool_input, sort_keys=True)
    return hashlib.md5(f"{tool_name}:{input_str}".encode()).hexdigest()

@before_tool_call
def check_cache(context: ToolCallHookContext) -> bool | None:
    key = cache_key(context.tool_name, context.tool_input)
    if key in tool_cache:
        print(f"💾 {context.tool_name} için önbellek isabeti (cache hit)")
        # Not: Before hook'undan önbelleğe alınmış sonucu döndüremezsiniz.
        # Bunu farklı şekilde uygulamak gerekir.
    return None

@after_tool_call
def cache_result(context: ToolCallHookContext) -> None:
    if context.tool_result:
        key = cache_key(context.tool_name, context.tool_input)
        tool_cache[key] = context.tool_result
        print(f"💾 {context.tool_name} sonucu önbelleğe alındı")
    return None
```

### 8. Hata Ayıklama Günlüğü (Debug Logging)

```python
@before_tool_call
def debug_tool_call(context: ToolCallHookContext) -> None:
    print(f"""
    🔍 Araç Çağrısı Hata Ayıklama:
    - Araç: {context.tool_name}
    - Temsilci: {context.agent.role if context.agent else 'Bilinmiyor'}
    - Görev: {context.task.description[:50] if context.task else 'Bilinmiyor'}...
    - Giriş: {context.tool_input}
    """)
    return None

@after_tool_call
def debug_tool_result(context: ToolCallHookContext) -> None:
    if context.tool_result:
        result_preview = context.tool_result[:200]
        print(f"✅ Sonuç Önizleme: {result_preview}...")
    else:
        print("⚠️  Sonuç döndürülmedi")
    return None
```

## Hook Yönetimi

### Hook'ların Kaydını Silme

```python
from crewai.hooks import (
    unregister_before_tool_call_hook,
    unregister_after_tool_call_hook
)

# Belirli bir hook'un kaydını sil
def my_hook(context):
    ...

register_before_tool_call_hook(my_hook)
# Daha sonra...
success = unregister_before_tool_call_hook(my_hook)
print(f"Kayıt silindi: {success}")
```

### Hook'ları Temizleme

```python
from crewai.hooks import (
    clear_before_tool_call_hooks,
    clear_after_tool_call_hooks,
    clear_all_tool_call_hooks
)

# Belirli hook türünü temizle
count = clear_before_tool_call_hooks()
print(f"{count} before hook'u temizlendi")

# Tüm araç hook'larını temizle
before_count, after_count = clear_all_tool_call_hooks()
print(f"{before_count} before ve {after_count} after hook'u temizlendi")
```

### Kayıtlı Hook'ları Listeleme

```python
from crewai.hooks import (
    get_before_tool_call_hooks,
    get_after_tool_call_hooks
)

# Mevcut hook'ları al
before_hooks = get_before_tool_call_hooks()
after_hooks = get_after_tool_call_hooks()

print(f"Kayıtlı: {len(before_hooks)} before, {len(after_hooks)} after")
```

## Gelişmiş Kalıplar

### Koşullu Hook Yürütme

```python
@before_tool_call
def conditional_blocking(context: ToolCallHookContext) -> bool | None:
    # Yalnızca belirli temsilciler için engelle
    if context.agent and context.agent.role == "junior_agent":
        if context.tool_name in ['delete_file', 'send_email']:
            print(f"❌ Junior temsilciler {context.tool_name} kullanamaz")
            return False

    # Yalnızca belirli görevler sırasında engelle
    if context.task and "hassas" in context.task.description.lower():
        if context.tool_name == 'web_search':
            print("❌ Hassas görevler için web araması engellendi")
            return False

    return None
```

### Bağlam Duyarlı Giriş Değişikliği

```python
@before_tool_call
def enhance_tool_inputs(context: ToolCallHookContext) -> None:
    # Temsilci rolüne bağlı olarak bağlam ekle
    if context.agent and context.agent.role == "araştırmacı":
        if context.tool_name == 'web_search':
            # Araştırmacılar için alan adı kısıtlamaları ekle
            context.tool_input['domains'] = ['edu', 'gov', 'org']

    # Göreve bağlı olarak bağlam ekle
    if context.task and "acil" in context.task.description.lower():
        if context.tool_name == 'send_email':
            context.tool_input['priority'] = 'high'

    return None
```

### Araç Zinciri İzleme (Tool Chain Monitoring)

```python
tool_call_chain = []

@before_tool_call
def track_tool_chain(context: ToolCallHookContext) -> None:
    tool_call_chain.append({
        'tool': context.tool_name,
        'timestamp': time.time(),
        'agent': context.agent.role if context.agent else 'Bilinmiyor'
    })

    # Olası sonsuz döngüleri tespit et
    recent_calls = tool_call_chain[-5:]
    if len(recent_calls) == 5 and all(c['tool'] == context.tool_name for c in recent_calls):
        print(f"⚠️  Uyarı: {context.tool_name} arka arkaya 5 kez çağrıldı")

    return None
```

## En İyi Uygulamalar

1. **Hook'ları Odaklanmış Tutun**: Her hook'un tek bir sorumluluğu olmalıdır
2. **Ağır Hesaplamalardan Kaçının**: Hook'lar her araç çağrısında çalışır
3. **Hataları Zarif Bir Şekilde Yönetin**: Hook hatalarını önlemek için try-except kullanın
4. **Tip İpuçlarını Kullanın**: Daha iyi IDE desteği için `ToolCallHookContext`'ten yararlanın
5. **Engelleme Koşullarını Belgeleyin**: Araçların neden/ne zaman engellendiğini netleştirin
6. **Hook'ları Bağımsız Olarak Test Edin**: Üretim ortamında kullanmadan önce hook'ları test edin
7. **Testlerde Hook'ları Temizleyin**: Test çalışmaları arasında `clear_all_tool_call_hooks()` kullanın
8. **Yerinde Değiştirin**: `context.tool_input`'u her zaman yerinde (in-place) değiştirin, asla tamamen değiştirmeyin
9. **Önemli Kararları Günlüğe Kaydedin**: Özellikle araç yürütmesini engellediğinizde
10. **Performansı Göz Önünde Bulundurun**: Mümkün olduğunda pahalı doğrulamaları önbelleğe alın

## Hata Yönetimi

```python
@before_tool_call
def safe_validation(context: ToolCallHookContext) -> bool | None:
    try:
        # Doğrulama mantığınız
        if not validate_input(context.tool_input):
            return False
    except Exception as e:
        print(f"⚠️ Hook hatası: {e}")
        # Karar verin: hata durumunda izin mi verilsin yoksa engellensin mi
        return None  # Hataya rağmen yürütmeye izin ver
```

## Tip Güvenliği

```python
from crewai.hooks import ToolCallHookContext, BeforeToolCallHookType, AfterToolCallHookType

# Açık tip notasyonları
def my_before_hook(context: ToolCallHookContext) -> bool | None:
    return None

def my_after_hook(context: ToolCallHookContext) -> str | None:
    return None

# Tip güvenli kayıt
register_before_tool_call_hook(my_before_hook)
register_after_tool_call_hook(my_after_hook)
```

## Mevcut Araçlarla Entegrasyon

### Mevcut Doğrulamayı Sarmalama

```python
def existing_validator(tool_name: str, inputs: dict) -> bool:
    """Mevcut doğrulama fonksiyonunuz."""
    # Doğrulama mantığınız
    return True

@before_tool_call
def integrate_validator(context: ToolCallHookContext) -> bool | None:
    if not existing_validator(context.tool_name, context.tool_input):
        print(f"❌ {context.tool_name} için doğrulama başarısız oldu")
        return False
    return None
```

### Harici Sistemlere Günlükleme

```python
import logging

logger = logging.getLogger(__name__)

@before_tool_call
def log_to_external_system(context: ToolCallHookContext) -> None:
    logger.info(f"Araç çağrısı: {context.tool_name}", extra={
        'tool_name': context.tool_name,
        'tool_input': context.tool_input,
        'agent': context.agent.role if context.agent else None
    })
    return None
```

## Sorun Giderme

### Hook Yürütülmüyor

* Hook'un ekip yürütülmeden önce kaydedildiğini doğrulayın
* Önceki bir hook'un `False` döndürüp döndürmediğini kontrol edin (yürütmeyi ve sonraki hook'ları engeller)
* Hook imzasının beklenen tiple eşleştiğinden emin olun

### Giriş Değişiklikleri Çalışmıyor

* Yerinde (in-place) değişiklikler kullanın: `context.tool_input['anahtar'] = değer`
* Sözlüğü tamamen değiştirmeyin: `context.tool_input = {}`

### Sonuç Değişiklikleri Çalışmıyor

* After hook'larından değiştirilmiş diziyi (string) döndürün
* `None` döndürmek orijinal sonucu korur
* Aracın gerçekten bir sonuç döndürdüğünden emin olun

### Araç Beklenmedik Bir Şekilde Engellendi

* Tüm before hook'larını engelleme koşulları açısından kontrol edin
* Hook yürütme sırasını doğrulayın
* Hangi hook'un engellediğini belirlemek için hata ayıklama günlüğü ekleyin

## Sonuç

Araç Çağrı Hook'ları, CrewAI'da araç yürütmesini kontrol etmek ve izlemek için güçlü yetenekler sağlar. Güvenlik önlemleri, onay geçitleri, giriş doğrulaması, sonuç temizleme, günlükleme ve analitik uygulamak için bunları kullanın. Düzgün hata yönetimi ve tip güvenliği ile birleştiğinde, hook'lar kapsamlı gözlemlenebilirlik ile güvenli ve üretime hazır temsilci sistemleri oluşturulmasına olanak tanır.
