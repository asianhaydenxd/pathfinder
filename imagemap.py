from PIL import Image
from pathfinder import NodeType
import numpy
import webcolors

class ImageMap:
    def __init__(self, image_name):
        self.image_name = image_name
        self.image = Image.open(image_name).convert('RGB')
        self.matrix = numpy.array(self.image)
    
    def generate_map(self):
        return [[self.get_node_type(node) for node in row] for row in self.matrix]
    
    def get_node_type(self, node):
        colormap = {
            'white': NodeType.BLANK.value,
            'black': NodeType.WALL.value,
            'lime': NodeType.START.value,
            'red': NodeType.TARGET.value,
        }
        return colormap[self.closest_color(node)]
    
    def closest_color(self, requested_color):
        requested_color = tuple(requested_color)
        min_colors = {}
        for key, name in webcolors.html4_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]