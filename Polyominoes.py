#Handles Manipulation of Polyominoes and the Grid in which they reside
import random

#rotate a polyomino 90 degrees
def rotate_poly(poly, rotations):
    newpoly = [i for i in poly]

    newpoly = [[i[0] - min([i[0] for i in newpoly]), i[1] - min([i[1] for i in newpoly])] for i in newpoly] #initialize

    boxsize = max(max([i[0] for i in newpoly]),max([i[1] for i in newpoly])) #create bounding box

    length_x = max([i[0] for i in newpoly]) - min([i[0] for i in newpoly])
    length_y = max([i[1] for i in newpoly]) - min([i[1] for i in newpoly]) #calculate lengths of polyomino

    x_shift = (boxsize - length_x) // 2
    y_shift = (boxsize - length_y) // 2 #shift amount to center polyomino

    newpoly = [[i[0] + x_shift, i[1] + y_shift] for i in newpoly] #center poly

    shift = boxsize / 2

    newpoly = [[i[0] - shift, i[1] - shift] for i in newpoly] #shift so rotation around center of box can be made


    for i in range(rotations):
        newpoly = [[i[1], -i[0]] for i in newpoly] #rotate

    newpoly = [[i[0] + shift, i[1] + shift] for i in newpoly] #undo shifting

    newpoly = [[int(round(i[0])), int(round(i[1]))] for i in newpoly] #integerize values


    return sorted(newpoly)

#generate the order of a polyomino, given a one-hot list of possible orders
def randomvalue(enabledpoly):
    value = random.randint(0, 11)
    while enabledpoly[value] != 1:
        value = random.randint(0, 11)

    return value

#exactly what it says on the tin
def shift_poly(brick, x, y):
    return [[i[0] + x, i[1] + y] for i in brick]

#adds garbage rows to a Grid
def addgarbage(grid, randomize):

    newgrid = [grid[i] for i in range(1,len(grid))]

    newgrid.append(grid[-1]) #clones bottom row

    if randomize: #randomizes garbage
        shuffler = grid[-1][:]
        random.shuffle(shuffler) #the truffle shuffle
        newgrid[-1] = shuffler[:]


    for i in range(len(grid[0])):
        if newgrid[-1][i] != 0:
            newgrid[-1][i] = 8

    print(newgrid)

    return newgrid

#takes a polyomino, and puts it on the Grid, shifted by the given coordinates
def imprint(brick, rowz, colz, grid, color):

    newgrid = grid[:]

    for i in brick:
        newgrid[rowz + i[1]][colz + i[0]] = color

    return newgrid

#takes a polyomino, and returns the shortest rotation
def flatten(brick,shiftz=False):
    candidates = [rotate_poly(brick, i) for i in range(4)]

    currentmin = 999

    for i in range(4):
        possiblemin = max([j[1] for j in candidates[i]])

        if possiblemin <= currentmin:
            currentmin = possiblemin
            choice = i

    if shiftz == False: return candidates[choice]
    if shiftz:
        minimum_x = min([i[0] for i in candidates[choice]])
        minimum_y = min([i[1] for i in candidates[choice]])
        return [[i[0] - minimum_x, i[1] - minimum_y] for i in candidates[choice]]

#calculates certain values of a polyomino
def vitals(poly):

    stats = []

    stats.append(max([i[0] for i in poly])) #max column
    stats.append(min([i[0] for i in poly])) #min column
    stats.append(stats[0] - stats[1] + 1) #length

    stats.append(max([i[1] for i in poly]))  # max row
    stats.append(min([i[1] for i in poly]))  # min row
    stats.append(stats[3] - stats[4] + 1)  # height

    return stats

#checks if a polyomino would collide with the given Grid after a shift
def checkifcollision(poly,grid,shiftx,shifty,gcol,grow):
    newpoly = shift_poly(poly,shiftx,shifty)

    height = len(grid)
    width = len(grid[0])

    for square in newpoly:
        if grow + square[1] >= height or gcol + square[0] >= width: return True

        if grow + square[1] < 0 or gcol + square[0] < 0: return True

        if grid[grow + square[1]][gcol + square[0]] != 0:
            return True
    return False







    return False

#takes a grid, and expands it to the new dimensions specified
def expandgrid(grid, newheight, newwidth):

    newgrid = grid[:]

    width = len(newgrid[0])

    while len(newgrid) < newheight:
        newgrid = [[0 for i in range(width)]] + newgrid

    for i in newgrid:
        while len(i) < newwidth:
            i.append(0)

    return newgrid


#workaround to the fact that negative list indices count backwards
def forcepositive(number):
    if number >= 0:
        return number
    else:
        return 99999999


#checks if a grid has a line to be cleared
def haslineclear(grid):
    for row in grid:
        if row.count(0) == 0:
            return True

    return False


#returns the proper color for a polyomino
def color(poly):


    if len(poly) == 1:
        return 7
    if len(poly) == 2:
        return 7
    if len(poly) == 3:
        if poly == [[0,0],[1,0],[2,0]]:
            return 7
        else:
            return 4

    if len(poly) == 4:
        if poly == [[0, 0], [1, 0], [2, 0], [3, 0]]: return 7 #I
        elif poly == [[0, 1], [0, 2], [1, 0], [1, 1]]: return 1 #Z
        elif poly == [[0, 0], [0, 1], [1, 0], [2, 0]]: return 4 #J
        elif poly == [[0, 1], [1, 0], [1, 1], [2, 0]]: return 3 #S
        elif poly == [[0, 0], [0, 1], [0, 2], [1, 0]]: return 2 #L
        elif poly == [[0, 0], [0, 1], [1, 0], [1, 1]]: return 5 #O
        elif poly == [[0, 0], [1, 0], [1, 1], [2, 0]]: return 6 #T

    if len(poly) == 5:
        if poly == [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0]]: return 5 #LP
        if poly == [[0, 0], [1, 0], [2, 0], [2, 1], [3, 0]]: return 7 #RY
        if poly == [[0, 0], [0, 1], [1, 1], [1, 2], [2, 1]]: return 2 #RF
        if poly == [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]]: return 6 #X
        if poly == [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1]]: return 5 #RP
        if poly == [[0, 0], [1, 0], [1, 1], [1, 2], [2, 0]]: return 6 #T
        if poly == [[0, 0], [1, 0], [1, 1], [2, 0], [3, 0]]: return 7 #LY
        if poly == [[0, 1], [1, 1], [1, 2], [2, 0], [2, 1]]: return 4 #LF
        if poly == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2]]: return 2 #U
        if poly == [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0]]: return 2 #RL
        if poly == [[0, 2], [1, 0], [1, 1], [1, 2], [2, 0]]: return 3 #LZ
        if poly == [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]]: return 4 #V
        if poly == [[0, 1], [0, 2], [0, 3], [1, 0], [1, 1]]: return 1 #RN
        if poly == [[0, 1], [0, 2], [1, 0], [1, 1], [2, 0]]: return 1 #W
        if poly == [[0, 1], [1, 1], [2, 0], [2, 1], [3, 0]]: return 3 #LN
        if poly == [[0, 0], [0, 1], [1, 0], [2, 0], [3, 0]]: return 4 #LL
        if poly == [[0, 1], [0, 2], [1, 1], [2, 0], [2, 1]]: return 1 #RZ
        if poly == [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]: return 7 #I

        '''


        ZZZ
          ZZ
        '''

    else:

        return random.randint(1,7) #TODO FiX

        '''
        .....
        .....
        .....
        .....
        .....

        '''

        # CYAN 0
        # RED 1
        # BLUE 2
        # GREEN 3
        # ORANGE 4
        # YELLOW 5
        # PURPLE 6























'''


X
XXX
  X
'''