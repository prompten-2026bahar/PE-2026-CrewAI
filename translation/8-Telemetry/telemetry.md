# Telemetri

> CrewAI tarafından toplanan telemetri verilerini anlamak ve bu verilerin kütüphanenin geliştirilmesine nasıl katkıda bulunduğunu öğrenmek.

## Telemetri

> **Not:**
> Varsayılan olarak, GDPR (Genel Veri Koruma Yönetmeliği) ve diğer gizlilik düzenlemeleri kapsamında kişisel bilgi sayılabilecek hiçbir veri toplamıyoruz.
> Araç (Tool) isimlerini ve Ajan (Agent) rollerini topluyoruz, bu nedenle araç isimlerine veya ajan rollerine herhangi bir kişisel bilgi dahil etmemeniz önerilir.
> Kişisel bilgi toplanmadığı için veri ikameti (data residency) konusunda endişelenmenize gerek yoktur.
> `share_crew` özelliği etkinleştirildiğinde, kullanıcı tarafından dahil edilmişse kişisel bilgiler içerebilecek ek veriler toplanır.
> Kullanıcılar, gizlilik düzenlemelerine uyumu sağlamak için bu özelliği etkinleştirirken dikkatli olmalıdır.

CrewAI, kütüphaneyi geliştirme temel amacıyla kullanım istatistiklerini toplamak için anonim telemetri kullanır. Odak noktamız, kullanıcılarımız tarafından en çok kullanılan özellikleri, entegrasyonları ve araçları iyileştirmek ve geliştirmektir.

Varsayılan olarak; istemler (prompts), görev açıklamaları, ajanların arka plan hikayeleri (backstories) veya hedefleri, araçların kullanımı, API çağrıları, yanıtlar, ajanlar tarafından işlenen herhangi bir veri veya sırlar (secrets) ve ortam değişkenleri ile ilgili **hiçbir kişisel veri toplanmadığını** anlamak çok önemlidir.

`share_crew` özelliği etkinleştirildiğinde; daha derin içgörüler sağlamak amacıyla görev açıklamaları, ajanların arka plan hikayeleri veya hedefleri ve diğer spesifik nitelikleri içeren ayrıntılı veriler toplanır. Bu genişletilmiş veri toplama süreci, kullanıcılar bunları ekiplerine veya görevlerine dahil etmişse kişisel bilgiler içerebilir. Kullanıcılar, `share_crew` özelliğini etkinleştirmeden önce ekiplerinin ve görevlerinin içeriğini dikkatlice değerlendirmelidir.

Kullanıcılar, `CREWAI_DISABLE_TELEMETRY` ortam değişkenini `true` olarak ayarlayarak veya `OTEL_SDK_DISABLED` değişkenini `true` olarak ayarlayarak telemetriyi devre dışı bırakabilirler (ikincisinin tüm OpenTelemetry enstrümantasyonunu küresel olarak devre dışı bıraktığını unutmayın).

### Örnekler:

```python  theme={null}
# Yalnızca CrewAI telemetrisini devre dışı bırak
os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'

# Tüm OpenTelemetry'yi devre dışı bırak (CrewAI dahil)
os.environ['OTEL_SDK_DISABLED'] = 'true'
```

### Veri Açıklaması:

| Varsayılan | Veri | Neden ve Detaylar |
| :--- | :--- | :--- |
| Evet | CrewAI ve Python Sürümü | Yazılım sürümlerini takip eder. Örnek: CrewAI v1.2.3, Python 3.8.10. Kişisel veri içermez. |
| Evet | Ekip (Crew) Meta Verileri | Şunları içerir: Rastgele oluşturulmuş anahtar ve ID, işlem tipi (örn. 'sequential', 'parallel'), bellek kullanımı için boole bayrağı (true/false), görev sayısı, ajan sayısı. Hepsi kişisel olmayan verilerdir. |
| Evet | Ajan Verileri | Şunları içerir: Rastgele oluşturulmuş anahtar ve ID, rol adı (kişisel bilgi içermemelidir), boole ayarları (ayrıntılı günlük, delegasyon etkin, kod yürütme izni), maksimum yineleme, maksimum RPM, maksimum deneme sınırı, LLM bilgisi (bkz. LLM Nitelikleri), araç isimleri listesi (kişisel bilgi içermemelidir). Kişisel veri içermez. |
| Evet | Görev Meta Verileri | Şunları içerir: Rastgele oluşturulmuş anahtar ve ID, boole yürütme ayarları (async\_execution, human\_input), ilişkili ajanın rolü ve anahtarı, araç isimleri listesi. Hepsi kişisel olmayan verilerdir. |
| Evet | Araç Kullanım İstatistikleri | Şunları içerir: Araç adı (kişisel bilgi içermemelidir), deneme sayısı (tam sayı), kullanılan LLM nitelikleri. Kişisel veri içermez. |
| Evet | Test Yürütme Verileri | Şunları içerir: Ekibin rastgele oluşturulmuş anahtarı ve ID'si, yineleme sayısı, kullanılan model adı, kalite puanı (float), yürütme süresi (saniye cinsinden). Hepsi kişisel olmayan verilerdir. |
| Evet | Görev Yaşam Döngüsü Verileri | Şunları içerir: Oluşturma ve yürütme başlangıç/bitiş zamanları, ekip ve görev tanımlayıcıları. Zaman damgalı 'span'lar olarak saklanır. Kişisel veri içermez. |
| Evet | LLM Nitelikleri | Şunları içerir: Adı, model\_name, model, top\_k, sıcaklık (temperature) ve LLM'nin sınıf adı. Hepsi teknik, kişisel olmayan verilerdir. |
| Evet | crewAI CLI kullanarak Ekip Dağıtım denemesi | Şunları içerir: Bir dağıtım yapıldığı gerçeği, ekip ID'si ve günlüklerin çekilmeye çalışılıp çalışılmadığı. Başka veri içermez. |
| Hayır | Ajanın Genişletilmiş Verileri | Şunları içerir: Hedef açıklaması, arka plan hikayesi metni, i18n istem dosyası tanımlayıcısı. Kullanıcılar, metin alanlarına kişisel bilgi dahil edilmediğinden emin olmalıdır. |
| Hayır | Detaylı Görev Bilgileri | Şunları içerir: Görev açıklaması, beklenen çıktı açıklaması, bağlam referansları. Kullanıcılar, bu alanlara kişisel bilgi dahil edilmediğinden emin olmalıdır. |
| Hayır | Ortam Bilgileri | Şunları içerir: Platform, sürüm, sistem, versiyon ve CPU sayısı. Örnek: 'Windows 10', 'x86\_64'. Kişisel veri içermez. |
| Hayır | Ekip ve Görev Giriş ve Çıktıları | Şunları içerir: Tanımlanamayan veriler olarak giriş parametreleri ve çıktı sonuçları. Kullanıcılar, kişisel bilgi dahil edilmediğinden emin olmalıdır. |
| Hayır | Kapsamlı Ekip Yürütme Verileri | Şunları içerir: Ekip operasyonlarının detaylı günlükleri, tüm ajan ve görev verileri, nihai çıktı. Hepsi doğası gereği kişisel olmayan ve teknik verilerdir. |

> **Not:**
> "Varsayılan" sütunundaki "Hayır", bu verilerin yalnızca `share_crew` değeri `true` olarak ayarlandığında toplandığını gösterir.

### Daha Fazla Telemetri Paylaşımına Katılma (Opt-In)

Kullanıcılar, ekip yapılandırmalarında `share_crew` özniteliğini `True` yaparak tüm telemetri verilerini paylaşmayı seçebilirler. `share_crew` özelliğinin etkinleştirilmesi, görevlerin `goal` (hedef), `backstory` (arka plan hikayesi), `context` (bağlam) ve `output` (çıktı) dahil olmak üzere ayrıntılı ekip ve görev yürütme verilerinin toplanmasına neden olur. Bu, kullanım kalıpları hakkında daha derin bir içgörü sağlar.

> **Uyarı:**
> Eğer `share_crew` özelliğini etkinleştirirseniz; ekip yapılandırmalarına, görev açıklamalarına veya çıktılara dahil edilmişse toplanan veriler kişisel bilgiler içerebilir.
> Kullanıcılar, bu özelliği etkinleştirmeden önce verilerini dikkatlice gözden geçirmeli ve GDPR ile diğer geçerli gizlilik düzenlemelerine uyumu sağlamalıdır.
