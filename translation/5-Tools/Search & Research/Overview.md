> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Genel Bakış

> Web araması yapın, depoları bulun ve internet genelinde bilgi araştırın

Bu araçlar, ajanlarınızın web araması yapmasını, konuları araştırmasını ve arama motorları, GitHub ve YouTube dahil olmak üzere çeşitli platformlar genelinde bilgi bulmasını sağlar.

## **Kullanılabilir Araçlar**

<CardGroup cols={2}>
  <Card title="Serper Dev Aracı" icon="google" href="/en/tools/search-research/serperdevtool">
    Kapsamlı web arama yetenekleri için Google arama API entegrasyonu.
  </Card>

  <Card title="Brave Arama Aracı" icon="shield" href="/en/tools/search-research/bravesearchtool">
    Brave'in bağımsız arama indeksi ile gizlilik odaklı arama.
  </Card>

  <Card title="Exa Arama Aracı" icon="magnifying-glass" href="/en/tools/search-research/exasearchtool">
    Belirli ve alakalı içeriği bulmak için yapay zeka destekli arama.
  </Card>

  <Card title="LinkUp Arama Aracı" icon="link" href="/en/tools/search-research/linkupsearchtool">
    Taze içerik indeksleme ile gerçek zamanlı web araması.
  </Card>

  <Card title="GitHub Arama Aracı" icon="github" href="/en/tools/search-research/githubsearchtool">
    GitHub depoları, kod, sorunlar ve belgelendirmeyi araştırın.
  </Card>

  <Card title="Web Sitesi Arama Aracı" icon="globe" href="/en/tools/search-research/websitesearchtool">
    Belirli web siteleri ve domainler içinde arama yapın.
  </Card>

  <Card title="Kod Dokümanları Arama Aracı" icon="code" href="/en/tools/search-research/codedocssearchtool">
    Kod belgelendirmesi ve teknik kaynakları araştırın.
  </Card>

  <Card title="YouTube Kanal Araması" icon="youtube" href="/en/tools/search-research/youtubechannelsearchtool">
    YouTube kanallarında belirli içeriği ve yaratıcıları araştırın.
  </Card>

  <Card title="YouTube Video Araması" icon="play" href="/en/tools/search-research/youtubevideosearchtool">
    YouTube videolarını konu, anahtar kelime veya ölçütlere göre bulun ve analiz edin.
  </Card>

  <Card title="Tavily Arama Aracı" icon="magnifying-glass" href="/en/tools/search-research/tavilysearchtool">
    Tavily'nin yapay zeka destekli arama API'sini kullanan kapsamlı web araması.
  </Card>

  <Card title="Tavily Çıkartma Aracı" icon="file-text" href="/en/tools/search-research/tavilyextractortool">
    Tavily API'sini kullanarak web sayfalarından yapılandırılmış içerik çıkartın.
  </Card>

  <Card title="Arxiv Makale Aracı" icon="box-archive" href="/en/tools/search-research/arxivpapertool">
    arXiv'de araştırma yapın ve isteğe bağlı olarak PDF'leri indirin.
  </Card>

  <Card title="SerpApi Google Araması" icon="search" href="/en/tools/search-research/serpapi-googlesearchtool">
    SerpApi üzerinden yapılandırılmış sonuçlarla Google araması.
  </Card>

  <Card title="SerpApi Google Alışveriş" icon="cart-shopping" href="/en/tools/search-research/serpapi-googleshoppingtool">
    SerpApi üzerinden Google Alışveriş sorguları.
  </Card>
</CardGroup>

## **Yaygın Kullanım Alanları**

* **Pazar Araştırması**: Endüstri trendleri ve rakip analizi araştırması
* **İçerik Keşfi**: İlgili makaleleri, videoları ve kaynakları bulma
* **Kod Araştırması**: Çözümler için depoları ve belgelendirmeyi araştırma
* **Potansiyel Müşteri Bulma**: Şirketleri ve bireysel kişileri araştırma
* **Akademik Araştırma**: Bilimsel makaleleri ve teknik belgeleri bulma

```python  theme={null}
from crewai_tools import SerperDevTool, GitHubSearchTool, YoutubeVideoSearchTool, TavilySearchTool, TavilyExtractorTool

# Araştırma araçları oluştur
web_search = SerperDevTool()
code_search = GitHubSearchTool()
video_research = YoutubeVideoSearchTool()
tavily_search = TavilySearchTool()
content_extractor = TavilyExtractorTool()

# Ajanınıza ekleyin
agent = Agent(
    role="Research Analyst",
    tools=[web_search, code_search, video_research, tavily_search, content_extractor],
    goal="Gather comprehensive information on any topic"
)
```

