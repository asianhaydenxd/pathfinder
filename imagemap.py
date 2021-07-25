from PIL import Image
from pathfinder import NodeType
import numpy
import webcolors

class ImageMap:
    def __init__(self, image_name):
        self.image_name = image_name
        self.image = Image.open(image_name).convert('RGB')
        self.matrix = numpy.array(self.image)
        self.colormap = {
            (255, 255, 255): NodeType.BLANK.value,
            (0, 0, 0): NodeType.WALL.value,
            (0, 255, 0): NodeType.START.value,
            (255, 0, 0): NodeType.TARGET.value,
        }
    
    def generate_map(self):
        return [[self.get_node_type(node) for node in row] for row in self.matrix]
    
    def get_node_type(self, node):
        node = tuple(node)
        return self.colormap[node]