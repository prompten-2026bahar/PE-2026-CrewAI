> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Streamable HTTP Taşıması

> Esnek Streamable HTTP taşımasını kullanarak CrewAI'yi uzak MCP sunucularına nasıl bağlayacağınızı öğrenin.

## Genel Bakış

Streamable HTTP taşıması, uzak MCP sunucularına bağlanmak için esnek bir yol sunar. Genellikle HTTP üzerine kuruludur ve istek-yanıt ile akış dahil olmak üzere çeşitli iletişim desenlerini destekleyebilir; bazen daha geniş bir HTTP etkileşimi içinde sunucudan istemciye akışlar için Server-Sent Events (SSE) de kullanır.

## Temel Kavramlar

* **Uzak Sunucular**: Uzakta barındırılan MCP sunucuları için tasarlanmıştır.
* **Esneklik**: Düz SSE'den daha karmaşık etkileşim desenlerini destekleyebilir; sunucu bunu uygularsa çift yönlü iletişimi de kapsayabilir.
* **`MCPServerAdapter` Yapılandırması**: MCP iletişimi için sunucunun temel URL'sini sağlamanız ve taşıma türü olarak `"streamable-http"` belirtmeniz gerekir.

## Streamable HTTP ile Bağlanma

Bir Streamable HTTP MCP sunucusuyla bağlantı yaşam döngüsünü yönetmek için iki temel yönteminiz vardır:

### 1. Tam Yönetilen Bağlantı (Önerilen)

Önerilen yaklaşım, bağlantının kurulmasını ve kapatılmasını otomatik olarak yöneten bir Python bağlam yöneticisi (`with` ifadesi) kullanmaktır.

```python  theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8001/mcp", # Kendi Streamable HTTP sunucu URL'niz ile değiştirin
    "transport": "streamable-http"
}

try:
    with MCPServerAdapter(server_params) as tools:
        print(f"Streamable HTTP MCP sunucusundan kullanılabilir araçlar: {[tool.name for tool in tools]}")

        http_agent = Agent(
            role="HTTP Servis Entegratörü",
            goal="Streamable HTTP aracılığıyla uzak bir MCP sunucusundaki araçları kullan.",
            backstory="Karmaşık web servisleriyle etkileşim kurma konusunda yetkin bir yapay zeka ajanı.",
            tools=tools,
            verbose=True,
        )

        http_task = Task(
            description="Streamable HTTP sunucusundaki bir aracı kullanarak karmaşık bir veri sorgusu gerçekleştir.",
            expected_output="Karmaşık veri sorgusunun sonucu.",
            agent=http_agent,
        )

        http_crew = Crew(
            agents=[http_agent],
            tasks=[http_task],
            verbose=True,
            process=Process.sequential
        )
        
        result = http_crew.kickoff() 
        print("\nEkip Görev Sonucu (Streamable HTTP - Yönetilen):\n", result)

except Exception as e:
    print(f"Streamable HTTP MCP sunucusuna bağlanırken veya kullanırken hata oluştu (Yönetilen): {e}")
    print("Streamable HTTP MCP sunucusunun çalıştığından ve belirtilen URL'de erişilebilir olduğundan emin olun.")

```

**Not:** `"http://localhost:8001/mcp"` ifadesini Streamable HTTP MCP sunucunuzun gerçek URL'si ile değiştirin.

### 2. Manuel Bağlantı Yaşam Döngüsü

Daha açık denetim gerektiren senaryolarda `MCPServerAdapter` bağlantısını manuel olarak yönetebilirsiniz.

<Info>
  İşiniz bittiğinde bağlantıyı kapatmak ve kaynakları serbest bırakmak için `mcp_server_adapter.stop()` çağrısını yapmanız **kritiktir**. Bunu garanti altına almanın en güvenli yolu `try...finally` bloğudur.
</Info>

```python  theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8001/mcp", # Kendi Streamable HTTP sunucu URL'niz ile değiştirin
    "transport": "streamable-http"
}

mcp_server_adapter = None 
try:
    mcp_server_adapter = MCPServerAdapter(server_params)
    mcp_server_adapter.start()
    tools = mcp_server_adapter.tools
    print(f"Kullanılabilir araçlar (manuel Streamable HTTP): {[tool.name for tool in tools]}")

    manual_http_agent = Agent(
        role="Gelişmiş Web Servisi Kullanıcısı",
        goal="Manuel olarak yönetilen Streamable HTTP bağlantıları kullanarak bir MCP sunucusuyla etkileşime gir.",
        backstory="HTTP tabanlı servis entegrasyonlarını ince ayar yapma konusunda uzman bir yapay zeka.",
        tools=tools,
        verbose=True
    )
    
    data_processing_task = Task(
        description="Veriyi işlenmek üzere gönder ve sonuçları Streamable HTTP üzerinden al.",
        expected_output="İşlenmiş veri veya onay.",
        agent=manual_http_agent
    )
    
    data_crew = Crew(
        agents=[manual_http_agent],
        tasks=[data_processing_task],
        verbose=True,
        process=Process.sequential
    )
    
    result = data_crew.kickoff()
    print("\nEkip Görev Sonucu (Streamable HTTP - Manuel):\n", result)

except Exception as e:
    print(f"Manuel Streamable HTTP MCP entegrasyonu sırasında bir hata oluştu: {e}")
    print("Streamable HTTP MCP sunucusunun çalıştığından ve erişilebilir olduğundan emin olun.")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected:
        print("Streamable HTTP MCP sunucu bağlantısı durduruluyor (manuel)...")
        mcp_server_adapter.stop()  # **Kritik: stop çağrısının yapıldığından emin olun**
    elif mcp_server_adapter:
        print("Streamable HTTP MCP sunucu adaptörü bağlı değildi. stop gerekmedi veya start başarısız oldu.")
```

## Güvenlik Hususları

Streamable HTTP taşıması kullanılırken genel web güvenliği en iyi uygulamaları büyük önem taşır:

* **HTTPS Kullanın**: Aktarım halindeki verileri şifrelemek için MCP sunucu URL'lerinizde her zaman HTTPS'i (HTTP Secure) tercih edin.
* **Kimlik Doğrulama**: MCP sunucunuz hassas araçlar veya veriler sunuyorsa güçlü kimlik doğrulama mekanizmaları uygulayın.
* **Girdi Doğrulama**: MCP sunucunuzun gelen tüm istekleri ve parametreleri doğruladığından emin olun.

MCP entegrasyonlarınızı güvence altına almaya yönelik kapsamlı bir rehber için lütfen [Security Considerations](./security.mdx) sayfamıza ve resmi [MCP Transport Security documentation](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations) belgesine bakın.

