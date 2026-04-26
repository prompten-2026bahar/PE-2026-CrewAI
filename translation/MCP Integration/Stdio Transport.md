> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Stdio Taşıması

> Stdio (Standart Girdi/Çıktı) taşıma mekanizmasını kullanarak CrewAI'yi yerel MCP sunucularına nasıl bağlayacağınızı öğrenin.

## Genel Bakış

Stdio (Standart Girdi/Çıktı) taşıması, `MCPServerAdapter` bileşenini standart girdi ve çıktı akışları üzerinden iletişim kuran yerel MCP sunucularına bağlamak için tasarlanmıştır. Bu genellikle MCP sunucusu, CrewAI uygulamanız ile aynı makinede çalışan bir betik ya da çalıştırılabilir dosya olduğunda kullanılır.

## Temel Kavramlar

* **Yerel Çalıştırma**: Stdio taşıması, MCP sunucusu için yerelde çalışan bir süreci yönetir.
* **`StdioServerParameters`**: `mcp` kütüphanesindeki bu sınıf, Stdio sunucusunu başlatmak için komut, argümanlar ve ortam değişkenlerini yapılandırmak amacıyla kullanılır.

## Stdio ile Bağlanma

Bağlantı yaşam döngüsünü yönetmek için iki temel yaklaşımla Stdio tabanlı bir MCP sunucusuna bağlanabilirsiniz:

### 1. Tam Yönetilen Bağlantı (Önerilen)

Önerilen yaklaşım, Python bağlam yöneticisi (`with` ifadesi) kullanmaktır. Bu yöntem MCP sunucu sürecinin başlatılmasını ve bağlamdan çıkıldığında durdurulmasını otomatik olarak yönetir.

```python  theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os

# Bir StdioServerParameters nesnesi oluştur
server_params=StdioServerParameters(
    command="python3", 
    args=["servers/your_stdio_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

with MCPServerAdapter(server_params) as tools:
    print(f"Stdio MCP sunucusundan kullanılabilir araçlar: {[tool.name for tool in tools]}")

    # Örnek: Stdio MCP sunucusundaki araçları bir CrewAI ajanında kullanma
    research_agent = Agent(
        role="Yerel Veri İşleyici",
        goal="Yerel bir Stdio tabanlı araç kullanarak veriyi işle.",
        backstory="Özel görevler için MCP aracılığıyla yerel betiklerden yararlanan bir yapay zeka.",
        tools=tools,
        reasoning=True,
        verbose=True,
    )
    
    processing_task = Task(
        description="'data.txt' girdi veri dosyasını işle ve içeriğini özetle.",
        expected_output="İşlenen verinin bir özeti.",
        agent=research_agent,
        markdown=True
    )
    
    data_crew = Crew(
        agents=[research_agent],
        tasks=[processing_task],
        verbose=True,
        process=Process.sequential 
    )
   
    result = data_crew.kickoff()
    print("\nEkip Görev Sonucu (Stdio - Yönetilen):\n", result)

```

### 2. Manuel Bağlantı Yaşam Döngüsü

Stdio MCP sunucu sürecinin ne zaman başlatılıp durdurulacağı üzerinde daha ayrıntılı denetime ihtiyaç duyuyorsanız `MCPServerAdapter` yaşam döngüsünü manuel olarak yönetebilirsiniz.

<Info>
  Sunucu sürecinin sonlandırıldığından ve kaynakların serbest bırakıldığından emin olmak için `mcp_server_adapter.stop()` çağrısını **MUTLAKA** yapmalısınız. `try...finally` bloğu kullanılması önemle tavsiye edilir.
</Info>

```python  theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os

# Bir StdioServerParameters nesnesi oluştur
stdio_params=StdioServerParameters(
    command="python3", 
    args=["servers/your_stdio_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

mcp_server_adapter = MCPServerAdapter(server_params=stdio_params)
try:
    mcp_server_adapter.start()  # Bağlantıyı ve sunucu sürecini manuel olarak başlat
    tools = mcp_server_adapter.tools
    print(f"Kullanılabilir araçlar (manuel Stdio): {[tool.name for tool in tools]}")

    # Örnek: Araçları Agent, Task, Crew kurulumunuzla kullanma
    manual_agent = Agent(
        role="Yerel Görev Yürütücüsü",
        goal="Manuel olarak yönetilen bir Stdio aracıyla belirli bir yerel görevi yürüt.",
        backstory="MCP üzerinden yerel süreçleri kontrol etmede yetkin bir yapay zeka.",
        tools=tools,
        verbose=True
    )
    
    manual_task = Task(
        description="'perform_analysis' komutunu Stdio aracı üzerinden çalıştır.",
        expected_output="Analiz sonuçları.",
        agent=manual_agent
    )
    
    manual_crew = Crew(
        agents=[manual_agent],
        tasks=[manual_task],
        verbose=True,
        process=Process.sequential
    )
        
       
    result = manual_crew.kickoff() # Gerçek girdiler kullandığınız araca bağlıdır
    print("\nEkip Görev Sonucu (Stdio - Manuel):\n", result)
            
except Exception as e:
    print(f"Manuel Stdio MCP entegrasyonu sırasında bir hata oluştu: {e}")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected: # Durdurmadan önce bağlı olup olmadığını kontrol et
        print("Stdio MCP sunucu bağlantısı durduruluyor (manuel)...")
        mcp_server_adapter.stop()  # **Kritik: stop çağrısının yapıldığından emin olun**
    elif mcp_server_adapter: # Adaptör varsa ama bağlı değilse (ör. start başarısız oldu)
        print("Stdio MCP sunucu adaptörü bağlı değildi. stop gerekmedi veya start başarısız oldu.")

```

Yer tutucu yolları ve komutları kendi gerçek Stdio sunucu bilgilerinizle değiştirmeyi unutmayın. `StdioServerParameters` içindeki `env` parametresi,
sunucu süreci için ortam değişkenleri ayarlamak amacıyla kullanılabilir; bu da davranışını yapılandırmak veya gerekli yolları sağlamak için yararlı olabilir (`PYTHONPATH` gibi).
