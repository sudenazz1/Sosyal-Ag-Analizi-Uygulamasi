import json
import csv
from node import Node
from edge import Edge

class SocialGraph:
    def __init__(self):
        self.nodes = {} 
        self.edges = [] 
        self.adjacency_list = {} 

    def add_node(self, node):
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []

    def remove_node(self, node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]
            del self.adjacency_list[node_id]
            # Bu düğüme bağlı kenarları temizle
            self.edges = [e for e in self.edges if e.source.id != node_id and e.target.id != node_id]
            # Komşuluk listelerinden temizle
            for nid in self.adjacency_list:
                if node_id in self.adjacency_list[nid]:
                    self.adjacency_list[nid].remove(node_id)

    def update_node(self, node_id, new_name, new_aktiflik, new_etkilesim=None):
        """Düğüm güncelleme - etkilesim parametresi eklendi"""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.name = new_name
            node.aktiflik = float(new_aktiflik)
            if new_etkilesim is not None:
                node.etkilesim = float(new_etkilesim)
            # Ağırlıklar değişeceği için kenarları güncelle
            for edge in self.edges:
                if edge.source.id == node_id or edge.target.id == node_id:
                    edge.weight = edge.calculate_weight()

    def add_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            if id1 == id2: return  # Self-loop engelle
            if id2 in self.adjacency_list[id1]: return  # Duplicate engelle

            n1 = self.nodes[id1]
            n2 = self.nodes[id2]
            
            # ✅ Bağlantı sayılarını hesapla (edge eklenmeden ÖNCE)
            baglanti_1 = len(self.adjacency_list.get(id1, []))
            baglanti_2 = len(self.adjacency_list.get(id2, []))
            
            # Edge'i bağlantı sayılarıyla oluştur
            new_edge = Edge(n1, n2, baglanti_1, baglanti_2)
            self.edges.append(new_edge)
            
            self.adjacency_list[id1].append(id2)
            self.adjacency_list[id2].append(id1)

    def remove_edge(self, id1, id2):
        """Bağlantı silme"""
        self.edges = [e for e in self.edges if not (
            (e.source.id == id1 and e.target.id == id2) or 
            (e.source.id == id2 and e.target.id == id1)
        )]
        if id1 in self.adjacency_list and id2 in self.adjacency_list[id1]:
            self.adjacency_list[id1].remove(id2)
        if id2 in self.adjacency_list and id1 in self.adjacency_list[id2]:
            self.adjacency_list[id2].remove(id1)

    def get_edge_weight(self, id1, id2):
        for edge in self.edges:
            if (edge.source.id == id1 and edge.target.id == id2) or \
               (edge.source.id == id2 and edge.target.id == id1):
                return edge.weight
        return float('inf')

    def load_from_csv(self, filename):
        """CSV'den veri yükleme - BaglantiSayisi artık opsiyonel"""
        self.nodes = {}
        self.edges = []
        self.adjacency_list = {}
        
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                
                # Önce tüm düğümleri oluştur
                for row in rows:
                    try:
                        nid = int(row['DugumId'])
                        # Node artık 4 parametre alıyor (baglanti_sayisi yok)
                        new_node = Node(
                            nid, 
                            row['Ad'], 
                            row['Aktiflik'], 
                            row['Etkilesim']
                        )
                        self.add_node(new_node)
                    except (ValueError, KeyError) as e:
                        print(f"Düğüm oluşturma hatası: {e}")
                        continue
                
                # Sonra kenarları ekle
                for row in rows:
                    try:
                        src_id = int(row['DugumId'])
                        komsular_str = row.get('Komsular', '').replace('"', '').strip()
                        
                        if komsular_str:
                            komsular = komsular_str.split(',')
                            for k in komsular:
                                k = k.strip()
                                if k and k.isdigit():
                                    neighbor_id = int(k)
                                    if neighbor_id in self.nodes:
                                        self.add_edge(src_id, neighbor_id)
                    except (ValueError, KeyError) as e:
                        print(f"Kenar ekleme hatası: {e}")
                        continue
                        
            return True
            
        except FileNotFoundError:
            return "Dosya bulunamadı!"
        except Exception as e:
            return f"Hata: {str(e)}"

    def save_to_csv(self, filename):
        """
        ✅ DÜZELTİLMİŞ: CSV'ye kaydetme - BaglantiSayisi dinamik hesaplanıyor
        PDF formatına uygun: DugumId,Ad,Aktiflik,Etkilesim,BaglantiSayisi,Komsular
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Başlıklar
                writer.writerow(['DugumId', 'Ad', 'Aktiflik', 'Etkilesim', 'BaglantiSayisi', 'Komsular'])
                
                # Her düğüm için
                for node_id in sorted(self.nodes.keys()):
                    node = self.nodes[node_id]
                    
                    # Komşuları al
                    komsular = self.adjacency_list.get(node_id, [])
                    
                    # ✅ Bağlantı sayısını dinamik hesapla
                    baglanti_sayisi = len(komsular)
                    
                    # Komşuları string'e çevir
                    if komsular:
                        komsular_str = ','.join(map(str, sorted(komsular)))
                    else:
                        komsular_str = ''
                    
                    # Satırı yaz
                    writer.writerow([
                        node_id,
                        node.name,
                        node.aktiflik,
                        node.etkilesim,
                        baglanti_sayisi,
                        f'"{komsular_str}"' if komsular_str else ''  # Virgüllü liste için tırnak
                    ])
            
            return True
            
        except Exception as e:
            print(f"CSV kaydetme hatası: {str(e)}")
            return False

    def save_to_json(self, filename="graph_data.json"):
        """JSON'a kaydetme"""
        data = {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [
                {
                    "source": e.source.id, 
                    "target": e.target.id, 
                    "weight": e.weight
                } for e in self.edges
            ]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)