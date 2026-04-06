> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Birden Fazla MCP Sunucusuna Bağlanma

> CrewAI içinde `MCPServerAdapter` kullanarak aynı anda birden fazla MCP sunucusuna nasıl bağlanacağınızı ve araçlarını nasıl bir araya getireceğinizi öğrenin.

## Genel Bakış

`crewai-tools` içindeki `MCPServerAdapter`, aynı anda birden fazla MCP sunucusuna bağlanmanızı sağlar. Bu, ajanlarınızın farklı servisler veya ortamlar arasında dağıtılmış araçlara erişmesi gerektiğinde kullanışlıdır. Adaptör, belirtilen tüm sunuculardaki araçları bir araya getirerek bunları CrewAI ajanlarınız için kullanılabilir hale getirir.

## Yapılandırma

Birden fazla sunucuya bağlanmak için `MCPServerAdapter` bileşenine sunucu parametre sözlüklerinden oluşan bir liste verirsiniz. Listedeki her sözlük, bir MCP sunucusunun parametrelerini tanımlamalıdır.

Listedeki her sunucu için desteklenen taşıma türleri `stdio`, `sse` ve `streamable-http` içerir.

```python  theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # Stdio örneği için gerekli

# Birden fazla MCP sunucusu için parametreleri tanımla
server_params_list = [
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

try:
    with MCPServerAdapter(server_params_list) as aggregated_tools:
        print(f"Kullanılabilir birleştirilmiş araçlar: {[tool.name for tool in aggregated_tools]}")

        multi_server_agent = Agent(
            role="Çok Yönlü Asistan",
            goal="Yerel Stdio, uzak SSE ve uzak HTTP MCP sunucularındaki araçları kullan.",
            backstory="Birden fazla kaynaktan gelen çeşitli araçlardan yararlanabilen bir yapay zeka ajanı.",
            tools=aggregated_tools, # Tüm araçlar burada kullanılabilir
            verbose=True,
        )

        ... # Diğer ajan, görev ve ekip kodlarınız burada

except Exception as e:
    print(f"Birden fazla MCP sunucusuna bağlanırken veya kullanırken hata oluştu (Yönetilen): {e}")
    print("Tüm MCP sunucularının çalıştığından ve doğru yapılandırmalarla erişilebilir olduğundan emin olun.")

```

## Bağlantı Yönetimi

Bağlam yöneticisi (`with` ifadesi) kullanıldığında, `MCPServerAdapter` yapılandırılmış MCP sunucularına olan tüm bağlantıların yaşam döngüsünü (başlatma ve durdurma) yönetir. Bu, kaynak yönetimini basitleştirir ve bağlamdan çıkıldığında tüm bağlantıların düzgün şekilde kapatılmasını sağlar.
