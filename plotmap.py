from node import Node
from map import Map
from matplotlib import pyplot as plt
from matplotlib import colors

BLANK = '#fff'
WALL = '#033'
START = '#193'
TARGET = '#c32'
PATH = '#db1'
CLOSED = '#27b'
OPEN = '#1bd'

COLORS = [BLANK, WALL, START, TARGET, PATH, CLOSED, OPEN]

class PlotMap:
    def __init__(self, map: Map): # remember to type all other args
        self.map = map
    
    def plot(self):
        path_matrix = self.append_path()
        PlotMap.show_plot_window(path_matrix)
    
    def append_path(self):
        matrix = self.map.matrix
        self.append_open_nodes(matrix)
        self.append_closed_nodes(matrix)
        self.append_path_nodes(matrix)
        return matrix
    
    def append_open_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path().open, 6)
    
    def append_closed_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path().closed, 5)
    
    def append_path_nodes(self, matrix):
        self.replace_matrix(matrix, self.map.get_path_list(), 4)
    
    def replace_matrix(self, matrix, list, val):
        for node in list:
            if self.is_at_end(node):
                continue
            row, col = node.get_coords()
            matrix[row][col] = val
    
    def is_at_end(self, node):
        return node.is_equal_to(self.map.start) or node.is_equal_to(self.map.target)
    
    def show_plot_window(matrix):
        plt.imshow(matrix, cmap=PlotMap.get_colors(COLORS))
        plt.show()
    
    def get_colors(colormap):
        return colors.ListedColormap(colormap)