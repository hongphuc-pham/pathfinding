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
heuristic = argv[3] if(len(argv) == 4) else " "


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

    if ( map[row][col].lower() == 'x'):
        return False

    # Otherwise
    return True


class Point:
    heuristic = 0.0
    g = 0.0
    head = None
    fValue = 0.0
    def __init__(self, x: float, y: float, val: float):
        self.x = x
        self.y = y
        self.val = val

    def __lt__(self, other):
        return self.fValue < other.fValue

    def __eq__(self, other):
        if (isinstance(other, Point)):
            return (self.x, self.y) == (other.x, other.y)
        return False

    def addHead(self, pt):
        assert isinstance(pt, Point)
        self.head = pt

    def addHeuristic(self, target, hType: str):
        assert isinstance(target, Point)
        if hType.lower() == 'euclidean':
            self.heuristic = mt.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
        elif hType.lower() == 'manhattan':
            self.heuristic = abs(self.x - target.x) + abs(self.y - target.y)

    def addG(self, g: float):
        self.g = g

    def updatePoint(self, parent, gcost):
        self.head = parent
        self.g = gcost

    def updateFValue(self, fVal: float):
        self.fValue = fVal


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
            if(j == colSize -1):
                print(map[i][j])
            else:
                print(map[i][j], end = ' ')



#Calculate cost
def calculateCost(curr: Point, next: Point):

    if(curr.val < next.val):
        return 1.0 + next.val - curr.val

    return 1.0


# These arrays are used to get next cells in 4 direction Up, Down, Left Right
rowNum = [-1, 1, 0, 0]
colNum = [0, 0, -1, 1]

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
    q = []

    # Distance of start point(or cell) is 0
    q.append(start)  # Enqueue start point( or cell)

    while q:

        curr = q.pop(0)  # Dequeue the front point

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

    # Create a queue
    q = []
    openQueue = []
    # Distance of start point is 0
    q.append(start)  # Enqueue start point

    while q:

        curr = q.pop(0)

        # Get next point that have lowest accumulate cost distance
        while len(q) != 0:
            test = q.pop(0)  # Dequeue the front  point
            if(test.g < curr.g):
                openQueue.append(curr)
                curr = test
            else:
                openQueue.append(test)


        # If end point reached,
        # then draw path and end searching

        if curr.x == end.x and curr.y == end.y:
            drawPath(curr)
            return curr.fValue
        else:
            visited[curr.x][curr.y] = True

            # Otherwise enqueue its neighbour points
            for i in range(4):
                row = curr.x + rowNum[i]
                col = curr.y + colNum[i]

                # if neighbour point is valid, has path
                # and not visited yet, enqueue it.
                if (isValid(row, col, visited)):
                    visited[row][col] = True
                    childPoint = Point(row, col, float(map[row][col]))
                    childPoint.addG(calculateCost(curr, childPoint) + curr.g)
                    childPoint.addHead(curr)

                    q.append(childPoint)

        if(len(q) == 0 and len(openQueue) != 0):
            for i in range(0, len(openQueue)):
                q.append(openQueue.pop())


        # Return -1 if the end point cannot be reached
    return -1.0

# A* search function
def aStart(map, start: Point, end: Point):

    # Declare the visited array
    visited = [[False for i in range(colSize)] for i in range(rowSize)]
    # Create a queue
    q = []
    # Distance of start point is 0
    q.append(start)  # Enqueue source start point


    while q:
        q.sort()
        curr = q.pop(0)

        # If end point reached,
        # then draw path and end searching

        if curr.x == end.x and curr.y == end.y:
            drawPath(curr)
            return curr.fValue

        else:

            visited[curr.x][curr.y] = True
            # Otherwise enqueue its neighbour points
            for i in range(4):

                row = curr.x + rowNum[i]
                col = curr.y + colNum[i]


                # if neighbour point is valid, has path
                # and not visited yet, enqueue it.
                if (isValid(row, col, visited) and not isinstance(curr.g, Point)):

                    childPoint = Point(row, col, float(map[row][col]))
                    childPoint.addHead(curr)

                    childPoint.addG(calculateCost(curr, childPoint) + curr.g)
                    childPoint.addHeuristic(end, heuristic)
                    childPoint.updateFValue(childPoint.g + childPoint.heuristic)


                    for p in q:
                        if( isinstance(p.g, Point)):
                            continue
                        if (childPoint == p and childPoint.g < p.g):
                            p.updatePoint(childPoint.g, childPoint.head)

                    q.append(childPoint)



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
        start.addHeuristic(end,heuristic)
        fValue = aStart(map, start, end)


    if fValue != -1.0:
        printMap(map)
    else:
        print("null")

main()