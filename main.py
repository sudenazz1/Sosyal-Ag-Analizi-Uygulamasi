import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import random
import math
from graph import SocialGraph
from algorithms import Algorithms

class ModernButton(tk.Canvas):
    """Özel modern buton widget'ı"""
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, height=40, bg="#2c3e50", highlightthickness=0, cursor="hand2")
        self.command = command
        self.text = text
        self.is_hovered = False

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.draw()

    def draw(self):
        self.delete("all")
        color = "#3498db" if self.is_hovered else "#2c3e50"
        self.config(bg=color)
        self.create_text(100, 20, text=self.text, fill="white", font=("Segoe UI", 10, "bold"))

    def on_enter(self, e):
        self.is_hovered = True
        self.draw()

    def on_leave(self, e):
        self.is_hovered = False
        self.draw()

class StatsPanel(tk.Frame):
    """İstatistik gösterge paneli"""
    def __init__(self, parent):
        super().__init__(parent, bg="#34495e", relief="flat")
        self.stats = {
            "nodes": tk.StringVar(value="0"),
            "edges": tk.StringVar(value="0"),
            "density": tk.StringVar(value="0.00")
        }
        self.create_widgets()

    def create_widgets(self):
        stats_config = [
            ("👤 Düğümler", self.stats["nodes"]),
            ("🔗 Bağlantılar", self.stats["edges"]),
            ("📊 Yoğunluk", self.stats["density"])
        ]

        for label, var in stats_config:
            frame = tk.Frame(self, bg="#34495e")
            frame.pack(side="left", padx=20, pady=10)

            tk.Label(frame, text=label, fg="#ecf0f1", bg="#34495e",
                    font=("Segoe UI", 9)).pack()
            tk.Label(frame, textvariable=var, fg="#3498db", bg="#34495e",
                    font=("Segoe UI", 14, "bold")).pack()

    def update_stats(self, graph):
        self.stats["nodes"].set(str(len(graph.nodes)))
        self.stats["edges"].set(str(len(graph.edges)))

        n = len(graph.nodes)
        density = len(graph.edges) / (n * (n-1) / 2) if n > 1 else 0
        self.stats["density"].set(f"{density:.2f}")

class App(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.title("🌐 Sosyal Ağ Analizi - Pro Edition")
        self.geometry("1400x800")
        self.configure(bg="#1a1a2e")

        # Animasyon ve özellikler
        self.animation_speed = 10
        self.physics_enabled = False
        self.node_velocities = {}
        self.show_labels = True
        self.dark_mode = True

        self.setup_ui()

        self.node_positions = {}
        self.selected_node = None
        self.dragging_node = None
        self.hover_node = None

        # Canvas mouse olayları
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<MouseWheel>", self.on_zoom)

        self.zoom_factor = 1.0
        self.pan_start = None

    def setup_ui(self):
        # Üst menü çubuğu
        menubar = tk.Menu(self, bg="#2c3e50", fg="white")
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg="#34495e", fg="white")
        menubar.add_cascade(label="📁 Dosya", menu=file_menu)
        file_menu.add_command(label="CSV Yükle", command=self.load_csv)
        file_menu.add_command(label="JSON Kaydet", command=self.save_json)
        file_menu.add_command(label="Görüntü Olarak Kaydet", command=self.save_as_image)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.quit)

        view_menu = tk.Menu(menubar, tearoff=0, bg="#34495e", fg="white")
        menubar.add_cascade(label="👁️ Görünüm", menu=view_menu)
        view_menu.add_command(label="Otomatik Düzenle", command=self.auto_layout)
        view_menu.add_command(label="Daire Düzeni", command=self.circular_layout)
        view_menu.add_command(label="Fizik Simülasyonu", command=self.toggle_physics)
        view_menu.add_separator()
        view_menu.add_command(label="Karanlık/Aydınlık Mod", command=self.toggle_theme)

        # Üst bilgi paneli
        self.stats_panel = StatsPanel(self)
        self.stats_panel.pack(side="top", fill="x")

        # Ana container
        main_container = tk.Frame(self, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Sol panel (Kontroller)
        self.create_sidebar(main_container)

        # Orta panel (Canvas)
        canvas_frame = tk.Frame(main_container, bg="#0f0f1e", relief="solid", bd=1)
        canvas_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Toolbar
        toolbar = tk.Frame(canvas_frame, bg="#2c3e50", height=40)
        toolbar.pack(side="top", fill="x")

        tk.Button(toolbar, text="🔍 Yakınlaştır", command=self.zoom_in,
                 bg="#34495e", fg="white", relief="flat").pack(side="left", padx=2)
        tk.Button(toolbar, text="🔍 Uzaklaştır", command=self.zoom_out,
                 bg="#34495e", fg="white", relief="flat").pack(side="left", padx=2)
        tk.Button(toolbar, text="🎯 Sıfırla", command=self.reset_zoom,
                 bg="#34495e", fg="white", relief="flat").pack(side="left", padx=2)
        tk.Button(toolbar, text="📸 Ekran Görüntüsü", command=self.save_as_image,
                 bg="#34495e", fg="white", relief="flat").pack(side="left", padx=2)

        self.canvas = tk.Canvas(canvas_frame, bg="#0f0f1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Sağ panel (Bilgi & Ayarlar)
        self.create_info_panel(main_container)

        # Alt log alanı
        log_frame = tk.Frame(self, bg="#2c3e50")
        log_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        tk.Label(log_frame, text="📋 İşlem Geçmişi", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=5, pady=2)

        self.log_area = tk.Text(log_frame, height=6, bg="#1a1a2e", fg="#00ff00",
                               font=("Consolas", 9), insertbackground="white")
        self.log_area.pack(fill="x", padx=5, pady=2)

        scrollbar = tk.Scrollbar(self.log_area)
        scrollbar.pack(side="right", fill="y")
        self.log_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_area.yview)

    def create_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg="#2c3e50", width=220)
        sidebar.pack(side="left", fill="y", padx=5)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🎮 KONTROL PANELİ", font=("Segoe UI", 13, "bold"),
                bg="#2c3e50", fg="#ecf0f1").pack(pady=15)

        # Buton grupları
        sections = [
            ("📂 DOSYA İŞLEMLERİ", [
                ("📥 CSV Yükle", self.load_csv),
                ("💾 JSON Kaydet", self.save_json),
                ("📝 CSV Olarak Kaydet", self.save_csv_as),
                ("📤 Veriyi Dışa Aktar", self.export_data)
            ]),
            ("🛤️ YOL BULMA", [
                ("🚀 Dijkstra", lambda: self.run_pathfinding("Dijkstra")),
                ("⭐ A* Algoritması", lambda: self.run_pathfinding("A*")),
                ("🔄 BFS Gezintisi", self.run_bfs),
                ("🌲 DFS Gezintisi", self.run_dfs)
            ]),
            ("📊 ANALİZ ARAÇLARI", [
                ("👑 Top 5 Etkililer", self.run_analysis),
                ("🎨 Grafik Renklendirme", self.run_coloring),
                ("👥 Topluluk Tespiti", self.run_community_detection),
                ("🔥 Merkezi Analiz", self.run_betweenness)
            ]),
            ("✏️ DÜZENLEME", [
                ("✨ Düğüm Ekle", self.add_new_node),
                ("🔧 Düğüm Güncelle", self.update_selected_node),
                ("🗑️ Bağlantı Sil", self.delete_edge_between_selected),
                ("🔄 Sıfırla", self.reset_view)
            ])
        ]

        for title, buttons in sections:
            tk.Label(sidebar, text=title, font=("Segoe UI", 9, "bold"),
                    bg="#34495e", fg="#ecf0f1").pack(fill="x", pady=(10, 0))

            for btn_text, cmd in buttons:
                btn = tk.Button(sidebar, text=btn_text, command=cmd,
                               bg="#34495e", fg="white", relief="flat",
                               font=("Segoe UI", 9), cursor="hand2",
                               activebackground="#3498db", activeforeground="white")
                btn.pack(fill="x", padx=5, pady=2)

        tk.Label(sidebar, text="💡 İPUÇLARI\n\n• Sol Tık: Bilgi/Bağla\n• Sağ Tık: Sil\n• Sürükle: Taşı\n• Scroll: Yakınlaştır",
                font=("Segoe UI", 8), bg="#2c3e50", fg="#95a5a6",
                justify="left").pack(side="bottom", pady=10, padx=5)

    def create_info_panel(self, parent):
        info_panel = tk.Frame(parent, bg="#2c3e50", width=250)
        info_panel.pack(side="right", fill="y", padx=5)
        info_panel.pack_propagate(False)

        tk.Label(info_panel, text="ℹ️ BİLGİ PANELİ", font=("Segoe UI", 12, "bold"),
                bg="#2c3e50", fg="#ecf0f1").pack(pady=10)

        self.info_text = tk.Text(info_panel, bg="#1a1a2e", fg="#ecf0f1",
                                font=("Segoe UI", 9), wrap="word", relief="flat")
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.info_text.insert("1.0", """🌟 SOSYAL AĞ ANALİZ ARACI

📌 ÖZELLİKLER:
• Gelişmiş görselleştirme
• Etkileşimli düğüm manipülasyonu
• Çoklu algoritma desteği
• Gerçek zamanlı analiz
• Profesyonel istatistikler

🎯 NASIL KULLANILIR:
1. CSV dosyası yükleyin
2. Düğümleri tıklayın veya sürükleyin
3. Analiz araçlarını kullanın
4. Sonuçları görüntüleyin

💡 Fare ile yakınlaştırma yapabilir,
düğümleri sürükleyebilirsiniz!
""")
        self.info_text.config(state="disabled")

    def log(self, msg, level="INFO"):
        colors = {"INFO": "#00ff00", "ERROR": "#ff0000", "SUCCESS": "#00ffff", "WARNING": "#ffaa00"}
        self.log_area.insert(tk.END, f"[{level}] {msg}\n")
        self.log_area.tag_add(level, "end-2l", "end-1l")
        self.log_area.tag_config(level, foreground=colors.get(level, "#00ff00"))
        self.log_area.see(tk.END)

    def draw_graph(self, custom_colors=None, highlight_path=None):
        self.canvas.delete("all")

        if not self.node_positions and self.graph.nodes:
            self.auto_layout()

        bg_color = "#0f0f1e" if self.dark_mode else "#f0f0f0"
        self.canvas.config(bg=bg_color)

        # Kenarları çiz
        for edge in self.graph.edges:
            if edge.source.id not in self.node_positions or edge.target.id not in self.node_positions:
                continue

            x1, y1 = self.node_positions[edge.source.id]
            x2, y2 = self.node_positions[edge.target.id]

            color, width = ("#555", 1) if self.dark_mode else ("#ccc", 1)

            if highlight_path:
                for i in range(len(highlight_path)-1):
                    if {edge.source.id, edge.target.id} == {highlight_path[i], highlight_path[i+1]}:
                        color, width = "#ff00ff", 4

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, smooth=True)

            # Ağırlık etiketi
            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            text_color = "#3498db" if self.dark_mode else "#2980b9"
            self.canvas.create_text(mid_x, mid_y, text=f"{edge.weight:.1f}",
                                   fill=text_color, font=("Arial", 8, "bold"))

        # Düğümleri çiz
        for nid, node in self.graph.nodes.items():
            if nid not in self.node_positions:
                continue

            x, y = self.node_positions[nid]

            # Hover efekti
            radius = 25 if self.hover_node == nid else 20

            color = custom_colors.get(nid, "#3498db") if custom_colors else "#3498db"

            # Seçili düğüm vurgusu
            if self.selected_node and self.selected_node.id == nid:
                self.canvas.create_oval(x-radius-5, y-radius-5, x+radius+5, y+radius+5,
                                       fill="", outline="#f39c12", width=3)

            # Düğüm
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                   fill=color, outline="white", width=2, tags=f"node_{nid}")

            # ID
            self.canvas.create_text(x, y, text=str(nid), fill="white",
                                   font=("Arial", 11, "bold"), tags=f"node_{nid}")

            # İsim etiketi
            if self.show_labels:
                label_color = "#ecf0f1" if self.dark_mode else "#2c3e50"
                self.canvas.create_text(x, y+radius+12, text=node.name,
                                       fill=label_color, font=("Arial", 8))

        self.stats_panel.update_stats(self.graph)

    def auto_layout(self):
        """Force-directed layout algoritması"""
        nodes = list(self.graph.nodes.keys())
        if not nodes:
            return

        # İlk pozisyonlar
        for i, nid in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = 400 + 200 * math.cos(angle)
            y = 300 + 200 * math.sin(angle)
            self.node_positions[nid] = (x, y)

        # Force-directed iterasyonlar
        for iteration in range(50):
            forces = {nid: [0, 0] for nid in nodes}

            # Repulsion (itme kuvveti)
            for i, nid1 in enumerate(nodes):
                for nid2 in nodes[i+1:]:
                    x1, y1 = self.node_positions[nid1]
                    x2, y2 = self.node_positions[nid2]
                    dx, dy = x2 - x1, y2 - y1
                    dist = math.sqrt(dx*dx + dy*dy) or 1

                    force = 5000 / (dist * dist)
                    fx, fy = force * dx / dist, force * dy / dist

                    forces[nid1][0] -= fx
                    forces[nid1][1] -= fy
                    forces[nid2][0] += fx
                    forces[nid2][1] += fy

            # Attraction (çekme kuvveti - kenarlar için)
            for edge in self.graph.edges:
                if edge.source.id in nodes and edge.target.id in nodes:
                    x1, y1 = self.node_positions[edge.source.id]
                    x2, y2 = self.node_positions[edge.target.id]
                    dx, dy = x2 - x1, y2 - y1
                    dist = math.sqrt(dx*dx + dy*dy) or 1

                    force = dist * 0.01
                    fx, fy = force * dx / dist, force * dy / dist

                    forces[edge.source.id][0] += fx
                    forces[edge.source.id][1] += fy
                    forces[edge.target.id][0] -= fx
                    forces[edge.target.id][1] -= fy

            # Pozisyonları güncelle
            for nid in nodes:
                x, y = self.node_positions[nid]
                fx, fy = forces[nid]
                x += fx * 0.1
                y += fy * 0.1

                # Canvas sınırları içinde tut
                x = max(50, min(750, x))
                y = max(50, min(550, y))
                self.node_positions[nid] = (x, y)

        self.draw_graph()
        self.log("Grafik otomatik düzenlendi", "SUCCESS")

    def circular_layout(self):
        """Düğümleri daire şeklinde düzenle"""
        nodes = list(self.graph.nodes.keys())
        if not nodes:
            return

        cx, cy, radius = 400, 300, 200
        for i, nid in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            self.node_positions[nid] = (x, y)

        self.draw_graph()
        self.log("Daire düzeni uygulandı", "SUCCESS")

    def toggle_physics(self):
        self.physics_enabled = not self.physics_enabled
        if self.physics_enabled:
            self.log("Fizik simülasyonu aktif", "INFO")
            self.run_physics()
        else:
            self.log("Fizik simülasyonu kapatıldı", "INFO")

    def run_physics(self):
        if not self.physics_enabled:
            return
        self.auto_layout()
        self.after(100, self.run_physics)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.draw_graph()
        self.log(f"Tema değiştirildi: {'Karanlık' if self.dark_mode else 'Aydınlık'}", "INFO")

    def on_motion(self, event):
        """Mouse hareketi - hover efekti"""
        old_hover = self.hover_node
        self.hover_node = None

        clicked = self.get_node_at_pos(event.x, event.y)
        if clicked:
            self.hover_node = clicked.id

        if old_hover != self.hover_node:
            self.draw_graph()

    def on_drag(self, event):
        """Düğüm sürükleme"""
        if self.dragging_node:
            self.node_positions[self.dragging_node] = (event.x, event.y)
            self.draw_graph()

    def on_release(self, event):
        """Mouse bırakma"""
        self.dragging_node = None

    def on_left_click(self, event):
        clicked = self.get_node_at_pos(event.x, event.y)

        if clicked:
            # Sürükleme başlat
            self.dragging_node = clicked.id

            # Bilgi göster
            info = f"ID: {clicked.id}\nAd: {clicked.name}\nAktiflik: {clicked.aktiflik}\nEtkileşim: {clicked.etkilesim}"
            messagebox.showinfo(f"📊 Düğüm: {clicked.name}", info)

            # Bağlantı oluştur
            if self.selected_node and self.selected_node != clicked:
                weight_dialog = tk.Toplevel(self)
                weight_dialog.title("⚖️ Ağırlık")
                weight_dialog.geometry("300x150")
                weight_dialog.configure(bg="#2c3e50")
                weight_dialog.transient(self)
                weight_dialog.grab_set()

                x = (weight_dialog.winfo_screenwidth() // 2) - 150
                y = (weight_dialog.winfo_screenheight() // 2) - 75
                weight_dialog.geometry(f"300x150+{x}+{y}")

                tk.Label(weight_dialog, text="Bağlantı Ağırlığı:", bg="#2c3e50",
                        fg="white", font=("Segoe UI", 11)).pack(pady=20)

                weight_entry = tk.Entry(weight_dialog, width=15, font=("Segoe UI", 12))
                weight_entry.insert(0, "1.0")
                weight_entry.pack(pady=10)
                weight_entry.focus()
                weight_entry.select_range(0, tk.END)

                result = {"weight": None}

                def on_ok():
                    try:
                        result["weight"] = float(weight_entry.get())
                        weight_dialog.destroy()
                    except ValueError:
                        messagebox.showerror("Hata", "Geçerli bir sayı girin!", parent=weight_dialog)

                btn_frame = tk.Frame(weight_dialog, bg="#2c3e50")
                btn_frame.pack(pady=10)
                tk.Button(btn_frame, text="✓ Tamam", command=on_ok, bg="#27ae60",
                         fg="white", width=8).pack(side="left", padx=5)
                tk.Button(btn_frame, text="✗ İptal", command=weight_dialog.destroy,
                         bg="#c0392b", fg="white", width=8).pack(side="left", padx=5)

                weight_entry.bind("<Return>", lambda e: on_ok())
                weight_dialog.wait_window()

                if result["weight"] is not None:
                    self.graph.add_edge(self.selected_node.id, clicked.id)
                    # Manuel olarak weight'i ayarla
                    for edge in self.graph.edges:
                        if ((edge.source.id == self.selected_node.id and edge.target.id == clicked.id) or
                            (edge.source.id == clicked.id and edge.target.id == self.selected_node.id)):
                            edge.weight = result["weight"]
                            break

                    self.log(f"Bağlantı: {self.selected_node.id} ↔ {clicked.id} (Ağırlık: {result['weight']})", "SUCCESS")

                    # Otomatik kaydet
                    if hasattr(self.graph, 'csv_file_path') and self.graph.csv_file_path:
                        self.save_to_csv(self.graph.csv_file_path)
                    self.graph.save_to_json()

                self.selected_node = None
                self.draw_graph()
            else:
                self.selected_node = clicked
                self.log(f"Seçildi: {clicked.name} (Bağlamak için başka düğüme tıkla)", "INFO")
                self.draw_graph()

    def on_right_click(self, event):
        clicked = self.get_node_at_pos(event.x, event.y)
        if clicked:
            confirm = messagebox.askyesno("⚠️ Sil", f"{clicked.name} (ID: {clicked.id}) silinsin mi?")
            if confirm:
                self.graph.remove_node(clicked.id)
                if clicked.id in self.node_positions:
                    del self.node_positions[clicked.id]
                self.draw_graph()
                self.log(f"Düğüm silindi: {clicked.name}", "WARNING")

    def on_zoom(self, event):
        """Mouse wheel ile zoom"""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        self.zoom_factor *= 1.1
        self.apply_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.1
        self.apply_zoom()

    def reset_zoom(self):
        self.zoom_factor = 1.0
        self.apply_zoom()

    def apply_zoom(self):
        center_x, center_y = 400, 300
        for nid in self.node_positions:
            x, y = self.node_positions[nid]
            dx, dy = x - center_x, y - center_y
            self.node_positions[nid] = (center_x + dx * self.zoom_factor,
                                       center_y + dy * self.zoom_factor)
        self.draw_graph()

    def get_node_at_pos(self, x, y):
        for nid, pos in self.node_positions.items():
            if (x-pos[0])**2 + (y-pos[1])**2 <= 400:
                return self.graph.nodes[nid]
        return None

    def add_new_node(self):
        """Yeni düğüm ekle"""
        dialog = tk.Toplevel(self)
        dialog.title("➕ Yeni Düğüm Ekle")
        dialog.geometry("400x320")
        dialog.configure(bg="#2c3e50")
        dialog.transient(self)
        dialog.grab_set()

        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 160
        dialog.geometry(f"400x320+{x}+{y}")

        tk.Label(dialog, text="➕ YENİ DÜĞÜM EKLE", font=("Segoe UI", 14, "bold"),
                bg="#2c3e50", fg="white").pack(pady=20)

        # ID
        frame1 = tk.Frame(dialog, bg="#2c3e50")
        frame1.pack(pady=8)
        tk.Label(frame1, text="Düğüm ID:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10), width=15, anchor="w").pack(side="left", padx=5)
        id_entry = tk.Entry(frame1, width=20, font=("Segoe UI", 10))
        id_entry.pack(side="left")
        id_entry.focus()

        # İsim
        frame2 = tk.Frame(dialog, bg="#2c3e50")
        frame2.pack(pady=8)
        tk.Label(frame2, text="İsim:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10), width=15, anchor="w").pack(side="left", padx=5)
        name_entry = tk.Entry(frame2, width=20, font=("Segoe UI", 10))
        name_entry.pack(side="left")

        # Aktiflik
        frame3 = tk.Frame(dialog, bg="#2c3e50")
        frame3.pack(pady=8)
        tk.Label(frame3, text="Aktiflik Skoru:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10), width=15, anchor="w").pack(side="left", padx=5)
        aktiflik_entry = tk.Entry(frame3, width=20, font=("Segoe UI", 10))
        aktiflik_entry.insert(0, "50.0")
        aktiflik_entry.pack(side="left")

        # Etkileşim
        frame4 = tk.Frame(dialog, bg="#2c3e50")
        frame4.pack(pady=8)
        tk.Label(frame4, text="Etkileşim:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10), width=15, anchor="w").pack(side="left", padx=5)
        etkilesim_entry = tk.Entry(frame4, width=20, font=("Segoe UI", 10))
        etkilesim_entry.insert(0, "0")
        etkilesim_entry.pack(side="left")

        result = {"added": False}

        def on_add():
            try:
                nid = int(id_entry.get())
                name = name_entry.get().strip()
                aktiflik = float(aktiflik_entry.get())
                etkilesim = int(etkilesim_entry.get())

                if nid in self.graph.nodes:
                    messagebox.showerror("Hata", f"ID {nid} zaten mevcut!", parent=dialog)
                    return

                if not name:
                    messagebox.showerror("Hata", "İsim boş olamaz!", parent=dialog)
                    return

                from graph import Node
                # BaglantiSayisi başlangıçta 0
                new_node = Node(nid, name, aktiflik, etkilesim)
                self.graph.nodes[nid] = new_node
                self.node_positions[nid] = (random.randint(100, 700), random.randint(100, 500))

                result["added"] = True
                dialog.destroy()

            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli değerler girin!", parent=dialog)

        # Butonlar
        btn_frame = tk.Frame(dialog, bg="#2c3e50")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="✓ Ekle", command=on_add, bg="#27ae60",
                 fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="✗ İptal", command=dialog.destroy, bg="#c0392b",
                 fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side="left", padx=5)

        id_entry.bind("<Return>", lambda e: name_entry.focus())
        name_entry.bind("<Return>", lambda e: aktiflik_entry.focus())
        aktiflik_entry.bind("<Return>", lambda e: etkilesim_entry.focus())
        etkilesim_entry.bind("<Return>", lambda e: on_add())

        dialog.wait_window()

        if result["added"]:
            self.draw_graph()
            self.log(f"Yeni düğüm eklendi: {name_entry.get()} (ID: {id_entry.get()})", "SUCCESS")
            messagebox.showinfo("✅ Başarılı", f"Düğüm başarıyla eklendi!\n\n{name_entry.get()}")

            # Otomatik kaydet
            if hasattr(self.graph, 'csv_file_path') and self.graph.csv_file_path:
                self.save_to_csv(self.graph.csv_file_path)
            self.graph.save_to_json()

    # ✅✅✅ FIX 1: load_csv (csv_file_path kesin set olsun)
    def load_csv(self):
        filename = filedialog.askopenfilename(title="CSV Seç", filetypes=(("CSV Files", "*.csv"),))
        if filename:
            res = self.graph.load_from_csv(filename)

            # DÜZELTME: load_from_csv bazen True yerine farklı truthy döndürür -> "res is True" takılır.
            if res:
                self.graph.csv_file_path = filename
                self.node_positions = {}
                self.auto_layout()
                self.log(f"CSV başarıyla yüklendi: {filename}", "SUCCESS")
            else:
                messagebox.showerror("❌ Hata", str(res))
                self.log(f"CSV yükleme hatası: {res}", "ERROR")

    def save_json(self):
        self.graph.save_to_json()
        messagebox.showinfo("💾 Kayıt", "Veriler 'graph_data.json' olarak kaydedildi.")
        self.log("JSON dosyası kaydedildi", "SUCCESS")

    def save_to_csv(self, filename):
        """CSV dosyasına kaydet - Orijinal formatta"""
        try:
            import csv

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                # CSV başlıkları
                fieldnames = ['DugumId', 'Ad', 'Aktiflik', 'Etkilesim', 'BaglantiSayisi', 'Komsular']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for node in self.graph.nodes.values():
                    # Bu düğümün komşularını bul
                    komsular = []
                    if node.id in self.graph.adjacency_list:
                        komsular = self.graph.adjacency_list[node.id]

                    # Komşuları string'e çevir
                    komsular_str = ','.join(map(str, komsular)) if komsular else ''

                    # Bağlantı sayısı
                    baglanti_sayisi = len(komsular)

                    writer.writerow({
                        'DugumId': node.id,
                        'Ad': node.name,
                        'Aktiflik': node.aktiflik,
                        'Etkilesim': node.etkilesim,
                        'BaglantiSayisi': baglanti_sayisi,
                        'Komsular': komsular_str
                    })

            self.log(f"✅ CSV başarıyla kaydedildi: {filename}", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"❌ CSV kayıt hatası: {str(e)}", "ERROR")
            messagebox.showerror("Hata", f"CSV kayıt hatası:\n{str(e)}")
            return False

    def save_csv_as(self):
        """Farklı kaydet - CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
            title="CSV Olarak Kaydet"
        )
        if filename:
            if self.save_to_csv(filename):
                self.graph.csv_file_path = filename
                messagebox.showinfo("✅ Başarılı", f"CSV kaydedildi:\n{filename}")
            else:
                messagebox.showerror("❌ Hata", "CSV kaydetme başarısız!")

    def export_data(self):
        """Veriyi farklı formatlarda dışa aktar"""
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=(("Text files", "*.txt"),
                                                          ("All files", "*.*")))
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== SOSYAL AĞ ANALİZ RAPORU ===\n\n")
                f.write(f"Toplam Düğüm: {len(self.graph.nodes)}\n")
                f.write(f"Toplam Bağlantı: {len(self.graph.edges)}\n\n")
                f.write("DÜĞÜMLER:\n")
                for node in self.graph.nodes.values():
                    f.write(f"- {node.name} (ID: {node.id}, Aktiflik: {node.aktiflik})\n")
            self.log(f"Veri dışa aktarıldı: {filename}", "SUCCESS")

    def save_as_image(self):
        """Canvas'ı görüntü olarak kaydet"""
        try:
            from PIL import Image, ImageDraw  # noqa: F401
        except ImportError:
            self.log("Görüntü kaydetme için PIL kütüphanesi yükleyin: pip install Pillow", "WARNING")
            messagebox.showinfo("📸 Bilgi", "Ekran görüntüsü özelliği için Pillow gerekli.\n\npip install Pillow")
            return

        messagebox.showinfo("📸 Bilgi", "Pillow var ama bu örnekte gerçek export kodu yazılmadı.")
        self.log("Pillow bulundu (export kodu eklenmemiş)", "INFO")

    def run_pathfinding(self, algo_type):
        dialog = tk.Toplevel(self)
        dialog.title(f"🎯 {algo_type} Yol Bulma")
        dialog.geometry("350x250")
        dialog.configure(bg="#2c3e50")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"350x250+{x}+{y}")

        tk.Label(dialog, text=f"🚀 {algo_type} Algoritması",
                font=("Segoe UI", 14, "bold"), bg="#2c3e50", fg="white").pack(pady=20)

        frame1 = tk.Frame(dialog, bg="#2c3e50")
        frame1.pack(pady=10)
        tk.Label(frame1, text="Başlangıç Düğüm ID:", bg="#2c3e50",
                fg="white", font=("Segoe UI", 10)).pack(side="left", padx=5)
        start_entry = tk.Entry(frame1, width=10, font=("Segoe UI", 11))
        start_entry.pack(side="left")
        start_entry.focus()

        frame2 = tk.Frame(dialog, bg="#2c3e50")
        frame2.pack(pady=10)
        tk.Label(frame2, text="Bitiş Düğüm ID:", bg="#2c3e50",
                fg="white", font=("Segoe UI", 10)).pack(side="left", padx=5)
        end_entry = tk.Entry(frame2, width=10, font=("Segoe UI", 11))
        end_entry.pack(side="left")

        result = {"start": None, "end": None}

        def on_ok():
            try:
                result["start"] = int(start_entry.get())
                result["end"] = int(end_entry.get())
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli sayılar girin!", parent=dialog)

        def on_cancel():
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg="#2c3e50")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="✓ Tamam", command=on_ok, bg="#27ae60",
                 fg="white", font=("Segoe UI", 10, "bold"), width=10,
                 cursor="hand2").pack(side="left", padx=5)
        tk.Button(btn_frame, text="✗ İptal", command=on_cancel, bg="#c0392b",
                 fg="white", font=("Segoe UI", 10, "bold"), width=10,
                 cursor="hand2").pack(side="left", padx=5)

        start_entry.bind("<Return>", lambda e: end_entry.focus())
        end_entry.bind("<Return>", lambda e: on_ok())

        dialog.wait_window()

        s_id = result["start"]
        e_id = result["end"]

        if s_id is not None and e_id is not None:
            if s_id not in self.graph.nodes or e_id not in self.graph.nodes:
                self.log("Geçersiz düğüm ID'leri!", "ERROR")
                messagebox.showerror("Hata", "Geçersiz düğüm ID'leri!")
                return

            if algo_type == "Dijkstra":
                path, cost = Algorithms.dijkstra(self.graph, s_id, e_id)
            else:
                path, cost = Algorithms.a_star(self.graph, s_id, e_id)

            if path:
                path_str = " → ".join(str(p) for p in path)
                self.log(f"{algo_type} Yolu: {path_str} | Maliyet: {cost:.2f}", "SUCCESS")
                messagebox.showinfo(f"✅ {algo_type} Sonucu",
                                   f"Yol: {path_str}\n\nToplam Maliyet: {cost:.2f}")
                self.draw_graph(highlight_path=path)
            else:
                self.log(f"{algo_type}: Yol bulunamadı!", "WARNING")
                messagebox.showwarning("⚠️ Sonuç", "Bu düğümler arasında yol bulunamadı!")

    def run_bfs(self):
        s_id = simpledialog.askinteger("🔄 BFS", "Başlangıç Düğüm ID:")
        if s_id and s_id in self.graph.nodes:
            res = Algorithms.bfs(self.graph, s_id)
            res_str = " → ".join(str(r) for r in res)
            self.log(f"BFS Gezintisi: {res_str}", "SUCCESS")
            messagebox.showinfo("🔄 BFS Sonucu", f"Gezinti Sırası:\n{res_str}")
        else:
            self.log("Geçersiz düğüm ID!", "ERROR")

    def run_dfs(self):
        s_id = simpledialog.askinteger("🌲 DFS", "Başlangıç Düğüm ID:")
        if s_id and s_id in self.graph.nodes:
            res = Algorithms.dfs(self.graph, s_id)
            res_str = " → ".join(str(r) for r in res)
            self.log(f"DFS Gezintisi: {res_str}", "SUCCESS")
            messagebox.showinfo("🌲 DFS Sonucu", f"Gezinti Sırası:\n{res_str}")
        else:
            self.log("Geçersiz düğüm ID!", "ERROR")

    def run_analysis(self):
        """Top 5 en etkili kullanıcıları bul"""
        top5 = Algorithms.calculate_centrality(self.graph)

        self.log("=" * 50, "INFO")
        self.log("👑 EN ETKİLİ 5 KULLANICI", "SUCCESS")
        self.log("=" * 50, "INFO")

        result_text = "🏆 EN ETKİLİ KULLANICILAR\n\n"
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

        for i, (node, deg) in enumerate(top5):
            medal = medals[i] if i < len(medals) else "•"
            log_msg = f"{medal} {node.name} (ID: {node.id}) - Derece: {deg}"
            self.log(log_msg, "INFO")
            result_text += f"{medal} {node.name}\n   ID: {node.id}\n   Bağlantı Sayısı: {deg}\n\n"

        messagebox.showinfo("👑 Etki Analizi", result_text)

    def run_coloring(self):
        """Welsh-Powell grafik renklendirme"""
        colors = Algorithms.welsh_powell(self.graph)
        self.draw_graph(custom_colors=colors)

        unique_colors = len(set(colors.values()))
        self.log(f"Grafik renklendirildi - {unique_colors} farklı renk kullanıldı", "SUCCESS")
        messagebox.showinfo("🎨 Renklendirme",
                           f"Grafik başarıyla renklendi!\n\nKullanılan renk sayısı: {unique_colors}")

    def run_community_detection(self):
        """Topluluk tespiti - Bağlı bileşenler"""
        components = Algorithms.find_connected_components(self.graph)

        self.log("=" * 50, "INFO")
        self.log(f"👥 TOPLULUK ANALİZİ - {len(components)} Grup Bulundu", "SUCCESS")
        self.log("=" * 50, "INFO")

        result_text = f"📊 Toplam {len(components)} bağımsız topluluk tespit edildi\n\n"

        for i, comp in enumerate(components, 1):
            comp_str = ", ".join(str(c) for c in sorted(comp))
            self.log(f"Topluluk {i} ({len(comp)} üye): {comp_str}", "INFO")
            result_text += f"Topluluk {i} ({len(comp)} üye):\n{comp_str}\n\n"

        messagebox.showinfo("👥 Topluluk Analizi", result_text)

        # Toplulukları farklı renklerle göster
        colors_list = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
                      "#1abc9c", "#e67e22", "#34495e", "#16a085", "#c0392b"]
        color_map = {}
        for i, comp in enumerate(components):
            color = colors_list[i % len(colors_list)]
            for node_id in comp:
                color_map[node_id] = color

        self.draw_graph(custom_colors=color_map)

    def run_betweenness(self):
        """Betweenness centrality analizi"""
        try:
            betweenness = {nid: 0 for nid in self.graph.nodes}

            nodes = list(self.graph.nodes.keys())
            for i, start in enumerate(nodes):
                for end in nodes[i+1:]:
                    path, _ = Algorithms.dijkstra(self.graph, start, end)
                    if path:
                        for node in path[1:-1]:  # Başlangıç ve bitiş hariç
                            betweenness[node] += 1

            sorted_bet = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]

            self.log("=" * 50, "INFO")
            self.log("🔥 ARACILIK MERKEZİLİĞİ ANALİZİ", "SUCCESS")
            self.log("=" * 50, "INFO")

            result_text = "🔥 EN YÜKSEK ARACILIK MERKEZİLİĞİ\n\n"

            for nid, score in sorted_bet:
                node = self.graph.nodes[nid]
                self.log(f"• {node.name} (ID: {nid}) - Skor: {score}", "INFO")
                result_text += f"• {node.name}\n   ID: {nid}\n   Aracılık Skoru: {score}\n\n"

            messagebox.showinfo("🔥 Aracılık Analizi", result_text)

        except Exception as e:
            self.log(f"Aracılık analizi hatası: {str(e)}", "ERROR")
            messagebox.showerror("Hata", f"Analiz sırasında hata oluştu:\n{str(e)}")

    # ✅✅✅ FIX 2: update_selected_node (graph.nodes dict kesin güncellensin + CSV'ye yazılsın)
    def update_selected_node(self):
        """Seçili düğümü güncelle - Hem ekranda hem CSV'de günceller (FIX)"""
        if not self.selected_node:
            messagebox.showwarning("⚠️ Uyarı", "Önce güncellenecek düğüme tıklayıp seçin!")
            return

        dialog = tk.Toplevel(self)
        dialog.title(f"✏️ Düğüm Güncelle - ID: {self.selected_node.id}")
        dialog.geometry("400x300")
        dialog.configure(bg="#2c3e50")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 150
        dialog.geometry(f"400x300+{x}+{y}")

        tk.Label(dialog, text="📝 DÜĞÜM GÜNCELLE", font=("Segoe UI", 14, "bold"),
                bg="#2c3e50", fg="white").pack(pady=20)

        info_frame = tk.Frame(dialog, bg="#34495e", relief="groove", bd=2)
        info_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(info_frame, text=f"Mevcut İsim: {self.selected_node.name}",
                bg="#34495e", fg="#ecf0f1", font=("Segoe UI", 9)).pack(pady=2)
        tk.Label(info_frame, text=f"Mevcut Aktiflik: {self.selected_node.aktiflik}",
                bg="#34495e", fg="#ecf0f1", font=("Segoe UI", 9)).pack(pady=2)

        frame1 = tk.Frame(dialog, bg="#2c3e50")
        frame1.pack(pady=10)
        tk.Label(frame1, text="Yeni İsim:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10)).pack(side="left", padx=5)
        name_entry = tk.Entry(frame1, width=20, font=("Segoe UI", 10))
        name_entry.insert(0, self.selected_node.name)
        name_entry.pack(side="left")
        name_entry.focus()
        name_entry.select_range(0, tk.END)

        frame2 = tk.Frame(dialog, bg="#2c3e50")
        frame2.pack(pady=10)
        tk.Label(frame2, text="Yeni Aktiflik:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10)).pack(side="left", padx=5)
        aktiflik_entry = tk.Entry(frame2, width=20, font=("Segoe UI", 10))
        aktiflik_entry.insert(0, str(self.selected_node.aktiflik))
        aktiflik_entry.pack(side="left")

        result = {"updated": False}
        updated_vals = {"name": None, "aktiflik": None}

        def on_save():
            new_name = name_entry.get().strip()
            try:
                new_aktiflik = float(aktiflik_entry.get())

                if not new_name:
                    messagebox.showerror("Hata", "İsim boş olamaz!", parent=dialog)
                    return

                # 1) UI'daki seçili node'u güncelle
                self.selected_node.name = new_name
                self.selected_node.aktiflik = new_aktiflik

                # 2) ✅ EN KRİTİK: graph.nodes sözlüğünü de güncelle (CSV buradan yazılıyor)
                self.graph.nodes[self.selected_node.id] = self.selected_node

                # 3) ❌ Bu bazı projelerde eski veriyi geri "ezebiliyor", şimdilik kapalı
                # if hasattr(self.graph, 'update_node'):
                #     self.graph.update_node(self.selected_node.id, new_name, new_aktiflik)

                updated_vals["name"] = new_name
                updated_vals["aktiflik"] = new_aktiflik
                result["updated"] = True
                dialog.destroy()

            except ValueError:
                messagebox.showerror("Hata", "Aktiflik sayı olmalı!", parent=dialog)

        def on_cancel():
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg="#2c3e50")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Kaydet", command=on_save, bg="#27ae60",
                 fg="white", font=("Segoe UI", 10, "bold"), width=12,
                 cursor="hand2").pack(side="left", padx=5)
        tk.Button(btn_frame, text="✗ İptal", command=on_cancel, bg="#c0392b",
                 fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side="left", padx=5)

        name_entry.bind("<Return>", lambda e: aktiflik_entry.focus())
        aktiflik_entry.bind("<Return>", lambda e: on_save())

        dialog.wait_window()

        if result["updated"]:
            self.draw_graph()
            self.log(f"✅ Düğüm güncellendi: {updated_vals['name']} (ID: {self.selected_node.id})", "SUCCESS")

            try:
                # JSON kaydet
                self.graph.save_to_json()
                self.log("📁 JSON dosyasına kaydedildi", "INFO")

                # CSV kaydet
                if hasattr(self.graph, 'csv_file_path') and self.graph.csv_file_path:
                    self.save_to_csv(self.graph.csv_file_path)
                    self.log(f"📁 CSV dosyasına kaydedildi: {self.graph.csv_file_path}", "SUCCESS")
                else:
                    save_csv = messagebox.askyesno("💾 CSV Kaydet",
                                                   "Değişiklikler CSV dosyasına kaydedilsin mi?")
                    if save_csv:
                        self.save_csv_as()

                messagebox.showinfo("✅ Başarılı",
                              f"Düğüm başarıyla güncellendi ve kaydedildi!\n\n"
                              f"Yeni İsim: {updated_vals['name']}\n"
                              f"Yeni Aktiflik: {updated_vals['aktiflik']}")
            except Exception as e:
                self.log(f"⚠️ Kayıt hatası: {str(e)}", "ERROR")
                messagebox.showwarning("⚠️ Uyarı",
                                     f"Güncelleme başarılı ama kayıt sırasında hata:\n{str(e)}\n\n"
                                     "Manuel olarak 'JSON Kaydet' butonunu kullanın.")

    def delete_edge_between_selected(self):
        """İki düğüm arasındaki bağlantıyı sil"""
        dialog = tk.Toplevel(self)
        dialog.title("🗑️ Bağlantı Sil")
        dialog.geometry("400x250")
        dialog.configure(bg="#2c3e50")
        dialog.transient(self)
        dialog.grab_set()

        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")

        tk.Label(dialog, text="🗑️ BAĞLANTI SİL", font=("Segoe UI", 14, "bold"),
                bg="#2c3e50", fg="white").pack(pady=20)

        frame1 = tk.Frame(dialog, bg="#2c3e50")
        frame1.pack(pady=10)
        tk.Label(frame1, text="1. Düğüm ID:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10), width=12).pack(side="left", padx=5)
        id1_entry = tk.Entry(frame1, width=15, font=("Segoe UI", 11))
        id1_entry.pack(side="left")
        id1_entry.focus()

        frame2 = tk.Frame(dialog, bg="#2c3e50")
        frame2.pack(pady=10)
        tk.Label(frame2, text="2. Düğüm ID:", bg="#2c3e50", fg="white",
                font=("Segoe UI", 10), width=12).pack(side="left", padx=5)
        id2_entry = tk.Entry(frame2, width=15, font=("Segoe UI", 11))
        id2_entry.pack(side="left")

        result = {"deleted": False}

        def on_delete():
            try:
                id1 = int(id1_entry.get())
                id2 = int(id2_entry.get())

                if id1 not in self.graph.nodes or id2 not in self.graph.nodes:
                    messagebox.showerror("Hata", "Geçersiz düğüm ID'leri!", parent=dialog)
                    return

                self.graph.remove_edge(id1, id2)
                result["deleted"] = True
                dialog.destroy()

            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli sayılar girin!", parent=dialog)

        btn_frame = tk.Frame(dialog, bg="#2c3e50")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="🗑️ Sil", command=on_delete, bg="#e74c3c",
                 fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="✗ İptal", command=dialog.destroy, bg="#95a5a6",
                 fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side="left", padx=5)

        id1_entry.bind("<Return>", lambda e: id2_entry.focus())
        id2_entry.bind("<Return>", lambda e: on_delete())

        dialog.wait_window()

        if result["deleted"]:
            self.draw_graph()
            self.log(f"Bağlantı silindi: {id1_entry.get()} ↔ {id2_entry.get()}", "WARNING")
            messagebox.showinfo("✅ Başarılı", f"Bağlantı silindi:\n{id1_entry.get()} ↔ {id2_entry.get()}")

            if hasattr(self.graph, 'csv_file_path') and self.graph.csv_file_path:
                self.save_to_csv(self.graph.csv_file_path)
            self.graph.save_to_json()

    def reset_view(self):
        """Görünümü sıfırla"""
        self.selected_node = None
        self.zoom_factor = 1.0
        self.draw_graph()
        self.log("Görünüm sıfırlandı", "INFO")


if __name__ == "__main__":
    g = SocialGraph()
    app = App(g)
    app.mainloop()
