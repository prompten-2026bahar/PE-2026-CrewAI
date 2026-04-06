> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Dosya Okuma

> `FileReadTool`, yerel dosya sistemindeki dosyaları okumak için tasarlanmıştır.

## Genel Bakış

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

FileReadTool kavramsal olarak, crewai\_tools paketi içindeki dosya okuma ve içerik alma işlemlerini kolaylaştırmaya yönelik bir işlevler kümesini temsil eder.
Bu küme; toplu metin dosyalarını işleme, çalışma zamanı yapılandırma dosyalarını okuma ve analiz için veri içe aktarma araçlarını içerir.
`.txt`, `.csv`, `.json` ve daha fazlası gibi çeşitli metin tabanlı dosya biçimlerini destekler. Dosya türüne bağlı olarak, bu küme özel işlevler sunar;
örneğin kullanım kolaylığı için JSON içeriğini bir Python sözlüğüne dönüştürmek gibi.

## Kurulum

FileReadTool'a atfedilen işlevleri kullanmak için crewai\_tools paketini kurun:

```shell  theme={null}
pip install 'crewai[tools]'
```

## Kullanım Örneği

FileReadTool ile başlamak için:

```python Code theme={null}
from crewai_tools import FileReadTool

# Aracı, ajanın bildiği veya yolunu öğrendiği
# herhangi bir dosyayı okuyabilecek şekilde başlat
file_read_tool = FileReadTool()

# OR

# Aracı belirli bir dosya yoluyla başlat;
# böylece ajan yalnızca belirtilen dosyanın içeriğini okuyabilsin
file_read_tool = FileReadTool(file_path='path/to/your/file.txt')
```

## Argümanlar

* `file_path`: Okumak istediğiniz dosyanın yolu. Hem mutlak hem göreli yolları kabul eder. Dosyanın mevcut olduğundan ve erişmek için gerekli izinlere sahip olduğunuzdan emin olun.


Built with [Mintlify](https://mintlify.com).
