Sosyal Ağ Analizi ve Görselleştirme Aracı
Ders: Yazılım Geliştirme Laboratuvarı I - Proje 2
Tarih: 2 Ocak 2026
Geliştiriciler: [Sude Naz Lekesiz], [Fatma Nilay Süzer]

   1. Proje Özeti ve Amacı
   Bu proje, kullanıcılar arasındaki ilişkileri bir graf yapısı olarak modelleyen, bu ilişkiler üzerinde çeşitli algoritmalar çalıştıran ve sonuçları etkileşimli bir arayüz (GUI) üzerinde görselleştiren bir masaüstü uygulamasıdır.
   
   Projenin temel amacı; Nesne Yönelimli Programlama (OOP) prensiplerine sadık kalarak, graf teorisi algoritmalarını (BFS, DFS, Dijkstra, A*, vb.) gerçek hayat senaryosuna uygun bir "Sosyal Ağ" modeli üzerinde uygulamaktır. Uygulama, düğümlerin (kullanıcıların) aktiflik ve etkileşim puanlarına göre dinamik ağırlık hesaplaması yaparak statik olmayan, yaşayan bir ağ yapısı sunmaktadır.
   
   2. Kullanılan Teknolojiler ve Mimari
   Proje Python dili kullanılarak geliştirilmiştir. Arayüz için Tkinter, veri görselleştirme ve çizim işlemleri için Canvas yapısı kullanılmıştır.
   
   Sınıf Yapısı (Class Diagram):
   Proje, OOP prensiplerine uygun olarak modüler bir yapıda tasarlanmıştır. Aşağıdaki diyagram sınıflar arasındaki ilişkiyi göstermektedir:
   
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
    BFS (Breadth-First Search): Ağ üzerindeki düğümleri genişlemesine arar. Düğümler arası en az kenar sayısına sahip yolu bulmak veya ağın bağlantı durumunu kontrol etmek için kullanılır.
    
    DFS (Depth-First Search): Ağın derinliklerine inerek arama yapar. Bağlı bileşenlerin tespiti ve döngü kontrolü gibi işlemlerde altyapı olarak kullanılmıştır.
    
    Dijkstra: İki kullanıcı arasındaki en kısa yolu (en düşük maliyetli) bulur. Maliyet hesabı, kullanıcılar arasındaki "benzerlik" durumuna göre dinamik hesaplanan kenar ağırlıklarına dayanır.
    
    *A (A-Star):** Dijkstra'nın optimize edilmiş halidir. Hedefe ulaşmak için "Aktiflik Puanı Farkı"nı bir sezgisel (heuristic) fonksiyon olarak kullanır ve aramayı hedefe yönlendirir.
    
    3.2. Ağ Analizi ve Görselleştirme
    Merkezilik Analizi (Degree Centrality): Ağdaki en popüler ve etkileşimi en yüksek kullanıcıları (influencer) tespit eder. En yüksek dereceye sahip 5 düğüm raporda listelenir.
    
    Topluluk Tespiti (Connected Components): Birbirinden kopuk arkadaş gruplarını veya izole toplulukları analiz eder.
    
    Welsh-Powell Renklendirme: Birbirine komşu olan düğümlerin farklı renklere sahip olmasını garanti ederek grafı en az sayıda renk ile boyar. Bu, görsel karmaşıklığı azaltmak için kullanılmıştır.
    
    4. Dinamik Ağırlık Hesaplama
    Projede iki düğüm arasındaki kenar ağırlığı (maliyet) sabit değildir. Kullanıcıların Aktiflik, Etkileşim ve Bağlantı Sayısı özelliklerine göre şu formülle hesaplanır:
    
    $$Ağırlık_{i,j} = 1 + \sqrt{(Aktiflik_i - Aktiflik_j)^2 + (Etkileşim_i - Etkileşim_j)^2 + (Bağlantı_i - Bağlantı_j)^2}$$
    Mantık: Özellikleri birbirine benzeyen kullanıcılar arasındaki "mesafe" (fark) azdır, dolayısıyla ağırlık düşüktür. Benzer olmayan kullanıcılar arasındaki ağırlık ise yüksektir.

    5. Kurulum ve Çalıştırma
    Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.Gereksinimler:
    Python 3.xKütüphaneler: Standart kütüphaneler (math, random, csv, json, tkinter) dışında harici bir bağımlılık yoktur.
    (Opsiyonel) Ekran görüntüsü özelliği için: pip install Pillow
    
    Çalıştırma Adımları
    Projeyi indirin ve klasör dizinine gidin.Terminal veya komut satırına şu komutu yazın:
    python main.py
    Uygulama açıldığında sol menüden CSV Yükle butonuna basarak veriler.csv (veya kendi oluşturduğunuz bir veri setini) sisteme yükleyin.

    6. Sonuç ve Değerlendirme
    Bu proje kapsamında, teorik olarak öğrenilen graf algoritmaları somut bir uygulama üzerinde test edilmiştir. Özellikle dinamik ağırlıklandırma mekanizması sayesinde, graf yapısının sadece topolojik değil, düğümlerin niteliklerine göre de değişebileceği gözlemlenmiştir.Performans testlerinde, 100 düğüme kadar olan orta ölçekli ağlarda algoritmaların anlık (milisaniye seviyesinde) sonuç verdiği görülmüştür. Tkinter Canvas kullanılarak yapılan "Force-Directed" yerleşim algoritması, karmaşık ağların görsel olarak daha anlaşılır bir forma girmesini sağlamıştır.