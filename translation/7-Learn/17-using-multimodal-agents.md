# Çok Modlu Ajanları Kullanma

> CrewAI çerçevesinde görsel ve diğer metin dışı içerikleri işlemek için ajanlarınızda çok modlu yetenekleri nasıl etkinleştireceğinizi ve kullanacağınızı öğrenin.

## Çok Modlu Ajanları Kullanma

CrewAI, hem metin hem de görsel gibi metin dışı içerikleri işleyebilen çok modlu ajanları destekler. Bu kılavuz, ajanlarınızda çok modlu yetenekleri nasıl etkinleştireceğinizi ve kullanacağınızı gösterecektir.

### Çok Modlu Yetenekleri Etkinleştirme

Çok modlu bir ajan oluşturmak için ajanı başlatırken `multimodal` parametresini `True` olarak ayarlayın:

```python
from crewai import Agent

agent = Agent(
    role="Image Analyst",
    goal="Görsellerden içgörüler analiz et ve çıkar",
    backstory="Görsel içerik yorumlamada uzman, görsel analizde yıllarca deneyim sahibi",
    multimodal=True  # Bu, çok modlu yetenekleri etkinleştirir
)
```

`multimodal=True` ayarladığınızda ajan, `AddImageTool` dahil metin dışı içerikleri yönetmek için gerekli araçlarla otomatik olarak yapılandırılır.

### Görsellerle Çalışma

Çok modlu ajan, görselleri işlemesine imkân tanıyan `AddImageTool` ile önceden yapılandırılmış olarak gelir. Bu aracı manuel olarak eklemenize gerek yoktur — çok modlu yetenekleri etkinleştirdiğinizde otomatik olarak dahil edilir.

Bir görseli analiz etmek için çok modlu ajanın nasıl kullanılacağını gösteren eksiksiz bir örnek:

```python
from crewai import Agent, Task, Crew

# Çok modlu bir ajan oluşturun
image_analyst = Agent(
    role="Product Analyst",
    goal="Ürün görsellerini analiz et ve ayrıntılı açıklamalar sun",
    backstory="Tasarım ve özellikler hakkında derin bilgiye sahip görsel ürün analizinde uzman",
    multimodal=True
)

# Görsel analizi için bir görev oluşturun
task = Task(
    description="https://example.com/product.jpg adresindeki ürün görselini analiz edin ve ayrıntılı bir açıklama sunun",
    expected_output="Ürün görselinin ayrıntılı açıklaması",
    agent=image_analyst
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(
    agents=[image_analyst],
    tasks=[task]
)

result = crew.kickoff()
```

### Bağlamla Gelişmiş Kullanım

Çok modlu ajanlar için görevler oluştururken görsel hakkında ek bağlam veya belirli sorular sağlayabilirsiniz. Görev açıklaması, ajanın odaklanmasını istediğiniz spesifik konuları içerebilir:

```python
from crewai import Agent, Task, Crew

# Ayrıntılı analiz için çok modlu bir ajan oluşturun
expert_analyst = Agent(
    role="Visual Quality Inspector",
    goal="Ürün görsellerinin ayrıntılı kalite analizini gerçekleştir",
    backstory="Görsel denetimde uzmanlığa sahip kıdemli kalite kontrol uzmanı",
    multimodal=True  # AddImageTool otomatik olarak dahil edilir
)

# Belirli analiz gereksinimleriyle bir görev oluşturun
inspection_task = Task(
    description="""
    https://example.com/product.jpg adresindeki ürün görselini şu konulara odaklanarak analiz edin:
    1. Malzeme kalitesi
    2. Üretim hataları
    3. Standartlara uygunluk
    Tespit edilen sorunları vurgulayan ayrıntılı bir rapor sunun.
    """,
    expected_output="Tespit edilen sorunları vurgulayan ayrıntılı bir rapor",
    agent=expert_analyst
)

# Ekibi oluşturun ve çalıştırın
crew = Crew(
    agents=[expert_analyst],
    tasks=[inspection_task]
)

result = crew.kickoff()
```

### Araç Ayrıntıları

Çok modlu ajanlarla çalışırken `AddImageTool` aşağıdaki şemayla otomatik olarak yapılandırılır:

```python
class AddImageToolSchema:
    image_url: str  # Zorunlu: İşlenecek görselin URL'si veya yolu
    action: Optional[str] = None  # İsteğe bağlı: Görsel hakkında ek bağlam veya belirli sorular
```

Çok modlu ajan, yerleşik araçları aracılığıyla görsel işlemeyi otomatik olarak yöneterek şunları yapabilir:

- URL'ler veya yerel dosya yolları aracılığıyla görsellere erişmek
- İsteğe bağlı bağlam veya belirli sorularla görsel içeriği işlemek
- Görsel bilgiye ve görev gereksinimlerine dayalı analiz ve içgörüler sunmak

### En İyi Uygulamalar

Çok modlu ajanlarla çalışırken şu en iyi uygulamaları göz önünde bulundurun:

1. **Görsel Erişimi**
   - Görsellerinizin ajanın erişebileceği URL'ler aracılığıyla erişilebilir olduğundan emin olun
   - Yerel görseller için bunları geçici olarak barındırmayı veya mutlak dosya yolları kullanmayı düşünün
   - Görevleri çalıştırmadan önce görsel URL'lerinin geçerli ve erişilebilir olduğunu doğrulayın

2. **Görev Açıklaması**
   - Ajanın görselin hangi yönlerini analiz etmesini istediğinizi spesifik biçimde belirtin
   - Görev açıklamasına net sorular veya gereksinimler ekleyin
   - Odaklanmış analiz için isteğe bağlı `action` parametresini kullanmayı düşünün

3. **Kaynak Yönetimi**
   - Görsel işleme, yalnızca metin içeren görevlere kıyasla daha fazla hesaplama kaynağı gerektirebilir
   - Bazı dil modelleri görsel veriler için base64 kodlaması gerektirebilir
   - Performansı optimize etmek için birden fazla görsel için toplu işlemeyi düşünün

4. **Ortam Kurulumu**
   - Ortamınızın görsel işleme için gerekli bağımlılıklara sahip olduğunu doğrulayın
   - Dil modelinizin çok modlu yetenekleri desteklediğinden emin olun
   - Kurulumunuzu doğrulamak için önce küçük görsellerle test edin

5. **Hata Yönetimi**
   - Görsel yükleme hataları için uygun hata yönetimi uygulayın
   - Görsel işleme başarısız olduğunda yedek stratejiler oluşturun
   - Hata ayıklama için görsel işleme operasyonlarını izleyin ve kaydedin
