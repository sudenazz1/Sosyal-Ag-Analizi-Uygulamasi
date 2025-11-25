EDGE.PY
import math

class Edge:
    def __init__(self, source_node, target_node):
        self.source = source_node
        self.target = target_node
        self.weight = self.calculate_weight()

    def calculate_weight(self):
        # PDF Formülü
        diff_aktif = self.source.aktiflik - self.target.aktiflik
        diff_etkilesim = self.source.etkilesim - self.target.etkilesim
        diff_baglanti = self.source.baglanti_sayisi - self.target.baglanti_sayisi
        
        inside_sqrt = (diff_aktif**2) + (diff_etkilesim**2) + (diff_baglanti**2)
        return 1 + math.sqrt(inside_sqrt)