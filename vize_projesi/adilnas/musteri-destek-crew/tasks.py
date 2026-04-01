from crewai import Task, Agent


def create_tasks(sikayet: str, agents: dict[str, Agent]) -> list[Task]:

    duygu_analizi = Task(
        description=(
            f"Aşağıdaki müşteri şikâyetini analiz et:\n\n"
            f"ŞİKÂYET: {sikayet}\n\n"
            f"Analizi şu adımları izleyerek yap (chain-of-thought):\n"
            f"ADIM 1 - Anahtar kelime tespiti: Metindeki duygusal yük taşıyan kelimeleri ve "
            f"ifadeleri listele (örn. 'çok sinir oldum', 'berbat', 'hemen', 'saçmalık' vb.).\n"
            f"ADIM 2 - Duygu türü: Baskın duyguyu belirle (öfke / hayal kırıklığı / endişe / sakin / karışık).\n"
            f"ADIM 3 - Yoğunluk skoru: 1 (çok sakin) ile 10 (son derece öfkeli) arasında puan ver.\n"
            f"ADIM 4 - Gerekçe: Verdiğin skoru neden seçtiğini kısaca açıkla.\n"
            f"ADIM 5 - Özet: Müşterinin duygusal durumunu bir cümlede özetle.\n\n"
            f"ÖNEMLI: Tüm yanıtını Türkçe yaz."
        ),
        expected_output=(
            "Şu bölümleri içeren yapılandırılmış bir duygu analizi raporu:\n"
            "- Tespit edilen anahtar kelimeler listesi\n"
            "- Baskın duygu türü\n"
            "- Yoğunluk skoru (1-10)\n"
            "- Skor gerekçesi\n"
            "- Tek cümlelik duygusal durum özeti"
        ),
        agent=agents["duygu_analizcisi"],
        async_execution=True,
    )

    kategori_tespiti = Task(
        description=(
            f"Aşağıdaki müşteri şikâyetini kategorize et:\n\n"
            f"ŞİKÂYET: {sikayet}\n\n"
            f"Şu bilgileri belirle:\n"
            f"1. Ana kategori (sadece biri seç):\n"
            f"   - Teknik Destek (uygulama/site hatası, ürün arızası, kullanım sorunu)\n"
            f"   - Fatura & Ödeme (yanlış tutar, çift ödeme, iade talebi, fatura hatası)\n"
            f"   - İade & Değişim (ürün iadesi, değişim talebi, hasarlı ürün)\n"
            f"   - Kargo & Teslimat (geç teslimat, kayıp kargo, yanlış adres)\n"
            f"   - Genel Bilgi (soru, öneri, dilek)\n"
            f"2. Alt kategori: Ana kategori içinde daha spesifik konu\n"
            f"3. Aciliyet seviyesi:\n"
            f"   - Düşük: Rutin, zaman hassasiyeti yok\n"
            f"   - Orta: 24-48 saat içinde yanıt bekleniyor\n"
            f"   - Yüksek: Finansal kayıp veya ciddi memnuniyetsizlik\n"
            f"   - Acil: Anında müdahale gerekiyor (güvenlik, büyük finansal kayıp)\n"
            f"4. Gerekçe: Seçimlerini kısaca açıkla\n\n"
            f"ÖNEMLI: Tüm yanıtını Türkçe yaz."
        ),
        expected_output=(
            "Şu bölümleri içeren yapılandırılmış bir kategori raporu:\n"
            "- Ana kategori\n"
            "- Alt kategori\n"
            "- Aciliyet seviyesi\n"
            "- Seçim gerekçesi"
        ),
        agent=agents["kategori_uzmani"],
        async_execution=True,
    )

    yanit_taslagi = Task(
        description=(
            "Duygu analizi ve kategori tespiti sonuçlarını kullanarak müşteriye "
            "gönderilecek yanıt taslağını hazırla.\n\n"
            "Yanıtı şu yapıya göre yaz:\n"
            "1. AÇILIŞ: Müşteriyi ismiyle selamla (isim bilinmiyorsa 'Sayın Müşterimiz'). "
            "Duygu skoruna göre empati kur:\n"
            "   - Skor 7-10 (yüksek öfke): 'Yaşadığınız durumun sizi ne denli rahatsız "
            "ettiğini anlıyorum...' tonu\n"
            "   - Skor 4-6 (orta): 'Böyle bir sorunla karşılaşmanızdan üzüntü duyuyoruz...' tonu\n"
            "   - Skor 1-3 (sakin): 'Bize ulaştığınız için teşekkür ederiz...' tonu\n"
            "2. SORUNUN KABULÜ: Şikâyeti kategoriye göre kısaca yeniden ifade et.\n"
            "3. ÇÖZÜM ADIMI: Kategoriye uygun somut bir çözüm veya sonraki adım öner.\n"
            "4. KAPANIŞ: Olumlu, güven verici bir cümleyle bitir.\n\n"
            "Yanıt 3-5 paragraf olmalı, samimi ve profesyonel bir dil kullanılmalı.\n\n"
            "ÖNEMLI: Tüm yanıtını Türkçe yaz."
        ),
        expected_output=(
            "Müşteriye gönderilmeye hazır, 3-5 paragraftan oluşan Türkçe yanıt taslağı. "
            "Empati içermeli, somut çözüm adımı sunmalı ve olumlu kapanışla bitmeli."
        ),
        agent=agents["yanit_yazari"],
        context=[duygu_analizi, kategori_tespiti],
    )

    eskalasyon_karari = Task(
        description=(
            "Duygu analizi, kategori tespiti ve hazırlanan yanıt taslağını inceleyerek "
            "eskalasyon kararını ver.\n\n"
            "Şunları değerlendir:\n"
            "1. ESKALASYON GEREKİYOR MU? (Evet / Hayır)\n"
            "   Eskalasyon gerektirir:\n"
            "   - Duygu skoru 8 veya üzeri\n"
            "   - Finansal kayıp (200 TL üzeri)\n"
            "   - Teknik arıza veya güvenlik sorunu\n"
            "   - Hukuki tehdit içeriyor\n"
            "   - İlk seviye destek çözemiyor\n"
            "2. ÖNCELİK SEVİYESİ (eskalasyon varsa):\n"
            "   - P1 (Acil): Anında müdahale\n"
            "   - P2 (Yüksek): 2 saat içinde\n"
            "   - P3 (Orta): Bugün içinde\n"
            "   - P4 (Düşük): 48 saat içinde\n"
            "3. ATANACAK DEPARTMAN: Teknik Ekip / Finans & Muhasebe / Hukuk / "
            "Kargo Operasyon / Ürün Yönetimi / Genel Müdürlük\n"
            "4. GEREKÇE: Kararını 2-3 cümleyle açıkla.\n"
            "5. TAVSİYE: Bir sonraki aksiyon için kısa öneri.\n\n"
            "ÖNEMLI: Tüm yanıtını Türkçe yaz."
        ),
        expected_output=(
            "Şu bölümleri içeren eskalasyon raporu:\n"
            "- Eskalasyon kararı (Evet/Hayır)\n"
            "- Öncelik seviyesi (P1-P4, sadece eskalasyon varsa)\n"
            "- Atanacak departman\n"
            "- Karar gerekçesi\n"
            "- Sonraki aksiyon tavsiyesi"
        ),
        agent=agents["eskalasyon_yoneticisi"],
        context=[duygu_analizi, kategori_tespiti, yanit_taslagi],
    )

    return [duygu_analizi, kategori_tespiti, yanit_taslagi, eskalasyon_karari]
