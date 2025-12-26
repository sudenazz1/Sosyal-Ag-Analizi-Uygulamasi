NODE.PY
class Node:
    def __init__(self, user_id, name, aktiflik, etkilesim, baglanti_sayisi):
        self.id = int(user_id)
        self.name = name
        self.aktiflik = float(aktiflik)      # Ozellik I
        self.etkilesim = float(etkilesim)    # Ozellik II
        self.baglanti_sayisi = int(baglanti_sayisi) # Ozellik III
    
    def to_dict(self):
        return {
            "id": self.id, "name": self.name,
            "aktiflik": self.aktiflik, "etkilesim": self.etkilesim,
            "baglanti_sayisi": self.baglanti_sayisi
        }
    
    