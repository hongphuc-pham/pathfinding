from sys import argv
import numpy as np

# Get arguments
## File name
mapFile = argv[1]
## Algorithm values: bfs, ucs, or astar
algorithm = argv[2]
## Heuristic values: euclidean or manhattan
heuristic = argv[3]

#### Test cmd line: python pathfinder.py map.txt bfs euclidean

# mapFile = open(map, "r")
with open(mapFile) as infile_object:
    lines = infile_object.read().splitlines()

# Generate 2D array map
map = np.empty((int(lines[0].split(" ")[0]), int(lines[0].split(" ")[1])), str)
startX = int(lines[1].split(" ")[0])
startY = int(lines[1].split(" ")[1])
endX = int(lines[2].split(" ")[0])
endY = int(lines[2].split(" ")[1])

print(startX, " - ", startY)

for pointer in range(3, len(lines)):
    col = 0
    for char in lines[pointer].split(" "):
        map[pointer-3][col] = char
        col += 1

