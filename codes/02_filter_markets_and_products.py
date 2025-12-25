import pandas as pd

# 1. Dosyayı Yükleme
dosya_adi = r"C:\Users\Zeynep\Desktop\2247-C\hububat_master_SIRALANMIS.csv"

try:
    df = pd.read_csv(dosya_adi)
    print(f"Dosya başarıyla yüklendi. İlk Satır Sayısı: {len(df)}")
except FileNotFoundError:
    print(f"Hata: '{dosya_adi}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
    exit()

# 2. Filtrelenecek (Silinecek) Listelerin Tanımlanması
silinecek_borsalar = [
    "BABAESKI TICARET BORSASI",
    "BAFRA TICARET BORSASI",
    "CANAKKALE TICARET BORSASI",
    "CORLU TICARET BORSASI",
    "DIYARBAKIR TICARET BORSASI",
    "ELAZIG TICARET BORSASI",
    "EREGLI/KONYA TICARET BORSASI",
    "ERZINCAN TICARET BORSASI",
    "GAZIANTEP TICARET BORSASI",
    "GONEN TICARET BORSASI",
    "HAYRABOLU TICARET BORSASI",
    "KARACABEY TICARET BORSASI",
    "KESAN TICARET BORSASI",
    "KIRKLARELI TICARET BORSASI",
    "SAKARYA TICARET BORSASI",
    "SANLIURFA TICARET BORSASI",
    "TEKIRDAG TICARET BORSASI",
    "YERKOY TICARET BORSASI"
]

# Alt ürün isimleri
silinecek_urunler = [
    "ARPA BIRALIK",
    "ARPA CAKIR",
    "ARPA BAREM DISI",
    "BUGDAY ANADOLU BEYAZ SERT 1. DERECE",
    "BUGDAY ANADOLU BEYAZ SERT 3. DERECE",
    "BUGDAY ANADOLU BEYAZ SERT 4.DERECE",
    "BUGDAY BAREM DISI",
    "BUGDAY EKMEKLIK KIRMIZI YARI SERT (4.DERECE)"
]

# 3. Normalizasyon Fonksiyonu
def standardize_text(text):
    if isinstance(text, str):
        return text.strip().upper()
    return text

# Silinecek listelerini de standart hale getirilmesi
silinecek_borsalar = [standardize_text(x) for x in silinecek_borsalar]
silinecek_urunler = [standardize_text(x) for x in silinecek_urunler]

# 4. Filtreleme İşlemi
df['temp_borsa'] = df['Borsa Adi'].apply(standardize_text)
df['temp_urun'] = df['Urun İsmi'].apply(standardize_text)

df_filtered = df[
    (~df['temp_borsa'].isin(silinecek_borsalar)) & 
    (~df['temp_urun'].isin(silinecek_urunler))
].copy()

df_filtered.drop(columns=['temp_borsa', 'temp_urun'], inplace=True)

# 5. Sonuçları Raporlama ve Kaydetme
silinen_sayisi = len(df) - len(df_filtered)
print(f"\nİşlem Tamamlandı.")
print(f"Orijinal Veri Sayısı : {len(df)}")
print(f"Kalan Veri Sayısı    : {len(df_filtered)}")
print(f"Silinen Satır Sayısı : {silinen_sayisi}")

cikti_yolu = r"C:\Users\Zeynep\Desktop\2247-C\hububat_temizlenmis.csv"

df_filtered.to_csv(cikti_yolu, index=False)

print(f"\nDosya şu adrese başarıyla kaydedildi:\n{cikti_yolu}")
