from collections import deque
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
rowSize = int(lines[0].split(" ")[0])
colSize = int(lines[0].split(" ")[1])
map = np.empty((rowSize, colSize), str)

# Create a 2D map array
for pointer in range(3, len(lines)):
    col = 0
    for char in lines[pointer].split(" "):
        map[pointer-3][col] = char
        col += 1

# Function to check if a cell
# is be visited or not

def isValid( row, col, visited):
    # Check if cell is not on map
    if (row < 0 or col < 0 or row >= rowSize or col >= colSize):
        return False

    # Check if cell is already visited
    if (visited[row][col]):
        return False

    # Otherwise
    return True

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.head = None

    def addHead(self, pt):
        assert isinstance(pt, Point)
        self.head = pt


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

# These arrays are used to get row and column
# numbers of 4 neighbours of a given cell
rowNum = [1, 0, 0, 1]
colNum = [0, 1, 1, 0]

def bfs(map, start: Point, end: Point):
    # Declare the visited array
    visited = [[False for i in range(colSize)] for i in range(rowSize)]

    visited[start.x][start.y] = True

    # Create a queue for BFS
    q = deque()

    # Distance of source cell is 0
    q.append(start)  # Enqueue source cell

    while q:

        curr = q.popleft()  # Dequeue the front cell

        if curr.x == end.x and curr.y == end.y:
            drawPath(curr)
            return 1

        # Otherwise enqueue its adjacent cells
        for i in range(4):
            row = curr.x + rowNum[i]
            col = curr.y + colNum[i]

            # if adjacent cell is valid, has path
            # and not visited yet, enqueue it.
            if (isValid(row, col, visited) and
                    map[row][col] == '1' ):
                visited[row][col] = True
                childPoint = Point(row, col)
                childPoint.addHead(curr)

                q.append(childPoint)

        # Return -1 if destination cannot be reached

    return -1

# Driver code
def main():

    start = Point(int(lines[1].split(" ")[0]) -1, int(lines[1].split(" ")[1]) -1)
    end = Point(int(lines[2].split(" ")[0]) -1, int(lines[2].split(" ")[1]) -1)

    dist = bfs(map, start, end)
    if dist != -1:
        printMap(map)
    else:
        print("null")

main()