from map import MapCompiler as mapc

compiled = mapc([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 1],
]).compile()