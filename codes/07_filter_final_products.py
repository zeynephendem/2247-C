import pandas as pd
import os

klasor_yolu = r"C:\Users\Zeynep\Desktop\2247-C"
dosya_adi = "cropprice_depo.xlsx"  # Dosya uzantısı xlsx varsayıldı
cikti_adi = "cropprice_depo_ARPA_BUGDAY.xlsx"  # Karışmasın diye yeni isimle kaydediyoruz

tam_girdi_yolu = os.path.join(klasor_yolu, dosya_adi)
tam_cikti_yolu = os.path.join(klasor_yolu, cikti_adi)

print("-" * 50)
print("FİLTRELEME İŞLEMİ BAŞLATILIYOR: SADECE ARPA VE BUĞDAY")
print("-" * 50)

try:
    # 1. Dosyayı Oku
    print(f"Dosya okunuyor: {tam_girdi_yolu}")
    
    # Dosya uzantısına göre okuma yapalım
    if dosya_adi.endswith('.csv'):
        df = pd.read_csv(tam_girdi_yolu)
    else:
        df = pd.read_excel(tam_girdi_yolu)

    print(f"Orijinal Satır Sayısı: {len(df)}")

    # 2. Filtreleme 
    hedef_sutun = None
    olasi_sutunlar = ['Urun Grubu', 'Grup İsmi', 'Urun Group', 'Ürün Grubu', 'Grup']

    for col in df.columns:
        if col.strip() in olasi_sutunlar:
            hedef_sutun = col
            break

    if not hedef_sutun:
        print("UYARI: 'Urun Grubu' sütunu bulunamadı, 'Urun' sütunundan filtreleme yapılacak.")
        hedef_sutun = 'Urun' if 'Urun' in df.columns else df.columns[0]

    print(f"Filtreleme yapılacak sütun: {hedef_sutun}")

    # Sadece ARPA ve BUĞDAY 
    filtre = df[hedef_sutun].astype(str).str.upper().apply(
        lambda x: 'ARPA' in x or 'BUGDAY' in x or 'BUĞDAY' in x
    )
    
    df_filtered = df[filtre]

    # 3. Sonuçları Göster ve Kaydet
    kalan_sayi = len(df_filtered)
    silinen_sayi = len(df) - kalan_sayi
    
    print(f"\nİşlem Sonucu:")
    print(f"Silinen (Diğer Ürünler): {silinen_sayi} satır")
    print(f"Kalan (Arpa ve Buğday): {kalan_sayi} satır")

    if kalan_sayi > 0:
        df_filtered.to_excel(tam_cikti_yolu, index=False)
        print("-" * 50)
        print("✅ BAŞARILI! Dosyanız filtrelendi.")
        print(f"Yeni dosya: {tam_cikti_yolu}")
        print("-" * 50)
    else:
        print("❌ HATA: Filtreleme sonucu hiç veri kalmadı! Sütun isimlerini kontrol edin.")

except FileNotFoundError:
    print(f"❌ HATA: '{dosya_adi}' dosyası bulunamadı. Lütfen dosya adının uzantısıyla (.xlsx) birlikte doğru olduğundan emin olun.")
except Exception as e:
    print(f"❌ BEKLENMEDİK HATA: {e}")

input("Çıkmak için Enter'a basın...")
