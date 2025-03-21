Bu proje, üretim süreçlerini simüle eden bir model içerir. salabim kütüphanesi kullanılarak makinelerin üretim süreçleri modellenmiş ve simülasyon sonunda üretim akışı görselleştirilmiştir.

🚀 Kurulum ve Kullanım
🔧 Gerekli Kütüphanelerin Kurulumu
Bu projeyi çalıştırmadan önce aşağıdaki kütüphanelerin yüklü olduğundan emin olun:

'''pip install salabim pandas matplotlib'''

▶️ Simülasyonu Çalıştırma
Kod dosyasını çalıştırarak simülasyonu başlatabilirsiniz:

'''python main.py'''

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




## 🔧 Üretim Simülasyonu Kodu

Aşağıdaki Python kodu, üretim süreçlerini simüle etmek için **salabim** kütüphanesini kullanır.  
Grafiklerle üretim sürecini, buffer (ara stok) durumunu ve makine verimliliğini analiz etmektedir.

```python
import salabim as sim
import pandas as pd
import matplotlib.pyplot as plt

sim.yieldless(False)  # selects not yieldless

# Üretim sürecini tanımlayan tablo
data = {
    "Makine": ["A", "B", "C", "D"],
    "Ürettiği Ürün": ["A", "B", "C", "Nihai Ürün"],
    "Üretim Süresi": [1, 1, 1, 2],
    "Gerekli Girdi Ürünler": [None, None, ["A", "B"], ["C"]],
    "Beklenen Girdi Adedi": [None, None, {"A": 2, "B": 1}, {"C": 1}],
    "Gönderilen Makine": ["C", "C", "D", None],
}

df = pd.DataFrame(data)

class Machine(sim.Component):
    def setup(self, machine_name):
        self.machine_name = machine_name
        self.process_time = df.loc[df["Makine"] == machine_name, "Üretim Süresi"].values[0]

    def process(self):
        while True:
            yield self.hold(self.process_time)
            print(f"{env.now()} dk: {self.machine_name} makinesi üretimi tamamladı.")

env = sim.Environment(time_unit="minutes")
machines = {row["Makine"]: Machine(machine_name=row["Makine"]) for _, row in df.iterrows()}
env.run(till=30)
