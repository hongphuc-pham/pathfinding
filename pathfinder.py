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


# Breadth first search function
def bfs(map, start: Point, end: Point):

    # Declare the visited array
    visited = [[False for i in range(colSize)] for i in range(rowSize)]

    # Marked start point
    visited[start.x][start.y] = True

    # Create a queue
    q = deque()

    # Distance of start point(or cell) is 0
    q.append(start)  # Enqueue start point( or cell)

    while q:

        curr = q.popleft()  # Dequeue the front point

        if curr.x == end.x and curr.y == end.y:
            drawPath(curr)
            return 1

        # Otherwise enqueue its neighbour points
        for i in range(4):
            row = curr.x + rowNum[i]
            col = curr.y + colNum[i]

            # if neighbour point is valid, has path
            # and not visited yet, enqueue it.
            if (isValid(row, col, visited)):
                visited[row][col] = True
                childPoint = Point(row, col, 1)
                childPoint.addHead(curr)

                q.append(childPoint)

        # Return -1 if destination cannot be reached

    return -1


# Uniform cost search function
def ucs(map, start: Point, end: Point):
    # Declare the visited array
    visited = [[False for i in range(colSize)] for i in range(rowSize)]

    # Marked start point
    visited[start.x][start.y] = True

    # Create a queue
    q = deque()

    # Distance of start point is 0
    s = queueNode(start, 0)
    q.append(s)  # Enqueue start point

    while q:
        curr = q.popleft()

        # Get next point that have lowest accumulate cost distance
        while len(q) != 0:
            test = q.popleft()  # Dequeue the front  point
            if(test.dist < curr.dist):
                visited[curr.pt.x][curr.pt.y] = True
                curr = test
            else:
                visited[test.pt.x][test.pt.y] = True

        # If end point reached,
        # then draw path and end searching
        pt = curr.pt
        if pt.x == end.x and pt.y == end.y:
            drawPath(pt)
            return curr.dist

        # Otherwise enqueue its neighbour points
        for i in range(4):
            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]

            # if neighbour point is valid, has path
            # and not visited yet, enqueue it.
            if (isValid(row, col, visited)):
                visited[row][col] = True
                childPoint = Point(row, col, float(map[row][col]))
                childPoint.addHead(pt)
                Adjcell = queueNode(childPoint,
                                    curr.dist + calculateCost(curr.pt, childPoint))
                q.append(Adjcell)

        # Return -1 if the end point cannot be reached
    return -1.0


# A* search function
def aStart(map, start: Point, end: Point):

    # Declare the visited array
    visited = [[False for i in range(colSize)] for i in range(rowSize)]

    # Marked start point
    visited[start.x][start.y] = True

    # Create a queue
    q = deque()

    # Distance of start point is 0
    s = queueNode(start, 0)
    q.append(s)  # Enqueue source start point

    while q:
        curr = q.popleft()

        # Get next point that have lowest accumulate cost distance
        while len(q) != 0:
            test = q.popleft()  # Dequeue the front point

            if (test.dist < curr.dist):
                visited[curr.pt.x][curr.pt.y] = True
                curr = test
            else:
                visited[test.pt.x][test.pt.y] = True

        # If end point reached,
        # then draw path and end searching
        pt = curr.pt
        if pt.x == end.x and pt.y == end.y:

            drawPath(pt)
            return curr.dist

        # Otherwise enqueue its neighbour points
        for i in range(4):

            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]

            # if neighbour point is valid, has path
            # and not visited yet, enqueue it.
            if (isValid(row, col, visited)):
                visited[row][col] = True
                childPoint = Point(row, col, float(map[row][col]))
                childPoint.addHead(pt)
                childPoint.addHeuristic(end, heuristic)
                childPoint.heuristic
                Adjcell = queueNode(childPoint,
                                    curr.dist + calculateCost(curr.pt, childPoint) + childPoint.heuristic )
                q.append(Adjcell)

        # Return -1 if end point cannot be reached
    return -1.0


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