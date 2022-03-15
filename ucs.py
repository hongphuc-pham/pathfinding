def ucs(map, start: Point, end: Point):
    # Declare the visited array
    visited = [[False for i in range(colSize)] for i in range(rowSize)]

    visited[start.x][start.y] = True

    # Create a queue for BFS
    q = deque()

    # Distance of source cell is 0
    s = queueNode(start, 0)
    q.append(s)  # Enqueue source cell

    while q:
        curr = q.popleft()

        while len(q) != 0:
            test = q.popleft()  # Dequeue the front cell
            if(test.dist < curr.dist):
                curr = test

        # If we have reached the destination cell,
        # we are done
        pt = curr.pt
        if pt.x == end.x and pt.y == end.y:
            drawPath(pt)
            return curr.dist

        # Otherwise enqueue its adjacent cells
        for i in range(4):
            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]

            # if adjacent cell is valid, has path
            # and not visited yet, enqueue it.
            if (isValid(row, col, visited) and
                    map[row][col] != 'X'):
                visited[row][col] = True
                childPoint = Point(row, col, 1)
                childPoint.addHead(pt)
                Adjcell = queueNode(childPoint,
                                    curr.dist + int(map[row][col]))
                q.append(Adjcell)

        # Return -1 if destination cannot be reached
    return -1
