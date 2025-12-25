import pandas as pd
import numpy as np
import math
import os

klasor_yolu = r"C:\Users\Zeynep\Desktop\2247-C"

dosya_ozet = "hububat_haftalik_ozet.csv"
dosya_borsa = "borsa_koordinat.csv"
dosya_depo = "depo_koordinat_TAMAM.csv"

cikti_dosyasi = "cropprice_depo.xlsx"

print("--------------------------------------------------")
print("BÜYÜK FİNAL: MESAFE ANALİZİ VE BİRLEŞTİRME")
print("--------------------------------------------------")

def haversine_mesafe(lat1, lon1, lat2, lon2):
  
    # Dünya yarıçapı (km)
    R = 6371.0
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

try:
    print("Dosyalar okunuyor...")
    path_ozet = os.path.join(klasor_yolu, dosya_ozet)
    path_borsa = os.path.join(klasor_yolu, dosya_borsa)
    path_depo = os.path.join(klasor_yolu, dosya_depo)

    df_ozet = pd.read_csv(path_ozet)
    df_borsa = pd.read_csv(path_borsa)

    try:
        df_depo = pd.read_csv(path_depo)
    except:
        df_depo = pd.read_excel(path_depo)

    print(f"Özet Veri Satır Sayısı: {len(df_ozet)}")
    print(f"Borsa Sayısı: {len(df_borsa)}")
    print(f"Depo Sayısı: {len(df_depo)}")

    # 2. Veri Temizliği ve Hazırlık
    df_borsa.columns = [c.strip() for c in df_borsa.columns]
    df_depo.columns = [c.strip() for c in df_depo.columns]

    kapasite_col = None
    for col in df_depo.columns:
        if "KAPASİTE" in col.upper() or "KAPASITE" in col.upper():
            kapasite_col = col
            break
    
    if kapasite_col:
        df_depo[kapasite_col] = pd.to_numeric(df_depo[kapasite_col], errors='coerce').fillna(0)
    else:
        print("UYARI: Kapasite sütunu bulunamadı, kapasiteler 0 alınacak.")
        df_depo['KAPASITE_YOK'] = 0
        kapasite_col = 'KAPASITE_YOK'

    # 3. Mesafe Matrisi Hesaplama
    print("\nMesafeler hesaplanıyor (Lütfen bekleyin)...")
    
    borsa_istatistikleri = []

    for index, borsa_row in df_borsa.iterrows():
        b_adi = borsa_row['Borsa']
        b_lat = borsa_row['Enlem']
        b_lon = borsa_row['Boylam']
  
        count_25, cap_25 = 0, 0
        count_50, cap_50 = 0, 0
        count_100, cap_100 = 0, 0
    
        for _, depo_row in df_depo.iterrows():
            d_lat = depo_row['ENLEM']
            d_lon = depo_row['BOYLAM']
            kapasite = depo_row[kapasite_col]
    
            if pd.isna(d_lat) or pd.isna(d_lon):
                continue
                
            dist = haversine_mesafe(b_lat, b_lon, d_lat, d_lon)
       
            if dist <= 25:
                count_25 += 1
                cap_25 += kapasite
            if dist <= 50:
                count_50 += 1
                cap_50 += kapasite
            if dist <= 100:
                count_100 += 1
                cap_100 += kapasite
        
        avg_cap_25 = cap_25 / count_25 if count_25 > 0 else 0
        avg_cap_50 = cap_50 / count_50 if count_50 > 0 else 0
        avg_cap_100 = cap_100 / count_100 if count_100 > 0 else 0
        
        borsa_istatistikleri.append({
            'Borsa': b_adi,
            'Within 25 km': count_25,
            'Within 25 km average capacity': avg_cap_25,
            'Within 50 km': count_50,
            'Within 50 km average capacity': avg_cap_50,
            'Within 100 km': count_100,
            'Within 100 km average capacity': avg_cap_100
        })

    df_stats = pd.DataFrame(borsa_istatistikleri)

    # 4. Ana Tabloyla Birleştirme
    print("Hesaplamalar bitti, tablolar birleştiriliyor...")
    
    df_ozet['Borsa_Key'] = df_ozet['Borsa'].astype(str).str.strip().str.upper()
    df_stats['Borsa_Key'] = df_stats['Borsa'].astype(str).str.strip().str.upper()
    
    df_final = pd.merge(df_ozet, df_stats.drop(columns=['Borsa']), on='Borsa_Key', how='left')
    
    df_final.drop(columns=['Borsa_Key'], inplace=True)
    
    # 5. Sütun İsimlerini Şablona Tam Uydurma
    rename_map = {
        'Ortalama en az fiyat': 'Ortalama en az fiyat', # Zaten aynı
        'Ortalama en fazla fiyat': 'Ortalama en fazla',
        'Ortalama fiyat': 'Ortalama-ortalama',
        'Toplam miktar': 'Toplam miktar',
        'Toplam islem sayisi': 'Toplam islem sayisi'
    }
    df_final.rename(columns=rename_map, inplace=True)

    path_cikti = os.path.join(klasor_yolu, cikti_dosyasi)
    df_final.to_excel(path_cikti, index=False)

    print("-" * 50)
    print("✅ TEBRİKLER! PROJE TAMAMLANDI.")
    print(f"Final dosyanız şurada: {path_cikti}")
    print("-" * 50)

except Exception as e:
    print(f"\n❌ BİR HATA OLUŞTU: {e}")
    print("Detaylar: Dosya isimlerini ve klasör yolunu kontrol edin.")
    
input("Çıkmak için Enter'a basın...")
