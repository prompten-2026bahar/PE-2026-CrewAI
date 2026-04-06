> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# SSE Taşıması

> Gerçek zamanlı iletişim için Server-Sent Events (SSE) kullanarak CrewAI'yi uzak MCP sunucularına nasıl bağlayacağınızı öğrenin.

## Genel Bakış

Server-Sent Events (SSE), bir web sunucusunun tek ve uzun ömürlü bir HTTP bağlantısı üzerinden istemciye güncellemeler göndermesi için standart bir yol sunar. MCP bağlamında SSE, uzak sunucuların verileri (araç yanıtları gibi) CrewAI uygulamanıza gerçek zamanlı olarak akıtması için kullanılır.

## Temel Kavramlar

* **Uzak Sunucular**: SSE, uzakta barındırılan MCP sunucuları için uygundur.
* **Tek Yönlü Akış**: SSE genellikle sunucudan istemciye doğru tek yönlü bir iletişim kanalıdır.
* **`MCPServerAdapter` Yapılandırması**: SSE için sunucunun URL'sini sağlar ve taşıma türünü belirtirsiniz.

## SSE ile Bağlanma

Bağlantı yaşam döngüsünü yönetmek için iki temel yaklaşımla SSE tabanlı bir MCP sunucusuna bağlanabilirsiniz:

### 1. Tam Yönetilen Bağlantı (Önerilen)

Önerilen yaklaşım, Python bağlam yöneticisi (`with` ifadesi) kullanmaktır. Bu yöntem SSE MCP sunucusuna bağlantının kurulmasını ve kapatılmasını otomatik olarak yönetir.

```python  theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8000/sse", # Kendi SSE sunucu URL'niz ile değiştirin
    "transport": "sse" 
}

# MCPServerAdapter'ı bir bağlam yöneticisi ile kullanma
try:
    with MCPServerAdapter(server_params) as tools:
        print(f"SSE MCP sunucusundan kullanılabilir araçlar: {[tool.name for tool in tools]}")

        # Örnek: SSE MCP sunucusundan bir araç kullanma
        sse_agent = Agent(
            role="Uzak Servis Kullanıcısı",
            goal="Uzak bir SSE MCP sunucusu tarafından sağlanan bir aracı kullan.",
            backstory="SSE aracılığıyla harici servislere bağlanan bir yapay zeka ajanı.",
            tools=tools,
            reasoning=True,
            verbose=True,
        )

        sse_task = Task(
            description="'AAPL' için gerçek zamanlı hisse güncellemelerini bir SSE aracı kullanarak getir.",
            expected_output="AAPL için en güncel hisse fiyatı.",
            agent=sse_agent,
            markdown=True
        )

        sse_crew = Crew(
            agents=[sse_agent],
            tasks=[sse_task],
            verbose=True,
            process=Process.sequential
        )
        
        if tools: # Yalnızca araçlar yüklendiyse başlat
            result = sse_crew.kickoff() # Araç gerektiriyorsa inputs={'stock_symbol': 'AAPL'} ekleyin
            print("\nEkip Görev Sonucu (SSE - Yönetilen):\n", result)
        else:
            print("Araçlar yüklenmediği için ekip başlatma atlanıyor (sunucu bağlantısını kontrol edin).")

except Exception as e:
    print(f"SSE MCP sunucusuna bağlanırken veya kullanırken hata oluştu (Yönetilen): {e}")
    print("SSE MCP sunucusunun çalıştığından ve belirtilen URL'de erişilebilir olduğundan emin olun.")

```

<Note>
  `"http://localhost:8000/sse"` ifadesini SSE MCP sunucunuzun gerçek URL'si ile değiştirin.
</Note>

### 2. Manuel Bağlantı Yaşam Döngüsü

Daha ayrıntılı denetime ihtiyaç duyuyorsanız `MCPServerAdapter` bağlantı yaşam döngüsünü manuel olarak yönetebilirsiniz.

<Info>
  Bağlantının kapatıldığından ve kaynakların serbest bırakıldığından emin olmak için `mcp_server_adapter.stop()` çağrısını **MUTLAKA** yapmalısınız. `try...finally` bloğu kullanılması önemle tavsiye edilir.
</Info>

```python  theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8000/sse", # Kendi SSE sunucu URL'niz ile değiştirin
    "transport": "sse"
}

mcp_server_adapter = None 
try:
    mcp_server_adapter = MCPServerAdapter(server_params)
    mcp_server_adapter.start()
    tools = mcp_server_adapter.tools
    print(f"Kullanılabilir araçlar (manuel SSE): {[tool.name for tool in tools]}")

    manual_sse_agent = Agent(
        role="Uzak Veri Analisti",
        goal="Manuel bağlantı yönetimi kullanarak uzak bir SSE MCP sunucusundan alınan verileri analiz et.",
        backstory="SSE bağlantılarını açık şekilde yönetme konusunda yetenekli bir yapay zeka.",
        tools=tools,
        verbose=True
    )
    
    analysis_task = Task(
        description="SSE sunucusundan en güncel kullanıcı etkinliği eğilimlerini getir ve analiz et.",
        expected_output="Kullanıcı etkinliği eğilimlerine dair bir özet rapor.",
        agent=manual_sse_agent
    )
    
    analysis_crew = Crew(
        agents=[manual_sse_agent],
        tasks=[analysis_task],
        verbose=True,
        process=Process.sequential
    )
    
    result = analysis_crew.kickoff()
    print("\nEkip Görev Sonucu (SSE - Manuel):\n", result)

except Exception as e:
    print(f"Manuel SSE MCP entegrasyonu sırasında bir hata oluştu: {e}")
    print("SSE MCP sunucusunun çalıştığından ve erişilebilir olduğundan emin olun.")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected:
        print("SSE MCP sunucu bağlantısı durduruluyor (manuel)...")
        mcp_server_adapter.stop()  # **Kritik: stop çağrısının yapıldığından emin olun**
    elif mcp_server_adapter:
        print("SSE MCP sunucu adaptörü bağlı değildi. stop gerekmedi veya start başarısız oldu.")

```

## SSE için Güvenlik Hususları

<Warning>
  **DNS Rebinding Saldırıları**: SSE taşıması, MCP sunucusu doğru şekilde güvence altına alınmazsa DNS rebinding saldırılarına karşı savunmasız olabilir. Bu durum, kötü amaçlı web sitelerinin yerel veya intranet tabanlı MCP sunucularıyla etkileşime girmesine izin verebilir.
</Warning>

Bu riski azaltmak için:

* MCP sunucu uygulamaları, gelen SSE bağlantılarında **`Origin` başlıklarını doğrulamalıdır**.
* Geliştirme için yerel SSE MCP sunucuları çalıştırırken tüm ağ arayüzleri (`0.0.0.0`) yerine **yalnızca `localhost` (`127.0.0.1`) üzerine bağlanın**.
* Hassas araçlar veya veriler sunuluyorsa tüm SSE bağlantıları için **uygun kimlik doğrulama** uygulayın.

Güvenlik için en iyi uygulamalara dair kapsamlı bir genel bakış için lütfen [Security Considerations](./security.mdx) sayfamıza ve resmi [MCP Transport Security documentation](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations) belgesine bakın.
