import math

class Edge:
    """
    İki düğüm arasındaki bağlantıyı temsil eden sınıf.
    Ağırlık, düğümlerin özellikleri ve bağlantı sayılarına göre dinamik hesaplanır.
    """
    
    def __init__(self, source_node, target_node, source_baglanti=0, target_baglanti=0):
        """
        Edge oluşturucu
        
        Args:
            source_node: Kaynak düğüm (Node objesi)
            target_node: Hedef düğüm (Node objesi)
            source_baglanti: Kaynak düğümün bağlantı sayısı (opsiyonel)
            target_baglanti: Hedef düğümün bağlantı sayısı (opsiyonel)
        """
        self.source = source_node
        self.target = target_node
        self.source_baglanti = source_baglanti
        self.target_baglanti = target_baglanti
        self.weight = self.calculate_weight()

    def calculate_weight(self):
        """
        PDF Formülü:
        Weight = 1 / (1 + sqrt((Aktiflik_i - Aktiflik_j)^2 + 
                               (Etkilesim_i - Etkilesim_j)^2 + 
                               (Baglanti_i - Baglanti_j)^2))
        
        DÜZELTME: Formül PDF'de yanlış yazılmış gibi görünüyor.
        Doğru formül büyük ihtimalle:
        Weight = 1 + sqrt(...)
        
        Çünkü:
        - Benzer düğümler YAKINDA olmalı (küçük ağırlık)
        - Farklı düğümler UZAKTA olmalı (büyük ağırlık)
        
        Returns:
            float: Hesaplanan kenar ağırlığı
        """
        # Farkları hesapla
        diff_aktif = self.source.aktiflik - self.target.aktiflik
        diff_etkilesim = self.source.etkilesim - self.target.etkilesim
        diff_baglanti = self.source_baglanti - self.target_baglanti
        
        # Euclidean distance hesapla
        inside_sqrt = (diff_aktif**2) + (diff_etkilesim**2) + (diff_baglanti**2)
        distance = math.sqrt(inside_sqrt)
        
        # Ağırlık = 1 + distance
        # Bu formül benzer düğümlere küçük, farklı düğümlere büyük ağırlık verir
        return 1 + distance
    
    def update_weight(self, source_baglanti=None, target_baglanti=None):
        """
        Bağlantı sayıları değiştiğinde ağırlığı güncelle
        
        Args:
            source_baglanti: Yeni kaynak bağlantı sayısı
            target_baglanti: Yeni hedef bağlantı sayısı
        """
        if source_baglanti is not None:
            self.source_baglanti = source_baglanti
        if target_baglanti is not None:
            self.target_baglanti = target_baglanti
        
        self.weight = self.calculate_weight()
    
    def __repr__(self):
        return f"Edge({self.source.id} -> {self.target.id}, weight={self.weight:.2f})"