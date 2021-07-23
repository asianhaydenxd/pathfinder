from map import Map, NodeType
from matplotlib import pyplot as plt
from matplotlib import colors

DEFAULT_COLORMAP = {
    NodeType.BLANK: (255, 255, 255), # White
    NodeType.WALL: (0, 0, 0), # Black
    NodeType.START: (22, 219, 75), # Green
    NodeType.TARGET: (232, 55, 35), # Red
    NodeType.PATH: (255, 205, 54), # Yellow
    NodeType.CLOSED: (58, 145, 214), # Blue
    NodeType.OPEN: (39, 117, 179), # Darker Blue
}

class Color:
    def __init__(self, colormap):
        colormap = self.fill_missing_keys(colormap)
        self.colors = self.get_colors(colormap)
        self.base_colors = self.get_base_colors(colormap)
    
    def fill_missing_keys(self, colormap):
        for type in NodeType:
            if not type in colormap:
                colormap[type] = DEFAULT_COLORMAP[type]
        return colormap

    def get_colors(self, colormap):
        return [colormap[type] for type in colormap]
    
    def get_base_colors(self, colormap):
        return [colormap[type] for type in colormap if type.is_from_init]

class PlotMap:
    def __init__(self, map: Map, colormap=DEFAULT_FULL_COLORMAP):
        self.map = map
        self.color = Color(colormap)
    
    def plot(self, plain=False):
        if plain:
            self.show_plot_window(self.map.matrix, base_only=True)
            return
        path_matrix = self.append_path()
        self.show_plot_window(path_matrix, base_only=False)
    
    def append_path(self):
        matrix = self.map.matrix
        self.append_open_nodes(matrix)
        self.append_closed_nodes(matrix)
        self.append_path_nodes(matrix)
        return matrix
    
    def append_open_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path().open, NodeState.OPEN.value)
    
    def append_closed_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path().closed, NodeState.CLOSED.value)
    
    def append_path_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path_list(), NodeState.PATH.value)
    
    def replace_matrix(self, matrix, list, val):
        for node in list:
            if self.is_at_end(node):
                continue
            row, col = node.get_coords()
            matrix[row][col] = val
    
    def is_at_end(self, node):
        return node == self.map.start or node == self.map.target
    
    def show_plot_window(self, matrix, base_only=False):
        plt.xlabel('Col')
        plt.ylabel('Row')
        plt.imshow(matrix, cmap=PlotMap.get_colors(self.color.base_colors if base_only else self.color.colors))
        plt.show()
    
    def get_colors(colormap):
        return colors.ListedColormap(colormap)