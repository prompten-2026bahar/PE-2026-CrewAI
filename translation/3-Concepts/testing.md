# Test Etme
CrewAI ekibinizin nasıl test edileceğini ve performansının nasıl değerlendirileceğini öğrenin.


## Genel Bakış

Test etme, geliştirme sürecinin önemli bir parçasıdır ve ekibinizin beklendiği gibi performans gösterdiğinden emin olmak için şarttır. crewAI ile yerleşik test yeteneklerini kullanarak ekibinizi kolayca test edebilir ve performansını değerlendirebilirsiniz.

### Test Özelliğini Kullanma

Ekibinizi test etmeyi kolaylaştırmak için `crewai test` CLI komutunu ekledik. Bu komut, ekibinizi belirtilen sayıda yineleme çalıştıracak ve ayrıntılı performans ölçümleri sağlayacaktır. Parametreler `n_iterations` ve `model`'dir; bunlar isteğe bağlıdır ve sırasıyla 2 ve `gpt-4o-mini` olarak varsayılan değerlere sahiptir. Şu anda yalnızca OpenAI sağlayıcısı mevcuttur.

```bash
crewai test
```

Daha fazla yineleme çalıştırmak veya farklı bir model kullanmak isterseniz, parametreleri şu şekilde belirtebilirsiniz:

```bash
crewai test --n_iterations 5 --model gpt-4o
```

veya kısa formlarını kullanarak:

```bash
crewai test -n 5 -m gpt-4o
```

`crewai test` komutunu çalıştırdığınızda, ekip belirtilen yineleme sayısını çalıştırılacak ve performans metrikleri çalıştırmanın sonunda görüntülenecektir.

Aşağıdaki metrikler açısından ekibin performansını gösteren bir puan tablosu sonunda gösterilecektir:

<center>**Görev Puanları (1-10 Daha yüksek daha iyidir)**</center>

| Görevler/Ekip/Agentlar | Çalışma 1 | Çalışma 2 | Ortalama Toplam | Agentlar                         | Ek Bilgi                  |
|:------------------|:-----:|:-----:|:----------:|:------------------------------:|:---------------------------------|
| Görev 1        |  9.0  |  9.5  |    **9.2**     | Professional Insights          |                                  |
|                    |       |       |            | Researcher                     |                                  |
| Görev 2        |  9.0  | 10.0  |    **9.5**     | Company Profile Investigator   |                                  |
| Görev 3        |  9.0  |  9.0  |    **9.0**     | Automation Insights            |                                  |
|                    |       |       |            | Specialist                     |                                  |
| Görev 4        |  9.0  |  9.0  |    **9.0**     | Final Report Compiler          | Automation Insights Specialist   |
| Ekip         | 9.00  | 9.38  |    **9.2**     |                                |                                  |
| Çalışma Süresi (s) |  126  |  145  |    **135**     |                                |                                  |

Yukarıdaki örnek, iki görevli ekibin iki çalıştırmasının test sonuçlarını göstermektedir; her görev ve ekip olarak tümü için ortalama toplam puanlar gösterilmektedir.