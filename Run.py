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

# Tabloyu DataFrame olarak oluştur
df = pd.DataFrame(data)

# Üretim kayıtlarını tutmak için liste
production_log = []

# Buffer miktarlarını kaydetmek için log
buffer_log = {machine: [] for machine in df["Makine"]}

# Makinelerin ürettiği toplam ürün sayısını tutan log
production_count_log = {machine: [] for machine in df["Makine"]}

# Makine kullanım oranlarını kaydetmek için log
machine_usage_log = {machine: {"total_time": 0, "active_time": 0} for machine in df["Makine"]}

class Product(sim.Component):
    def setup(self, product_name):
        self.product_name = product_name

class Machine(sim.Component):
    def setup(self, machine_name):
        self.machine_name = machine_name
        self.process_time = df.loc[df["Makine"] == machine_name, "Üretim Süresi"].values[0]
        self.required_products = df.loc[df["Makine"] == machine_name, "Gerekli Girdi Ürünler"].values[0]
        self.required_counts = df.loc[df["Makine"] == machine_name, "Beklenen Girdi Adedi"].values[0]
        self.output_product = df.loc[df["Makine"] == machine_name, "Ürettiği Ürün"].values[0]
        self.next_machine_name = df.loc[df["Makine"] == machine_name, "Gönderilen Makine"].values[0]
        self.in_queue = sim.Queue(f"{self.machine_name}_queue")
        self.production_count = 0  # Bu makinenin ürettiği toplam ürün sayısı

    def process(self):
        while True:
            # Buffer miktarını kaydet
            buffer_log[self.machine_name].append((env.now(), len(self.in_queue)))
            
            # Eğer giriş ürünü gerekiyorsa, yeterli malzeme gelene kadar bekle
            if self.required_products:
                while not self._check_inputs():
                    yield self.hold(1)  # Bekleme süresi

                # Gerekli ürünleri sıradan çek
                for prod_name, count in self.required_counts.items():
                    for _ in range(count):
                        for product in self.in_queue:
                            if product.product_name == prod_name:
                                self.in_queue.remove(product)
                                break

            # Üretim başlangıcını kaydet
            start_time = env.now()
            
            # Üretim süresini bekle
            yield self.hold(self.process_time)

            # Üretim bitişini kaydet
            end_time = env.now()
            production_log.append((self.machine_name, start_time, end_time))
            
            # Toplam üretim sayısını artır
            self.production_count += 1
            production_count_log[self.machine_name].append((env.now(), self.production_count))

            # Makine kullanım sürelerini kaydet
            machine_usage_log[self.machine_name]["active_time"] += (end_time - start_time)
            machine_usage_log[self.machine_name]["total_time"] = env.now()

            # Yeni ürün oluştur ve sonraki makinaya gönder
            product = Product(product_name=self.output_product)
            if self.next_machine_name:
                machines[self.next_machine_name].in_queue.add(product)

            print(f"{env.now()} dk: {self.machine_name} makinesi {self.output_product} üretti.")

    def _check_inputs(self):
        if not self.required_products:
            return True
        counts = {prod: sum(1 for p in self.in_queue if p.product_name == prod) for prod in self.required_counts}
        return all(counts[prod] >= self.required_counts[prod] for prod in self.required_counts)

env = sim.Environment(time_unit="minutes")

# Makineleri tablodan oluştur
machines = {row["Makine"]: Machine(machine_name=row["Makine"]) for _, row in df.iterrows()}

# Simülasyonu başlat
env.run(till=30)

# Tek bir pencere içinde dört grafiği göstermek için subplots kullanıyoruz
fig, axs = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid

# 1. Gantt Diyagramı
ax = axs[0, 0]
for machine_name, start, end in production_log:
    ax.barh(machine_name, end - start, left=start, color="skyblue", edgecolor="black")
ax.set_xlabel("Zaman (Dakika)")
ax.set_ylabel("Makine")
ax.set_title("Üretim Süreci Gantt Diyagramı")
ax.grid(axis="x", linestyle="--", alpha=0.7)

# 2. Buffer Durumu
ax = axs[0, 1]
for machine, buffer_data in buffer_log.items():
    times = [entry[0] for entry in buffer_data]
    counts = [entry[1] for entry in buffer_data]
    ax.plot(times, counts, label=machine)
ax.set_xlabel("Zaman (Dakika)")
ax.set_ylabel("Buffer'daki Ürün Sayısı")
ax.set_title("Makine Buffer Durumu")
ax.legend()
ax.grid(True)

# 3. Zamanla Üretilen Ürün Sayısı
ax = axs[1, 0]
for machine_name, log in production_count_log.items():
    times = [entry[0] for entry in log]
    production_count = [entry[1] for entry in log]
    ax.plot(times, production_count, label=machine_name)
ax.set_xlabel("Zaman (Dakika)")
ax.set_ylabel("Toplam Üretilen Ürün Sayısı")
ax.set_title("Zamanla Toplam Üretilen Ürün Sayısı")
ax.legend()
ax.grid(True)

# 4. Makine Kullanım Oranı
ax = axs[1, 1]
for machine_name, usage_data in machine_usage_log.items():
    total_time = usage_data["total_time"]
    active_time = usage_data["active_time"]
    usage_rate = active_time / total_time if total_time > 0 else 0
    ax.bar(machine_name, usage_rate*100, color='Green')  # Kullanım oranı
    ax.bar(machine_name, 100 - usage_rate*100, bottom=usage_rate*100, color='red')  # Boşta kalma oranı
ax.set_xlabel("Makine")
ax.set_ylabel("Oran (1 = %100)")
ax.set_title("Makine Kullanım Oranı (Yeşil: Kullanım, Kırmızı: Boşta)")
ax.set_ylim(0, 100)
ax.grid(True, axis="y", linestyle="--", alpha=0.7)

# Layout'ı düzenle
plt.tight_layout()

# Grafikleri göster
plt.show()
