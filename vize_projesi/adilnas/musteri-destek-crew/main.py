import sys
import os
from datetime import datetime
from pathlib import Path


def main():
    print("=" * 60)
    print("  Müşteri Destek Otomasyonu - CrewAI Çok Ajanlı Sistem")
    print("=" * 60)
    print()
    print("Müşteri şikâyetini girin veya örnek dosya yolu yazın.")
    print("Örnekler:")
    print("  examples/sikayet_ofkeli.txt")
    print("  examples/sikayet_teknik.txt")
    print("  examples/sikayet_fatura.txt")
    print()

    kullanici_girisi = input("Şikâyet metni (veya dosya yolu): ").strip()

    if not kullanici_girisi:
        print("Giriş yapılmadı. Çıkılıyor.")
        sys.exit(1)

    if os.path.isfile(kullanici_girisi):
        with open(kullanici_girisi, "r", encoding="utf-8") as f:
            sikayet = f.read().strip()
        print(f"\nDosyadan yüklendi: {kullanici_girisi}")
    else:
        sikayet = kullanici_girisi

    print(f"\nŞikâyet analiz ediliyor: {sikayet[:80]}...")
    print("Bu işlem birkaç dakika sürebilir.\n")
    print("-" * 60)

    from crew import run
    sonuc = run(sikayet)

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"rapor_{timestamp}.md"

    icerik = f"# Müşteri Destek Analiz Raporu\n\n"
    icerik += f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    icerik += f"**Şikâyet:**\n> {sikayet}\n\n"
    icerik += "---\n\n"
    icerik += str(sonuc)

    output_file.write_text(icerik, encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"Rapor kaydedildi: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
