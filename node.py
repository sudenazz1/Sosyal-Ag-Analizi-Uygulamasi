class Node:
    """
    Sosyal ağ düğümünü temsil eden sınıf.
    baglanti_sayisi artık dinamik olarak graph'tan hesaplanacak.
    """
    def __init__(self, user_id, name, aktiflik, etkilesim):
        self.id = int(user_id)
        self.name = name
        self.aktiflik = float(aktiflik)      # Ozellik I
        self.etkilesim = float(etkilesim)    # Ozellik II
        # baglanti_sayisi kaldırıldı - Graph sınıfı tarafından dinamik hesaplanacak
    
    def to_dict(self):
        """Node'u JSON formatına çevir"""
        return {
            "id": self.id,
            "name": self.name,
            "aktiflik": self.aktiflik,
            "etkilesim": self.etkilesim
        }
    
    def __repr__(self):
        return f"Node(id={self.id}, name='{self.name}')"