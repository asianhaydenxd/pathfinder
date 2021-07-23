from map import CompiledMap, Map
from node import Node
from plotmap import PlotMap

# small_map = Map([
#     [0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 3],
#     [0, 0, 1, 0, 0],
#     [0, 0, 1, 0, 0],
#     [2, 0, 1, 0, 1],
# ])

large_map = CompiledMap([
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

pltmap = PlotMap(large_map)
pltmap.plot(plain=True)
pltmap.plot()

path = large_map.get_path()

path.node # Last node in path
path.checks # Number of times the algorithm checked a node
Node.list_coords(path.open) # Lists all open nodes
Node.list_coords(path.closed) # Lists all closed nodes
Node.list_coords(path.list) # Lists the nodes along the path from the starting node