# 2247-C – Hububat Piyasası Veri İşleme Süreci

Bu repo, hububat ticaret borsalarına ait verilerin ham dosyalardan başlayarak
temizlenmesi, haftalık düzeyde özetlenmesi ve lisanslı depo altyapısı ile
ilişkilendirilmesi sürecini kapsamaktadır.

Çalışmanın amacı, fiyat ve işlem verilerini yalnızca zaman boyutunda değil,
aynı zamanda coğrafi ve lojistik bağlamda analiz edilebilir hale getirmektir.

---

## Kullanılan Dosyalar ve Yapılan İşlemler

### Dosya 01 – `01_ingest_and_clean_hububat.py`
- ZIP dosyaları içindeki Excel borsa verileri okunmuş ve tek bir veri setinde birleştirilmiştir.
- Ürün ve borsa adları standartlaştırılmış, ana ürün grupları oluşturulmuştur.
- Tarih ve sayısal alanlar düzeltilmiş, mantıksal ve istatistiksel aykırı değer temizliği yapılmıştır.
- Analiz için tutarlı ve karşılaştırılabilir bir temel veri seti elde edilmiştir.

---

### Dosya 02 – `02_filter_markets_and_products.py`
- Analizi bozabilecek düşük hacimli borsalar veri setinden çıkarılmıştır.
- Aynı ürün grubunu temsil eden ancak detay düzeyi yüksek alt ürünler elenmiştir.
- Veri seti daha homojen ve analiz odaklı hale getirilmiştir.

---

### Dosya 03 – `03_create_weekly_summary.py`
- Günlük veriler haftalık zaman dilimine dönüştürülmüştür.
- Ürün ve borsa bazında fiyatlar ortalama, işlem miktarları toplam alınmıştır.
- Veri zaman serisi analizine uygun hale getirilmiştir.

---

### Dosya 04 – `04_generate_market_coordinates.py`
- Ticaret borsalarına ait enlem ve boylam bilgileri tanımlanmıştır.
- Borsalar için coğrafi referans noktaları oluşturulmuştur.

---

### Dosya 05 – `05_fetch_warehouse_coordinates.py`
- Lisanslı depoların ilçe bilgileri kullanılarak coğrafi koordinatları elde edilmiştir.
- Depo kapasite bilgileri korunarak konumsal veri yapısı oluşturulmuştur.

---

### Dosya 06 – `06_compute_distance_and_capacity_metrics.py`
- Borsa ve depo koordinatları kullanılarak aralarındaki mesafeler hesaplanmıştır.
- Her borsa için belirli yarıçaplar (25 km, 50 km, 100 km) içinde bulunan depo sayısı belirlenmiştir.
- Aynı yarıçaplar için ortalama depo kapasitesi hesaplanarak piyasa verisiyle ilişkilendirilmiştir.
- Haftalık fiyat ve işlem verileri lojistik altyapı ile bütünleştirilmiştir.

---

### Dosya 07 – `07_filter_final_products.py`
- Veri seti yalnızca Arpa ve Buğday ürünlerini kapsayacak şekilde sınırlandırılmıştır.
- Analiz kapsamı temel ürünler üzerinde yoğunlaştırılmıştır.

---

### Dosya 08 – `08_generate_final_weekly_dataset.py`
- Ürün, borsa ve zaman bazında son düzenlemeler yapılmıştır.
- Haftalık düzeyde tekilleştirilmiş ve sadeleştirilmiş nihai veri seti oluşturulmuştur.
- Veri, istatistiksel analiz ve modelleme aşamaları için hazır hale getirilmiştir.

---

## Genel Değerlendirme

Bu çalışma kapsamında, hububat piyasasına ait fiyat ve işlem verileri
sistematik bir veri işleme sürecinden geçirilmiş ve
borsa çevresindeki lisanslı depo altyapısı ile birlikte
analiz edilebilir bütünleşik bir veri seti oluşturulmuştur.
