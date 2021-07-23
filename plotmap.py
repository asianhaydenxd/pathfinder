from map import Map, NodeType
from matplotlib import pyplot as plt

DEFAULT_COLORMAP = {
    NodeType.BLANK.value: (255, 255, 255), # White
    NodeType.WALL.value: (0, 0, 0), # Black
    NodeType.START.value: (22, 219, 75), # Green
    NodeType.TARGET.value: (232, 55, 35), # Red
    NodeType.PATH.value: (255, 205, 54), # Yellow
    NodeType.CLOSED.value: (58, 145, 214), # Blue
    NodeType.OPEN.value: (39, 117, 179), # Darker Blue
}

class Color:
    def __init__(self, colormap):
        self.colors = self.fill_missing_keys(colormap)
    
    def fill_missing_keys(self, colormap):
        for type in NodeType:
            if not type.value in colormap:
                colormap[type] = DEFAULT_COLORMAP[type]
        return colormap

class PlotMap:
    def __init__(self, map: Map, colormap=DEFAULT_COLORMAP):
        self.map = map
        self.color = Color(colormap)
    
    def plot(self, plain=False):
        if plain:
            self.show_plot_window(self.map.matrix, base_only=True)
            return
        path_matrix = self.append_path()
        self.show_plot_window(path_matrix)
    
    def show_plot_window(self, matrix, base_only=False):
        plt.xlabel('Col')
        plt.ylabel('Row')
        plt.imshow(self.get_color_matrix(matrix, self.color.colors))
        plt.show()
    
    def get_color_matrix(self, matrix, colormap):
        for row_i, row in enumerate(matrix):
            for col_i, node in enumerate(row):
                matrix[row_i][col_i] = colormap[node]
        return matrix
    
    def append_path(self):
        matrix = self.map.matrix
        self.append_open_nodes(matrix)
        self.append_closed_nodes(matrix)
        self.append_path_nodes(matrix)
        return matrix
    
    def append_open_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path().open, NodeType.OPEN.value)
    
    def append_closed_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path().closed, NodeType.CLOSED.value)
    
    def append_path_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path_list(), NodeType.PATH.value)
    
    def replace_matrix(self, matrix, list, type):
        for node in list:
            if self.is_at_end(node):
                continue
            row, col = node.get_coords()
            matrix[row][col] = type
    
    def is_at_end(self, node):
        return node == self.map.start or node == self.map.target