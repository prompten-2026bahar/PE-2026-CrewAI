# Kurulum
CrewAI ile başlayın - Kurulum yapın, yapılandırın ve ilk yapay zeka ekibinizi oluşturun.

## Video Eğitim

Kurulum sürecinin adım adım gösterimini içeren bu video eğitimini izleyin:

<iframe
  className="w-full aspect-video rounded-xl"
  src="https://www.youtube.com/embed/-kSOTtYzgEw"
  title="CrewAI Kurulum Kılavuzu"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
></iframe>

## Yazılı Eğitim

**Python Sürüm Gereksinimleri**

CrewAI `Python >=3.10 ve <3.14` gerektirir. Sürümünüzü kontrol etme şekli:

```bash
python3 --version
```

Python'u güncellemeniz gerekiyorsa [python.org/downloads](https://python.org/downloads) adresini ziyaret edin.

**OpenAI SDK Gereksinimi**

CrewAI 0.175.0, `openai >= 1.13.3` gerektirir. Bağımlılıkları kendiniz yönetiyorsanız, import/çalışma zamanı sorunlarını önlemek için ortamınızın bu kısıtlamayı karşıladığından emin olun.

CrewAI, bağımlılık yönetimi ve paket işleme aracı olarak `uv`'yi kullanır. Proje kurulumunu ve yürütmeyi basitleştirir, sorunsuz bir deneyim sunar.

Henüz `uv` kurmadıysanız, sisteminize hızlıca kurmak için **1. adıma** bakın, aksi takdirde **2. adıma** atlayabilirsiniz.

  - **macOS/Linux'ta:**

    `curl`'ü kullanarak komut dosyasını indirin ve `sh` ile çalıştırın:

    ```shell
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    Sisteminizde `curl` yoksa, `wget`'i kullanabilirsiniz:

    ```shell
    wget -qO- https://astral.sh/uv/install.sh | sh
    ```

  - **Windows'ta:**

    `irm`'yi kullanarak komut dosyasını indirin ve `iex` ile çalıştırın:

    ```shell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    Herhangi bir sorunla karşılaşırsanız, daha fazla bilgi için [UV'nin kurulum kılavuzuna](https://docs.astral.sh/uv/getting-started/installation/) bakın.

  - `crewai` CLI'sini yüklemek için aşağıdaki komutu çalıştırın:
    ```shell
    uv tool install crewai
    ```
    
      PATH uyarısı alırsanız, kabuğunuzu güncellemek için bu komutu çalıştırın:
      ```bash
      uv tool update-shell
      ```
    
      Windows'ta `chroma-hnswlib==0.7.6` oluşturma hatasını (`fatal error C1083: Cannot open include file: 'float.h'`) alırsanız, *Desktop development with C++* ile [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) yükleyin.
  

  - `crewai`'nin yüklü olup olmadığını doğrulamak için şunu çalıştırın:
    ```shell
    uv tool list
    ```
  - Şuna benzer bir şey görmelisiniz:
    ```shell
    crewai v0.102.0
    - crewai
    ```
  - `crewai`'yi güncellemeniz gerekirse, şunu çalıştırın:
    ```shell
    uv tool install crewai --upgrade
    ```
  Kurulum başarılı! İlk ekibinizi oluşturmaya hazırsınız! 🎉

## Bir CrewAI Projesi Oluşturma

Tümleşik bir yaklaşımla agent'ları ve görevleri tanımlamak için `YAML` şablon iskeletini kullanmanızı öneririz. Başlamak için nasıl yapacağınız aşağıdadır:

  - `crewai` CLI komutunu çalıştırın:
    ```shell
    crewai create crew <proje_adınız>
    ```

  - Bu, aşağıdaki yapıya sahip yeni bir proje oluşturur:
    ```
    my_project/
    ├── .gitignore
    ├── knowledge/
    ├── pyproject.toml
    ├── README.md
    ├── .env
    └── src/
        └── my_project/
            ├── __init__.py
            ├── main.py
            ├── crew.py
            ├── tools/
            │   ├── custom_tool.py
            │   └── __init__.py
            └── config/
                ├── agents.yaml
                └── tasks.yaml
    ```

  - Projeniz aşağıdaki temel dosyaları içerir:
    | Dosya | Amaç |
    | --- | --- |
    | `agents.yaml` | Yapay zeka agent'larınızı ve rollarını tanımlayın |
    | `tasks.yaml` | Agent görevlerini ve iş akışlarını ayarlayın |
    | `.env` | API anahtarlarını ve ortam değişkenlerini saklayın |
    | `main.py` | Proje giriş noktası ve yürütme akışı |
    | `crew.py` | Ekip orkestrasyonu ve koordinasyon |
    | `tools/` | Özel agent araçları için dizin |
    | `knowledge/` | Bilgi tabanı için dizin |

  - Ekibinizin davranışını tanımlamak için `agents.yaml` ve `tasks.yaml`'i düzenlemeye başlayın.
  - API anahtarları gibi hassas bilgileri `.env` içinde saklayın.

  - Ekibinizi çalıştırmadan önce, şunu çalıştırdığınızdan emin olun:
    ```bash
    crewai install
    ```
  - Ek paketler yüklemeniz gerekirse, şunu kullanın:
    ```shell
    uv add <paket_adı>
    ```
  - Ekibinizi çalıştırmak için, projenizin kök dizininde aşağıdaki komutu çalıştırın:
    ```shell
    crewai run
    ```

## Kurumsal Kurulum Seçenekleri

Takımlar ve kuruluşlar için, CrewAI, kurulum karmaşıklığını ortadan kaldıran kurumsal dağıtım seçenekleri sunar:

### CrewAI AMP (SaaS)

- Herhangi bir kurulum gerektirmez - ücretsiz olarak [app.crewai.com](https://app.crewai.com) adresinden kaydolun
- Otomatik güncellemeler ve bakım
- Yönetilen altyapı ve ölçekleme
- Kodsuz Crews oluşturun

### CrewAI Fabrikası (Kendi kendine barındırılan)

- Altyapınız için kapsüllenmiş dağıtım
- On-prem dağıtımları dahil olmak üzere herhangi bir hiper ölçekleyiciyi destekler
- Mevcut güvenlik sistemlerinizle entegrasyon

### Kurumsal Seçenekleri Keşfedin

CrewAI'nin kurumsal teklifleri hakkında bilgi edinin ve bir demoyu planlayın

## Sonraki Adımlar

### İlk Agent'ınızı Oluşturun

Hemen başlayıp ilk CrewAI agent'ınızı oluşturmak ve pratik deneyim kazanmak için hızlı başlangıç ​​kılavuzumuza uyun.

### Topluluğa Katılın

Diğer geliştiricilerle iletişim kurun, yardım alın ve CrewAI deneyimlerinizi paylaşın.