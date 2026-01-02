**Sosyal Ağ Analizi ve Görselleştirme Aracı**

**Ders:** Yazılım Geliştirme Laboratuvarı I – Proje 2

**Tarih:** 2 Ocak 2026

**Geliştiriciler:** [Sude Naz Lekesiz] , [Fatma Nilay Süzer]

1. Proje Özeti ve Amacı

Bu proje, kullanıcılar arasındaki ilişkileri bir graf yapısı olarak modelleyen, bu ilişkiler üzerinde çeşitli algoritmalar çalıştıran ve sonuçları etkileşimli bir grafik arayüz (GUI) üzerinde görselleştiren bir masaüstü uygulamasıdır.

Projenin temel amacı; Nesne Yönelimli Programlama (OOP) prensiplerine sadık kalarak, graf teorisi algoritmalarını (BFS, DFS, Dijkstra, A* vb.) gerçek hayat senaryosuna uygun bir sosyal ağ modeli üzerinde uygulamaktır.

Uygulama, düğümlerin aktiflik ve etkileşim puanlarına göre dinamik ağırlık hesaplaması yaparak statik olmayan, yaşayan bir ağ yapısı sunar.

2. Kullanılan Teknolojiler ve Mimari

Programlama Dili: Python

Arayüz: Tkinter

Görselleştirme: Canvas

Sınıf Yapısı (Class Diagram)

Proje, OOP prensiplerine uygun olarak modüler bir yapıda tasarlanmıştır. Aşağıdaki diyagram sınıflar arasındaki ilişkileri göstermektedir:

classDiagram
    class Node {
        +int id
        +str name
        +float aktiflik
        +float etkilesim
        +to_dict()
    }
    class Edge {
        +Node source
        +Node target
        +float weight
        +calculate_weight()
    }
    class SocialGraph {
        +dict nodes
        +list edges
        +dict adjacency_list
        +add_node()
        +add_edge()
        +save_to_csv()
    }
    class Algorithms {
        +bfs()
        +dfs()
        +dijkstra()
        +a_star()
        +welsh_powell()
    }
    class App {
        +tk.Tk root
        +setup_ui()
        +draw_graph()
    }

    SocialGraph *-- Node
    SocialGraph *-- Edge
    App o-- SocialGraph
    App ..> Algorithms : uses

3. Gerçeklenen Algoritmalar ve Analizler

Uygulama içerisinde aşağıdaki algoritmalar ve analiz yöntemleri entegre edilmiştir:

3.1. Yol Bulma Algoritmaları

BFS (Breadth-First Search):
Ağ üzerindeki düğümleri genişlemesine arar. En az kenar sayısına sahip yolu bulmak ve ağın bağlantı durumunu kontrol etmek için kullanılır.

DFS (Depth-First Search):
Ağın derinliklerine inerek arama yapar. Bağlı bileşenlerin tespiti ve döngü kontrolü için kullanılmıştır.

Dijkstra:
İki kullanıcı arasındaki en düşük maliyetli yolu bulur. Kenar ağırlıkları kullanıcı benzerliklerine göre dinamik hesaplanır.

A* (A-Star):
Dijkstra’nın optimize edilmiş halidir. Aktiflik puanı farkı, sezgisel (heuristic) fonksiyon olarak kullanılır.

3.2. Ağ Analizi ve Görselleştirme

Merkezilik Analizi (Degree Centrality):
Ağdaki en popüler ve etkileşimi en yüksek kullanıcıları tespit eder.

Topluluk Tespiti (Connected Components):
Birbirinden kopuk kullanıcı gruplarını analiz eder.

Welsh-Powell Renklendirme:
Komşu düğümlerin farklı renkte olmasını sağlayarak grafın görsel karmaşıklığını azaltır.

4. Dinamik Ağırlık Hesaplama

İki düğüm arasındaki kenar ağırlığı sabit değildir. Aşağıdaki formülle hesaplanır:

$$Ağırlık_{i,j} = 1 + \sqrt{(Aktiflik_i - Aktiflik_j)^2 + (Etkileşim_i - Etkileşim_j)^2 + (Bağlantı_i - Bağlantı_j)^2}$$​

Mantık:
Özellikleri birbirine benzeyen kullanıcılar arasındaki mesafe küçüktür → ağırlık düşüktür.
Benzer olmayan kullanıcılar → daha yüksek ağırlık.

5. Kurulum ve Çalıştırma
Gereksinimler

Python 3.x

Standart kütüphaneler: math, random, csv, json, tkinter

(Opsiyonel) Ekran görüntüsü için:

pip install Pillow

Çalıştırma Adımları
python main.py


Uygulama açıldığında sol menüden CSV Yükle butonuna basarak veriler.csv dosyasını yükleyin.

6. Sonuç ve Değerlendirme

Bu proje kapsamında, graf algoritmaları somut bir sosyal ağ senaryosu üzerinde başarıyla uygulanmıştır.
Dinamik ağırlıklandırma sayesinde ağ yapısının yalnızca topolojik değil, kullanıcı özelliklerine göre de değiştiği gözlemlenmiştir.

Performans testlerinde 100 düğüme kadar olan ağlarda algoritmaların milisaniye seviyesinde sonuç verdiği görülmüştür.
Tkinter Canvas kullanılarak uygulanan Force-Directed yerleşim, karmaşık ağların görsel olarak daha anlaşılır olmasını sağlamıştır.