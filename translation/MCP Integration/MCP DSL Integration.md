> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# MCP DSL Entegrasyonu

> CrewAI'nın basit DSL sütaksını kullanarak MCP sunucularını mcps alanı ile doğrudan ajanlarınızla entegre etmeyi öğrenin.

## Genel Bakış

CrewAI'nın MCP DSL (Alan Özgü Dili) entegrasyonu, ajanlarınızı MCP (Model Context Protocol) sunucularına bağlamanın **en basit yolunu** sağlar. Ajanınıza sadece bir `mcps` alanı ekleyin ve CrewAI tüm karmaşıklığı otomatik olarak kullanır.

<Info>
  Bu, çoğu MCP kullanım alanı için **önerilen yaklaşımdır**. Manuel bağlantı yönetimi gerektiren gelişmiş senaryolar için bkz.
  [MCPServerAdapter](/en/mcp/overview#advanced-mcpserveradapter).
</Info>

## Temel Kullanım

`mcps` alanını kullanarak ajanınıza MCP sunucuları ekleyin:

```python  theme={null}
from crewai import Agent

agent = Agent(
    role="Research Assistant",
    goal="Help with research and analysis tasks",
    backstory="Expert assistant with access to advanced research tools",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key&profile=research"
    ]
)

# MCP araçları artık otomatik olarak kullanılabilir!
# Manuel bağlantı yönetimi veya araç yapılandırmasına gerek yoktur
```

## Desteklenen Referans Formatları

### Harici MCP Uzak Sunucuları

```python  theme={null}
# Temel HTTPS sunucusu
"https://api.example.com/mcp"

# Kimlik doğrulaması ile sunucu
"https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile"

# Özel yol ile sunucu
"https://services.company.com/api/v1/mcp"
```

### Belirli Araç Seçimi

Bir sunucudan belirli araçları seçmek için `#` sütaksını kullanın:

```python  theme={null}
# Hava durumu sunucusundan yalnızca tahmin aracını al
"https://weather.api.com/mcp#get_forecast"

# Exa'dan yalnızca arama aracını al
"https://mcp.exa.ai/mcp?api_key=your_key#web_search_exa"
```

### Bağlantılı MCP Entegrasyonları

CrewAI kataloğundan MCP sunucularını bağlayın veya kendi sunucunuzu getirin. Hesabınızda bağlandıktan sonra, slug tarafından referans verin:

```python  theme={null}
# Bağlantılı MCP tüm araçlarla
"snowflake"

# Bağlantılı MCP'den belirli araç
"stripe#list_invoices"

# Birden fazla bağlantılı MCP
mcps=[
    "snowflake",
    "stripe",
    "github"
]
```

## Tam Örnek

Birden fazla MCP sunucusu kullanan tam bir örnek:

```python  theme={null}
from crewai import Agent, Task, Crew, Process

# Birden fazla MCP kaynağı ile ajan oluştur
multi_source_agent = Agent(
    role="Multi-Source Research Analyst",
    goal="Conduct comprehensive research using multiple data sources",
    backstory="""Expert researcher with access to web search, weather data,
    financial information, and academic research tools""",
    mcps=[
        # Harici MCP sunucuları
        "https://mcp.exa.ai/mcp?api_key=your_exa_key&profile=research",
        "https://weather.api.com/mcp#get_current_conditions",

        # Kataloğundan bağlantılı MCP'ler
        "snowflake",
        "stripe#list_invoices",
        "github#search_repositories"
    ]
)

# Kapsamlı araştırma görevi oluştur
research_task = Task(
    description="""Research the impact of AI agents on business productivity.
    Include current weather impacts on remote work, financial market trends,
    and recent academic publications on AI agent frameworks.""",
    expected_output="""Comprehensive report covering:
    1. AI agent business impact analysis
    2. Weather considerations for remote work
    3. Financial market trends related to AI
    4. Academic research citations and insights
    5. Competitive landscape analysis""",
    agent=multi_source_agent
)

# Crew oluştur ve çalıştır
research_crew = Crew(
    agents=[multi_source_agent],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

result = research_crew.kickoff()
print(f"Research completed with {len(multi_source_agent.mcps)} MCP data sources")
```

## Araç Adlandırması ve Organizasyonu

CrewAI, çatışmaları önlemek için araç adlandırmasını otomatik olarak yönetir:

```python  theme={null}
# Orijinal MCP sunucusunun araçları vardır: "search", "analyze"
# CrewAI araçları oluşturur: "mcp_exa_ai_search", "mcp_exa_ai_analyze"

agent = Agent(
    role="Tool Organization Demo",
    goal="Show how tool naming works",
    backstory="Demonstrates automatic tool organization",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=key",      # Araçlar: mcp_exa_ai_*
        "https://weather.service.com/mcp",         # Araçlar: weather_service_com_*
        "snowflake"                                # Araçlar: snowflake_*
    ]
)

# Her sunucu'nun araçları sunucu adı temel alınarak benzersiz ön ekler alır
# Bu, farklı MCP sunucuları arasında adlandırma çatışmalarını engeller
```

## Hata İşleme ve Dayanıklılık

MCP DSL, sağlam ve kullanıcı dostu olacak şekilde tasarlanmıştır:

### Zarif Sunucu Arızaları

```python  theme={null}
agent = Agent(
    role="Resilient Researcher",
    goal="Research despite server issues",
    backstory="Experienced researcher who adapts to available tools",
    mcps=[
        "https://primary-server.com/mcp",         # Birincil veri kaynağı
        "https://backup-server.com/mcp",          # Birincil başarısız olursa yedek
        "https://unreachable-server.com/mcp",     # Uyarı ile atlanacak
        "snowflake"                               # Kataloğundan bağlantılı MCP
    ]
)

# Ajan:
# 1. Çalışan sunuculara başarıyla bağlanır
# 2. Başarısız sunucular için uyarıları günlüğe kaydeder
# 3. Kullanılabilir araçlarla devam eder
# 4. Sunucu arızalarında çökmez veya asılı kalmaz
```

### Zaman Aşımı Koruması

Tüm MCP işlemleri yerleşik zaman aşımlarına sahiptir:

* **Bağlantı zaman aşımı**: 10 saniye
* **Araç yürütme zaman aşımı**: 30 saniye
* **Keşif zaman aşımı**: 15 saniye

```python  theme={null}
# Bu sunucular yanıt vermezse zarif şekilde zaman aşımına uğrar
mcps=[
    "https://slow-server.com/mcp",        # Yanıt vermezse 10s sonra zaman aşımına uğrar
    "https://overloaded-api.com/mcp"      # Keşif 15s'den fazla sürerse zaman aşımına uğrar
]
```

## Performans Özellikleri

### Otomatik Önbelleğe Alma

Araç şemaları performansı iyileştirmek için 5 dakika boyunca önbelleğe alınır:

```python  theme={null}
# İlk ajan oluşturması - sunucudan araçları keşfeder
agent1 = Agent(role="First", goal="Test", backstory="Test",
               mcps=["https://api.example.com/mcp"])

# İkinci ajan oluşturması (5 dakika içinde) - önbelleğe alınan araç şemalarını kullanır
agent2 = Agent(role="Second", goal="Test", backstory="Test",
               mcps=["https://api.example.com/mcp"])  # Çok daha hızlı!
```

### Talep Üzerine Bağlantılar

Araç bağlantıları yalnızca araçlar gerçekte kullanılırken kurulur:

```python  theme={null}
# Ajan oluşturması hızlıdır - henüz MCP bağlantıları yapılmamış
agent = Agent(
    role="On-Demand Agent",
    goal="Use tools efficiently",
    backstory="Efficient agent that connects only when needed",
    mcps=["https://api.example.com/mcp"]
)

# MCP bağlantısı yalnızca araç gerçekte yürütüldüğünde yapılır
# Bu, bağlantı yükünü en aza indirir ve başlangıç performansını iyileştirir
```

## Mevcut Özellikleriyle Entegrasyon

MCP araçları CrewAI'nın diğer özellikleriyle sorunsuz çalışır:

```python  theme={null}
from crewai.tools import BaseTool

class CustomTool(BaseTool):
    name: str = "custom_analysis"
    description: str = "Custom analysis tool"

    def _run(self, **kwargs):
        return "Custom analysis result"

agent = Agent(
    role="Full-Featured Agent",
    goal="Use all available tool types",
    backstory="Agent with comprehensive tool access",

    # Tüm araç türleri birlikte çalışır
    tools=[CustomTool()],                          # Özel araçlar
    apps=["gmail", "slack"],                       # Platform entegrasyonları
    mcps=[                                         # MCP sunucuları
        "https://mcp.exa.ai/mcp?api_key=key",
        "snowflake"
    ],

    verbose=True,
    max_iter=15
)
```

## En İyi Uygulamalar

### 1. Mümkün Olduğunda Belirli Araçları Kullanın

```python  theme={null}
# İyi - yalnızca ihtiyacınız olan araçları alır
mcps=["https://weather.api.com/mcp#get_forecast"]

# Daha az verimli - sunucudan tüm araçları alır
mcps=["https://weather.api.com/mcp"]
```

### 2. Kimlik Doğrulamayı Güvenli Şekilde İşleyin

```python  theme={null}
import os

# API anahtarlarını ortam değişkenlerinde saklayın
exa_key = os.getenv("EXA_API_KEY")
exa_profile = os.getenv("EXA_PROFILE")

agent = Agent(
    role="Secure Agent",
    goal="Use MCP tools securely",
    backstory="Security-conscious agent",
    mcps=[f"https://mcp.exa.ai/mcp?api_key={exa_key}&profile={exa_profile}"]
)
```

### 3. Sunucu Arızaları İçin Plan Yapın

```python  theme={null}
# Her zaman yedek seçenekleri dahil edin
mcps=[
    "https://primary-api.com/mcp",       # Birincil seçim
    "https://backup-api.com/mcp",        # Yedek seçenek
    "snowflake"                          # Bağlantılı MCP geri dönüşü
]
```

### 4. Açıklayıcı Ajan Rolleri Kullanın

```python  theme={null}
agent = Agent(
    role="Weather-Enhanced Market Analyst",
    goal="Analyze markets considering weather impacts",
    backstory="Financial analyst with access to weather data for agricultural market insights",
    mcps=[
        "https://weather.service.com/mcp#get_forecast",
        "stripe#list_invoices"
    ]
)
```

## Sorun Giderme

### Yaygın Sorunlar

**Araç keşfedilmedi:**

```python  theme={null}
# MCP sunucu URL'inizi ve kimlik doğrulamanızı kontrol edin
# Sunucunun çalıştığından ve erişilebilir olduğundan emin olun
mcps=["https://mcp.example.com/mcp?api_key=valid_key"]
```

**Bağlantı zaman aşımları:**

```python  theme={null}
# Sunucu yavaş veya aşırı yüklü olabilir
# CrewAI uyarıları günlüğe kaydeder ve diğer sunucularla devam eder
# Sunucu durumunu kontrol edin veya yedek sunucuları deneyin
```

**Kimlik doğrulama arızaları:**

```python  theme={null}
# API anahtarlarını ve kimlik bilgilerini doğrulayın
# Sunucu belgelendirmesinde gerekli parametreleri kontrol edin
# Sorgu parametrelerinin düzgün URL kodlandığından emin olun
```

## Gelişmiş: MCPServerAdapter

Manuel bağlantı yönetimi gerektiren karmaşık senaryolar için, `crewai-tools` kütüphanesinden `MCPServerAdapter` sınıfını kullanın. Python bağlam yöneticisini (`with` ifadesi) kullanmak, MCP sunucusunun bağlantısını otomatik olarak başlatıp durdurmak için önerilen yaklaşımdır.
