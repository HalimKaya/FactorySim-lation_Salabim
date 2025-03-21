 Kod Açıklamaları
Kodda üç temel bileşen bulunmaktadır:

1️⃣ Product (Ürün) Sınıfı
Üretim sürecinde makineler tarafından üretilen ürünleri temsil eder.

python

class Product(sim.Component):
    def setup(self, product_name):
        self.product_name = product_name
📌 Üretilen her ürün bu sınıftan bir nesne olarak oluşturulur.

2️⃣ Machine (Makine) Sınıfı
Her makine, belirli bir ürünü üretmek için çalışır. Gerekli giriş ürünleri varsa, bunlar gelene kadar bekler.

python

class Machine(sim.Component):
    def setup(self, machine_name):
        ...
📌 Makine, üretime başlamadan önce gerekli girdilerin geldiğini kontrol eder.

Makine İşleyişi
python

def process(self):
    while True:
        yield self.hold(self.process_time)  # Üretim süresi kadar bekle
        product = Product(product_name=self.output_product)  # Yeni ürün oluştur
