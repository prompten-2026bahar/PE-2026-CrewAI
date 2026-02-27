# CLI
CrewAI CLI’yi kullanarak CrewAI ile nasıl etkileşim kuracağınızı öğrenin.

0.140.0 sürümünden itibaren CrewAI AMP, giriş (login) sağlayıcısını taşıma sürecini başlattı. Bu nedenle CLI üzerinden kimlik doğrulama (authentication) akışı güncellendi.

Google ile giriş yapan kullanıcılar veya 3 Temmuz 2025’ten sonra hesap oluşturan kullanıcılar, crewai kütüphanesinin eski sürümleriyle giriş yapamayacaktır.


## Genel Bakış

CrewAI CLI, CrewAI ile etkileşim kurmanızı sağlayan bir dizi komut sağlar, bu sayede ekipleri ve akışları oluşturabilir, eğitebilir, çalıştırabilir ve yönetebilirsiniz.

## Kurulum

CrewAI CLI'yı kullanmak için öncelikle CrewAI'nın kurulu olduğundan emin olun:

```shell Terminal
pip install crewai
```

## Temel Kullanım

Bir CrewAI CLI komutunun temel yapısı şöyledir:

```shell Terminal
crewai [KOMUT] [SEÇENEKLER] [ARGÜMANLAR]
```

## Mevcut Komutlar

### 1. Oluştur (Create)

Yeni bir ekip veya akış oluşturur.

```shell Terminal
crewai create [SEÇENEKLER] TİP İSİM
```

- `TİP`: "ekip" veya "akış" seçeneklerinden birini seçin.
- `İSİM`: Ekip veya akışın adı.

Örnek:

```shell Terminal
crewai create crew my_new_crew
crewai create flow my_new_flow
```

### 2. Sürüm (Version)

Yüklü CrewAI sürümünü gösterir.

```shell Terminal
crewai version [SEÇENEKLER]
```

- `--tools`: (İsteğe bağlı) Yüklü CrewAI araçlarının sürümünü gösterir.

Örnek:

```shell Terminal
crewai version
crewai version --tools
```

### 3. Eğit (Train)

Ekipti belirli sayıda yineleme için eğitin.

```shell Terminal
crewai train [SEÇENEKLER]
```

- `-n, --n_iterations TAM_SAYI`: Ekibi eğitmek için kullanılacak yineleme sayısı (varsayılan: 5)
- `-f, --filename METİN`: Eğitim için özel bir dosyanın yolu (varsayılan: "trained_agents_data.pkl")

Örnek:

```shell Terminal
crewai train -n 10 -f my_training_data.pkl
```

### 4. Tekrarla (Replay)

Ekipti belirli bir görevden itibaren tekrar çalıştırır.

```shell Terminal
crewai replay [SEÇENEKLER]
```

- `-t, --task_id METİN`: Ekipti bu görev kimliğinden itibaren çalıştırır, ardından gelen tüm görevleri de dahil eder.

Örnek:

```shell Terminal
crewai replay -t task_123456
```

### 5. Görev Çıktılarını Günlükle (Log-tasks-outputs)

En son ekip kickoff() görev çıktılarınızı alın.

```shell Terminal
crewai log-tasks-outputs
```

### 6. Anıları Sıfırla (Reset-memories)

Ekip anılarını sıfırlayın (uzun, kısa, varlık, son_ekip_kickoff_çıktıları).

```shell Terminal
crewai reset-memories [SEÇENEKLER]
```

- `-l, --long`: UZUN DÖNEM hafızasını sıfırlar
- `-s, --short`: KISA DÖNEM hafızasını sıfırlar
- `-e, --entities`: VARLIK hafızasını sıfırlar
- `-k, --kickoff-outputs`: SON KICKOFF GÖREV ÇIKTILARI hafızasını sıfırlar
- `-kn, --knowledge`: BİLGİ depolamasını sıfırlar
- `-akn, --agent-knowledge`: AJAN BİLGİ depolamasını sıfırlar
- `-a, --all`: TÜM anıları sıfırlar

Örnek:

```shell Terminal
crewai reset-memories --long --short
crewai reset-memories --all
```

### 7. Test Et (Test)

Ekipti test edin ve sonuçları değerlendirin.

```shell Terminal
crewai test [SEÇENEKLER]
```

- `-n, --n_iterations TAM_SAYI`: Ekibi test etmek için kullanılacak yineleme sayısı (varsayılan: 3)
- `-m, --model METİN`: Ekipti test etmek için kullanılacak LLM Modeli (varsayılan: "gpt-4o-mini")

Örnek:

```shell Terminal
crewai test -n 5 -m gpt-3.5-turbo
```

### 8. Çalıştır (Run)

Ekipti veya akışı çalıştırır.

```shell Terminal
crewai run
```

0.103.0 sürümünden itibaren `crewai run` komutu hem standart ekipleri hem de akışları çalıştırmak için kullanılabilir. Akışlar için, türü pyproject.toml dosyasından otomatik olarak algılar ve uygun komutu çalıştırır. Bu artık hem ekipleri hem de akışları çalıştırmanın önerilen yoludur.

CrewAI projenizin bulunduğu dizinden bu komutları çalıştırdığınızdan emin olun. Bazı komutlar projenizin yapısı içindeki ek yapılandırma veya kurulum gerektirebilir.

### 9. Sohbet Et (Chat)

0.98.0 sürümünden itibaren `crewai chat` komutunu çalıştırdığınızda, ekibinizle etkileşimli bir oturum başlatırsınız. Yapay zeka asistanı, ekibin görevlerini yürütmek için gerekli girdileri istemeniz için size rehberlik eder. Tüm girdiler sağlandıktan sonra, ekip görevlerini yürütür.

Sonuçları aldıktan sonra, daha fazla talimat veya soru için asistanla etkileşime devam edebilirsiniz.

```shell Terminal
crewai chat
```

CrewAI projenizin kök dizininden bu komutları çalıştırdığınızdan emin olun.

ÖNEMLİ: Bu komutu etkinleştirmek için `crew.py` dosyanızdaki `chat_llm` özelliğini ayarlayın.

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True,
        chat_llm="gpt-4o",  # Sohbet orkestrasyonu için LLM
    )
```

### 10. Dağıt (Deploy)

Ekipti veya akışı [CrewAI AMP](https://app.crewai.com)'ye dağıtın.

- **Kimlik Doğrulama**: CrewAI AMP'ye dağıtmak için kimliğinizin doğrulanmış olması gerekir.
  Aşağıdaki komutla giriş yapabilir veya hesap oluşturabilirsiniz:

  ```shell Terminal
  crewai login
  ```

- **Dağıtım Oluşturma**: Kimliğiniz doğrulandıktan sonra, yerel projenizin kökünden ekip veya akışınız için bir dağıtım oluşturabilirsiniz.
  ```shell Terminal
  crewai deploy create
  ```
  - Yerel proje yapılandırmanızı okur.
  - Yerel olarak bulunan ortam değişkenlerini (örneğin, `OPENAI_API_KEY`, `SERPER_API_KEY`) onaylamanız istenir. Bu değişkenler, Enterprise platformunda dağıtımla birlikte güvenli bir şekilde saklanacaktır. Hassas anahtarlarınızın yerel olarak doğru şekilde yapılandırıldığından (örneğin, bir `.env` dosyasında) bu komutu çalıştırmadan önce emin olun.

### 11. Kuruluş Yönetimi (Organization Management)

CrewAI AMP kuruluşlarınızı yönetin.

```shell Terminal
crewai org [KOMUT] [SEÇENEKLER]
```

#### Komutlar:

- `list`: Üye olduğunuz tüm kuruluşları listeler

```shell Terminal
crewai org list
```

- `current`: Şu anda etkin olan kuruluşunuzu gösterir

```shell Terminal
crewai org current
```

- `switch`: Belirli bir kuruluşa geçiş yapar

```shell Terminal
crewai org switch <kuruluş_kimliği>
```

Bu kuruluş yönetimi komutlarını kullanmak için CrewAI AMP'ye kimliğinizin doğrulanmış olması gerekir.

- **Dağıtım Oluşturma** (devam):

  - Dağıtımı ilgili uzak GitHub depolama alanına bağlar (genellikle bunu otomatik olarak algılar).

- **Ekip Dağıtımı**: Kimliğiniz doğrulandıktan sonra, ekip veya akışınızı CrewAI AMP'ye dağıtabilirsiniz.

  ```shell Terminal
  crewai deploy push
  ```

  - CrewAI AMP platformunda dağıtım sürecini başlatır.
  - Başarılı bir şekilde başlatıldıktan sonra, Dağıtım başarıyla oluşturuldu! mesajını ve benzersiz bir Dağıtım Kimliğini (UUID) yazdırır.

- **Dağıtım Durumu**: Dağıtımınızın durumunu aşağıdaki komutla kontrol edebilirsiniz:

  ```shell Terminal
  crewai deploy status
  ```

  Bu, en son dağıtım denemenizin en son durumunu (örneğin, `Crew için Görüntüler Oluşturuluyor`, `Dağıtım Kuyruğa Alındı`, `Çevrimiçi`) alır.

- **Dağıtım Günlükleri**: Dağıtımınızın günlüklerini aşağıdaki komutla kontrol edebilirsiniz:

  ```shell Terminal
  crewai deploy logs
  ```

  Bu, dağıtım günlüklerini terminalinize aktırır.

- **Dağıtımları Listele**: Tüm dağıtımlarınızı aşağıdaki komutla listeleyebilirsiniz:

  ```shell Terminal
  crewai deploy list
  ```

  Bu, tüm dağıtımlarınızı listeler.

- **Dağıtımı Sil**: Bir dağıtımı aşağıdaki komutla silebilirsiniz:

  ```shell Terminal
  crewai deploy remove
  ```

  Bu, dağıtımı CrewAI AMP platformundan siler.

- **Yardım Komutu**: CLI hakkında yardım almak için:
  ```shell Terminal
  crewai deploy --help
  ```
  Bu, CrewAI Dağıtım CLI yardım mesajını gösterir.

Adım adım bir gösteri için CLI'yı kullanarak ekibinizi [CrewAI AMP](http://app.crewai.com)'ye dağıtma eğitimi için bu videoyu izleyin.

<iframe
  className="w-full aspect-video rounded-xl"
  src="https://www.youtube.com/embed/3EqSV-CYDZA"
  title="CrewAI Deployment Guide"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
></iframe>

### 11. Giriş Yap (Login)

Güvenli bir cihaz kodu akışı kullanarak CrewAI AMP ile kimlik doğrulaması yapın (e-posta girişi gerektirmez).

```shell Terminal
crewai login
```

Olanlar:

- Terminalinizde bir doğrulama URL'si ve kısa bir kod görüntülenir
- Tarayıcınız doğrulama URL'sine yönlendirilir
- Kimlik doğrulamayı tamamlamak için kodu girin/onaylayın

Notlar:

- OAuth2 sağlayıcısı ve etki alanı `crewai config` aracılığıyla yapılandırılır (varsayılanlar `login.crewai.com` kullanır)
- Başarılı bir girişten sonra CLI ayrıca Araç Deposu'na otomatik olarak kimlik doğrulaması yapmaya çalışır
- Yapılandırmanızı sıfırlarsanız, tekrar kimlik doğrulaması yapmak için `crewai login` komutunu tekrar çalıştırın.

### 12. API Anahtarları

`crewai create crew` komutunu çalıştırırken CLI, seçebileceğiniz mevcut LLM sağlayıcılarının bir listesini ve ardından seçtiğiniz sağlayıcı için model seçimini gösterir.

Bir LLM sağlayıcısı ve model seçtikten sonra, API anahtarlarınızı girmeniz istenecektir.

#### Mevcut LLM Sağlayıcıları

CLI'nın önerdiği en popüler LLM sağlayıcılarından oluşan bir liste:

- OpenAI
- Groq
- Anthropic
- Google Gemini
- SambaNova

Bir sağlayıcıyı seçtiğinizde, CLI ardından bu sağlayıcı için mevcut modelleri gösterir ve API anahtarınızı girmenizi ister.

#### Diğer Seçenekler

"diğer"i seçerseniz, LiteLLM tarafından desteklenen sağlayıcılar listesinden seçim yapabilirsiniz.

Bir sağlayıcıyı seçtiğinizde, CLI Size bir Anahtar adı ve API anahtarını girmeniz için bir istemde bulunur.

Her sağlayıcının anahtar adları için bkz:

- [LiteLLM Sağlayıcıları](https://docs.litellm.ai/docs/providers)

### 13. Yapılandırma Yönetimi

CrewAI için CLI yapılandırma ayarlarını yönetin.

```shell Terminal
crewai config [KOMUT] [SEÇENEKLER]
```

#### Komutlar:

- `list`: Tüm CLI yapılandırma parametrelerini gösterir

```shell Terminal
crewai config list
```

- `set`: Bir CLI yapılandırma parametresini ayarlar

```shell Terminal
crewai config set <anahtar> <değer>
```

- `reset`: Tüm CLI yapılandırma parametrelerini varsayılan değerlere sıfırlar

```shell Terminal
crewai config reset
```

#### Mevcut Yapılandırma Parametreleri

- `enterprise_base_url`: CrewAI AMP örneğinin temel URL'si
- `oauth2_provider`: Kimlik doğrulama için kullanılan OAuth2 sağlayıcısı (örneğin, workos, okta, auth0)
- `oauth2_audience`: Genellikle API veya kaynağı tanımlamak için kullanılan OAuth2 kitle değeri
- `oauth2_client_id`: Sağlayıcı tarafından verilen OAuth2 istemci kimliği, kimlik doğrulama istekleri sırasında kullanılır
- `oauth2_domain`: Sağlayıcının etki alanı (örneğin, your-org.auth0.com) kimlik doğrulama için kullanılır

#### Örnekler

Mevcut yapılandırmayı görüntüle:

```shell Terminal
crewai config list
```

Örnek çıktı:
| Ayar | Değer | Açıklama |
| :------------------ | :----------------------- | :---------------------------------------------------------- |
| enterprise_base_url | https://app.crewai.com | CrewAI AMP örneğinin temel URL'si |
| org_name | Ayarlanmadı | Şu anda etkin olan kuruluşun adı |
| org_uuid | Ayarlanmadı | Şu anda etkin olan kuruluşun UUID'si |
| oauth2_provider | workos | OAuth2 sağlayıcısı (örneğin, workos, okta, auth0) |
| oauth2_audience | client_01YYY | Hedef API/kaynağı tanımlayan Kitle |
| oauth2_client_id | client_01XXX | Sağlayıcı tarafından verilen OAuth2 istemci kimliği |
| oauth2_domain | login.crewai.com | Sağlayıcının etki alanı (örneğin, your-org.auth0.com) |

Kurumsal temel URL'yi ayarlayın:

```shell Terminal
crewai config set enterprise_base_url https://my-enterprise.crewai.com
```

OAuth2 sağlayıcısını ayarlayın:

```shell Terminal
crewai config set oauth2_provider auth0
```

OAuth2 alanını ayarlayın:

```shell Terminal
crewai config set oauth2_domain my-company.auth0.com
```

Tüm yapılandırmayı varsayılanlara sıfırla:

```shell Terminal
crewai config reset
```

Yapılandırmayı sıfırladıktan sonra tekrar kimlik doğrulaması yapmak için `crewai login` komutunu tekrar çalıştırın.

### 14. İzleme Yönetimi (Trace Management)

Ekip ve akış yürütmeleriniz için izleme toplama tercihlerinizi yönetin.

```shell Terminal
crewai traces [KOMUT]
```

#### Komutlar:

- `enable`: Ekip/akış yürütmeleri için izleme toplamayı etkinleştirin

```shell Terminal
crewai traces enable
```

- `disable`: Ekip/akış yürütmeleri için izleme toplamayı devre dışı bırakın

```shell Terminal
crewai traces disable
```

- `status`: Mevcut izleme toplama durumunu gösterin

```shell Terminal
crewai traces status
```

#### İzlemenin Çalışma Şekli

İzleme toplama, aşağıdaki üç ayarın öncelik sırasına göre kontrol edilerek yönetilir:

1. **Kodda açık işaret** (en yüksek öncelik - hem etkinleştirebilir hem de devre dışı bırakabilir):

   ```python
   crew = Crew(agents=[...], tasks=[...], tracing=True)   # Her zaman etkinleştir
   crew = Crew(agents=[...], tasks=[...], tracing=False)  # Her zaman devre dışı bırak
   crew = Crew(agents=[...], tasks=[...])                 # Daha düşük öncelikli ayarları kontrol edin (varsayılan)
   ```

   - `tracing=True` izlemeyi **her zaman etkinleştirir** (her şeyi geçersiz kılar)
   - `tracing=False` izlemeyi **her zaman devre dışı bırakır** (her şeyi geçersiz kılar)
   - `tracing=None` veya atlanmışsa daha düşük öncelikli ayarlar kontrol edilir

2. **Ortam değişkeni** (ikinci öncelik):

   ```env
   CREWAI_TRACING_ENABLED=true
   ```

   - `tracing` `True` veya `False` olarak açıkça ayarlanmadığında yalnızca kontrol edilir
   - İzlemeyi etkinleştirmek için `true` veya `1` olarak ayarlanır

3. **Kullanıcı tercihi** (en düşük öncelik):
   ```shell Terminal
   crewai traces enable
   ```
   - `tracing` kodda ayarlanmadığında ve `CREWAI_TRACING_ENABLED` ayarlanmadığında yalnızca kontrol edilir
   - `crewai traces enable` komutunu çalıştırmak tek başına izlemeyi etkinleştirmek için yeterlidir

**İzlemeyi etkinleştirmek** için bu yöntemlerden herhangi birini kullanın:
- Kodu içinde `tracing=True` ayarlayın, VEYA
- `.env` dosyanıza `CREWAI_TRACING_ENABLED=true` ekleyin, VEYA
- `crewai traces enable` komutunu çalıştırın

**İzlemeyi devre dışı bırakmak** için bu yöntemlerden herhangi birini kullanın:

- Kodu içinde `tracing=False` ayarlayın (her şeyi geçersiz kılar), VEYA
- `CREWAI_TRACING_ENABLED` ortam değişkenini kaldırın veya `false` olarak ayarlayın, VEYA
- `crewai traces disable` komutunu çalıştırın

Daha düşük öncelikli ayarlar, daha yüksek öncelikli ayarları geçersiz kılar.

CrewAI CLI, projelerinize paket eklerken Araç Deposu'na otomatik olarak kimlik doğrulaması yapar. Sadece `crewai` komutunu herhangi bir `uv` komutundan önce ekleyerek kullanabilirsiniz. Örneğin: `crewai uv add requests`. Daha fazla bilgi için [Araç Deposu](https://docs.crewai.com/enterprise/features/tool-repository) belgelerine bakın.

Yapılandırma ayarları `~/.config/crewai/settings.json` dosyasında saklanır. Kuruluş adı ve UUID gibi bazı ayarlar salt okunurluktur ve kimlik doğrulama ve kuruluş komutları aracılığıyla yönetilir. Araç deposuyla ilgili ayarlar gizlidir ve kullanıcılar tarafından doğrudan değiştirilemez.