import pandas as pd
import os

klasor_yolu = r"C:\Users\Zeynep\Desktop\2247-C"

girdi_dosyasi = "hububat_temizlenmis.csv"
cikti_dosyasi = "hububat_haftalik_ozet.csv"

okunacak_tam_yol = os.path.join(klasor_yolu, girdi_dosyasi)
yazilacak_tam_yol = os.path.join(klasor_yolu, cikti_dosyasi)

print("-------------------------------------------------------")
print(f"Hedef Klasör: {klasor_yolu}")
print(f"İşleniyor...: {okunacak_tam_yol}")
print("-------------------------------------------------------")

try:
    if not os.path.exists(okunacak_tam_yol):
        print(f"HATA: '{girdi_dosyasi}' dosyası bulunamadı!")
    else:
        df = pd.read_csv(okunacak_tam_yol)
        
        # --- DÜZELTME BURADA YAPILDI ---
        df['Son islem tarihi'] = pd.to_datetime(df['Son islem tarihi'], dayfirst=True, errors='coerce')
        
        # Tarihi boş olan (hatalı) satırların temizlenmesi
        df = df.dropna(subset=['Son islem tarihi'])

        df['Yil'] = df['Son islem tarihi'].dt.year
        df['Hafta'] = df['Son islem tarihi'].dt.isocalendar().week
        
        # Gruplama
        grup_sutunlari = ['Grup İsmi', 'Urun İsmi', 'Borsa Adi', 'Yil', 'Hafta']
        
        hesaplamalar = {
            'En az': 'mean',
            'En cok': 'mean', 
            'Ortalama': 'mean',
            'Islem miktarı': 'sum',
            'Islem adedi': 'sum'
        }
        
        df_ozet = df.groupby(grup_sutunlari).agg(hesaplamalar).reset_index()
        
        # Sütun İsimlerini Değiştirme
        df_ozet.rename(columns={
            'Grup İsmi': 'Urun Grubu',
            'Urun İsmi': 'Urun',
            'Borsa Adi': 'Borsa',
            'En az': 'Ortalama en az fiyat',
            'En cok': 'Ortalama en fazla fiyat',
            'Ortalama': 'Ortalama fiyat',
            'Islem miktarı': 'Toplam miktar',
            'Islem adedi': 'Toplam islem sayisi'
        }, inplace=True)
        
        df_ozet.sort_values(by=['Urun Grubu', 'Urun', 'Borsa', 'Yil', 'Hafta'], inplace=True)
        
        df_ozet.to_csv(yazilacak_tam_yol, index=False)
        
        print("\nBAŞARILI!")
        print(f"Dosya şuraya kaydedildi: {yazilacak_tam_yol}")

except Exception as e:
    print(f"\nBEKLENMEDİK BİR HATA OLUŞTU:\n{e}")
