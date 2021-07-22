class Node:
    def __init__(self, row, col, parent):
        self.row = row
        self.col = col
        self.parent = parent
    
    def __str__(self):
        return str(self.__dict__)
    
    def get_coords(self):
        return (self.row, self.col)
