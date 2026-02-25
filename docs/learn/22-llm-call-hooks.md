> ## Dokümantasyon İndeksi
> Tüm dokümantasyon indeksine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları öğrenmek için bu dosyayı kullanın.

# LLM Çağrı Hook'ları (LLM Call Hooks)

> CrewAI'da dil modeli etkileşimlerini yakalamayı, değiştirmeyi ve kontrol etmeyi öğrenin.

LLM Çağrı Hook'ları, temsilci yürütmesi sırasında dil modeli etkileşimleri üzerinde ince ayarlı kontrol sağlar. Bu hook'lar LLM çağrılarını yakalamanıza, istemleri (prompts) değiştirmenize, yanıtları dönüştürmenize, onay geçitleri uygulamanıza ve özel günlükleme veya izleme eklemenize olanak tanır.

## Genel Bakış

LLM hook'ları iki kritik noktada yürütülür:

* **LLM Çağrısından Önce**: Mesajları değiştirin, girişleri doğrulayın veya yürütmeyi engelleyin
* **LLM Çağrısından Sonra**: Yanıtları dönüştürün, çıktıları temizleyin veya konuşma geçmişini değiştirin

## Hook Türleri

### LLM Çağrısı Öncesi Hook'lar (Before LLM Call Hooks)

Her LLM çağrısından önce yürütülür, bu hook'lar şunları yapabilir:

* LLM'e gönderilen mesajları inceleyebilir ve değiştirebilir
* Koşullara bağlı olarak LLM yürütmesini engelleyebilir
* Hız sınırlama (rate limiting) veya onay geçitleri uygulayabilir
* Bağlam veya sistem mesajları ekleyebilir
* İstek ayrıntılarını günlüğe kaydedebilir

**İmza:**

```python
def before_hook(context: LLMCallHookContext) -> bool | None:
    # Yürütmeyi engellemek için False döndürün
    # Yürütmeye izin vermek için True veya None döndürün
    ...
```

### LLM Çağrısı Sonrası Hook'lar (After LLM Call Hooks)

Her LLM çağrısından sonra yürütülür, bu hook'lar şunları yapabilir:

* LLM yanıtlarını değiştirebilir veya temizleyebilir
* Meta veri veya biçimlendirme ekleyebilir
* Yanıt ayrıntılarını günlüğe kaydedebilir
* Konuşma geçmişini güncelleyebilir
* İçerik filtreleme uygulayabilir

**İmza:**

```python
def after_hook(context: LLMCallHookContext) -> str | None:
    # Değiştirilmiş yanıt dizisini döndürün
    # Orijinal yanıtı korumak için None döndürün
    ...
```

## LLM Hook Bağlamı (Context)

`LLMCallHookContext` nesnesi yürütme durumuna kapsamlı erişim sağlar:

```python
class LLMCallHookContext:
    executor: CrewAgentExecutor  # Tam yürütücü referansı
    messages: list               # Değiştirilebilir mesaj listesi
    agent: Agent                 # Mevcut temsilci
    task: Task                   # Mevcut görev
    crew: Crew                   # Ekip örneği
    llm: BaseLLM                 # LLM örneği
    iterations: int              # Mevcut tekrar sayısı
    response: str | None         # LLM yanıtı (yalnızca after hook'larından sonra)
```

### Mesajları Değiştirme

**Önemli:** Mesajları her zaman yerinde (in-place) değiştirin:

```python
# ✅ Doğru - yerinde değiştir
def add_context(context: LLMCallHookContext) -> None:
    context.messages.append({"role": "system", "content": "Kısa ve öz ol"})

# ❌ Yanlış - liste referansını değiştirir
def wrong_approach(context: LLMCallHookContext) -> None:
    context.messages = [{"role": "system", "content": "Kısa ve öz ol"}]
```

## Kayıt Yöntemleri

### 1. Global Hook Kaydı

Tüm ekiplerdeki tüm LLM çağrılarına uygulanan hook'ları kaydedin:

```python
from crewai.hooks import register_before_llm_call_hook, register_after_llm_call_hook

def log_llm_call(context):
    print(f"{context.agent.role} tarafından {context.iterations}. tekrarda LLM çağrısı yapıldı")
    return None  # Yürütmeye izin ver

register_before_llm_call_hook(log_llm_call)
```

### 2. Dekoratör Tabanlı Kayıt

Daha temiz bir yazım için dekoratörleri kullanın:

```python
from crewai.hooks import before_llm_call, after_llm_call

@before_llm_call
def validate_iteration_count(context):
    if context.iterations > 10:
        print("⚠️ Maksimum tekrar sayısı aşıldı")
        return False  # Yürütmeyi engelle
    return None

@after_llm_call
def sanitize_response(context):
    if context.response and "API_KEY" in context.response:
        return context.response.replace("API_KEY", "[GİZLENDİ]")
    return None
```

### 3. Ekip Kapsamlı (Crew-Scoped) Hook'lar

Belirli bir ekip örneği için hook'ları kaydedin:

```python
@CrewBase
class MyProjCrew:
    @before_llm_call_crew
    def validate_inputs(self, context):
        # Yalnızca bu ekip için geçerlidir
        if context.iterations == 0:
            print(f"Görev başlatılıyor: {context.task.description}")
        return None

    @after_llm_call_crew
    def log_responses(self, context):
        # Ekibe özel yanıt günlüğe kaydetme
        print(f"Yanıt uzunluğu: {len(context.response)}")
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

### 1. Tekrar Sınırlama

```python
@before_llm_call
def limit_iterations(context: LLMCallHookContext) -> bool | None:
    max_iterations = 15
    if context.iterations > max_iterations:
        print(f"⛔ Engellendi: {max_iterations} tekrar sayısı aşıldı")
        return False  # Yürütmeyi engelle
    return None
```

### 2. İnsan Onay Geçidi

```python
@before_llm_call
def require_approval(context: LLMCallHookContext) -> bool | None:
    if context.iterations > 5:
        response = context.request_human_input(
            prompt=f"Tekrar {context.iterations}: LLM çağrısını onayla?",
            default_message="Onaylamak için Enter'a basın veya engellemek için 'hayır' yazın:"
        )
        if response.lower() == "hayır":
            print("🚫 LLM çağrısı kullanıcı tarafından engellendi")
            return False
    return None
```

### 3. Sistem Bağlamı Ekleme

```python
@before_llm_call
def add_guardrails(context: LLMCallHookContext) -> None:
    # Her LLM çağrısına güvenlik yönergeleri ekleyin
    context.messages.append({
        "role": "system",
        "content": "Yanıtların gerçeklere dayalı olduğundan ve mümkün olduğunda kaynak gösterildiğinden emin olun."
    })
    return None
```

### 4. Yanıt Temizleme (Response Sanitization)

```python
@after_llm_call
def sanitize_sensitive_data(context: LLMCallHookContext) -> str | None:
    if not context.response:
        return None

    # Hassas kalıpları kaldırın
    import re
    sanitized = context.response
    sanitized = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[TCKN-GİZLENDİ]', sanitized)
    sanitized = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[KART-GİZLENDİ]', sanitized)

    return sanitized
```

### 5. Maliyet Takibi

```python
import tiktoken

@before_llm_call
def track_token_usage(context: LLMCallHookContext) -> None:
    encoding = tiktoken.get_encoding("cl100k_base")
    total_tokens = sum(
        len(encoding.encode(msg.get("content", "")))
        for msg in context.messages
    )
    print(f"📊 Giriş token'ları: ~{total_tokens}")
    return None

@after_llm_call
def track_response_tokens(context: LLMCallHookContext) -> None:
    if context.response:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = len(encoding.encode(context.response))
        print(f"📊 Yanıt token'ları: ~{tokens}")
    return None
```

### 6. Hata Ayıklama Günlüğü (Debug Logging)

```python
@before_llm_call
def debug_request(context: LLMCallHookContext) -> None:
    print(f"""
    🔍 LLM Çağrısı Hata Ayıklama (Debug):
    - Temsilci: {context.agent.role}
    - Görev: {context.task.description[:50]}...
    - Tekrar: {context.iterations}
    - Mesaj Sayısı: {len(context.messages)}
    - Son Mesaj: {context.messages[-1] if context.messages else 'Yok'}
    """)
    return None

@after_llm_call
def debug_response(context: LLMCallHookContext) -> None:
    if context.response:
        print(f"✅ Yanıt Önizleme: {context.response[:100]}...")
    return None
```

## Hook Yönetimi

### Hook'ların Kaydını Silme

```python
from crewai.hooks import (
    unregister_before_llm_call_hook,
    unregister_after_llm_call_hook
)

# Belirli bir hook'un kaydını sil
def my_hook(context):
    ...

register_before_llm_call_hook(my_hook)
# Daha sonra...
unregister_before_llm_call_hook(my_hook)  # Bulunursa True döner
```

### Hook'ları Temizleme

```python
from crewai.hooks import (
    clear_before_llm_call_hooks,
    clear_after_llm_call_hooks,
    clear_all_llm_call_hooks
)

# Belirli hook türünü temizle
count = clear_before_llm_call_hooks()
print(f"{count} before hook'u temizlendi")

# Tüm LLM hook'larını temizle
before_count, after_count = clear_all_llm_call_hooks()
print(f"{before_count} before ve {after_count} after hook'u temizlendi")
```

### Kayıtlı Hook'ları Listeleme

```python
from crewai.hooks import (
    get_before_llm_call_hooks,
    get_after_llm_call_hooks
)

# Mevcut hook'ları al
before_hooks = get_before_llm_call_hooks()
after_hooks = get_after_llm_call_hooks()

print(f"Kayıtlı: {len(before_hooks)} before, {len(after_hooks)} after")
```

## Gelişmiş Kalıplar

### Koşullu Hook Yürütme

```python
@before_llm_call
def conditional_blocking(context: LLMCallHookContext) -> bool | None:
    # Yalnızca belirli temsilciler için engelle
    if context.agent.role == "araştırmacı" and context.iterations > 10:
        return False

    # Yalnızca belirli görevler için engelle
    if "hassas" in context.task.description.lower() and context.iterations > 5:
        return False

    return None
```

### Bağlam Duyarlı Değişiklikler

```python
@before_llm_call
def adaptive_prompting(context: LLMCallHookContext) -> None:
    # Tekrar sayısına bağlı olarak farklı bağlam ekle
    if context.iterations == 0:
        context.messages.append({
            "role": "system",
            "content": "Üst düzey bir genel bakışla başla."
        })
    elif context.iterations > 3:
        context.messages.append({
            "role": "system",
            "content": "Belirli ayrıntılara odaklan ve örnekler ver."
        })
    return None
```

### Hook Zincirleme (Chaining Hooks)

```python
# Birden fazla hook kayıt sırasına göre yürütülür

@before_llm_call
def first_hook(context):
    print("1. İlk hook yürütüldü")
    return None

@before_llm_call
def second_hook(context):
    print("2. İkinci hook yürütüldü")
    return None

@before_llm_call
def blocking_hook(context):
    if context.iterations > 10:
        print("3. Engelleyici hook - yürütme durduruldu")
        return False  # Sonraki hook'lar yürütülmez
    print("3. Engelleyici hook - yürütmeye izin verildi")
    return None
```

## En İyi Uygulamalar

1. **Hook'ları Odaklanmış Tutun**: Her hook'un tek bir sorumluluğu olmalıdır
2. **Ağır Hesaplamalardan Kaçının**: Hook'lar her LLM çağrısında çalışır
3. **Hataları Zarif Bir Şekilde Yönetin**: Hook hatalarının yürütmeyi bozmasını önlemek için try-except kullanın
4. **Tip İpuçlarını Kullanın**: Daha iyi IDE desteği için `LLMCallHookContext`'ten yararlanın
5. **Hook Davranışını Belgeleyin**: Özellikle engelleme koşulları için
6. **Hook'ları Bağımsız Olarak Test Edin**: Üretim ortamında kullanmadan önce hook'ları birim testinden geçirin
7. **Testlerde Hook'ları Temizleyin**: Test çalışmaları arasında `clear_all_llm_call_hooks()` kullanın
8. **Yerinde Değiştirin**: `context.messages`'ı her zaman yerinde (in-place) değiştirin, asla referansı tamamen değiştirmeyin

## Hata Yönetimi

```python
@before_llm_call
def safe_hook(context: LLMCallHookContext) -> bool | None:
    try:
        # Hook mantığınız
        if some_condition:
            return False
    except Exception as e:
        print(f"⚠️ Hook hatası: {e}")
        # Karar verin: hata durumunda izin mi verilsin yoksa engellensin mi
        return None  # Hataya rağmen yürütmeye izin ver
```

## Tip Güvenliği

```python
from crewai.hooks import LLMCallHookContext, BeforeLLMCallHookType, AfterLLMCallHookType

# Açık tip notasyonları
def my_before_hook(context: LLMCallHookContext) -> bool | None:
    return None

def my_after_hook(context: LLMCallHookContext) -> str | None:
    return None

# Tip güvenli kayıt
register_before_llm_call_hook(my_before_hook)
register_after_llm_call_hook(my_after_hook)
```

## Sorun Giderme

### Hook Yürütülmüyor

* Hook'un ekip yürütülmeden önce kaydedildiğini doğrulayın
* Önceki bir hook'un `False` döndürüp döndürmediğini kontrol edin (sonraki hook'ları engeller)
* Hook imzasının beklenen tiple eşleştiğinden emin olun

### Mesaj Değişiklikleri Kalıcı Olmuyor

* Yerinde (in-place) değişiklikler kullanın: `context.messages.append()`
* Listeyi tamamen değiştirmeyin: `context.messages = []`

### Yanıt Değişiklikleri Çalışmıyor

* After hook'larından değiştirilmiş diziyi (string) döndürün
* `None` döndürmek orijinal yanıtı korur

## Sonuç

LLM Çağrı Hook'ları, CrewAI'da dil modeli etkileşimlerini kontrol etmek ve izlemek için güçlü yetenekler sağlar. Güvenlik önlemleri, onay geçitleri, günlükleme, maliyet takibi ve yanıt temizleme uygulamak için bunları kullanın. Düzgün hata yönetimi ve tip güvenliği ile birleştiğinde, hook'lar sağlam ve üretime hazır temsilci sistemleri oluşturulmasına olanak tanır.
