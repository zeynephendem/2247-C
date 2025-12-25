import pandas as pd
import os
import zipfile
import numpy as np
from scipy import stats

klasor_yolu = r"C:\Users\Zeynep\Desktop\2247-C"
zip_file_names = ['hubutat1', 'hubutat2', 'hubutat3', 'hubutat4', 'hubutat5']

all_dataframes = []
print("Adım 1: Dosyalar okunuyor ve birleştiriliyor...")

for name in zip_file_names:
    zip_file_path = os.path.join(klasor_yolu, f"{name}.zip")
    if not os.path.isfile(zip_file_path): 
        print(f"UYARI: '{zip_file_path}' bulunamadı, atlanıyor.")
        continue
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as z:
            for excel_file_in_zip in z.namelist():
                if excel_file_in_zip.endswith(('.xlsx', '.xls')):
                    with z.open(excel_file_in_zip) as excel_file:
                        
                        df = pd.read_excel(excel_file, header=None, skiprows=2)
                        
                        df.dropna(how='all', inplace=True)
                        if df.empty: continue
                        
                        if df.shape[1] == 8:
                            df.columns = ['Borsa Adi', 'Son islem tarihi', 'En az', 'En cok', 'Ortalama', 'Islem miktarı', 'Islem adedi', 'Islem tutari']
                        elif df.shape[1] == 7:
                            df.columns = ['Son islem tarihi', 'En az', 'En cok', 'Ortalama', 'Islem miktarı', 'Islem adedi', 'Islem tutari']
                        else:
                            continue
                            
                        product_name = os.path.splitext(os.path.basename(excel_file_in_zip))[0]
                        if ' - ' in product_name: product_name = product_name.split(' - ', 1)[1]
                        df['Urun İsmi'] = product_name
                        all_dataframes.append(df)
    except Exception as e:
        print(f"HATA: '{name}.zip' okunurken bir hata oluştu: {e}")

if not all_dataframes:
    raise ValueError("Hiçbir dosya okunamadı, işlem durduruldu.")

merged_df = pd.concat(all_dataframes, ignore_index=True)
print("Veri okuma tamamlandı.")

# --- ADIM 2: KARAKTER DÜZELTME ---
print("Adım 2: Karakterler harmonize ediliyor...")
char_map = {
    'Ş':'S','ş':'S','Þ':'S','þ':'S','Ğ':'G','ğ':'G','ª':'G','º':'G','Ð':'G','ð':'G',
    'İ':'I','ı':'I','Ý':'I','ý':'I','ÿ':'I','Ö':'O','ö':'O','Ü':'U','ü':'U','Ç':'C','ç':'C'
}
for col in ['Urun İsmi', 'Borsa Adi']:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col].astype(str)
        for bad_char, good_char in char_map.items():
            merged_df[col] = merged_df[col].str.replace(bad_char, good_char, regex=False)
        merged_df[col] = merged_df[col].str.upper().str.strip()

# --- ADIM 3: ÜRÜN GRUPLARI ---
print("Adım 3: Ürün grupları oluşturuluyor...")
def get_group_name(product_name):
    product_name = str(product_name)
    if 'BUGDAY UNU' in product_name: return 'BUGDAY UNU'
    if 'BUGDAY' in product_name: return 'BUGDAY'
    if 'ARPA' in product_name: return 'ARPA'
    if 'MISIR' in product_name: return 'MISIR'
    if 'YULAF' in product_name: return 'YULAF'
    if 'CAVDAR' in product_name: return 'CAVDAR'
    if 'PIRINC' in product_name: return 'PIRINC'
    if 'CELTIK' in product_name: return 'CELTIK'
    return 'DIGER'
merged_df['Grup İsmi'] = merged_df['Urun İsmi'].apply(get_group_name)

# --- ADIM 4: VERİ TİPLERİ VE TEMİZLİK ---
print("Adım 4: Veri tipleri düzeltiliyor...")
merged_df['Son islem tarihi'] = pd.to_datetime(merged_df['Son islem tarihi'], errors='coerce')
numeric_cols = ['En az','En cok','Ortalama','Islem miktarı','Islem adedi','Islem tutari']
for col in numeric_cols:
    if col in merged_df.columns:
        merged_df[col] = pd.to_numeric(merged_df[col].astype(str).str.replace(',', '.'), errors='coerce')
merged_df.dropna(subset=['Son islem tarihi'], inplace=True)

# --- ADIM 4.5: AYKIRI DEĞER DÜZELTME (GELİŞMİŞ) ---
print("Adım 4.5: Gelişmiş aykırı değer düzeltmeleri başlatılıyor...")

# 0 veya negatif değerleri güvenli NaN yapma
merged_df.loc[merged_df['Islem miktarı'] <= 0, ['Ortalama','Islem tutari']] = np.nan
merged_df.loc[merged_df['En az'] < 0, 'En az'] = np.nan
merged_df.loc[merged_df['En cok'] < 0, 'En cok'] = np.nan
merged_df.loc[merged_df['Ortalama'] <= 0, 'Ortalama'] = np.nan 

# En az > En cok hatalarını düzeltme
condition_min_max = merged_df['En az'] > merged_df['En cok']
merged_df.loc[condition_min_max, ['En az','En cok']] = merged_df.loc[condition_min_max, ['En cok','En az']].values

print("  - Kuruş/TL Birim Hatası (örn: 267.0) kontrolü yapılıyor...")
unit_error_threshold = 10 
condition_tl_error = (merged_df['En az'] > unit_error_threshold) | (merged_df['Ortalama'] > unit_error_threshold)

print(f"  - Fiyatı {unit_error_threshold}'den büyük {condition_tl_error.sum()} satırın fiyatları NaN yapılıyor.")
merged_df.loc[condition_tl_error, ['En az', 'En cok', 'Ortalama']] = np.nan

print("  - Mantıksal ölçek kontrolü (örn: 0.3 vs 396) yapılıyor...")
threshold_fark = 50 # 50 birimden fazla fark
threshold_diger = 1  # diğer fark 1 birimden azsa

enaz_fark_ort = (merged_df['En az'] - merged_df['Ortalama']).abs()
encok_fark_ort = (merged_df['En cok'] - merged_df['Ortalama']).abs()
enaz_fark_ort.fillna(0, inplace=True) # NaN'ları 0 fark olarak kabul et
encok_fark_ort.fillna(0, inplace=True) # NaN'ları 0 fark olarak kabul et

condition_encok_is_outlier = (encok_fark_ort > threshold_fark) & (enaz_fark_ort < threshold_diger)
condition_enaz_is_outlier = (enaz_fark_ort > threshold_fark) & (encok_fark_ort < threshold_diger)

print(f"  - Ölçek hatası (En Cok) bulunan {condition_encok_is_outlier.sum()} satır NaN yapılıyor.")
merged_df.loc[condition_encok_is_outlier, 'En cok'] = np.nan
print(f"  - Ölçek hatası (En Az) bulunan {condition_enaz_is_outlier.sum()} satır NaN yapılıyor.")
merged_df.loc[condition_enaz_is_outlier, 'En az'] = np.nan


# Mantıksal Fiyat Aralığı Kontrolü 
print("  - Ortalama'nın [En az, En cok] aralığı dışında kalma kontrolü...")
condition_avg_outside_range = (merged_df['Ortalama'] < merged_df['En az']) | (merged_df['Ortalama'] > merged_df['En cok'])
print(f"  - [En az, En cok] aralığı dışında kalan {condition_avg_outside_range.sum()} 'Ortalama' değeri NaN yapılıyor.")
merged_df.loc[condition_avg_outside_range, 'Ortalama'] = np.nan


# Mantıksal Fiyat Kontrolü (Tutar/Miktar vs Ortalama)
print("  - Mantıksal fiyat kontrolü yapılıyor (Tutar/Miktar)...")
merged_df['hesaplanan_birim_fiyat'] = np.nan
valid_mask = (merged_df['Islem tutari'] > 0) & (merged_df['Islem miktarı'] > 0)
merged_df.loc[valid_mask, 'hesaplanan_birim_fiyat'] = merged_df['Islem tutari'] / merged_df['Islem miktarı']
fark_orani = (merged_df['Ortalama'] - merged_df['hesaplanan_birim_fiyat']).abs() / merged_df['Ortalama']
fark_orani.fillna(0, inplace=True) 
condition_mismatch = (fark_orani > 0.20) & (merged_df['hesaplanan_birim_fiyat'].notna())
print(f"  - Mantıksal tutarsızlık bulunan {condition_mismatch.sum()} satır 'Ortalama' değeri NaN yapılıyor.")
merged_df.loc[condition_mismatch, 'Ortalama'] = np.nan
del merged_df['hesaplanan_birim_fiyat'] 

# Grup Bazlı İstatistiksel Temizlik (Z-Score)
print("  - Grup bazlı Z-Score ile istatistiksel aykırı değer tespiti...")
numeric_cols_to_clean = ['En az', 'En cok', 'Ortalama']

for col in numeric_cols_to_clean:
    if col not in merged_df.columns: continue
    
    grp_stats = merged_df.groupby('Grup İsmi')[col]
    mean = grp_stats.transform('mean')
    std = grp_stats.transform('std')
    std.replace(0, np.nan, inplace=True) 
    z_scores = (merged_df[col] - mean).abs() / std
    
    outlier_condition = z_scores > 3
    print(f"  - '{col}' sütununda Z-Score > 3 olan {outlier_condition.sum()} aykırı değer NaN yapılıyor.")
    merged_df.loc[outlier_condition, col] = np.nan

print("Adım 4.5: Aykırı değer düzeltmeleri tamamlandı.")

# --- ADIM 5: MASTER DOSYASI ---
print("Adım 5: Master dosya oluşturuluyor...")
final_cols = ['Grup İsmi','Urun İsmi','Borsa Adi','Son islem tarihi','En az','En cok','Ortalama','Islem miktarı','Islem adedi','Islem tutari']
existing_cols = [c for c in final_cols if c in merged_df.columns]
master_df = merged_df[existing_cols].copy()
master_df['Son islem tarihi'] = master_df['Son islem tarihi'].dt.strftime('%Y-%m-%d')
master_file_path = os.path.join(klasor_yolu,'hububat_master_SIRALANMIS.csv')
master_df.to_csv(master_file_path,index=False,encoding='utf-8-sig')

# --- ADIM 6: GÜNLÜK ÖZET ---
print("Adım 6: Günlük özet tablosu oluşturuluyor...")
merged_df['Borsa Adi'] = merged_df['Borsa Adi'].fillna('BELIRTILMEMIS')
agg_dict = {'En az':'mean','En cok':'mean','Ortalama':'mean',
            'Islem miktarı':'sum','Islem adedi':'sum','Islem tutari':'sum'}
summary_df = merged_df.groupby(['Grup İsmi','Urun İsmi','Borsa Adi','Son islem tarihi']).agg(agg_dict).reset_index()
summary_df.rename(columns={
    'En az':'ortalama_en_az','En cok':'ortalama_en_cok','Ortalama':'ortalama_fiyat',
    'Islem miktarı':'toplam_islem_miktari','Islem adedi':'toplam_islem_adedi','Islem tutari':'toplam_islem_tutari'
}, inplace=True)
summary_df['Son islem tarihi'] = pd.to_datetime(summary_df['Son islem tarihi']).dt.strftime('%Y-%m-%d')

# --- ADIM 7: ÖZET DOSYA KAYDI ---
summary_file_path = os.path.join(klasor_yolu,'hububat_gunluk_ozet_URUN_DETAYLI.csv')
summary_df.to_csv(summary_file_path,index=False,encoding='utf-8-sig')

print("\n--- TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI ---")
