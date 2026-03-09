# Genel Bakış

> Bulut servisleri, depolama sistemleri ve bulut tabanlı yapay zeka platformlarıyla etkileşim kurun.

Bu araçlar, ajanlarınızın bulut servisleriyle etkileşime girmesini, bulut depolamaya erişmesini ve ölçeklenebilir operasyonlar için bulut tabanlı yapay zeka platformlarından yararlanmasını sağlar.

## **Mevcut Araçlar**

- **[S3 Reader Tool](/en/tools/cloud-storage/s3readertool)**: Amazon S3 bucket'larından dosya ve veri okuyun.
- **[S3 Writer Tool](/en/tools/cloud-storage/s3writertool)**: Amazon S3 depolama birimine dosya yazın ve yükleyin.
- **[Bedrock Invoke Agent](/en/tools/integration/bedrockinvokeagenttool)**: Yapay zeka destekli görevler için Amazon Bedrock ajanlarını çağırın.
- **[Bedrock KB Retriever](/en/tools/cloud-storage/bedrockkbretriever)**: Amazon Bedrock bilgi tabanlarından (knowledge bases) bilgi getirin.

## **Genel Kullanım Durumları**

* **Dosya Depolama**: Bulut depolama sistemlerinde dosya depolayın ve geri çağırın.
* **Veri Yedekleme**: Önemli verileri bulut depolamaya yedekleyin.
* **Yapay Zeka Servisleri**: Bulut tabanlı yapay zeka modellerine ve servislerine erişin.
* **Bilgi Edinme**: Bulutta barındırılan bilgi tabanlarını sorgulayın.
* **Ölçeklenebilir Operasyonlar**: İşleme süreçleri için bulut altyapısından yararlanın.

```python  theme={null}
from crewai_tools import S3ReaderTool, S3WriterTool, BedrockInvokeAgentTool

# Bulut araçlarını oluşturun
s3_reader = S3ReaderTool()
s3_writer = S3WriterTool()
bedrock_agent = BedrockInvokeAgentTool()

# Ajanınıza ekleyin
agent = Agent(
    role="Bulut Operasyonları Uzmanı",
    tools=[s3_reader, s3_writer, bedrock_agent],
    goal="Bulut kaynaklarını ve yapay zeka servislerini yönet"
)
```
