import pandas as pd
import os

klasor_yolu = r'C:\Users\Zeynep\Desktop\2247-C'

try:
    dosyalar = os.listdir(klasor_yolu)
    bulunan_dosya = next((f for f in dosyalar if 'cropprice' in f.lower()), None)

    if bulunan_dosya is None:
        print("HATA: Klasörde uygun dosya bulunamadı! Dosya adında 'cropprice' geçtiğinden emin ol.")
    else:
        girdi_yolu = os.path.join(klasor_yolu, bulunan_dosya)
        print(f"İşlenen Dosya: {bulunan_dosya}")

        if bulunan_dosya.lower().endswith('.csv'):
            df = pd.read_csv(girdi_yolu)
        else:
            df = pd.read_excel(girdi_yolu)

        if 'Urun' in df.columns:
            df = df.drop(columns=['Urun'])
          
        def urun_grupla(val):
            v = str(val).upper()
            if 'ARPA' in v: return 'Arpa'
            if 'BUGDAY' in v or 'BUĞDAY' in v: return 'Buğday'
            return val
        
        df['Urun Grubu'] = df['Urun Grubu'].apply(urun_grupla)

        df = df.rename(columns={
            'Urun Grubu': 'Ürün Grubu',
            'Yil': 'Yıl',
            'Ortalama-ortalama': 'Ortalama ortalama'
        })

        gruplar = ['Ürün Grubu', 'Borsa', 'Yıl', 'Hafta']
        islemler = {
            'Ortalama en az fiyat': 'mean', 
            'Ortalama en fazla': 'mean', 
            'Ortalama ortalama': 'mean',
            'Toplam miktar': 'sum', 
            'Toplam islem sayisi': 'sum',
            'Within 25 km': 'mean', 
            'Within 25 km average capacity': 'mean',
            'Within 50 km': 'mean', 
            'Within 50 km average capacity': 'mean',
            'Within 100 km': 'mean', 
            'Within 100 km average capacity': 'mean'
        }
        df_final = df.groupby(gruplar).agg(islemler).reset_index()

        df_final = df_final.sort_values(by=['Ürün Grubu', 'Borsa', 'Yıl', 'Hafta'])

        sirali_basliklar = [
            "Ürün Grubu", "Borsa", "Yıl", "Hafta", "Ortalama en az fiyat",
            "Ortalama en fazla", "Ortalama ortalama", "Toplam miktar",
            "Toplam islem sayisi", "Within 25 km", "Within 25 km average capacity",
            "Within 50 km", "Within 50 km average capacity",
            "Within 100 km", "Within 100 km average capacity"
        ]
  
        mevcut_sutunlar = [c for c in sirali_basliklar if c in df_final.columns]
        df_final = df_final[mevcut_sutunlar]

        cikti_yolu = os.path.join(klasor_yolu, 'FINAL_VERI.csv')
        df_final.to_csv(cikti_yolu, index=False, encoding='utf-8-sig')
        
        print("-" * 50)
        print("TEBRİKLER! İŞLEM BAŞARIYLA TAMAMLANDI.")
        print(f"Final dosyanız hazır: {cikti_yolu}")
        print("-" * 50)

except Exception as e:
    print(f"HATA OLUŞTU: {e}")
    
