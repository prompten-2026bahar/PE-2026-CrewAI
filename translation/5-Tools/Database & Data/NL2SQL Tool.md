> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# NL2SQL Aracı

> `NL2SQLTool`, doğal dili SQL sorgularına dönüştürmek için tasarlanmıştır.

## Genel Bakış

Bu araç, doğal dili SQL sorgularına dönüştürmek için kullanılır. Ajana verildiğinde sorgular üretir ve ardından veritabanıyla etkileşim kurmak için bunları kullanır.

Bu; bir ajanın hedefe göre veritabanına erişip bilgi getirmesi ve ardından bu bilgiyi yanıt, rapor veya başka bir çıktı üretmek için kullanması gibi çoklu iş akışlarını mümkün kılar.
Bunun yanında ajanın hedefi doğrultusunda veritabanını güncelleme yeteneği de sağlar.

**Dikkat**: Ajanın bir Read-Replica'ya erişimi olduğundan veya ajanın veritabanında insert/update sorguları çalıştırmasının kabul edilebilir olduğundan emin olun.

## Güvenlik Modeli

`NL2SQLTool`, çalıştırma yeteneğine sahip bir araçtır. Model tarafından üretilen SQL'i doğrudan yapılandırılmış veritabanı bağlantısı üzerinde çalıştırır.

Bu, riskin dağıtım tercihlerinize bağlı olduğu anlamına gelir:

* `db_uri` içinde hangi kimlik bilgilerini verdiğiniz
* Güvenilmeyen girdinin prompt'ları etkileyip etkileyemeyeceği
* Çalıştırma öncesinde araç çağrısı koruma kuralları ekleyip eklemediğiniz

Güvenilmeyen girdiyi bu aracı kullanan ajanlara yönlendiriyorsanız bunu yüksek riskli bir entegrasyon olarak değerlendirin.

## Güçlendirme Önerileri

Prodüksiyonda aşağıdakilerin tamamını kullanın:

* Mümkün olduğunda salt okunur bir veritabanı kullanıcısı kullanın
* Analitik/getirme iş yükleri için bir read replica tercih edin
* En az ayrıcalık verin (superuser/admin rolleri yok, dosya/sistem düzeyi yetenekler yok)
* Veritabanı tarafı kaynak sınırları uygulayın (statement timeout, lock timeout, cost/row limitleri)
* İzin verilen sorgu kalıplarını zorlamak için `before_tool_call` kancaları ekleyin
* Yıkıcı ifadeler için sorgu günlükleme ve uyarı mekanizmalarını etkinleştirin

## Gereksinimler

* SqlAlchemy
* Any DB compatible library (e.g. psycopg2, mysql-connector-python)

## Kurulum

crewai\_tools paketini kurun

```shell  theme={null}
pip install 'crewai[tools]'
```

## Kullanım

NL2SQLTool'u kullanmak için veritabanı URI'sini araca vermeniz gerekir. URI şu biçimde olmalıdır: `dialect+driver://username:password@host:port/database`.

```python Code theme={null}
from crewai_tools import NL2SQLTool

# Bu örneği PostgreSQL ile çalıştırmak için psycopg2 kuruldu
nl2sql = NL2SQLTool(db_uri="postgresql://example@localhost:5432/test_db")

@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config["researcher"],
        allow_delegation=False,
        tools=[nl2sql]
    )
```

## Örnek

Birincil görev hedefi şuydu:

"Retrieve the average, maximum, and minimum monthly revenue for each city, but only include cities that have more than one user. Also, count the number of user in each city and
sort the results by the average monthly revenue in descending order"

Böylece ajan DB'den bilgi almaya çalıştı; ilki yanlıştı, bu yüzden ajan tekrar denedi, doğru bilgiyi aldı ve bunu sonraki ajana aktardı.

![alt text](../images/NL2SQL-Example-1)
![alt text](../images/NL2SQL-Example-2)

İkinci görev hedefi şuydu:

"Review the data and create a detailed report, and then create the table on the database with the fields based on the data provided.
Include information on the average, maximum, and minimum monthly revenue for each city, but only include cities that have more than one user. Also, count the number of users in each city and sort the results by the average monthly revenue in descending order."

Burada işler ilginçleşmeye başlıyor; ajan yalnızca tabloyu oluşturmakla kalmayıp veriyi tabloya eklemek için de SQL sorgusu üretiyor. Sonunda ajan, veritabanında bulunanla tam olarak aynı olan nihai raporu da döndürüyor.

![alt text](../images/NL2SQL-Example-3)
![alt text](../images/NL2SQL-Example-4)

![alt text](../images/NL2SQL-Example-5)
![alt text](../images/NL2SQL-Example-6)

Bu, NL2SQLTool'un veritabanıyla etkileşim kurmak ve veritabanındaki verilere dayalı raporlar üretmek için nasıl kullanılabileceğine dair basit bir örnektir.

Araç, ajanın mantığı ve veritabanıyla nasıl etkileşime gireceği konusunda sonsuz olasılıklar sunar.

```md  theme={null}
 DB -> Agent -> ... -> Agent -> DB
```
