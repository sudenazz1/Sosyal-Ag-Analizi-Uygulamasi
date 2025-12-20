import heapq

class Algorithms:
    @staticmethod
    def bfs(graph, start_id):
        visited = set()
        queue = [start_id]
        visited.add(start_id)
        result = []
        while queue:
            vertex = queue.pop(0)
            result.append(vertex)
            for neighbor in graph.adjacency_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    @staticmethod
    def dfs(graph, start_id):
        visited = set()
        stack = [start_id]
        result = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                neighbors = sorted(graph.adjacency_list.get(vertex, []), reverse=True)
                stack.extend(neighbors)
        return result

    @staticmethod
    def dijkstra(graph, start_id, end_id):
        distances = {node: float('inf') for node in graph.nodes}
        distances[start_id] = 0
        previous = {node: None for node in graph.nodes}
        pq = [(0, start_id)]
        
        while pq:
            d, current = heapq.heappop(pq)
            if current == end_id: break
            if d > distances[current]: continue
            
            for neighbor in graph.adjacency_list.get(current, []):
                weight = graph.get_edge_weight(current, neighbor)
                new_dist = d + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        path = []
        curr = end_id
        if distances[end_id] == float('inf'): return [], float('inf')
        while curr is not None:
            path.insert(0, curr)
            curr = previous[curr]
        return path, distances[end_id]

    @staticmethod
    def a_star(graph, start_id, end_id):
        def heuristic(id1, id2):
            return abs(graph.nodes[id1].aktiflik - graph.nodes[id2].aktiflik)

        open_set = [(0, start_id)]
        came_from = {}
        g_score = {node: float('inf') for node in graph.nodes}
        g_score[start_id] = 0
        f_score = {node: float('inf') for node in graph.nodes}
        f_score[start_id] = heuristic(start_id, end_id)
        
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == end_id:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_id)
                return path[::-1], g_score[end_id]
            
            for neighbor in graph.adjacency_list.get(current, []):
                weight = graph.get_edge_weight(current, neighbor)
                tentative_g = g_score[current] + weight
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end_id)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return [], float('inf')