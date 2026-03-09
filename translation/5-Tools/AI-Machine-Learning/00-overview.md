# Genel Bakış

> Yapay zeka (AI) servislerinden yararlanın, görüntüler oluşturun, görsel verileri işleyin ve akıllı sistemler geliştirin.

Bu araçlar, ajanlarınızı görüntü oluşturma, görüntü işleme ve akıllı kod yürütme gibi gelişmiş yeteneklerle donatmak için yapay zeka ve makine öğrenimi (ML) servisleriyle entegre olur.

## **Mevcut Araçlar**

- **[DALL-E Tool](/en/tools/ai-ml/dalletool)**: OpenAI'ın DALL-E modelini kullanarak yapay zeka görüntüleri oluşturun.
- **[Vision Tool](/en/tools/ai-ml/visiontool)**: Bilgisayarlı görme (computer vision) yetenekleriyle görüntüleri işleyin ve analiz edin.
- **[AI Mind Tool](/en/tools/ai-ml/aimindtool)**: Gelişmiş yapay zeka akıl yürütme ve karar verme yetenekleri.
- **[LlamaIndex Tool](/en/tools/ai-ml/llamaindextool)**: LlamaIndex ile bilgi tabanları ve veri alma (retrieval) sistemleri oluşturun.
- **[LangChain Tool](/en/tools/ai-ml/langchaintool)**: Karmaşık yapay zeka iş akışları için LangChain ile entegrasyon sağlayın.
- **[RAG Tool](/en/tools/ai-ml/ragtool)**: Veri Alma Destekli Nesil (Retrieval-Augmented Generation) sistemlerini uygulayın.
- **[Code Interpreter Tool](/en/tools/ai-ml/codeinterpretertool)**: Python kodlarını yürütün ve veri analizi yapın.

## **Genel Kullanım Durumları**

* **İçerik Oluşturma**: Görüntüler, metinler ve multimedya içerikleri oluşturun.
* **Veri Analizi**: Kodları çalıştırarak karmaşık veri setlerini analiz edin.
* **Bilgi Sistemleri**: RAG sistemleri ve akıllı veritabanları oluşturun.
* **Bilgisayarlı Görme**: Görsel içerikleri işleyin ve anlamlandırın.
* **Yapay Zeka Güvenliği**: İçerik denetimi ve güvenlik kontrollerini uygulayın.

```python  theme={null}
from crewai_tools import DallETool, VisionTool, CodeInterpreterTool

# Yapay zeka araçlarını oluşturun
image_generator = DallETool()
vision_processor = VisionTool()
code_executor = CodeInterpreterTool()

# Ajanınıza ekleyin
agent = Agent(
    role="Yapay Zeka Uzmanı",
    tools=[image_generator, vision_processor, code_executor],
    goal="Yapay zeka yeteneklerini kullanarak içerik oluşturun ve analiz edin"
)
```
