from path import Path
from node import Node, NodeState
from map import Map
from matplotlib import pyplot as plt
from matplotlib import colors

DEFAULT_BASE_COLORMAP = {
    NodeState.BLANK: '#fff',
    NodeState.WALL: '#033',
    NodeState.START: '#193',
    NodeState.TARGET: '#c32'
}

DEFAULT_FULL_COLORMAP = {
    NodeState.PATH: '#db1',
    NodeState.CLOSED: '#27b',
    NodeState.OPEN: '#1bd'
}
DEFAULT_FULL_COLORMAP.update(DEFAULT_BASE_COLORMAP)

class Color:
    def __init__(self, colormap):
        colormap = self.fill_missing_keys(colormap)
        self.colors = self.get_colors(colormap)
        self.base_colors = self.get_base_colors(colormap)
    
    def fill_missing_keys(self, colormap):
        for state in NodeState:
            if not state in colormap:
                colormap[state] = DEFAULT_FULL_COLORMAP[state]
        return colormap

    def get_colors(self, colormap):
        color_list = [colormap[state] for state in NodeState]
        largest_colormap_int = max(NodeState, key=lambda k: k.value).value
        if len(color_list) - 1 < largest_colormap_int:
            raise ValueError('Invalid NodeState static variables (must be consecutive integers from 0)')
        return color_list
    
    def get_base_colors(self, colormap):
        return [colormap[state] for state in (nodestate for nodestate in DEFAULT_BASE_COLORMAP)]

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