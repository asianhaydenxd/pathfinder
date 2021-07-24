import pathfinder as pf
from plotmap import PlotMap
from imagemap import ImageMap

pf.TURN_WEIGHT = 2

# Maps

small_map = pf.CompiledMap([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 0],
])

large_map = pf.CompiledMap([
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

custom_map = pf.Map.new(
    rows=7, 
    cols=15, 
    start=(0, 0), 
    target=(6, 14), 
    walls=[(6, 1), (6, 2), (5, 3), (4, 4)]
)
custom_map.append_walls([(4, 4), (3, 3)])
custom_map.relocate_start((0, 1))
custom_map.relocate_target((6, 12))

image_map = pf.Map(ImageMap('map.png').generate_map())

# Pathfinding

pltmap = PlotMap(image_map)
pltmap.plot(plain=True)
pltmap.plot()

path = image_map.get_path()

path.node # Last node in path
path.checks # Number of times the algorithm checked a node
pf.list_coords(path.open) # Lists all open nodes
pf.list_coords(path.closed) # Lists all closed nodes
pf.list_coords(path.list) # Lists the nodes along the path from the starting node