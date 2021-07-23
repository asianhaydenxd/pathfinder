from map import Map
from node import Node, NodeState
from plotmap import PlotMap

small_map = Map([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 1],
])

large_map = Map([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,3,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
    [0,2,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,0,1,0,0,1,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
])

custom_map = Map.new(20, 15, (0, 0), (19, 14))

path = custom_map.get_path()
print(f'Node: {path.node}')
print(f'Open: {Node.list_coords(path.open)}')
print(f'Closed: {Node.list_coords(path.closed)}')
print(f'Checks: {path.checks}')
print(f'List: {Node.list_coords(path.list)}')

pltmap = PlotMap(small_map)
pltmap.plot()