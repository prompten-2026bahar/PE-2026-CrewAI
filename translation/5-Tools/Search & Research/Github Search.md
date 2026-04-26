> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Github Araması

> `GithubSearchTool`, web sitelerini aramak ve bunları temiz markdown veya yapılandırılmış verilere dönüştürmek için tasarlanmıştır.

# `GithubSearchTool`

<Note>
  Araçları iyileştirmek üzerinde çalışıyoruz, bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

GithubSearchTool, GitHub depoları içinde anlamsal aramalar yapmak için özel olarak tasarlanmış bir Retrieval-Augmented Generation (RAG) aracıdır. Gelişmiş anlamsal arama yeteneklerini kullanarak, kodu, pull request'leri, sorunları ve depoları inceleyerek, geliştiriciler, araştırmacılar veya GitHub'dan hassas bilgi gereken herkes için gerekli bir araç haline gelmektedir.

## Kurulum

GithubSearchTool'u kullanmak için, önce crewai_tools paketinin Python ortamınızda yüklü olduğundan emin olun:

```shell  theme={null}
pip install 'crewai[tools]'
```

Bu komut, GithubSearchTool'u çalıştırmak için gerekli paketi ve crewai_tools paketine dahil olan diğer araçları da yükler.

[https://github.com/settings/tokens](https://github.com/settings/tokens) adresinde (Geliştirici ayarları → İnce taneli tokenler veya klasik tokenler) GitHub Kişisel Erişim Jetonu alın.

## Örnek

Here’s how you can use the GithubSearchTool to perform semantic searches within a GitHub repository:

```python Code theme={null}
from crewai_tools import GithubSearchTool

# Aracı belirli bir GitHub deposu içinde anlamsal aramalar yapmak için başlat
tool = GithubSearchTool(
	github_repo='https://github.com/example/repo',
	gh_token='your_github_personal_access_token',
	content_types=['code', 'issue'] # Seçenekler: code, repo, pr, issue
)

# VEYA

# Aracı belirli bir GitHub deposu içinde anlamsal aramalar yapmak için başlat, so the agent can search any repository if it learns about during its execution
tool = GithubSearchTool(
	gh_token='your_github_personal_access_token',
	content_types=['code', 'issue'] # Seçenekler: code, repo, pr, issue
)
```

## Argümanlar

* `github_repo` : Aramanın yapılacağı GitHub deposunun URL'si. Bu zorunlu bir alandır ve arama için hedef depoyu belirtir.
* `gh_token` : Kimlik doğrulama için gerekli GitHub Kişisel Erişim Token'ı (PAT). GitHub hesap ayarlarınızda Geliştirici Ayarları > Kişisel Erişim Token'ları altında bir tane oluşturabilirsiniz.
* `content_types` : Aramanıza dahil etmek için içerik türlerini belirtir. Aşağıdaki seçeneklerden bir içerik türleri listesi sağlamanız gerekir: `code` kod içinde arama yapmak için,
  `repo` deponun genel bilgilerinde arama yapmak için, `pr` çekme istekleri içinde arama yapmak için ve `issue` sorunlar içinde arama yapmak için.
  Bu alan zorunludur ve arama işlemini GitHub deposu içinde belirli içerik türlerine uyarlanmasını sağlar.

## Özel model ve yerleştirmeler

Varsayılan olarak, araç hem yerleştirmeler hem de özetleme için OpenAI kullanır. Modeli özelleştirmek için aşağıdaki gibi bir yapılandırma sözlüğü kullanabilirsiniz:

```python Code theme={null}
tool = GithubSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # veya google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google-generativeai", # veya openai, ollama, ...
            config=dict(
                model_name="gemini-embedding-001",
                task_type="RETRIEVAL_DOCUMENT",
                # title="Embeddings",
            ),
        ),
    )
)
```
