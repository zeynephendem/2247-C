import pandas as pd
import urllib.request
import urllib.parse
import json
import time
import os

klasor_yolu = r"C:\Users\Zeynep\Desktop\2247-C"
cikti_dosyasi = "depo_koordinat_TAMAM.csv"

print("--------------------------------------------------")
print("SİSTEM HAZIR (EKSTRA KÜTÜPHANE GEREKTİRMEZ)")
print("--------------------------------------------------")

okunacak_dosya = None
dosya_turu = ""

if os.path.exists(os.path.join(klasor_yolu, "lisanslıdepo.xlsx")):
    okunacak_dosya = os.path.join(klasor_yolu, "lisanslıdepo.xlsx")
    dosya_turu = "excel"
elif os.path.exists(os.path.join(klasor_yolu, "lisanslıdepo.csv")):
    okunacak_dosya = os.path.join(klasor_yolu, "lisanslıdepo.csv")
    dosya_turu = "csv"
else:
    print("HATA: Klasörde 'lisanslıdepo.xlsx' veya 'lisanslıdepo.csv' bulunamadı!")
    input("Kapatmak için Enter'a basın...")
    exit()

print(f"Dosya bulundu: {okunacak_dosya}")

try:
    if dosya_turu == "excel":
        try:
            df = pd.read_excel(okunacak_dosya, header=1)
        except:
            df = pd.read_excel(okunacak_dosya, header=0)
    else:
        df = pd.read_csv(okunacak_dosya)

    df.columns = [c.strip() for c in df.columns]

    ilce_sutunu = None
    for col in df.columns:
        if "İLÇE" in col or "ILCE" in col:
            ilce_sutunu = col
            break
            
    if not ilce_sutunu:
        print("HATA: Dosyada 'İLÇE' bilgisini içeren bir sütun bulunamadı.")
        exit()

    sirket_sutunu = df.columns[1] # Genelde 2. sütundur
    kapasite_sutunu = df.columns[3] if len(df.columns) > 3 else None

    # Veriyi hazırlama
    if kapasite_sutunu:
        df_clean = df[[sirket_sutunu, ilce_sutunu, kapasite_sutunu]].copy()
        df_clean.columns = ['ŞİRKET İSMİ', 'İLÇE', 'KAPASİTE']
    else:
        df_clean = df[[sirket_sutunu, ilce_sutunu]].copy()
        df_clean.columns = ['ŞİRKET İSMİ', 'İLÇE']

    df_clean.dropna(subset=['İLÇE'], inplace=True)
    unique_ilceler = df_clean['İLÇE'].unique()
    
    print(f"Toplam {len(df_clean)} depo kaydı var.")
    print(f"Aranacak {len(unique_ilceler)} farklı ilçe var.")
    print("İnternetten koordinatlar çekiliyor (Lütfen bekleyin)...")

    # 2. Koordinat Bulucu (Saf Python - urllib)
    def koordinat_bul(ilce_adi):
        try:
            adres = f"{ilce_adi}, Turkey"
            query = urllib.parse.quote(adres)
            url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
          
            headers = {'User-Agent': 'OgrenciProjesi/1.0 (iletisim@ornek.com)'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                if len(data) > 0:
                    return float(data[0]['lat']), float(data[0]['lon'])
        except Exception as e:
            pass
        return None, None

    # 3. Döngü ve Hafıza
    ilce_hafizasi = {}
    
    for i, ilce in enumerate(unique_ilceler):
        # Durum çubuğu
        if i % 5 == 0:
            print(f"İşleniyor ({i}/{len(unique_ilceler)}): {ilce}")
            
        lat, lon = koordinat_bul(ilce)
        ilce_hafizasi[ilce] = (lat, lon)
        
        # Site bizi engellemesin diye 1 saniye bekle
        time.sleep(1.0)

    # 4. Sonuçları Birleştirme
    print("\nSonuçlar tabloya yazılıyor...")
    df_clean['ENLEM'] = df_clean['İLÇE'].map(lambda x: ilce_hafizasi.get(x, (None, None))[0])
    df_clean['BOYLAM'] = df_clean['İLÇE'].map(lambda x: ilce_hafizasi.get(x, (None, None))[1])
  
    tam_cikti_yolu = os.path.join(klasor_yolu, cikti_dosyasi)
    df_clean.to_csv(tam_cikti_yolu, index=False)
    
    print("-" * 50)
    print("✅ BAŞARILI! Dosya oluşturuldu.")
    print(f"Dosya şurada: {tam_cikti_yolu}")
    print("-" * 50)

except Exception as e:
    print(f"\n❌ BİR HATA OLUŞTU: {e}")
    print("Eğer Excel hatası alıyorsanız, lütfen 'lisanslıdepo.xlsx' dosyasını açıp 'Farklı Kaydet' diyerek 'CSV (Virgülle Ayrılmış)' formatında kaydedin.")

input("Çıkmak için Enter'a basın...")
