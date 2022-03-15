from collections import deque
from sys import argv
import numpy as np
import math as mt

# Get arguments
## File name
mapFile = argv[1]
## Algorithm values: bfs, ucs, or astar
algorithm = argv[2]
## Heuristic values: euclidean or manhattan
heuristic = argv[3] if(len(argv) == 2) else " "

# mapFile = open(map, "r")
with open(mapFile) as infile_object:
    lines = infile_object.read().splitlines()

# Generate 2D array map
rowSize = int(lines[0].split(" ")[0])
colSize = int(lines[0].split(" ")[1])
map = np.empty((rowSize, colSize), str)

# Create a 2D map array
for pointer in range(3, len(lines)):
    col = 0
    for char in lines[pointer].split(" "):
        map[pointer-3][col] = char
        col += 1


# Function to check if a next point
# is be visited or not and valid
def isValid( row, col, visited):
    # Check if cell is not on map
    if (row < 0 or col < 0 or row >= rowSize or col >= colSize):
        return False

    # Check if cell is already visited
    if (visited[row][col]):
        return False

    if ( map[row][col] == 'X'):
        return False

    # Otherwise
    return True


class Point:
    def __init__(self, x: float, y: float, val: float):
        self.x = x
        self.y = y
        self.val = val
        self.heuristic = 0.0
        self.head = None

    def addHead(self, pt):
        assert isinstance(pt, Point)
        self.head = pt

    def addHeuristic(self, target, type):
        assert isinstance(target, Point)

        if type.lower() == 'euclidean':
            self.heuristic = mt.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
        elif type.lower() == 'manhattan':
            self.heuristic = abs(self.x - target.x) + abs(self.y - target.y)


class queueNode:
    def __init__(self, pt: Point, dist: float):
        self.head = None
        self.pt = pt  # The coordinates of the cell
        self.dist = dist


# Draw path function
def drawPath(pt: Point):
    path = deque()
    path.append(pt)
    counter = 0
    while path:
        pointer = path.popleft()
        map[pointer.x][pointer.y] = '*'
        if (pointer.head != None):
            path.append(pointer.head)
        else:
            break
        counter += 1


# Print map function
def printMap(map):
    for i in range (0, rowSize):
        for j in range (0, colSize):
            print(map[i][j], end = ' ')
        print("")


#Calculate cost
def calculateCost(curr: Point, next: Point):

    if(curr.val < next.val):
        return 1.0 + next.val - curr.val

    return 1.0


# These arrays are used to get next cells in 4 direction Up, Down, Left Right
rowNum = [1, 0, 0,- 1]
colNum = [0, 1, -1, 0]

# Get start and end point corr by extracting text file
startX = int(lines[1].split(" ")[0]) -1
startY = int(lines[1].split(" ")[1]) -1
endX = int(lines[2].split(" ")[0]) -1
endY = int(lines[2].split(" ")[1]) -1


# Driver code
def main():

    # Init some variable
    start = Point(startX, startY, float(map[startX][startY]))
    end = Point(endX, endY, float(map[endX][endY]))
    fValue = -1.0


    if(algorithm.lower() == 'bfs'):
        fValue = bfs(map, start, end)
    elif(algorithm.lower() == 'ucs'):
        fValue = ucs(map, start, end)
    elif (algorithm.lower() == "astar"):
        # add hueristic for start point
        print("in")
        start.addHeuristic(end, heuristic)
        fValue = aStart(map, start, end)


    if fValue != -1.0:
        printMap(map)
    else:
        print("null")

main()