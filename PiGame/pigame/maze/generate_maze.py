import random

__all__ = ["generate_maze"]

def validate(pos, maze):
    x = pos[0]
    y = pos[1]
    mx = maze[0]
    my = maze[1]

    return (x >= 0 and x < mx) and (y >= 0 and y < my)

# def generate_maze(length, breadth, start_pos):
#     """Generates a maze as a 2D list
#     0 represents a wall in the maze while 1 represents an empty space
    
#     length - horizontal length of maze
#     breadth - vertical length of maze
#     start_pos - tuple of the starting position, (length, breadth)

#     Example usage:
#     # Create a 32 by 32 grid starting with the starting position at (0, 0)
#     generate_maze(32, 32, (0, 0))
#     """

#     # Fill maze with zeros
#     maze = [[0 for x in range(length)] for y in range(breadth)]
#     # Previously visited positions
#     stack = [start_pos]

#     # Directions
#     dx = [0, 1, 0, -1]
#     dy = [-1, 0, 1, 0]

#     while stack:
#         (current_x, current_y) = stack[-1]
#         maze[current_y][current_x] = 1

#         neighbours = []
#         for i in range(4):
#             neighbour_x = current_x + dx[i]
#             neighbour_y = current_y + dy[i]

#             # Ensure that the neighbour's position is valid
#             if validate((neighbour_x, neighbour_y), (length, breadth)):
#                 if maze[neighbour_y][neighbour_x] == 0:
#                     ctr = 0
#                     for j in range(4):
#                         ex = neighbour_x + dx[j]
#                         ey = neighbour_y + dy[j]

#                         if (validate((ex, ey), (length, breadth)) and
#                                 maze[ey][ex] == 1):
#                             ctr += 1

#                     if ctr == 1:
#                         neighbours.append(i)

#         if neighbours:
#             ir = neighbours[random.randint(0, len(neighbours) - 1)]
#             current_x += dx[ir]
#             current_y += dy[ir]
            
#             stack.append((current_x, current_y))
#         else:
#             stack.pop()

#     return maze

def generate_maze(mx, my, pos):
    maze = [[0 for x in range(mx)] for y in range(my)]
    dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze

    # start the maze from a random cell
    cx, cy = pos
    maze[cy][cx] = 1; stack = [(cx, cy, 0)] # stack element: (x, y, direction)

    while len(stack) > 0:
        (cx, cy, cd) = stack[-1]
        # to prevent zigzags:
        # if changed direction in the last move then cannot change again
        if len(stack) > 2:
            if cd != stack[-2][2]: dirRange = [cd]
            else: dirRange = range(4)
        else: dirRange = range(4)

        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in dirRange:
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 0:
                    ctr = 0 # of occupied neighbors must be 1
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey][ex] == 1: ctr += 1
                    if ctr == 1: nlst.append(i)

        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]; maze[cy][cx] = 1
            stack.append((cx, cy, ir))
        else: stack.pop()

    return maze