# Kodlama Araçları
Kodlama ajanlarını ve IDE'leri CrewAI projelerinizde yönlendirmek için AGENTS.md'yi kullanın.

## Neden AGENTS.md

`AGENTS.md`, kodlama ajanlarına tutarlı, proje özelinde rehberlik sağlayan hafif, repo'da yerel bir talimat dosyasındır. Proje kök dizininde bulundurun ve yardımcıların nasıl çalışmasını istediğiniz için tek kaynak olarak kabul edin: gelenekler, komutlar, mimari notları ve kısıtlamalar.

## CLI ile Proje Oluşturma

Projenizi oluşturmak için CrewAI CLI'yı kullanın, ardından `AGENTS.md` otomatik olarak köke eklenir.

```bash
# Crew
crewai create crew my_crew

# Flow
crewai create flow my_flow

# Tool repository
crewai tool create my_tool
```

## Araç Kurulumu: Ajanları AGENTS.md'ye Yönlendirme

### Codex

Codex, depo’nuzda bulunan `AGENTS.md` dosyalarıyla yönlendirilebilir. Sürekli proje bağlamı sağlamak için bunları kullanın, örneğin gelenekler, komutlar ve iş akışı beklentileri.

### Claude Code

Claude Code, proje belleğini `CLAUDE.md` içinde saklar. Bunu `/init` ile başlatabilir ve `/memory` ile düzenleyebilirsiniz. Claude Code ayrıca `CLAUDE.md` içinde import'ları da destekler, böylece tekrarlamaktan kaçınarak paylaşılan talimatları çekmek için tek bir satır ekleyebilirsiniz: `@AGENTS.md`.

Basitçe şunu kullanabilirsiniz:

```bash
mv AGENTS.md CLAUDE.md
```

### Gemini CLI ve Google Antigravity

Gemini CLI ve Antigravity, depo kök dizininden ve üst dizinlerden bir proje bağlam dosyası (varsayılan: `GEMINI.md`) yükler. Bunu `context.fileName`'ı Gemini CLI ayarlarınızda `AGENTS.md` olarak (veya ek olarak) ayarlayarak `AGENTS.md` okumasını sağlayabilirsiniz. Örneğin, yalnızca `AGENTS.md` olarak ayarlayın veya her aracın biçimini korumak için hem `AGENTS.md` hem de `GEMINI.md`'yi dahil edin.

Basitçe şunu kullanabilirsiniz:

```bash
mv AGENTS.md GEMINI.md
```

### Cursor

Cursor, `AGENTS.md`'yi bir proje talimat dosyası olarak destekler. Cursor'un kodlama asistanı için rehberlik sağlamak üzere proje kök dizininde yerleştirin.

### Windsurf

Claude Code, Windsurf ile resmi bir entegrasyon sağlar. Windsurf içinde Claude Code kullanıyorsanız, yukarıdaki Claude Code rehberliğini izleyin ve `CLAUDE.md`'den `AGENTS.md`'yi içe aktarın.

Windsurf'ün yerel asistanını kullanıyorsanız, proje kurallarını veya talimatlar özelliğini (varsa) `AGENTS.md`'den okuyacak şekilde yapılandırın veya içeriği doğrudan yapıştırın.