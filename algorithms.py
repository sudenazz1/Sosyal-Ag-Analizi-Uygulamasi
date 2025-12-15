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