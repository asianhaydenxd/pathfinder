class Map:
    def __init__(self, map):
        self.map = map
        self.start = self.get_node_with_value(2)
        self.target = self.get_node_with_value(3)
        self.height = len(self.map)
        self.width = len(self.map[0])
    
    def __str__(self):
        return str(self.map)

    def get_node_with_value(self, target):
        for index, row in enumerate(self.map):
            if target in row:
                return Node(index, row.index(target), None)
        raise ValueError('No value exists in map')
