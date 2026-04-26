> ## Dokümantasyon İndeksi
> Tam dokümantasyon indeksini şurada bulabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazlasını keşfetmeden önce tüm kullanılabilir sayfaları keşfetmek için bu dosyayı kullanın.

# Kod Dokları RAG Araması

> `CodeDocsSearchTool`, kod belgelendirmesi içinde anlamsal aramalar için tasarlanmış güçlü bir RAG (Retrieval-Augmented Generation) aracıdır.

# `CodeDocsSearchTool`

<Note>
  **Deneysel**: Araçları iyileştirmek üzerinde çalışıyoruz, bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

CodeDocsSearchTool, kod belgelendirmesi içinde anlamsal aramalar için tasarlanmış güçlü bir RAG (Retrieval-Augmented Generation) aracıdır.
Kullanıcıların kod belgelendirmesi içinde belirli bilgileri veya konuları etkili bir şekilde bulmasını sağlar. Başlangıç sırasında bir `docs_url` sağlayarak,
araç aramasını bu özel belgelendirme sitesiyle sınırlandırır. Alternatif olarak, belirli bir `docs_url` olmadan,
yürütülmesi boyunca bilinen veya keşfedilen çok çeşitli kod belgelendirmesi genelinde araştırır, bu da çeşitli belgelendirme arama ihtiyaçları için çok yönlü hale getirir.

## Kurulum

CodeDocsSearchTool'u kullanmaya başlamak için, önce crewai_tools paketini pip aracılığıyla yükleyin:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

CodeDocsSearchTool'u kod belgelendirmesi içinde aramalar yapmak için aşağıdaki şekilde kullanın:

```python Code theme={null}
from crewai_tools import CodeDocsSearchTool

# URL'si bilinen veya yürütülmesi sırasında keşfedilen herhangi bir kod belgelendirmesi içeriğini arama yapma:
tool = CodeDocsSearchTool()

# VEYA

# Sunulan URL'yi sağlayarak belirli bir belgelendirme sitesinde aramanızı odaklandırmak için:
tool = CodeDocsSearchTool(docs_url='https://docs.example.com/reference')
```

<Note>
  '[https://docs.example.com/reference](https://docs.example.com/reference)' öğesini hedef belgelendirme URL'si ile ve 'Arama aracını nasıl kullanacağı' ile ilgili arama sorgunuzla değiştirin.
</Note>

## Argümanlar

Aşağıdaki parametreler `CodeDocsSearchTool`'ün davranışını özelleştirmek için kullanılabilir:

| Argüman       | Tür      | Açıklama                                                             |
| :------------ | :------- | :---------------------------------------------------------------------- |
| **docs_url** | `string` | *İsteğe bağlı*. Araştırılacak kod belgelendirmesinin URL'sini belirtir. |

## Özel model ve embeddings

Varsayılan olarak, araç hem embeddings hem de özetleme için OpenAI kullanır. Modeli özelleştirmek için, aşağıdaki gibi bir config sözlüğü kullanabilirsiniz:

```python Code theme={null}
tool = CodeDocsSearchTool(
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
