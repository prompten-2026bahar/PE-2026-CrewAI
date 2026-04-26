> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# CrewAI'da Araçlar Olarak MCP Sunucuları

> `crewai-tools` kütüphanesini kullanarak CrewAI ajanlarınıza araçlar olarak MCP sunucularını nasıl entegre edebileceğinizi öğrenin.

## Genel Bakış

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP), AI ajanlarının MCP Sunucuları olarak bilinen harici hizmetlerle iletişim kurarak LLM'lere bağlam sağlaması için standartlaştırılmış bir yol sağlar.

CrewAI, MCP entegrasyonu için **iki yaklaşım** sunmaktadır:

### 🚀 **Basit DSL Entegrasyonu** (Önerilen)

Sorunsuz MCP araç entegrasyonu için ajanlar üzerinde `mcps` alanını doğrudan kullanın. DSL, hem **string referanslarını** (hızlı kurulum için) hem de **yapılandırılmış konfigürasyonları** (tam kontrol için) destekler.

#### String Tabanlı Referanslar (Hızlı Kurulum)

Uzak HTTPS sunucuları ve CrewAI kataloğundaki bağlantılı MCP entegrasyonları için ideal:

```python  theme={null}
from crewai import Agent

agent = Agent(
    role="Research Analyst",
    goal="Research and analyze information",
    backstory="Expert researcher with access to external tools",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key",           # External MCP server
        "https://api.weather.com/mcp#get_forecast",          # Specific tool from server
        "snowflake",                                         # Connected MCP from catalog
        "stripe#list_invoices"                               # Specific tool from connected MCP
    ]
)
# MCP araçları artık ajanınız tarafından otomatik olarak kullanılabilir!
```

#### Yapılandırılmış Konfigürasyonlar (Tam Kontrol)

Bağlantı ayarları, araç filtreleme ve tüm taşıma türleri üzerinde tam kontrol için:

```python  theme={null}
from crewai import Agent
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE
from crewai.mcp.filters import create_static_tool_filter

agent = Agent(
    role="Advanced Research Analyst",
    goal="Research with full control over MCP connections",
    backstory="Expert researcher with advanced tool access",
    mcps=[
        # Stdio transport for local servers
        MCPServerStdio(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            env={"API_KEY": "your_key"},
            tool_filter=create_static_tool_filter(
                allowed_tool_names=["read_file", "list_directory"]
            ),
            cache_tools_list=True,
        ),
        # HTTP/Streamable HTTP transport for remote servers
        MCPServerHTTP(
            url="https://api.example.com/mcp",
            headers={"Authorization": "Bearer your_token"},
            streamable=True,
            cache_tools_list=True,
        ),
        # SSE transport for real-time streaming
        MCPServerSSE(
            url="https://stream.example.com/mcp/sse",
            headers={"Authorization": "Bearer your_token"},
        ),
    ]
)
```

### 🔧 **Gelişmiş: MCPServerAdapter** (Karmaşık Senaryolar İçin)

Manuel bağlantı yönetimi gerektiren gelişmiş kullanım durumları için `crewai-tools` kütüphanesi `MCPServerAdapter` sınıfını sağlar.

Şu anda aşağıdaki taşıma mekanizmalarını destekliyoruz:

* **Stdio**: yerel sunucular için (aynı makinedeki süreçler arasında standart giriş/çıkış üzerinden iletişim)
* **Server-Sent Events (SSE)**: uzak sunucular için (HTTP üzerinden sunucudan istemciye tek yönlü, gerçek zamanlı veri akışı)
* **Streamable HTTPS**: uzak sunucular için (esnek, HTTP üzerinden çift yönlü iletişim potansiyeli, sunucudan istemciye akışlar için genellikle SSE kullanıyor)

## Video Eğitimi

CrewAI ile MCP entegrasyonu hakkında kapsamlı bir rehber için bu video eğitimini izleyin:

https://www.youtube.com/embed/TpQ45lAZh48

## Kurulum

CrewAI MCP entegrasyonu `mcp` kütüphanesini gerektirir:

```shell  theme={null}
# Basit DSL Entegrasyonu İçin (Önerilen)
uv add mcp

# Gelişmiş MCPServerAdapter Kullanımı İçin
uv pip install 'crewai-tools[mcp]'
```

## Hızlı Başlangıç: Basit DSL Entegrasyonu

MCP sunucularını entegre etmenin en kolay yolu, ajanlarınızda `mcps` alanını kullanmaktır. String referansları veya yapılandırılmış konfigürasyonları kullanabilirsiniz.

### String Referanslarıyla Hızlı Başlangıç

```python  theme={null}
from crewai import Agent, Task, Crew

# Create agent with MCP tools using string references
research_agent = Agent(
    role="Research Analyst",
    goal="Find and analyze information using advanced search tools",
    backstory="Expert researcher with access to multiple data sources",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile",
        "snowflake#run_query"
    ]
)

# Create task
research_task = Task(
    description="Research the latest developments in AI agent frameworks",
    expected_output="Comprehensive research report with citations",
    agent=research_agent
)

# Create and run crew
crew = Crew(agents=[research_agent], tasks=[research_task])
result = crew.kickoff()
```

### Yapılandırılmış Konfigürasyonlarla Hızlı Başlangıç

```python  theme={null}
from crewai import Agent, Task, Crew
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE

# Create agent with structured MCP configurations
research_agent = Agent(
    role="Research Analyst",
    goal="Find and analyze information using advanced search tools",
    backstory="Expert researcher with access to multiple data sources",
    mcps=[
        # Local stdio server
        MCPServerStdio(
            command="python",
            args=["local_server.py"],
            env={"API_KEY": "your_key"},
        ),
        # Remote HTTP server
        MCPServerHTTP(
            url="https://api.research.com/mcp",
            headers={"Authorization": "Bearer your_token"},
        ),
    ]
)

# Create task
research_task = Task(
    description="Research the latest developments in AI agent frameworks",
    expected_output="Comprehensive research report with citations",
    agent=research_agent
)

# Create and run crew
crew = Crew(agents=[research_agent], tasks=[research_task])
result = crew.kickoff()
```

Hepsi bu! MCP araçları otomatik olarak keşfedilir ve ajanınız tarafından kullanılabilir.

## MCP Referans Formatları

`mcps` alanı hem **string referanslarını** (hızlı kurulum için) hem de **yapılandırılmış konfigürasyonları** (tam kontrol için) destekler. Her iki formatı aynı listede karıştırabilirsiniz.

### String Tabanlı Referanslar

#### Harici MCP Sunucuları

```python  theme={null}
mcps=[
    # Full server - get all available tools
    "https://mcp.example.com/api",

    # Specific tool from server using # syntax
    "https://api.weather.com/mcp#get_current_weather",

    # Server with authentication parameters
    "https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile"
]
```

#### Bağlantılı MCP Entegrasyonları

CrewAI kataloğundan MCP sunucularını bağlayın veya kendi sunucunuzu getirin. Hesabınızda bağlandıktan sonra, slug tarafından referans verin:

```python  theme={null}
mcps=[
    # Connected MCP - get all available tools
    "snowflake",

    # Specific tool from a connected MCP using # syntax
    "stripe#list_invoices",

    # Multiple connected MCPs
    "snowflake",
    "stripe",
    "github"
]
```

### Yapılandırılmış Konfigürasyonlar

#### Stdio Taşıması (Yerel Sunucular)

Süreç olarak çalışan yerel MCP sunucuları için ideal:

```python  theme={null}
from crewai.mcp import MCPServerStdio
from crewai.mcp.filters import create_static_tool_filter

mcps=[
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        env={"API_KEY": "your_key"},
        tool_filter=create_static_tool_filter(
            allowed_tool_names=["read_file", "write_file"]
        ),
        cache_tools_list=True,
    ),
    # Python-based server
    MCPServerStdio(
        command="python",
        args=["path/to/server.py"],
        env={"UV_PYTHON": "3.12", "API_KEY": "your_key"},
    ),
]
```

#### HTTP/Streamable HTTP Taşıması (Uzak Sunucular)

HTTP/HTTPS üzerinden uzak MCP sunucuları için:

```python  theme={null}
from crewai.mcp import MCPServerHTTP

mcps=[
    # Streamable HTTP (default)
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer your_token"},
        streamable=True,
        cache_tools_list=True,
    ),
    # Standard HTTP
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer your_token"},
        streamable=False,
    ),
]
```

#### SSE Taşıması (Gerçek Zamanlı Akış)

Server-Sent Events kullanan uzak sunucular için:

```python  theme={null}
from crewai.mcp import MCPServerSSE

mcps=[
    MCPServerSSE(
        url="https://stream.example.com/mcp/sse",
        headers={"Authorization": "Bearer your_token"},
        cache_tools_list=True,
    ),
]
```

### Karışık Referanslar

String referanslarını ve yapılandırılmış konfigürasyonları birleştirebilirsiniz:

```python  theme={null}
from crewai.mcp import MCPServerStdio, MCPServerHTTP

mcps=[
    # String references
    "https://external-api.com/mcp",              # External server
    "snowflake",                                 # Connected MCP from catalog

    # Structured configurations
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
    ),
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer token"},
    ),
]
```

### Araç Filtreleme

Yapılandırılmış konfigürasyonlar gelişmiş araç filtrelemeyi destekler:

```python  theme={null}
from crewai.mcp import MCPServerStdio
from crewai.mcp.filters import create_static_tool_filter, create_dynamic_tool_filter, ToolFilterContext

# Static filtering (allow/block lists)
static_filter = create_static_tool_filter(
    allowed_tool_names=["read_file", "write_file"],
    blocked_tool_names=["delete_file"],
)

# Dynamic filtering (context-aware)
def dynamic_filter(context: ToolFilterContext, tool: dict) -> bool:
    # Block dangerous tools for certain agent roles
    if context.agent.role == "Code Reviewer":
        if "delete" in tool.get("name", "").lower():
            return False
    return True

mcps=[
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        tool_filter=static_filter,  # or dynamic_filter
    ),
]
```

## Konfigürasyon Parametreleri

Her taşıma türü belirli konfigürasyon seçeneklerini destekler:

### MCPServerStdio Parametreleri

* **`command`** (gerekli): Yürütülecek komut (ör. `"python"`, `"node"`, `"npx"`, `"uvx"`)
* **`args`** (isteğe bağlı): Komut argümanlarının listesi (ör. `["server.py"]` veya `["-y", "@mcp/server"]`)
* **`env`** (isteğe bağlı): Sürece iletilecek ortam değişkenlerinin sözlüğü
* **`tool_filter`** (isteğe bağlı): Kullanılabilir araçları filtrelemek için araç filtre işlevi
* **`cache_tools_list`** (isteğe bağlı): Daha hızlı sonraki erişim için araç listesini önbelleğe alıp almayacağı (varsayılan: `False`)

### MCPServerHTTP Parametreleri

* **`url`** (gerekli): Sunucu URL'si (ör. `"https://api.example.com/mcp"`)
* **`headers`** (isteğe bağlı): Kimlik doğrulama veya diğer amaçlar için HTTP başlıklarının sözlüğü
* **`streamable`** (isteğe bağlı): Streamable HTTP taşımasının kullanılıp kullanılmayacağı (varsayılan: `True`)
* **`tool_filter`** (isteğe bağlı): Kullanılabilir araçları filtrelemek için araç filtre işlevi
* **`cache_tools_list`** (isteğe bağlı): Daha hızlı sonraki erişim için araç listesini önbelleğe alıp almayacağı (varsayılan: `False`)

### MCPServerSSE Parametreleri

* **`url`** (gerekli): Sunucu URL'si (ör. `"https://api.example.com/mcp/sse"`)
* **`headers`** (isteğe bağlı): Kimlik doğrulama veya diğer amaçlar için HTTP başlıklarının sözlüğü
* **`tool_filter`** (isteğe bağlı): Kullanılabilir araçları filtrelemek için araç filtre işlevi
* **`cache_tools_list`** (isteğe bağlı): Daha hızlı sonraki erişim için araç listesini önbelleğe alıp almayacağı (varsayılan: `False`)

### Ortak Parametreler

Tüm taşıma türleri şunları destekler:

* **`tool_filter`**: Hangi araçların kullanılabilir olduğunu kontrol etmek için filtre işlevi. Olabilir:
  * `None` (varsayılan): Tüm araçlar kullanılabilir
  * Statik filtre: İzin ver/engelle listeleri için `create_static_tool_filter()` ile oluşturulur
  * Dinamik filtre: Bağlam farkında filtreleme için `create_dynamic_tool_filter()` ile oluşturulur
* **`cache_tools_list`**: `True` olduğunda, sonraki bağlantılar için performansı iyileştirmek üzere ilk keşiften sonra araç listesini önbelleğe alır

## Temel Özellikler

* 🔄 **Otomatik Araç Keşfi**: Araçlar otomatik olarak keşfedilir ve entegre edilir
* 🏷️ **Ad Çarpışması Önleme**: Sunucu adları araç adlarında önek olarak yer alır
* ⚡ **Performans Optimizasyonu**: Talep üzerine bağlantılar ve şema önbelleği
* 🛡️ **Hata Direnci**: Kullanılamayan sunucuların zarif şekilde işlenmesi
* ⏱️ **Zaman Aşımı Koruması**: Yerleşik zaman aşımları, asılı bağlantıları engeller
* 📊 **Şeffaf Entegrasyon**: Mevcut CrewAI özellikleriyle sorunsuz çalışır
* 🔧 **Tam Taşıma Desteği**: Stdio, HTTP/Streamable HTTP ve SSE taşımaları
* 🎯 **Gelişmiş Filtreleme**: Statik ve dinamik araç filtreleme yetenekleri
* 🔐 **Esnek Kimlik Doğrulama**: Başlıklar, ortam değişkenleri ve sorgu parametreleri desteği

## Hata İşleme

MCP DSL entegrasyonu esnek olacak şekilde tasarlanmış ve hataları zarif bir şekilde işler:

```python  theme={null}
from crewai import Agent
from crewai.mcp import MCPServerStdio, MCPServerHTTP

agent = Agent(
    role="Resilient Agent",
    goal="Continue working despite server issues",
    backstory="Agent that handles failures gracefully",
    mcps=[
        # String references
        "https://reliable-server.com/mcp",        # Will work
        "https://unreachable-server.com/mcp",     # Will be skipped gracefully
        "snowflake",                              # Connected MCP from catalog

        # Structured configs
        MCPServerStdio(
            command="python",
            args=["reliable_server.py"],          # Will work
        ),
        MCPServerHTTP(
            url="https://slow-server.com/mcp",     # Will timeout gracefully
        ),
    ]
)
# Ajan çalışan sunuculardan araçları kullanacak ve başarısız olanlar için uyarıları günlüğe kaydedecek
```

Tüm bağlantı hataları zarif bir şekilde işlenir:

* **Bağlantı hataları**: Uyarı olarak günlüğe kaydedilir, ajan kullanılabilir araçlarla devam eder
* **Zaman aşımı hataları**: Bağlantılar 30 saniye sonra zaman aşımına uğrar (yapılandırılabilir)
* **Kimlik doğrulama hataları**: Hata ayıklama için açıkça günlüğe kaydedilir
* **Geçersiz konfigürasyonlar**: Ajan oluşturma sırasında doğrulama hataları yükseltilir

## Gelişmiş: MCPServerAdapter

Manuel bağlantı yönetimi gerektiren karmaşık senaryolar için `crewai-tools` kütüphanesinden `MCPServerAdapter` sınıfını kullanın. Python bağlam yöneticisini (`with` ifadesi) kullanmak, MCP sunucusunun bağlantısını otomatik olarak başlatıp durdurmak için önerilen yaklaşımdır.

## Bağlantı Konfigürasyonu

`MCPServerAdapter`, bağlantı davranışını özelleştirmek için birkaç yapılandırma seçeneğini destekler:

* **`connect_timeout`** (isteğe bağlı): MCP sunucusu ile bağlantı kurulmayı beklemek için maksimum saniye cinsinden zaman. Belirtilmezse varsayılan olarak 30 saniyedir. Bu, değişken yanıt sürelerine sahip olabilecek uzak sunucular için özellikle yararlıdır.

```python  theme={null}
# Özel bağlantı zaman aşımı ile örnek
with MCPServerAdapter(server_params, connect_timeout=60) as tools:
    # Bağlantı kurulmamışsa 60 saniye sonra zaman aşımına uğrar
    pass
```

```python  theme={null}
from crewai import Agent
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # For Stdio Server

# Örnek server_params (sunucu türünüzü temel alarak birini seçin):
# 1. Stdio Sunucusu:
server_params=StdioServerParameters(
    command="python3",
    args=["servers/your_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

# 2. SSE Sunucusu:
server_params = {
    "url": "http://localhost:8000/sse",
    "transport": "sse"
}

# 3. Akışlanabilir HTTP Sunucusu:
server_params = {
    "url": "http://localhost:8001/mcp",
    "transport": "streamable-http"
}

# Örnek kullanım (server_params ayarlandıktan sonra açıklama kaldırın ve uyarlayın):
with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

    my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=mcp_tools, # Pass the loaded tools to your agent
        reasoning=True,
        verbose=True
    )
    # ... rest of your crew setup ...
```

Bu genel model, araçların nasıl entegre edileceğini gösterir. Her taşıma için özel örnekler için aşağıdaki ayrıntılı kılavuzlara bakın.

## Araçları Filtreleme

Araçları filtrelemek için iki yol vardır:

1. Sözlük stili indeksleme kullanarak belirli bir araça erişme.
2. Araç adlarının listesini `MCPServerAdapter` yapıcısına geçme.

### Sözlük stili indeksleme kullanarak belirli bir araça erişme.

```python  theme={null}
with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

    my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
tools=[mcp_tools["tool_name"]], # Yüklenen araçları ajanınıza geçin
    reasoning=True,
    verbose=True
)
    # ... crew kurulumunuzun geri kalanı ...
```

### Araç adlarının listesini `MCPServerAdapter` yapıcısına geçme.

```python  theme={null}
with MCPServerAdapter(server_params, "tool_name", connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

    my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=mcp_tools, # Yüklenen araçları ajanınıza geçin
        reasoning=True,
        verbose=True
    )
    # ... crew kurulumunuzun geri kalanı ...
```

## CrewBase ile Kullanım

MCPServer araçlarını bir CrewBase sınıfı içinde kullanmak için `get_mcp_tools` yöntemini kullanın. Sunucu konfigürasyonları `mcp_server_params` özniteliği aracılığıyla sağlanmalıdır. Tek bir yapılandırma veya birden fazla sunucu yapılandırmasının bir listesini geçebilirsiniz.

```python  theme={null}
@CrewBase
class CrewWithMCP:
  # ... ajan ve görev konfigürasyon dosyanızı tanımlayın ...

  mcp_server_params = [
    # Streamable HTTP Sunucusu
    {
        "url": "http://localhost:8001/mcp",
        "transport": "streamable-http"
    },
    # SSE Sunucusu
    {
        "url": "http://localhost:8000/sse",
        "transport": "sse"
    },
    # StdIO Sunucusu
    StdioServerParameters(
        command="python3",
        args=["servers/your_stdio_server.py"],
        env={"UV_PYTHON": "3.12", **os.environ},
    )
  ]

  @agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools()) # tüm kullanılabilir araçları al

    # ... crew kurulumunuzun geri kalanı ...
```

<Tip>
  Bir crew sınıfı `@CrewBase` ile dekore edildiğinde, uyumlu yaşam döngüsü sizin için yönetilir:

  * `get_mcp_tools()` için ilk çağrı, crew'daki her ajan tarafından yeniden kullanılan paylaşılan bir `MCPServerAdapter` tembel olarak oluşturur.
  * Uyumlu, `@CrewBase` tarafından enjekte edilen örtülü bir after-kickoff kancası sayesinde `.kickoff()` tamamlandıktan sonra otomatik olarak kapatılır, bu nedenle el ile temizlik gerekmez.
  * `mcp_server_params` tanımlanmamışsa, `get_mcp_tools()` basitçe boş bir liste döndürür ve aynı kod yollarının MCP yapılandırılmış veya yapılandırılmamış şekilde çalışması sağlanır.

  Bu, `get_mcp_tools()` öğesini birden fazla ajan yönteminden çağırmayı veya ortam başına MCP'yi seçerek etkinleştirmeyi güvenli hale getirir.
</Tip>

### Bağlantı Zaman Aşımı Yapılandırması

`mcp_connect_timeout` sınıf özniteliğini ayarlayarak MCP sunucuları için bağlantı zaman aşımını yapılandırabilirsiniz. Hiçbir zaman aşımı belirtilmemişse, varsayılan olarak 30 saniye olur.

```python  theme={null}
@CrewBase
class CrewWithMCP:
  mcp_server_params = [...]
  mcp_connect_timeout = 60  # Tüm MCP bağlantıları için 60 saniye zaman aşımı

  @agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools())
```

```python  theme={null}
@CrewBase
class CrewWithDefaultTimeout:
  mcp_server_params = [...]
  # mcp_connect_timeout belirtilmedi - varsayılan 30 saniye kullanır

  @agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools())
```

### Araçları Filtreleme

`get_mcp_tools` yöntemine araç adlarının bir listesini geçerek ajanınıza hangi araçların kullanılabilir olduğunu filtreleyebilirsiniz.

```python  theme={null}
@agent
def another_agent(self):
    return Agent(
      config=self.agents_config["your_agent"],
      tools=self.get_mcp_tools("tool_1", "tool_2") # belirli araçları al
    )
```

Zaman aşımı yapılandırması, crew içindeki tüm MCP araç çağrılarına uygulanır:

```python  theme={null}
@CrewBase
class CrewWithCustomTimeout:
  mcp_server_params = [...]
  mcp_connect_timeout = 90  # Tüm MCP bağlantıları için 90 saniye zaman aşımı

  @agent
  def filtered_agent(self):
      return Agent(
        config=self.agents_config["your_agent"],
        tools=self.get_mcp_tools("tool_1", "tool_2") # özel araçlar özel zaman aşımıyla
      )
```

## MCP Entegrasyonlarını Keşfedin

<CardGroup cols={2}>
  <Card title="Basit DSL Entegrasyonu" icon="code" href="/en/mcp/dsl-integration" color="#3B82F6">
    **Önerilen**: Sorunsuz MCP entegrasyonu için basit `mcps=[]` alan sütaksını kullanın.
  </Card>

  <Card title="Stdio Taşıması" icon="server" href="/en/mcp/stdio" color="#10B981">
    Standart giriş/çıkış aracılığıyla yerel MCP sunucularına bağlanın. Scriptler ve yerel yürütebilir dosyalar için ideal.
  </Card>

  <Card title="SSE Taşıması" icon="wifi" href="/en/mcp/sse" color="#F59E0B">
    Gerçek zamanlı veri akışı için Server-Sent Events kullanan uzak MCP sunucularıyla entegre olun.
  </Card>

  <Card title="Streamable HTTP Taşıması" icon="globe" href="/en/mcp/streamable-http" color="#8B5CF6">
    Uzak MCP sunucularla sağlam iletişim için esnek Streamable HTTP'yi kullanın.
  </Card>

  <Card title="Birden Fazla Sunucuya Bağlantı" icon="layer-group" href="/en/mcp/multiple-servers" color="#EF4444">
    Tek bir uyumlu kullanarak birden fazla MCP sunucusundan araçları aynı anda toplayın.
  </Card>

  <Card title="Güvenlik Dikkatleri" icon="lock" href="/en/mcp/security" color="#DC2626">
    Ajanlarınızı güvenli tutmak için MCP entegrasyonu için önemli güvenlik en iyi uygulamalarını inceleyin.
  </Card>
</CardGroup>

CrewAI ile MCP entegrasyonunun tam demolar ve örnekleri için bu havuzuna bakın! 👇

<Card title="GitHub Deposu" icon="github" href="https://github.com/tonykipkemboi/crewai-mcp-demo" target="_blank">
  CrewAI MCP Demo
</Card>

## MCP ile Güvenli Kalma

<Warning>MCP Sunucusunu kullanmadan önce her zaman ona güvenip güvenemeyeceğinizden emin olun.</Warning>

#### Güvenlik Uyarısı: DNS Rebinding Saldırıları

SSE taşımaları, uygun şekilde güvenlik altına alınmazsa DNS rebinding saldırılarına karşı zafiyetli olabilir.
Bunu önlemek için:

1. **Gelen SSE bağlantılarındaki Origin başlıklarını her zaman doğrulayın** - beklenen kaynaklardan geldiğinden emin olmak için
2. **Sunucuları yerel olarak çalıştırırken tüm ağ arayüzlerine bağlantı kurmayın** (0.0.0.0) - bunun yerine sadece localhost (127.0.0.1) kullanın
3. **Tüm SSE bağlantıları için uygun kimlik doğrulama uygulayın**

Bu korumalar olmadan, saldırganlar uzak websitelerden DNS rebinding kullanarak yerel MCP sunucularıyla etkileşim kurabilir.

Daha fazla bilgi için bkz. [Anthropic'in MCP Transport Güvenlik dokümantasyonu](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

### Sınırlamalar

* **Desteklenen Primitivler**: Şu anda `MCPServerAdapter` öncelikle MCP `tools` uyumlaştırılmasını destekler.
  `prompts` veya `resources` gibi diğer MCP primitifleri şu anda bu uyumlu araç vasıtasıyla CrewAI bileşenleri olarak doğrudan entegre edilmemektedir.
* **Çıktı İşleme**: Uyumlu, tipik olarak bir MCP aracından asıl metin çıktısını işler (ör. `.content[0].text`). Karmaşık veya çok modlu çıktılar, bu düzene uymazsa özel işlemeyi gerektirebilir.
