> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Dizin Okuma

> `DirectoryReadTool`, dizin içeriğinin kapsamlı bir listesini sunmak için tasarlanmış güçlü bir yardımcı araçtır.

# `DirectoryReadTool`

<Note>
  Araçları geliştirmeye devam ediyoruz; bu nedenle gelecekte beklenmeyen davranışlar veya değişiklikler olabilir.
</Note>

## Açıklama

DirectoryReadTool, dizin içeriğinin kapsamlı bir listesini sunmak için tasarlanmış güçlü bir yardımcı araçtır.
Belirtilen dizin içinde özyinelemeli olarak gezebilir ve alt dizinlerde bulunanlar dahil tüm dosyaların ayrıntılı bir dökümünü kullanıcıya sunar.
Bu araç, dizin yapılarının eksiksiz envanterini çıkarmayı veya dizinlerdeki dosya organizasyonunu doğrulamayı gerektiren görevler için kritik öneme sahiptir.

## Kurulum

DirectoryReadTool'u projenizde kullanmak için `crewai_tools` paketini yükleyin. Bu paket henüz ortamınızda yoksa aşağıdaki komutla pip üzerinden kurabilirsiniz:

```shell  theme={null}
pip install 'crewai[tools]'
```

Bu komut, `crewai_tools` paketinin en güncel sürümünü kurar ve diğer yardımcı araçların yanı sıra DirectoryReadTool'a erişim sağlar.

## Örnek

DirectoryReadTool'u kullanmak oldukça basittir. Aşağıdaki kod parçası, aracı nasıl kuracağınızı ve belirtilen bir dizinin içeriğini listelemek için nasıl kullanacağınızı gösterir:

```python Code theme={null}
from crewai_tools import DirectoryReadTool

# Aracı, ajan çalışması sırasında öğrendiği
# herhangi bir dizinin içeriğini okuyabilecek şekilde başlat
tool = DirectoryReadTool()

# OR

# Aracı belirli bir dizinle başlat;
# böylece ajan yalnızca belirtilen dizinin içeriğini okuyabilsin
tool = DirectoryReadTool(directory='/path/to/your/directory')
```

## Argümanlar

`DirectoryReadTool` davranışını özelleştirmek için aşağıdaki parametreler kullanılabilir:

| Argument      | Type     | Description                                                                                                                                                                                                   |
| :------------ | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **directory** | `string` | *İsteğe bağlı*. İçeriğini listelemek istediğiniz dizinin yolunu belirtir. Hem mutlak hem göreli yolları kabul eder ve aracı içerik listeleme için istenen dizine yönlendirir. |
