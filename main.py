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

custom_map = Map.new(7, 15, (0, 0), (6, 14))
custom_map.append_walls([(6, 1), (6, 2), (5, 3), (4, 4)])
custom_map.relocate_start((0,1))
custom_map.relocate_target((6,12))

pltmap = PlotMap(custom_map)
pltmap.plot()

# path = custom_map.get_path()
# print(f'Node: {path.node}')
# print(f'Open: {Node.list_coords(path.open)}')
# print(f'Closed: {Node.list_coords(path.closed)}')
# print(f'Checks: {path.checks}')
# print(f'List: {Node.list_coords(path.list)}')