Bu proje, üretim süreçlerini simüle eden bir model içerir. salabim kütüphanesi kullanılarak makinelerin üretim süreçleri modellenmiş ve simülasyon sonunda üretim akışı görselleştirilmiştir.

🚀 Kurulum ve Kullanım
🔧 Gerekli Kütüphanelerin Kurulumu
Bu projeyi çalıştırmadan önce aşağıdaki kütüphanelerin yüklü olduğundan emin olun:

pip install salabim pandas matplotlib

▶️ Simülasyonu Çalıştırma
Kod dosyasını çalıştırarak simülasyonu başlatabilirsiniz:

#python main.py

📊 Veri Tablosu Açıklaması ve Kullanımı
Kodun başında üretim sürecini tanımlayan bir tablo (data değişkeni) bulunmaktadır. Bu tablo, makinelerin hangi ürünü ürettiğini, üretim süresini, gerekli girdileri ve üretim akışını tanımlar.

Aşağıdaki tabloyu örnek olarak kullanabilirsiniz:

## 📊 Üretim Tablosu

| Makine | Ürettiği Ürün | Üretim Süresi (dk) | Gerekli Girdi Ürünler | Beklenen Girdi Adedi | Gönderilen Makine |
|--------|--------------|--------------------|----------------------|---------------------|-------------------|
| A      | A            | 1                  | -                    | -                   | C                 |
| B      | B            | 1                  | -                    | -                   | C                 |
| C      | C            | 1                  | A, B                 | A:2, B:1            | D                 |
| D      | Nihai Ürün   | 2                  | C                    | C:1                 | -                 |

