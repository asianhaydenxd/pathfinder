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