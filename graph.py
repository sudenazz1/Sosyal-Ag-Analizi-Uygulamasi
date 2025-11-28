from node import Node
from edge import Edge

class SocialGraph:
    def __init__(self):
        self.nodes = {} 
        self.edges = [] 
        self.adjacency_list = {} 

    def add_node(self, node):
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []