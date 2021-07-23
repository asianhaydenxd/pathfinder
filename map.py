from enum import Enum, unique
from path import Path
import node as Node

class NodeTypeInitiator:
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return f'NodeType.{self.type}.value'

@unique
class NodeType(Enum):
    BLANK = NodeTypeInitiator('BLANK')
    WALL = NodeTypeInitiator('WALL')
    START = NodeTypeInitiator('START')
    TARGET = NodeTypeInitiator('TARGET')
    PATH = NodeTypeInitiator('PATH')
    OPEN = NodeTypeInitiator('OPEN')
    CLOSED = NodeTypeInitiator('CLOSED')
    
    FROM_ASSIGN = [BLANK, WALL, START, TARGET]
    FROM_PATH = [PATH, OPEN, CLOSED]

class MapCompiler:
    def __init__(self, matrix, blank=0, wall=1, start=2, target=3):
        self.matrix = matrix
        if self.has_duplicate_values([blank, wall, start, target]):
            raise ValueError('MapCompiler keys cannot have duplicate values.')
        self.keys = {
            blank: NodeType.BLANK.value,
            wall: NodeType.WALL.value,
            start: NodeType.START.value,
            target: NodeType.TARGET.value,
        }
    
    def has_duplicate_values(self, keys):
        return len(keys) != len(set(keys))
    
    def compile(self, force=False):
        compiled_matrix = self.matrix
        for row_i, row in enumerate(compiled_matrix):
            for col_i, node in enumerate(row):
                try:
                    compiled_matrix[row_i][col_i] = self.keys[node]
                except KeyError:
                    if not force:
                        raise ValueError('MapCompiler matrix contains uncompilable value.')
                    compiled_matrix[row_i][col_i] = NodeType.BLANK.value

        return compiled_matrix

class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.start = self.get_node_of_type(NodeType.START.value)
        self.target = self.get_node_of_type(NodeType.TARGET.value)
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])
    
    def __str__(self):
        return str([[node.type for node in row] for row in self.matrix])

    def get_node_of_type(self, type):
        for index, row in enumerate(self.matrix):
            if type in row:
                return Node(index, row.index(type), None)
        raise ValueError(f'Value {type} does not exist in map.')
    
    def get_path(self):
        open = []
        closed = []
        open.append(self.start)
        self.start.g_score = 0
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
            
            ideal_g_score = node.g_score + 1
            if neighbor.g_score > ideal_g_score:
                neighbor.g_score = ideal_g_score
                if not neighbor in open:
                    open.append(neighbor)
    
    def get_best_node(self, node_list):
        hashmap = []
        best_node = node_list[0]
        
        for node in node_list:
            node_total_distance = node.get_f_score(self.target)
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

        new_map[start_row][start_col] = NodeType.START.value
        new_map[target_row][target_col] = NodeType.TARGET.value

        return Map(new_map)
    
    def append_walls(self, coords: list):
        if self.start.get_coords() in coords:
            raise ValueError('Wall cannot be appended on top of the start node.')
        if self.target.get_coords() in coords:
            raise ValueError('Wall cannot be appended on top of the target node.')
        
        for node in coords:
            row, col = node
            self.matrix[row][col] = NodeType.WALL.value
    
    def relocate_start(self, new_coords: tuple):
        self.start = self.relocate_node(self.start, NodeType.START.value, new_coords)
    
    def relocate_target(self, new_coords: tuple):
        self.target = self.relocate_node(self.target, NodeType.TARGET.value, new_coords)
    
    def relocate_node(self, node, type, new_coords) -> Node:
        prev_row, prev_col = node.get_coords()
        new_row, new_col = new_coords
        new_node = Node(new_row, new_col, None)

        if new_node.is_out_of_bounds(self):
            raise ValueError(f'The provided coordinates for the new {type} node are out of bounds.')
        
        self.matrix[prev_row][prev_col] = NodeType.BLANK.value
        self.matrix[new_row][new_col] = type
        return new_node