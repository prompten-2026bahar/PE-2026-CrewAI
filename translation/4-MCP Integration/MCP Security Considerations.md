> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# MCP Güvenlik Hususları

> MCP sunucularını CrewAI ajanlarınızla entegre ederken önemli güvenlik en iyi uygulamaları hakkında bilgi edinin.

## Genel Bakış

<Warning>
  MCP güvenliğinin en kritik yönü **güven** unsurudur. CrewAI ajanlarınızı **yalnızca** tamamen güvendiğiniz MCP sunucularına bağlamalısınız.
</Warning>

MCP (Model Context Protocol) sunucuları gibi harici servisleri CrewAI ajanlarınıza entegre ederken güvenlik en yüksek önceliktir.
MCP sunucuları, sundukları araçlara bağlı olarak kod çalıştırabilir, verilere erişebilir veya başka sistemlerle etkileşime girebilir.
Uygulamalarınızı ve verilerinizi korumak için etkilerini anlamak ve en iyi uygulamaları takip etmek kritik önem taşır.

### Riskler

* Ajanın çalıştığı makinede keyfi kod çalıştırabilirler (`Stdio` taşımasında özellikle, sunucu çalıştırılan komutu kontrol edebiliyorsa).
* Ajanınızdan veya ortamından hassas verileri açığa çıkarabilirler.
* Sizin adınıza yetkisiz API çağrıları yapmak dahil olmak üzere ajanınızın davranışını istenmeyen şekillerde manipüle edebilirler.
* Gelişmiş prompt injection teknikleriyle ajanınızın akıl yürütme sürecini ele geçirebilirler (aşağıya bakın).

### 1. MCP Sunucularına Güvenmek

<Warning>
  **Yalnızca güvendiğiniz MCP sunucularına bağlanın.**
</Warning>

`MCPServerAdapter` bileşenini bir MCP sunucusuna bağlanacak şekilde yapılandırmadan önce şunları bildiğinizden emin olun:

* **Sunucuyu kim işletiyor?** Bilinen ve güvenilir bir servis mi, yoksa sizin kontrolünüz altındaki dahili bir sunucu mu?
* **Hangi araçları sunuyor?** Araçların yeteneklerini anlayın. Bir saldırgan kontrolü ele geçirirse veya sunucunun kendisi kötü niyetliyse bunlar kötüye kullanılabilir mi?
* **Hangi verilere erişiyor veya onları işliyor?** MCP sunucusuna gönderilebilecek ya da onun tarafından işlenebilecek hassas bilgilerin farkında olun.

Özellikle ajanlarınız hassas görevler veya verilerle çalışıyorsa, bilinmeyen ya da doğrulanmamış MCP sunucularına bağlanmaktan kaçının.

### 2. Araç Meta Verisi Üzerinden Prompt Injection: "Model Control Protocol" Riski

Önemli ve sinsi bir risk, araç meta verisi üzerinden prompt injection yapılabilmesidir. Bunun işleyişi şöyledir:

1. CrewAI ajanınız bir MCP sunucusuna bağlandığında genellikle mevcut araçların listesini ister.
2. MCP sunucusu her araç için adı, açıklaması ve parametre açıklamaları dahil olmak üzere meta veri döndürür.
3. Ajanınızın altında çalışan Dil Modeli (LLM), araçların nasıl ve ne zaman kullanılacağını anlamak için bu meta veriyi kullanır. Bu meta veri çoğu zaman LLM'in sistem prompt'una veya bağlamına dahil edilir.
4. Kötü niyetli bir MCP sunucusu, araç meta verisini (isimler, açıklamalar) gizli veya açık talimatlar içerecek şekilde hazırlayabilir. Bu talimatlar bir prompt injection görevi görerek LLM'inize belirli şekilde davranmasını, hassas bilgi açığa çıkarmasını veya kötü amaçlı eylemler gerçekleştirmesini söyleyebilir.

**Kritik olarak, bu saldırı ajanınız o araçlardan herhangi birini açıkça *kullanmaya* hiç karar vermese bile yalnızca kötü niyetli bir sunucuya bağlanıp araç listesini almakla gerçekleşebilir.** Kötü niyetli meta veriye maruz kalmak tek başına ajan davranışını tehlikeye atmaya yeterli olabilir.

**Azaltma Yöntemi:**

* **Güvenilmeyen Sunuculara Karşı Aşırı Dikkat:** Tekrar vurgulayalım: *Tam olarak güvenmediğiniz MCP sunucularına bağlanmayın.* Meta veri enjeksiyonu riski bunu hayati hale getirir.

### Stdio Taşıması Güvenliği

Stdio (Standart Girdi/Çıktı) taşıması genellikle CrewAI uygulamanızla aynı makinede çalışan yerel MCP sunucuları için kullanılır.

* **Süreç Yalıtımı**: Varsayılan olarak ağ maruziyeti içermediği için genelde daha güvenli olsa da, `StdioServerParameters` tarafından çalıştırılan betiğin veya komutun güvenilir bir kaynaktan geldiğinden ve uygun dosya sistemi izinlerine sahip olduğundan emin olun. Kötü niyetli bir Stdio sunucu betiği yine de yerel sisteminize zarar verebilir.
* **Girdi Temizleme**: Stdio sunucu betiğiniz ajan etkileşimlerinden türetilen karmaşık girdiler alıyorsa, komut enjeksiyonu veya betik mantığı içindeki diğer açıklara karşı bunların betiğin kendisi tarafından temizlendiğinden emin olun.
* **Kaynak Sınırları**: Yerel bir Stdio sunucu sürecinin yerel kaynakları (CPU, bellek) tüketeceğini unutmayın. Düzgün davrandığından ve sistem kaynaklarını tüketmeyeceğinden emin olun.

### Confused Deputy Saldırıları

[Confused Deputy Problem](https://en.wikipedia.org/wiki/Confused_deputy_problem), özellikle bir MCP sunucusu yetkilendirme için OAuth 2.0 kullanan diğer üçüncü taraf servislere (ör. Google Calendar, GitHub) vekil olarak davrandığında MCP entegrasyonlarında ortaya çıkabilen klasik bir güvenlik açığıdır.

**Senaryo:**

1. Bir MCP sunucusu (`MCP-Proxy` diyelim) ajanınızın `ThirdPartyAPI` ile etkileşime girmesine izin verir.
2. `MCP-Proxy`, `ThirdPartyAPI` yetkilendirme sunucusuyla konuşurken kendi tek ve sabit `client_id` değerini kullanır.
3. Siz kullanıcı olarak `MCP-Proxy` bileşenine `ThirdPartyAPI`'ye sizin adınıza erişme yetkisini meşru biçimde verirsiniz. Bu sırada `ThirdPartyAPI` yetkilendirme sunucusu, tarayıcınıza `MCP-Proxy` için verdiğiniz onayı gösteren bir çerez bırakabilir.
4. Bir saldırgan kötü amaçlı bir bağlantı hazırlar. Bu bağlantı `MCP-Proxy` ile bir OAuth akışı başlatır, ancak `ThirdPartyAPI` yetkilendirme sunucusunu kandıracak şekilde tasarlanmıştır.
5. Bu bağlantıya tıklarsanız ve `ThirdPartyAPI` yetkilendirme sunucusu `MCP-Proxy` için mevcut onay çerezinizi görürse, sizden yeniden onay istemeyi *atlayabilir*.
6. Ardından `MCP-Proxy`, (`ThirdPartyAPI` için) bir yetkilendirme kodunu saldırgana iletmeye veya saldırganın sizi `MCP-Proxy`'ye karşı taklit etmek için kullanabileceği bir MCP yetkilendirme kodunu aktarmaya kandırılabilir.

**Azaltma Yöntemi (Temelde MCP Sunucu Geliştiricileri İçin):**

* Alt servisler için sabit istemci kimlikleri kullanan MCP proxy sunucuları, üçüncü taraf servisle OAuth akışı başlatmadan *önce* kendilerine bağlanan *her istemci uygulama veya ajan* için açık kullanıcı onayı **almalıdır**. Bu, `MCP-Proxy` bileşeninin kendisinin bir onay ekranı göstermesi gerektiği anlamına gelir.

**CrewAI Kullanıcısı İçin Anlamı:**

* Bir MCP sunucusu sizi birden fazla OAuth kimlik doğrulamasına yönlendiriyorsa, özellikle bu beklenmedik görünüyorsa veya istenen izinler aşırı genişse dikkatli olun.
* Kendi kimliğini, vekil olabileceği üçüncü taraf servislerden net şekilde ayıran MCP sunucularını tercih edin.

### Uzak Taşıma Güvenliği (SSE ve Streamable HTTP)

Server-Sent Events (SSE) veya Streamable HTTP aracılığıyla uzak MCP sunucularına bağlanırken standart web güvenliği uygulamaları zorunludur.

### SSE Güvenlik Hususları

### a. DNS Rebinding Saldırıları (Özellikle SSE için)

<Critical>
  **DNS Rebinding Saldırılarına karşı koruma sağlayın.**
</Critical>

DNS rebinding, saldırganın kontrol ettiği bir web sitesinin aynı kaynak ilkesini aşmasına ve kullanıcının yerel ağındaki (`localhost` gibi) ya da intranetindeki sunuculara istek göndermesine olanak tanır. Bu, özellikle bir MCP sunucusunu yerelde (ör. geliştirme için) çalıştırıyorsanız ve tarayıcı benzeri bir ortamda bir ajanınız varsa (tipik CrewAI backend kurulumlarında daha az yaygındır) veya MCP sunucusu dahili bir ağ üzerindeyse oldukça risklidir.

**MCP Sunucusu Uygulayıcıları İçin Azaltma Stratejileri:**

* **`Origin` ve `Host` Başlıklarını Doğrulayın**: MCP sunucuları (özellikle SSE kullananlar), isteklerin beklenen alan adlarından/istemcilerden geldiğini doğrulamak için `Origin` ve/veya `Host` HTTP başlıklarını kontrol etmelidir.
* **`localhost` (127.0.0.1) Üzerine Bağlanın**: Geliştirme için MCP sunucularını yerelde çalıştırırken `0.0.0.0` yerine `127.0.0.1` üzerine bağlayın. Bu, ağdaki diğer makinelerden erişilmelerini engeller.
* **Kimlik Doğrulama**: Halka açık anonim erişim amaçlanmıyorsa MCP sunucunuza yapılan tüm bağlantılar için kimlik doğrulama zorunlu olsun.

### b. HTTPS Kullanın

* **Aktarım Halindeki Veriyi Şifreleyin**: Uzak MCP sunucularının URL'leri için her zaman HTTPS (HTTP Secure) kullanın. Bu, CrewAI uygulamanız ile MCP sunucusu arasındaki iletişimi şifreleyerek dinleme ve aradaki adam saldırılarına karşı korur. `MCPServerAdapter`, URL içinde verilen şemaya (`http` veya `https`) uyacaktır.

### c. Token Passthrough (Kaçınılması Gereken Desen)

Bu öncelikle MCP sunucu geliştiricilerini ilgilendirir, ancak bunu anlamak güvenli sunucular seçmenize yardımcı olur.

"Token passthrough", bir MCP sunucusunun CrewAI ajanınızdan aldığı erişim jetonunu (bu jeton *farklı* bir servis, örneğin `ServiceA` için olabilir) uygun doğrulama yapmadan başka bir alt API'ye (`ServiceB`) doğrudan iletmesidir. Özellikle `ServiceB` (veya MCP sunucusunun kendisi), yalnızca açıkça *kendileri için* verilmiş jetonları kabul etmelidir; yani jetondaki `audience` alanı sunucu/servis ile eşleşmelidir.

**Riskler:**

* MCP sunucusundaki veya alt API'deki güvenlik kontrollerini (oran sınırlama ya da ince taneli izinler gibi) atlatır.
* Denetim kayıtlarını ve hesap verebilirliği bozar.
* Çalınmış jetonların kötüye kullanılmasına izin verir.

**Azaltma Yöntemi (MCP Sunucu Geliştiricileri İçin):**

* MCP sunucuları, açıkça kendileri için verilmemiş jetonları **KABUL ETMEMELİDİR**. Jetonun `audience` alanını doğrulamalıdırlar.

**CrewAI Kullanıcısı İçin Anlamı:**

* Kullanıcı tarafından doğrudan kontrol edilemese de bu, güvenlik en iyi uygulamalarına uyan iyi tasarlanmış MCP sunucularına bağlanmanın önemini gösterir.

#### Kimlik Doğrulama ve Yetkilendirme

* **Kimliği Doğrulayın**: MCP sunucusu hassas araçlar veya özel verilere erişim sağlıyorsa, istemcinin (CrewAI uygulamanızın) kimliğini doğrulamak için güçlü kimlik doğrulama mekanizmaları uygulaması ZORUNLUDUR. Bu, API anahtarları, OAuth jetonları veya diğer standart yöntemleri içerebilir.
* **En Az Ayrıcalık İlkesi**: `MCPServerAdapter` tarafından kullanılan kimlik bilgilerinin (varsa) yalnızca gerekli araçlara erişmek için gereken izinlere sahip olduğundan emin olun.

### d. Girdi Doğrulama ve Temizleme

* **Girdi Doğrulama Kritiktir**: MCP sunucuları, ajanlardan alınan tüm girdileri bunları işlemeden ya da araçlara iletmeden *önce* sıkı şekilde doğrulamalıdır. Bu, birçok yaygın güvenlik açığına karşı birincil savunmadır:
  * **Komut Enjeksiyonu:** Bir araç, girdiye göre kabuk komutları, SQL sorguları veya başka yorumlanan dil ifadeleri oluşturuyorsa, kötü amaçlı komutların eklenip çalıştırılmasını önlemek için sunucu bu girdiyi titizlikle temizlemelidir.
  * **Yol Geçişi (Path Traversal):** Bir araç girdi parametrelerine göre dosyalara erişiyorsa, yetkisiz dosya ve dizinlere erişimi önlemek için sunucu bu yolları doğrulamalı ve temizlemelidir (ör. `../` dizilerini engelleyerek).
  * **Veri Türü ve Aralık Kontrolleri:** Sunucular, giriş verisinin beklenen veri türlerine (ör. string, number, boolean) uyduğundan ve kabul edilebilir aralıklarda olduğundan veya tanımlanmış biçimlere (ör. URL'ler için regex) uyduğundan emin olmalıdır.
  * **JSON Schema Doğrulaması:** Tüm araç parametreleri, tanımlanmış JSON şemalarına karşı sıkı biçimde doğrulanmalıdır. Bu, bozuk isteklerin erken yakalanmasına yardımcı olur.
* **İstemci Tarafı Farkındalığı**: Sunucu tarafı doğrulama birincil öneme sahip olsa da, CrewAI kullanıcısı olarak ajanlarınızın MCP araçlarına göndermek üzere tasarlandığı verilerin farkında olun; özellikle daha az güvenilen veya yeni MCP sunucularıyla etkileşim kurarken.

### e. Oran Sınırlama ve Kaynak Yönetimi

* **Kötüye Kullanımı Önleyin**: MCP sunucuları, ister kasıtlı (Hizmet Reddi saldırıları) ister kazara (ör. yanlış yapılandırılmış bir ajan çok fazla istek gönderiyorsa) olsun, kötüye kullanımı önlemek için oran sınırlama uygulamalıdır.
* **İstemci Tarafı Yeniden Denemeler**: Geçici ağ sorunları veya sunucu oran sınırları bekleniyorsa CrewAI görevlerinizde makul yeniden deneme mantığı uygulayın; ancak sunucu yükünü artırabilecek agresif tekrar denemelerden kaçının.

## 4. Güvenli MCP Sunucusu Uygulama Tavsiyeleri (Geliştiriciler İçin)

CrewAI ajanlarının bağlanabileceği bir MCP sunucusu geliştiriyorsanız, yukarıdaki noktalara ek olarak şu en iyi uygulamaları değerlendirin:

* **Güvenli Kodlama Uygulamalarını İzleyin**: Seçtiğiniz dil ve çatı için standart güvenli kodlama ilkelerine uyun (ör. OWASP Top 10).
* **En Az Ayrıcalık İlkesi**: MCP sunucusunu çalıştıran sürecin (özellikle `Stdio` için) yalnızca gereken en düşük izinlere sahip olduğundan emin olun. Araçların kendileri de işlevlerini yerine getirmek için gerekli olan en az ayrıcalıkla çalışmalıdır.
* **Bağımlılık Yönetimi**: Bilinen açıkları yamamak için işletim sistemi paketleri, çalışma zamanları ve üçüncü taraf kütüphaneler dahil tüm sunucu tarafı bağımlılıklarını güncel tutun. Açıklı bağımlılıkları taramak için araçlar kullanın.
* **Güvenli Varsayılanlar**: Sunucunuzu ve araçlarını varsayılan olarak güvenli olacak şekilde tasarlayın. Örneğin riskli olabilecek özellikler varsayılan olarak kapalı olmalı veya açık uyarılarla birlikte açık onay gerektirmelidir.
* **Araçlar için Erişim Kontrolü**: Özellikle güçlü, hassas veya maliyet doğuran araçlara hangi kimliği doğrulanmış ve yetkilendirilmiş ajanların ya da kullanıcıların erişebileceğini kontrol etmek için sağlam mekanizmalar uygulayın.
* **Güvenli Hata Yönetimi**: Sunucular, istemciye ayrıntılı dahili hata mesajları, yığın izleri veya hata ayıklama bilgileri göstermemelidir; çünkü bunlar iç işleyişi veya olası açıkları ortaya çıkarabilir. Tanılama için hataları sunucu tarafında kapsamlı şekilde kaydedin.
* **Kapsamlı Günlükleme ve İzleme**: Güvenlikle ilgili olayların (ör. kimlik doğrulama girişimleri, araç çağrıları, hatalar, yetkilendirme değişiklikleri) ayrıntılı günlüklemesini uygulayın. Bu günlükleri şüpheli etkinlik veya kötüye kullanım desenleri açısından izleyin.
* **MCP Yetkilendirme Şartnamesine Uyum**: Kimlik doğrulama ve yetkilendirme uyguluyorsanız [MCP Authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization) ile ilgili [OAuth 2.0 security best practices](https://datatracker.ietf.org/doc/html/rfc9700) belgelerine sıkı şekilde uyun.
* **Düzenli Güvenlik Denetimleri**: MCP sunucunuz hassas verileri işliyorsa, kritik işlemler yapıyorsa veya herkese açıksa, yetkin profesyoneller tarafından düzenli güvenlik denetimleri yaptırmayı değerlendirin.

## 5. Ek Okumalar

MCP güvenliği hakkında daha ayrıntılı bilgi için resmi dokümantasyona bakın:

* **[MCP Transport Security](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations)**

Bu güvenlik hususlarını anlayıp en iyi uygulamaları hayata geçirerek MCP sunucularının gücünden CrewAI projelerinizde güvenli şekilde yararlanabilirsiniz.
Bunlar hiçbir şekilde eksiksiz bir liste değildir, ancak en yaygın ve en kritik güvenlik endişelerini kapsar.
Tehditler gelişmeye devam edecektir; bu nedenle bilgili kalmak ve güvenlik önlemlerinizi buna göre uyarlamak önemlidir.
