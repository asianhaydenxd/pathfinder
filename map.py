from node import Node
from path import Path

class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.start = self.get_node_with_value(2)
        self.target = self.get_node_with_value(3)
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])
    
    def __str__(self):
        return str(self.matrix)

    def get_node_with_value(self, target):
        for index, row in enumerate(self.matrix):
            if target in row:
                return Node(index, row.index(target), None)
        raise ValueError('No value exists in map')

    def get_best_node(self, node_list):
        hashmap = []
        best_node = node_list[0]
        
        for node in node_list:
            node_total_distance = node.get_total_distance(self.start, self.target)
            hashmap.append(node_total_distance)
            if min(hashmap) == node_total_distance:
                best_node = node
        
        return best_node
    
    def get_path(self):
        open = []
        closed = []
        open.append(self.start)
        return self.iterate_through_path(open, closed)
    
    def iterate_through_path(self, open, closed):
        while True:
            next_node = self.get_next_node(open, closed)
            if next_node != None:
                return Path(next_node, open, closed)
    
    def get_next_node(self, open, closed):
        current = self.get_best_node(open)
        open.remove(current)
        closed.append(current)

        if current.is_equal_to(self.target):
            return current

        self.iterate_through_neighbors(current, open, closed)
    
    def iterate_through_neighbors(self, node, open, closed):
        for neighbor in node.get_neighbors():
            if neighbor.is_blocked(self) or neighbor.is_in_list(closed):
                continue

            if not neighbor in open:
                open.append(neighbor)
    
    def get_path_list(self):
        return self.get_path().get_list()