<details>
<summary><strong>2247-C – Hububat Piyasası Veri İşleme Süreci</strong></summary>

<br>

#### Dosya 01 – `01_ingest_and_clean_hububat.py`
- ZIP dosyaları içindeki Excel borsa verileri okunmuş ve tek bir veri setinde birleştirilmiştir.
- Ürün ve borsa adları standartlaştırılmış, ana ürün grupları oluşturulmuştur.
- Tarih ve sayısal alanlar düzeltilmiş, mantıksal ve istatistiksel aykırı değer temizliği yapılmıştır.

<br>

#### Dosya 02 – `02_filter_markets_and_products.py`
- Analizi bozabilecek düşük hacimli borsalar veri setinden çıkarılmıştır.
- Aynı ürün grubunu temsil eden ancak detay düzeyi yüksek alt ürünler elenmiştir.

<br>

#### Dosya 03 – `03_create_weekly_summary.py`
- Günlük veriler haftalık zaman dilimine dönüştürülmüştür.
- Ürün ve borsa bazında fiyatlar ortalama, işlem miktarları toplam alınmıştır.

<br>

#### Dosya 04 – `04_generate_market_coordinates.py`
- Ticaret borsalarına ait enlem ve boylam bilgileri tanımlanmıştır.
- Borsalar için coğrafi referans noktaları oluşturulmuştur.

<br>

#### Dosya 05 – `05_fetch_warehouse_coordinates.py`
- Lisanslı depoların ilçe bilgileri kullanılarak coğrafi koordinatları elde edilmiştir.
- Depo kapasite bilgileri korunarak konumsal veri yapısı oluşturulmuştur.

<br>

#### Dosya 06 – `06_compute_distance_and_capacity_metrics.py`
- Borsa ve depo koordinatları kullanılarak aralarındaki mesafeler hesaplanmıştır.
- Her borsa için belirli mesafeler (25 km, 50 km, 100 km) içinde bulunan depo sayısı belirlenmiştir.
- Aynı mesafeler için ortalama depo kapasitesi hesaplanarak piyasa verisiyle ilişkilendirilmiştir.

<br>

#### Dosya 07 – `07_filter_final_products.py`
- Veri seti yalnızca **Arpa** ve **Buğday** ürünlerini kapsayacak şekilde sınırlandırılmıştır.

<br>

#### Dosya 08 – `08_generate_final_weekly_dataset.py`
- Ürün, borsa ve zaman bazında son düzenlemeler yapılmıştır.
- Haftalık düzeyde sadeleştirilmiş nihai veri seti oluşturulmuştur.

</details>

---

## Kullanılan Python Kütüphaneleri

- **pandas** — Veri okuma/yazma, temizleme, gruplama ve birleştirme işlemleri  
- **numpy** — Sayısal veri temizliği ve NaN yönetimi  
- **os** — Dosya ve klasör yönetimi  
- **zipfile** — ZIP dosyaları içinden Excel verilerinin okunması  
- **math** — Coğrafi mesafe hesaplamaları  
- **urllib** — Harici servislerden (OpenStreetMap) koordinat verisi çekilmesi  
- **json** — Harici servis yanıtlarının ayrıştırılması  
- **time** — Harici servis çağrıları arasında bekleme (rate limit)
