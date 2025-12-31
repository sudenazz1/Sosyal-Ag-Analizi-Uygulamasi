import csv
import random

def generate_test_csv(filename, num_nodes, connection_probability=0.3):
    """
    Test için rastgele graf CSV'si oluşturur
    
    Args:
        filename: Kaydedilecek dosya adı
        num_nodes: Düğüm sayısı (10-20 için küçük, 50-100 için orta)
        connection_probability: İki düğüm arasında bağlantı olma olasılığı
    """
    
    # İsim havuzu
    names = [
        "Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Veli", "Zeynep", "Elif",
        "Mustafa", "Hüseyin", "Emine", "Hatice", "Can", "Cem", "Deniz", "Ege",
        "Selin", "Ömer", "Yusuf", "İbrahim", "Esra", "Merve", "Burak", "Kemal",
        "Leyla", "Murat", "Serkan", "Tuğba", "Gökhan", "Emre", "Berna", "Canan",
        "Derya", "Ebru", "Ferhat", "Gizem", "Hakan", "İpek", "Jale", "Kerem",
        "Lale", "Melisa", "Nalan", "Onur", "Pelin", "Rıza", "Seda", "Taner",
        "Umut", "Volkan", "Yasemin", "Zafer", "Ayla", "Bülent", "Ceren", "Dilek",
        "Erdem", "Funda", "Gülay", "Hande", "İrem", "Kaan", "Leman", "Metin",
        "Nilüfer", "Okan", "Perihan", "Ramazan", "Sevgi", "Tolga", "Ufuk", "Vildan",
        "Yakup", "Zühal", "Adem", "Beste", "Cem", "Dilara", "Eren", "Fulya",
        "Gonca", "Halil", "İlknur", "Kadir", "Leman", "Mete", "Neslihan", "Orhan",
        "Pınar", "Recep", "Sibel", "Tayfun", "Ülkü", "Vedat", "Yıldız", "Zeki"
    ]
    
    # Düğümleri oluştur
    nodes = []
    for i in range(1, num_nodes + 1):
        name = names[(i - 1) % len(names)] + str(i // len(names) + 1 if i > len(names) else "")
        aktiflik = round(random.uniform(0.1, 1.0), 2)
        etkilesim = random.randint(1, 50)
        
        nodes.append({
            'id': i,
            'name': name,
            'aktiflik': aktiflik,
            'etkilesim': etkilesim,
            'neighbors': []
        })
    
    # Bağlantılar oluştur (rastgele ama bağlı graf garantisi)
    # Önce her düğümün en az 1 bağlantısı olsun
    for i in range(num_nodes - 1):
        nodes[i]['neighbors'].append(i + 2)  # Bir sonraki düğüme bağla
        nodes[i + 1]['neighbors'].append(i + 1)  # Karşılıklı
    
    # Rastgele ek bağlantılar
    for i in range(num_nodes):
        for j in range(i + 2, num_nodes + 1):  # i+2 çünkü zaten i+1'e bağlı
            if random.random() < connection_probability:
                if j not in nodes[i]['neighbors']:
                    nodes[i]['neighbors'].append(j)
                if (i + 1) not in nodes[j - 1]['neighbors']:
                    nodes[j - 1]['neighbors'].append(i + 1)
    
    # CSV'ye yaz
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['DugumId', 'Ad', 'Aktiflik', 'Etkilesim', 'BaglantiSayisi', 'Komsular'])
        
        for node in nodes:
            baglanti_sayisi = len(node['neighbors'])
            komsular_str = ','.join(map(str, sorted(node['neighbors'])))
            
            writer.writerow([
                node['id'],
                node['name'],
                node['aktiflik'],
                node['etkilesim'],
                baglanti_sayisi,
                f'"{komsular_str}"' if komsular_str else ''
            ])
    
    print(f"✅ {filename} oluşturuldu - {num_nodes} düğüm")
    print(f"   Toplam bağlantı: {sum(len(n['neighbors']) for n in nodes) // 2}")
    print(f"   Ortalama derece: {sum(len(n['neighbors']) for n in nodes) / num_nodes:.2f}")


def generate_all_test_files():
    """Tüm test dosyalarını oluştur"""
    print("🔧 Test grafları oluşturuluyor...\n")
    
    # Küçük graf - 10 düğüm
    generate_test_csv('test_small_10.csv', 10, connection_probability=0.4)
    print()
    
    # Küçük graf - 20 düğüm
    generate_test_csv('test_small_20.csv', 20, connection_probability=0.3)
    print()
    
    # Orta graf - 50 düğüm
    generate_test_csv('test_medium_50.csv', 50, connection_probability=0.15)
    print()
    
    # Orta graf - 100 düğüm
    generate_test_csv('test_medium_100.csv', 100, connection_probability=0.1)
    print()
    
    # Yoğun küçük graf - stres testi için
    generate_test_csv('test_dense_15.csv', 15, connection_probability=0.6)
    print()
    
    print("✅ Tüm test dosyaları oluşturuldu!")
    print("\nKullanım: Bu CSV dosyalarını uygulamanıza yükleyerek test edebilirsiniz.")


if __name__ == "__main__":
    generate_all_test_files()