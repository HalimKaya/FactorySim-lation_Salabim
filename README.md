Bu proje, üretim süreçlerini simüle eden bir model içerir. salabim kütüphanesi kullanılarak makinelerin üretim süreçleri modellenmiş ve simülasyon sonunda üretim akışı görselleştirilmiştir.

🚀 Kurulum ve Kullanım
🔧 Gerekli Kütüphanelerin Kurulumu
Bu projeyi çalıştırmadan önce aşağıdaki kütüphanelerin yüklü olduğundan emin olun:

bash
Kopyala
Düzenle
pip install salabim pandas matplotlib
▶️ Simülasyonu Çalıştırma
Kod dosyasını çalıştırarak simülasyonu başlatabilirsiniz:

bash
Kopyala
Düzenle
python main.py
📊 Veri Tablosu Açıklaması ve Kullanımı
Kodun başında üretim sürecini tanımlayan bir tablo (data değişkeni) bulunmaktadır. Bu tablo, makinelerin hangi ürünü ürettiğini, üretim süresini, gerekli girdileri ve üretim akışını tanımlar.

Aşağıdaki tabloyu örnek olarak kullanabilirsiniz:

Makine	Ürettiği Ürün	Üretim Süresi (dk)	Gerekli Girdi Ürünler	Beklenen Girdi Adedi	Gönderilen Makine
A	A	1	-	-	C
B	B	1	-	-	C
C	C	1	A, B	A:2, B:1	D
D	Nihai Ürün	2	C	C:1	-
Tablodaki Alanların Açıklamaları
Makine: Üretimi gerçekleştiren makinenin adı.

Ürettiği Ürün: Bu makinenin ürettiği ürün.

Üretim Süresi: Makinenin bir ürünü üretmesi için gereken süre (dakika cinsinden).

Gerekli Girdi Ürünler: Eğer bu makine başka ürünleri işleyerek yeni bir ürün üretiyorsa, burada hangi ürünleri kullanacağı belirtilir.

Beklenen Girdi Adedi: Eğer makine, birden fazla ürünü işleyerek yeni bir ürün üretiyorsa, hangi üründen kaç adet gerektiği burada tanımlanır.

Gönderilen Makine: Üretilen ürünün hangi makineye gönderileceği belirtilir. Eğer nihai ürünse, burası None bırakılır.

📌 Tabloyu Kendi Sürecinize Göre Düzenleyebilirsiniz!
Eğer yeni makineler veya ürünler eklemek isterseniz, data değişkenini yukarıdaki yapıya uygun şekilde güncelleyebilirsiniz.

🛠 Kod İçerisindeki Fonksiyonlar ve Açıklamaları
Kodda kullanılan ana sınıflar ve fonksiyonlar aşağıda açıklanmıştır:

📌 Product Sınıfı
python
Kopyala
Düzenle
class Product(sim.Component):
    def setup(self, product_name):
        self.product_name = product_name
Bu sınıf, üretilen ürünleri temsil eder.

product_name: Ürünün adını tutar.

📌 Machine Sınıfı
python
Kopyala
Düzenle
class Machine(sim.Component):
    def setup(self, machine_name):
        self.machine_name = machine_name
        self.process_time = df.loc[df["Makine"] == machine_name, "Üretim Süresi"].values[0]
        self.required_products = df.loc[df["Makine"] == machine_name, "Gerekli Girdi Ürünler"].values[0]
        self.required_counts = df.loc[df["Makine"] == machine_name, "Beklenen Girdi Adedi"].values[0]
        self.output_product = df.loc[df["Makine"] == machine_name, "Ürettiği Ürün"].values[0]
        self.next_machine_name = df.loc[df["Makine"] == machine_name, "Gönderilen Makine"].values[0]
        self.in_queue = sim.Queue(f"{self.machine_name}_queue")
        self.production_count = 0
Makineyi oluşturur ve ilgili parametreleri alır.

Üretim süresi, gerekli girdiler, beklenen girdi miktarları, üretilecek ürün ve sonraki makine bilgileri gibi değerleri alır.

📌 process Fonksiyonu
python
Kopyala
Düzenle
def process(self):
    while True:
        if self.required_products:
            while not self._check_inputs():
                yield self.hold(1)

            for prod_name, count in self.required_counts.items():
                for _ in range(count):
                    for product in self.in_queue:
                        if product.product_name == prod_name:
                            self.in_queue.remove(product)
                            break

        start_time = env.now()
        yield self.hold(self.process_time)
        end_time = env.now()
        
        product = Product(product_name=self.output_product)
        if self.next_machine_name:
            machines[self.next_machine_name].in_queue.add(product)
Üretim işlemi burada gerçekleşir.

Eğer makine, başka girdiler gerektiriyorsa, yeterli girdi gelene kadar bekler.

Gerekli girdiler alındıktan sonra, üretim süresi kadar bekleyerek ürün oluşturur.

Üretilen ürün, bir sonraki makineye aktarılır.

📌 _check_inputs Fonksiyonu
python
Kopyala
Düzenle
def _check_inputs(self):
    if not self.required_products:
        return True
    counts = {prod: sum(1 for p in self.in_queue if p.product_name == prod) for prod in self.required_counts}
    return all(counts[prod] >= self.required_counts[prod] for prod in self.required_counts)
Makinenin üretime başlamadan önce gerekli girdileri kontrol etmesini sağlar.

Eğer gerekli ürünler yeterli miktarda sıraya girdiyse, üretim başlar.

📈 Çıktılar ve Analizler
Simülasyon çalıştırıldığında 4 farklı grafik oluşturulur:

1️⃣ Gantt Diyagramı
Üretim süreçlerinin ne zaman başladığını ve bittiğini gösterir.

2️⃣ Buffer (Bekleyen Ürün) Durumu
Makinelerin önünde biriken ürün miktarını zaman içinde gösterir.

3️⃣ Toplam Üretim Grafiği
Zamanla üretilen toplam ürün miktarını görselleştirir.

4️⃣ Makine Kullanım Oranı
Her makinenin ne kadar çalıştığını ve ne kadar boşta kaldığını gösterir.

Yeşil = Aktif Çalışma Süresi

Kırmızı = Boşta Kalma Süresi

🔍 Örnek Simülasyon Çıktısı
bash
Kopyala
Düzenle
5 dk: A makinesi A üretti.
6 dk: B makinesi B üretti.
7 dk: C makinesi C üretti.
9 dk: D makinesi Nihai Ürün üretti.
Bu çıktılar, makinelerin belirli zamanlarda üretim yaptığını gösterir.

✨ Gelecekteki Geliştirmeler
Daha karmaşık üretim hatları eklenebilir.

Stok ve depo yönetimi entegre edilebilir.

Üretim hatlarının verimliliğini artırmak için optimizasyon çalışmaları yapılabilir.

📌 Kendi üretim sürecinizi simüle etmek için tabloları değiştirerek testler yapabilirsiniz!

📞 İletişim ve Katkı
Bu projeye katkıda bulunmak isterseniz pull request gönderebilirsiniz!

🚀 İyi simülasyonlar!







