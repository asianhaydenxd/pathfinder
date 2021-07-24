from copy import deepcopy
from enum import Enum, auto

TURN_WEIGHT = 0
HEURISTIC_WEIGHT = 0

class NodeTypeInitiator:
    def __init__(self, type, is_from_init=True):
        self.type = type
        self.is_from_init = is_from_init

    def __str__(self):
        return f'NodeType.{self.type}.value'

class NodeType(Enum):
    BLANK = NodeTypeInitiator('BLANK')
    WALL = NodeTypeInitiator('WALL')
    START = NodeTypeInitiator('START')
    TARGET = NodeTypeInitiator('TARGET')
    PATH = NodeTypeInitiator('PATH', is_from_init=False)
    OPEN = NodeTypeInitiator('OPEN', is_from_init=False)
    CLOSED = NodeTypeInitiator('CLOSED', is_from_init=False)

class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

class Node:
    def __init__(self, row, col, parent, direction=None):
        self.row = row
        self.col = col
        self.parent = parent
        self.direction = direction
        self.g_score = float('inf')
    
    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def get_coords(self):
        return (self.row, self.col)
    
    def get_f_score(self, target):
        return self.g_score + self.get_distance_from_target(target)
    
    def get_distance_from_target(self, target):
        return (self.get_horizontal_distance(target) + self.get_vertical_distance(target)) * (1 + HEURISTIC_WEIGHT)
    
    def get_horizontal_distance(self, node):
        return abs(self.row - node.row)
    
    def get_vertical_distance(self, node):
        return abs(self.col - node.col)
    
    def get_neighbors(self):
        neighbor_north = Node(self.row - 1, self.col, self, Direction.NORTH)
        neighbor_south = Node(self.row + 1, self.col, self, Direction.SOUTH)

        neighbor_west = Node(self.row, self.col - 1, self, Direction.WEST)
        neighbor_east = Node(self.row, self.col + 1, self, Direction.EAST)

        neighbors = [neighbor_north, neighbor_east, neighbor_south, neighbor_west]
        
        return neighbors
    
    def is_blocked(self, map):
        return self.is_out_of_bounds(map) or self.is_wall(map)
    
    def is_out_of_bounds(self, map):
        return self.is_outside_lower_bound() or self.is_outside_upper_bound(map)
    
    def is_outside_lower_bound(self):
        return self.row < 0 or self.col < 0
    
    def is_outside_upper_bound(self, map):
        return self.row + 1 > map.height or self.col + 1 > map.width
    
    def is_wall(self, map):
        return map.matrix[self.row][self.col] == NodeType.WALL.value

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
        while len(open) > 0:
            next_node = self.get_next_node(open, closed)
            if next_node:
                return Path(next_node, open, closed)
        return Path(self.start, open, closed)
    
    def get_next_node(self, open, closed):
        current = self.get_best_node(open)
        
        open.remove(current)
        closed.append(current)

        if current == self.target:
            return current

        self.add_neighbors_to_open(current, open, closed)
    
    def add_neighbors_to_open(self, node, open, closed):
        for neighbor in node.get_neighbors():
            if neighbor.is_blocked(self) or neighbor in closed:
                continue
            
            ideal_g_score = node.g_score + 1
            if neighbor.g_score > ideal_g_score:
                if neighbor.direction == node.direction:
                    neighbor.g_score = ideal_g_score
                else:
                    neighbor.g_score = ideal_g_score * (1 + TURN_WEIGHT)

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
    
    def new(rows=5, cols=5, start=(0,0), target=(4,4), walls=[]):
        new_matrix = [[NodeType.BLANK.value for _ in range(cols)] for _ in range(rows)]

        start_row, start_col = start
        target_row, target_col = target

        new_matrix[start_row][start_col] = NodeType.START.value
        new_matrix[target_row][target_col] = NodeType.TARGET.value

        new_map = Map(new_matrix)
        new_map.append_walls(walls)

        return new_map
    
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

class Path:
    def __init__(self, node, open_list, closed_list):
        self.node = node
        self.open = open_list
        self.closed = closed_list
        self.checks = len(self.open)+len(self.closed)
        self.list = self.get_list()
    
    def get_list(self):
        node = self.node
        path_list = [node]

        while node.parent:
            node = node.parent
            path_list.append(node)

        path_list.reverse()
        return path_list

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
        compiled_matrix = deepcopy(self.matrix)
        for row_i, row in enumerate(compiled_matrix):
            for col_i, node in enumerate(row):
                try: compiled_matrix[row_i][col_i] = self.keys[node]
                except KeyError:
                    if not force:
                        raise ValueError('MapCompiler matrix contains uncompilable value.')
                    compiled_matrix[row_i][col_i] = NodeType.BLANK.value
        return compiled_matrix

class CompiledMap(Map):
    def __init__(self, matrix, blank=0, wall=1, start=2, target=3):
        super().__init__(MapCompiler(matrix, blank, wall, start, target).compile())

def list_coords(node_list):
        return [node.get_coords() for node in node_list]