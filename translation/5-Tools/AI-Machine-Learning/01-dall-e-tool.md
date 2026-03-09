# DALL-E Aracı

> `DallETool`, metinsel açıklamalardan görüntüler oluşturmak için tasarlanmış güçlü bir araçtır.

# `DallETool`

## Açıklama

Bu araç, ajana DALL-E modelini kullanarak görüntüler oluşturma yeteneği kazandırmak için kullanılır. Metinsel açıklamalardan görüntüler üreten transforver tabanlı bir modeldir. Bu araç, ajanın kullanıcı tarafından sağlanan metin girişine dayanarak görüntüler oluşturmasına olanak tanır.

## Kurulum

`crewai_tools` paketini yükleyin:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Örnek

Bu aracı kullanırken, metnin bizzat ajan tarafından oluşturulması gerektiğini unutmayın. Metin, oluşturmak istediğiniz görüntünün bir açıklaması olmalıdır.

```python Code theme={null}
from crewai_tools import DallETool

# Ajan tanımı
Agent(
    ...
    tools=[DallETool()],
)
```

Gerekirse, DALL-E model parametrelerini `DallETool` sınıfına argüman olarak geçirerek ince ayar yapabilirsiniz. Örneğin:

```python Code theme={null}
from crewai_tools import DallETool

dalle_tool = DallETool(model="dall-e-3",
                       size="1024x1024",
                       quality="standard",
                       n=1)

Agent(
    ...
    tools=[dalle_tool]
)
```

Parametreler, OpenAI API'sinin `client.images.generate` metoduna dayanmaktadır. Parametreler hakkında daha fazla bilgi için lütfen [OpenAI API dökümantasyonuna](https://platform.openai.com/docs/guides/images/introduction?lang=python) bakın.
