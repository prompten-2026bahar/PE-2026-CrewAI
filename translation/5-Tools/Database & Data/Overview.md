> ## Dokümantasyon Dizini
> Tam dokümantasyon dizinini şuradan alın: https://docs.crewai.com/llms.txt
> Daha fazla incelemeden önce mevcut tüm sayfaları keşfetmek için bu dosyayı kullanın.

# Genel Bakış

> Kapsamlı veri erişimi için veritabanlarına, vektör depolarına ve veri ambarlarına bağlanın

Bu araçlar, ajanlarınızın geleneksel SQL veritabanlarından modern vektör depolarına ve veri ambarlarına kadar çeşitli veritabanı sistemleriyle etkileşime girmesini sağlar.

## **Kullanılabilir Araçlar**

<CardGroup cols={2}>
  <Card title="MySQL Tool" icon="database" href="/en/tools/database-data/mysqltool">
    SQL işlemleriyle MySQL veritabanlarına bağlanın ve sorgulayın.
  </Card>

  <Card title="PostgreSQL Search" icon="elephant" href="/en/tools/database-data/pgsearchtool">
    PostgreSQL veritabanlarında verimli şekilde arama yapın ve sorgulayın.
  </Card>

  <Card title="Snowflake Search" icon="snowflake" href="/en/tools/database-data/snowflakesearchtool">
    Analitik ve raporlama için Snowflake veri ambarına erişin.
  </Card>

  <Card title="NL2SQL Tool" icon="language" href="/en/tools/database-data/nl2sqltool">
    Doğal dil sorgularını otomatik olarak SQL ifadelerine dönüştürün.
  </Card>

  <Card title="Qdrant Vector Search" icon="vector-square" href="/en/tools/database-data/qdrantvectorsearchtool">
    Qdrant vektör veritabanını kullanarak vektör embedding'leri arayın.
  </Card>

  <Card title="Weaviate Vector Search" icon="network-wired" href="/en/tools/database-data/weaviatevectorsearchtool">
    Weaviate vektör veritabanı ile anlamsal arama yapın.
  </Card>

  <Card title="MongoDB Vector Search" icon="leaf" href="/en/tools/database-data/mongodbvectorsearchtool">
    İndeksleme yardımcılarıyla MongoDB Atlas üzerinde vektör benzerliği araması yapın.
  </Card>

  <Card title="SingleStore Search" icon="database" href="/en/tools/database-data/singlestoresearchtool">
    Havuzlama ve doğrulama ile SingleStore üzerinde güvenli SELECT/SHOW sorguları.
  </Card>
</CardGroup>

## **Yaygın Kullanım Senaryoları**

* **Veri Analizi**: İş zekası ve raporlama için veritabanlarını sorgulayın
* **Vektör Arama**: Anlamsal embedding'ler kullanarak benzer içerikleri bulun
* **ETL İşlemleri**: Sistemler arasında veriyi çıkarın, dönüştürün ve yükleyin
* **Gerçek Zamanlı Analitik**: Karar verme için canlı verilere erişin

```python  theme={null}
from crewai_tools import MySQLTool, QdrantVectorSearchTool, NL2SQLTool

# Veritabanı araçlarını oluştur
mysql_db = MySQLTool()
vector_search = QdrantVectorSearchTool()
nl_to_sql = NL2SQLTool()

# Ajanınıza ekleyin
agent = Agent(
    role="Veri Analisti",
    tools=[mysql_db, vector_search, nl_to_sql],
    goal="Çeşitli veri kaynaklarından içgörü çıkar"
)
```
