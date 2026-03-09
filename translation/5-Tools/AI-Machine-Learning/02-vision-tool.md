# Vision (Görüntü İşleme) Aracı

> `VisionTool`, görüntülerden metin ayıklamak için tasarlanmıştır.

# `VisionTool`

## Açıklama

Bu araç, görüntülerden metin ayıklamak için kullanılır. Bir ajana aktarıldığında, görüntüden metni çıkararak yanıt, rapor veya başka bir çıktı oluşturmak için kullanacaktır. Görüntünün URL'si veya yolu (PATH) ajana iletilmelidir.

## Kurulum

`crewai_tools` paketini yükleyin:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Kullanım

VisionTool'u kullanmak için, `OPENAI_API_KEY` ortam değişkeninde (environment variable) OpenAI API anahtarınız ayarlanmış olmalıdır.

```python Code theme={null}
from crewai_tools import VisionTool

vision_tool = VisionTool()

@agent
def researcher(self) -> Agent:
    '''
    Bu ajan, görüntülerden metin ayıklamak için VisionTool'u kullanır.
    '''
    return Agent(
        config=self.agents_config["researcher"],
        allow_delegation=False,
        tools=[vision_tool]
    )
```

## Argümanlar

VisionTool aşağıdaki argümanları gerektirir:

| Argüman              | Tip      | Açıklama                                                                          |
| :------------------- | :------- | :-------------------------------------------------------------------------------- |
| **image\_path\_url** | `string` | **Zorunlu**. Metnin çıkarılacağı görüntü dosyasının yolu veya URL'si.             |
