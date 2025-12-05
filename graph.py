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

    def update_node(self, node_id, new_name, new_aktiflik):
        # Düğüm Güncelleme
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.name = new_name
            node.aktiflik = float(new_aktiflik)
            # Ağırlıklar değişeceği için kenarları güncelle
            for edge in self.edges:
                if edge.source.id == node_id or edge.target.id == node_id:
                    edge.weight = edge.calculate_weight()

    def add_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            if id1 == id2: return 
            if id2 in self.adjacency_list[id1]: return

            n1 = self.nodes[id1]
            n2 = self.nodes[id2]
            new_edge = Edge(n1, n2)
            self.edges.append(new_edge)
            
            self.adjacency_list[id1].append(id2)
            self.adjacency_list[id2].append(id1)

    def remove_edge(self, id1, id2):
        #  Bağlantı Silme
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
        self.nodes = {}
        self.edges = []
        self.adjacency_list = {}
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows:
                    try:
                        nid = int(row['DugumId'])
                        new_node = Node(nid, row['Ad'], row['Aktiflik'], row['Etkilesim'], row['BaglantiSayisi'])
                        self.add_node(new_node)
                    except ValueError: continue
                for row in rows:
                    src_id = int(row['DugumId'])
                    komsular = row['Komsular'].replace('"', '').split(',')
                    for k in komsular:
                        if k.strip() and int(k.strip()) in self.nodes:
                            self.add_edge(src_id, int(k.strip()))
            return True
        except Exception as e:
            return str(e)

    def save_to_json(self, filename="graph_data.json"):
        data = {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [{"source": e.source.id, "target": e.target.id, "weight": e.weight} for e in self.edges]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)