import time
import random
from graph import SocialGraph
from algorithms import Algorithms
import csv

class PerformanceTester:
    """Algoritmaların performansını test eden sınıf"""
    
    def __init__(self, csv_file):
        self.graph = SocialGraph()
        self.csv_file = csv_file
        self.results = []
        
    def load_graph(self):
        """Grafı yükle"""
        result = self.graph.load_from_csv(self.csv_file)
        if result is True:
            print(f"✅ Graf yüklendi: {len(self.graph.nodes)} düğüm, {len(self.graph.edges)} kenar")
            return True
        else:
            print(f"❌ Graf yükleme hatası: {result}")
            return False
    
    def test_bfs(self):
        """BFS performans testi"""
        if not self.graph.nodes:
            return None
        
        start_node = random.choice(list(self.graph.nodes.keys()))
        
        start_time = time.time()
        result = Algorithms.bfs(self.graph, start_node)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000  # milisaniye
        
        return {
            'algorithm': 'BFS',
            'start_node': start_node,
            'nodes_visited': len(result),
            'duration_ms': round(duration, 4)
        }
    
    def test_dfs(self):
        """DFS performans testi"""
        if not self.graph.nodes:
            return None
        
        start_node = random.choice(list(self.graph.nodes.keys()))
        
        start_time = time.time()
        result = Algorithms.dfs(self.graph, start_node)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        
        return {
            'algorithm': 'DFS',
            'start_node': start_node,
            'nodes_visited': len(result),
            'duration_ms': round(duration, 4)
        }
    
    def test_dijkstra(self):
        """Dijkstra performans testi"""
        if len(self.graph.nodes) < 2:
            return None
        
        nodes = list(self.graph.nodes.keys())
        start_node = random.choice(nodes)
        end_node = random.choice([n for n in nodes if n != start_node])
        
        start_time = time.time()
        path, cost = Algorithms.dijkstra(self.graph, start_node, end_node)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        
        return {
            'algorithm': 'Dijkstra',
            'start_node': start_node,
            'end_node': end_node,
            'path_length': len(path) if path else 0,
            'cost': round(cost, 2) if cost != float('inf') else 'inf',
            'duration_ms': round(duration, 4)
        }
    
    def test_astar(self):
        """A* performans testi"""
        if len(self.graph.nodes) < 2:
            return None
        
        nodes = list(self.graph.nodes.keys())
        start_node = random.choice(nodes)
        end_node = random.choice([n for n in nodes if n != start_node])
        
        start_time = time.time()
        path, cost = Algorithms.a_star(self.graph, start_node, end_node)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        
        return {
            'algorithm': 'A*',
            'start_node': start_node,
            'end_node': end_node,
            'path_length': len(path) if path else 0,
            'cost': round(cost, 2) if cost != float('inf') else 'inf',
            'duration_ms': round(duration, 4)
        }
    
    def test_centrality(self):
        """Merkezilik analizi performans testi"""
        if not self.graph.nodes:
            return None
        
        start_time = time.time()
        top5 = Algorithms.calculate_centrality(self.graph)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        
        return {
            'algorithm': 'Degree Centrality',
            'top_nodes': len(top5),
            'max_degree': top5[0][1] if top5 else 0,
            'duration_ms': round(duration, 4)
        }
    
    def test_coloring(self):
        """Welsh-Powell renklendirme performans testi"""
        if not self.graph.nodes:
            return None
        
        start_time = time.time()
        colors = Algorithms.welsh_powell(self.graph)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        unique_colors = len(set(colors.values()))
        
        return {
            'algorithm': 'Welsh-Powell',
            'nodes_colored': len(colors),
            'colors_used': unique_colors,
            'duration_ms': round(duration, 4)
        }
    
    def test_connected_components(self):
        """Bağlı bileşenler performans testi"""
        if not self.graph.nodes:
            return None
        
        start_time = time.time()
        components = Algorithms.find_connected_components(self.graph)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        
        return {
            'algorithm': 'Connected Components',
            'num_components': len(components),
            'largest_component': max(len(c) for c in components) if components else 0,
            'duration_ms': round(duration, 4)
        }
    
    def run_all_tests(self, iterations=5):
        """Tüm testleri çalıştır"""
        print(f"\n{'='*70}")
        print(f"📊 PERFORMANS TESTLERİ: {self.csv_file}")
        print(f"{'='*70}")
        print(f"Graf Boyutu: {len(self.graph.nodes)} düğüm, {len(self.graph.edges)} kenar")
        print(f"Test Sayısı: {iterations} iterasyon\n")
        
        tests = [
            ('BFS', self.test_bfs),
            ('DFS', self.test_dfs),
            ('Dijkstra', self.test_dijkstra),
            ('A*', self.test_astar),
            ('Degree Centrality', self.test_centrality),
            ('Welsh-Powell', self.test_coloring),
            ('Connected Components', self.test_connected_components)
        ]
        
        for test_name, test_func in tests:
            durations = []
            results_data = None
            
            for i in range(iterations):
                result = test_func()
                if result:
                    durations.append(result['duration_ms'])
                    results_data = result
            
            if durations:
                avg_duration = sum(durations) / len(durations)
                min_duration = min(durations)
                max_duration = max(durations)
                
                print(f"🔹 {test_name}")
                print(f"   Ortalama: {avg_duration:.4f}ms")
                print(f"   Min: {min_duration:.4f}ms | Max: {max_duration:.4f}ms")
                
                if results_data:
                    for key, value in results_data.items():
                        if key not in ['algorithm', 'duration_ms']:
                            print(f"   {key}: {value}")
                
                # Sonuçları kaydet
                self.results.append({
                    'csv_file': self.csv_file,
                    'algorithm': test_name,
                    'avg_duration_ms': round(avg_duration, 4),
                    'min_duration_ms': round(min_duration, 4),
                    'max_duration_ms': round(max_duration, 4),
                    'graph_nodes': len(self.graph.nodes),
                    'graph_edges': len(self.graph.edges)
                })
                
                print()
    
    def save_results_to_csv(self, output_file='performance_results.csv'):
        """Test sonuçlarını CSV'ye kaydet"""
        if not self.results:
            print("❌ Kaydedilecek sonuç yok!")
            return
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if self.results:
                fieldnames = self.results[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)
        
        print(f"✅ Sonuçlar kaydedildi: {output_file}")


def main():
    """Ana test fonksiyonu"""
    test_files = [
        'test_small_10.csv',
        'test_small_20.csv',
        'test_medium_50.csv',
        'test_medium_100.csv'
    ]
    
    all_results = []
    
    for test_file in test_files:
        try:
            tester = PerformanceTester(test_file)
            if tester.load_graph():
                tester.run_all_tests(iterations=5)
                all_results.extend(tester.results)
        except FileNotFoundError:
            print(f"⚠️ Dosya bulunamadı: {test_file}")
            print(f"   Önce 'test_graph_generator.py' çalıştırın!\n")
            continue
    
    # Tüm sonuçları tek CSV'de topla
    if all_results:
        with open('all_performance_results.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = all_results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        
        print(f"\n{'='*70}")
        print("✅ TÜM SONUÇLAR KAYDEDİLDİ: all_performance_results.csv")
        print(f"{'='*70}\n")
        
        # Özet tablosu
        print("📊 ÖZET TABLO\n")
        print(f"{'Algoritma':<25} {'10 Düğüm':<12} {'20 Düğüm':<12} {'50 Düğüm':<12} {'100 Düğüm':<12}")
        print("-" * 73)
        
        algorithms = list(set(r['algorithm'] for r in all_results))
        for algo in algorithms:
            row = [algo]
            for test_file in test_files:
                matching = [r for r in all_results if r['algorithm'] == algo and test_file in r['csv_file']]
                if matching:
                    row.append(f"{matching[0]['avg_duration_ms']:.2f}ms")
                else:
                    row.append("N/A")
            print(f"{row[0]:<25} {row[1]:<12} {row[2]:<12} {row[3]:<12} {row[4]:<12}")


if __name__ == "__main__":
    main()