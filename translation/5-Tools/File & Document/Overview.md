> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Genel Bakış

> CrewAI'nin belge işleme araçlarıyla çeşitli dosya biçimlerinde okuma, yazma ve arama yapın

Bu araçlar, ajanlarınızın çeşitli dosya biçimleri ve belge türleriyle çalışmasını sağlar. PDF okumaktan JSON verisi işlemeye kadar, belge işleme ihtiyaçlarınızın tamamını karşılar.

## **Kullanılabilir Araçlar**

<CardGroup cols={2}>
  <Card title="File Read Tool" icon="folders" href="/en/tools/file-document/filereadtool">
    Metin, markdown ve daha fazlası dahil olmak üzere her türlü dosyadan içerik okuyun.
  </Card>

  <Card title="File Write Tool" icon="file-pen" href="/en/tools/file-document/filewritetool">
    Dosyalara içerik yazın, yeni belgeler oluşturun ve işlenmiş verileri kaydedin.
  </Card>

  <Card title="PDF Search Tool" icon="file-pdf" href="/en/tools/file-document/pdfsearchtool">
    PDF belgelerinde verimli şekilde arama yapın ve metin içeriği çıkarın.
  </Card>

  <Card title="DOCX Search Tool" icon="file-word" href="/en/tools/file-document/docxsearchtool">
    Microsoft Word belgelerinde arama yapın ve ilgili içeriği çıkarın.
  </Card>

  <Card title="JSON Search Tool" icon="brackets-curly" href="/en/tools/file-document/jsonsearchtool">
    Gelişmiş sorgulama yetenekleriyle JSON dosyalarını ayrıştırın ve arayın.
  </Card>

  <Card title="CSV Search Tool" icon="table" href="/en/tools/file-document/csvsearchtool">
    CSV dosyalarını işleyin ve arayın, belirli satırları ve sütunları çıkarın.
  </Card>

  <Card title="XML Search Tool" icon="code" href="/en/tools/file-document/xmlsearchtool">
    XML dosyalarını ayrıştırın ve belirli öğeleri ile öznitelikleri arayın.
  </Card>

  <Card title="MDX Search Tool" icon="markdown" href="/en/tools/file-document/mdxsearchtool">
    MDX dosyalarında arama yapın ve dokümantasyondan içerik çıkarın.
  </Card>

  <Card title="TXT Search Tool" icon="file-lines" href="/en/tools/file-document/txtsearchtool">
    Düz metin dosyalarında desen eşleştirme yetenekleriyle arama yapın.
  </Card>

  <Card title="Directory Search Tool" icon="folder-open" href="/en/tools/file-document/directorysearchtool">
    Dizin yapıları içinde dosya ve klasör arayın.
  </Card>

  <Card title="Directory Read Tool" icon="folder" href="/en/tools/file-document/directoryreadtool">
    Dizin içeriklerini, dosya yapılarını ve meta verileri okuyup listeleyin.
  </Card>

  <Card title="OCR Tool" icon="image" href="/en/tools/file-document/ocrtool">
    Görsel yetenekli bir LLM kullanarak görsellerden (yerel dosyalar veya URL'ler) metin çıkarın.
  </Card>

  <Card title="PDF Text Writing Tool" icon="file-pdf" href="/en/tools/file-document/pdf-text-writing-tool">
    PDF'lere belirli koordinatlarda metin yazın; isteğe bağlı olarak özel yazı tipleri kullanın.
  </Card>
</CardGroup>

## **Yaygın Kullanım Senaryoları**

* **Belge İşleme**: Çeşitli dosya biçimlerinden içerik çıkarın ve analiz edin
* **Veri İçe Aktarma**: CSV, JSON ve XML dosyalarından yapılandırılmış veri okuyun
* **İçerik Arama**: Büyük belge koleksiyonları içinde belirli bilgileri bulun
* **Dosya Yönetimi**: Dosyaları ve dizinleri düzenleyin ve yönetin
* **Veri Dışa Aktarma**: İşlenmiş sonuçları çeşitli dosya biçimlerinde kaydedin

## **Hızlı Başlangıç Örneği**

```python  theme={null}
from crewai_tools import FileReadTool, PDFSearchTool, JSONSearchTool

# Create tools
# Araçları oluştur
file_reader = FileReadTool()
pdf_searcher = PDFSearchTool()
json_processor = JSONSearchTool()

# Ajanınıza ekleyin
agent = Agent(
    role="Belge Analisti",
    tools=[file_reader, pdf_searcher, json_processor],
    goal="Çeşitli belge türlerini işle ve analiz et"
)
```

## **Belge İşleme İpuçları**

* **Dosya İzinleri**: Ajanınızın uygun okuma/yazma izinlerine sahip olduğundan emin olun
* **Büyük Dosyalar**: Çok büyük belgeler için parçalama kullanmayı değerlendirin
* **Biçim Desteği**: Desteklenen dosya biçimleri için araç dokümantasyonunu kontrol edin
* **Hata Yönetimi**: Bozuk veya erişilemeyen dosyalar için uygun hata yönetimi uygulayın
