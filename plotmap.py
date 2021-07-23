from path import Path
from node import Node, NodeState
from map import Map
from matplotlib import pyplot as plt
from matplotlib import colors

DEFAULT_COLORMAP = {
    NodeState.BLANK: '#fff',
    NodeState.WALL: '#033',
    NodeState.START: '#193',
    NodeState.TARGET: '#c32',
    NodeState.PATH: '#db1',
    NodeState.CLOSED: '#27b',
    NodeState.OPEN: '#1bd'
}

class Color:
    def __init__(self, colormap):
        self.colormap = self.check_colormap_keys(colormap)
        self.colors = self.get_colors(self.colormap)
    
    def check_colormap_keys(self, colormap):
        for state in NodeState:
            if not state in colormap:
                colormap[state] = DEFAULT_COLORMAP[state]
        return colormap

    def get_colors(self, colormap):
        color_list = [colormap[state] for state in NodeState]
        if len(color_list) - 1 < max(NodeState, key=lambda k: k.value).value:
            raise ValueError('Invalid NodeState static variables (must be consecutive integers from 0)')
        return color_list

class PlotMap:
    def __init__(self, map: Map, colormap=DEFAULT_COLORMAP):
        self.map = map
        self.color = Color(colormap)
    
    def plot(self):
        path_matrix = self.append_path()
        self.show_plot_window(path_matrix)
    
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
    
    def show_plot_window(self, matrix):
        plt.imshow(matrix, cmap=PlotMap.get_colors(self.color.colors))
        plt.show()
    
    def get_colors(colormap):
        return colors.ListedColormap(colormap)