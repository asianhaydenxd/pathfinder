from node import Node, NodeState
from path import Path

class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.start = self.get_node_with_state(NodeState.START)
        self.target = self.get_node_with_state(NodeState.TARGET)
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])
    
    def __str__(self):
        return str(self.matrix)

    def get_node_with_state(self, state):
        for index, row in enumerate(self.matrix):
            if state.value in row:
                return Node(index, row.index(state.value), None)
        raise ValueError(f'Value {state} ({state.value}) does not exist in map.')
    
    def get_path(self):
        open = []
        closed = []
        open.append(self.start)
        return self.get_final_node(open, closed)
    
    def get_final_node(self, open, closed):
        while True:
            next_node = self.get_next_node(open, closed)
            if next_node:
                return Path(next_node, open, closed)
    
    def get_next_node(self, open, closed):
        current = self.get_best_node(open)
        open.remove(current)
        closed.append(current)

        if current == self.target:
            return current

        self.add_neighbors_to_open(current, open, closed)
    
    def add_neighbors_to_open(self, node, open, closed):
        for neighbor in node.get_neighbors():
            if neighbor.is_blocked(self) or neighbor.is_in_list(closed):
                continue

            if not neighbor in open:
                open.append(neighbor)
    
    def get_best_node(self, node_list):
        hashmap = []
        best_node = node_list[0]
        
        for node in node_list:
            node_total_distance = node.get_total_distance(self.start, self.target)
            hashmap.append(node_total_distance)
            if min(hashmap) == node_total_distance:
                best_node = node
        
        return best_node
    
    def get_path_list(self):
        return self.get_path().get_list()
    
    def new(rows=5, cols=5, start=(0,0), target=(4,4)):
        new_map = [[0 for _ in range(cols)] for _ in range(rows)]

        start_row, start_col = start
        target_row, target_col = target

        new_map[start_row][start_col] = NodeState.START.value
        new_map[target_row][target_col] = NodeState.TARGET.value

        return Map(new_map)