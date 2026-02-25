> ## Dokümantasyon İndeksi
> Tüm dokümantasyon indeksine şu adresten ulaşabilirsiniz: https://docs.crewai.com/llms.txt
> Daha fazla keşfetmeden önce mevcut tüm sayfaları öğrenmek için bu dosyayı kullanın.

# En Son Crew Kickoff'undan Görevleri Yeniden Başlatma

> En son `crew.kickoff(...)` çağrısından görevleri yeniden başlatın.

## Giriş

CrewAI, en son crew kickoff'undan belirtilen bir görevden itibaren yeniden başlatma (replay) imkanı sunar. Bu özellik, bir kickoff'u tamamladığınızda belirli görevleri tekrar denemek istediğinizde veya verileri tekrar çekmeye ihtiyaç duymadığınızda oldukça kullanışlıdır; çünkü temsilcileriniz (agents) kickoff yürütmesinden gelen bağlama (context) zaten sahiptir, bu nedenle sadece istediğiniz görevleri yeniden oynatmanız yeterlidir.

> [!NOTE]
> Bir görevi yeniden başlatabilmek için önce `crew.kickoff()` komutunu çalıştırmış olmanız gerekir.
> Şu anda sadece en son kickoff desteklenmektedir, bu nedenle `kickoff_for_each` kullanıyorsanız, yalnızca en son crew çalışmasından itibaren yeniden başlatmanıza izin verecektir.

İşte bir görevden itibaren yeniden başlatmanın bir örneği:

### CLI Kullanarak Belirli Bir Görevden Yeniden Başlatma

Yeniden başlatma özelliğini kullanmak için şu adımları izleyin:

1. **Terminalinizi veya komut satırınızı açın.**

2. **CrewAI projenizin bulunduğu dizine gidin.**

3. **Aşağıdaki komutları çalıştırın:**
    En son kickoff `task_id`'lerini görüntülemek için şunu kullanın:

    ```shell
    crewai log-tasks-outputs
    ```

    Yeniden başlatmak istediğiniz `task_id`'yi aldıktan sonra şunu kullanın:

    ```shell
    crewai replay -t <task_id>
    ```

> [!NOTE]
> Geliştirme ortamınızda `crewai`'nin kurulu ve doğru şekilde yapılandırılmış olduğundan emin olun.

### Programatik Olarak Bir Görevden Yeniden Başlatma

Programatik olarak bir görevden yeniden başlatmak için aşağıdaki adımları kullanın:

1. **Yeniden başlatma işlemi için `task_id` ve giriş parametrelerini belirtin.**
    Yeniden başlatma işlemi için `task_id` ve giriş parametrelerini belirtin.

2. **Olası hataları yönetmek için bir try-except bloğu içinde yeniden başlatma komutunu yürütün.**

    ```python
    def replay():
        """
        Crew yürütmesini belirli bir görevden itibaren yeniden başlatın.
        """
        task_id = '<task_id>'
        inputs = {"topic": "CrewAI Training"}  # Bu isteğe bağlıdır; yeniden oynatmak istediğiniz girişleri geçebilirsiniz; aksi takdirde bir önceki kickoff'un girişlerini kullanır.
        try:
            YourCrewName_Crew().crew().replay(task_id=task_id, inputs=inputs)

        except subprocess.CalledProcessError as e:
            raise Exception(f"Crew yeniden başlatılırken bir hata oluştu: {e}")

        except Exception as e:
            raise Exception(f"Beklenmedik bir hata oluştu: {e}")
    ```

## Sonuç

Yukarıdaki iyileştirmeler ve detaylı işlevsellik ile CrewAI'da belirli görevleri yeniden başlatmak daha verimli ve sağlam hale getirilmiştir.
Bu özelliklerden en iyi şekilde yararlanmak için komutları ve adımları tam olarak takip ettiğinizden emin olun.
