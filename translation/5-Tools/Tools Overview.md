> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Bu dosyayı, daha fazla keşfetmeden önce kullanılabilir tüm sayfaları bulmak için kullanın.

# Araçlar Genel Bakış

> AI ajanlarınızı güçlendirmek için CrewAI'nin 40+ araçtan oluşan geniş kütüphanesini keşfedin

CrewAI, ajanlarınızın yeteneklerini geliştirmek için önceden oluşturulmuş geniş bir araç kütüphanesi sunar. Dosya işleme, web kazıma, veritabanı sorguları ve AI hizmetlerinden başlayarak her ihtiyacı kapsıyoruz.

## **Araç Kategorileri**

<CardGroup cols={2}>
  <Card title="Dosya ve Belge" icon="folder-open" href="/en/tools/file-document/overview" color="#3B82F6">
    PDF, DOCX, JSON, CSV ve daha fazlası dahil olmak üzere çeşitli dosya formatlarını okuyun, yazın ve arayın. Belge işleme iş akışları için idealdir.
  </Card>

  <Card title="Web Kazıma ve Tarama" icon="globe" href="/en/tools/web-scraping/overview" color="#10B981">
    Web sitelerinden veri çıkarın, tarayıcı etkileşimlerini otomatikleştirin ve Firecrawl, Selenium gibi araçlarla ölçekli içerik kazıyın.
  </Card>

  <Card title="Arama ve Araştırma" icon="magnifying-glass" href="/en/tools/search-research/overview" color="#F59E0B">
    Web aramaları yapın, kod depolarını bulun, YouTube içeriğini araştırın ve internet genelinde bilgi keşfedin.
  </Card>

  <Card title="Veritabanı ve Veri" icon="database" href="/en/tools/database-data/overview" color="#8B5CF6">
    SQL veritabanlarına, vektör depolarına ve veri ambarlarına bağlanın. MySQL, PostgreSQL, Snowflake, Qdrant ve Weaviate sorgulayın.
  </Card>

  <Card title="AI ve Makine Öğrenimi" icon="brain" href="/en/tools/ai-ml/overview" color="#EF4444">
    DALL-E ile görseller oluşturun, görsel görevleri işleyin, LangChain ile entegre edin, RAG sistemleri kurun ve kod yorumlayıcılarından yararlanın.
  </Card>

  <Card title="Bulut ve Depolama" icon="cloud" href="/en/tools/cloud-storage/overview" color="#06B6D4">
    AWS S3, Amazon Bedrock ve diğer bulut depolama ve AI hizmetleriyle etkileşim kurun.
  </Card>

  <Card title="Otomasyon" icon="bolt" href="/en/tools/automation/overview" color="#84CC16">
    Apify, Composio ve diğer platformlarla iş akışlarını otomatikleştirin, ajanlarınızı harici hizmetlerle bağlayın.
  </Card>

  <Card title="Entegrasyonlar" icon="plug" href="/en/tools/tool-integrations/overview" color="#0891B2">
    CrewAI'yi Amazon Bedrock ve CrewAI Otomasyon araç seti gibi harici sistemlerle entegre edin.
  </Card>
</CardGroup>

## **Hızlı Erişim**

Belirli bir araç mı arıyorsunuz? İşte bazı popüler seçenekler:

<CardGroup cols={3}>
  <Card title="RAG Aracı" icon="image" href="/en/tools/ai-ml/ragtool">
    Retrieval-Augmented Generation uygulayın
  </Card>

  <Card title="Serper Dev" icon="book-atlas" href="/en/tools/search-research/serperdevtool">
    Google arama API'si
  </Card>

  <Card title="Dosya Okuma" icon="file" href="/en/tools/file-document/filereadtool">
    Her dosya türünü okuyun
  </Card>

  <Card title="Web Sitesi Kazıma" icon="globe" href="/en/tools/web-scraping/scrapewebsitetool">
    Web içeriği çıkarın
  </Card>

  <Card title="Kod Yorumlayıcı" icon="code" href="/en/tools/ai-ml/codeinterpretertool">
    Python kodu çalıştırın
  </Card>

  <Card title="S3 Okuyucu" icon="cloud" href="/en/tools/cloud-storage/s3readertool">
    AWS S3 dosyalarına erişin
  </Card>
</CardGroup>

## **Başlarken**

CrewAI projenizde herhangi bir aracı kullanmak için:

1. Ara aracı ekip yapılandırmanıza **içe aktarın**
2. Aracı ajanınızın araç listesine **ekleyin**
3. Gerekli API anahtarlarını veya ayarları **yapılandırın**

```python  theme={null}
from crewai_tools import FileReadTool, SerperDevTool

# Ajanınıza araçlar ekleyin
agent = Agent(
    role="Research Analyst",
    tools=[FileReadTool(), SerperDevTool()],
    # ... diğer yapılandırma
)
```

## **Maksimum Kullanım Adedi**

Bir aracın belirli sayıda kereden fazla kullanılmasını önlemek için maksimum kullanım adedi ayarlayabilirsiniz.
Varsayılan olarak, maksimum kullanım adedi sınırsızdır.

```python  theme={null}
from crewai_tools import FileReadTool

tool = FileReadTool(max_usage_count=5, ...)
```

Keşfetmeye hazır mısınız? Kullanım durumunuza uygun araçları keşfetmek için yukarıdaki kategorilerden birini seçin!

