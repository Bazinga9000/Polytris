import json, random, pygame, operator, pathlib

'''
                    statsstring = "Last Game's Stats"
                    resultstring = "Score: " + intWithCommas(score)
                    resultstring2 = "Level: " + str(level) + " (Started at " + str(startinglevel) + ")"
                    resultstring3 = "Polyominoes: "
                    for i in range(12):
                        if enabledpoly[i] == 1:
                            resultstring3 = resultstring3 + str(i + 1) + ","
                    resultstring3 = resultstring3[:-1]

                    if gamemode == 1:
                        resultstring3 = resultstring3 + " [SURVIVAL MODE]"
                    gamemode = 0
                    score = 0
                    level = 0
'''

if True:  # compression
    polylist = []

    for i in range(1, 13):
        if pathlib.Path(str("Poly Order " + str(i) + ".txt")).is_file():
            with open(str("Poly Order " + str(i) + ".txt"), "r") as savefile:
                polylist.append(json.loads(savefile.read()))
        else:
            polylist.append("FOUR OH FOUR")

    pygame.init()
    screen = pygame.display.set_mode((1000, 760))

    gamemode = 0
    polynum = 4
    polysettings = 0

    font = pygame.font.SysFont("Trebuchet MS", 25)
    bigfont = pygame.font.SysFont("Trebuchet MS", 45)
    smallfont = pygame.font.SysFont("Trebuchet MS", 18)
    enabledpoly = [0 for i in range(12)]
    enabledpoly[3] = 1
    boardsize = 0
    speedmult = 0
    gametimer = 0
    currentpoly = []
    score = 0
    softdrop = False
    lockdelay = -1
    level = 0
    score = 0
    gravity = 120
    harddrop = False
    statsstring = ""
    resultstring = ""
    resultstring2 = ""
    resultstring3 = ""
    version = "1.7.0"
    ghostpoly = []
    startinglevel = 0
    nextpoly = [[] for i in range(5)]
    heldpoly = []
    rotations = 0
    automove = [0, 0]
    lines = 0
    rot = 0
    autotime = 0
    gametype = 0
    difficulty = 0
    minpolyvalue = [1,0,0,0,"X","X","X","X","X",0,0]
    maxpolyvalue = [12,2,12,12,"X","X","X","X","X",1,5]
    expandatlist = [75,60,55,50,40,30]
    garbagelist = ["X",15000,12000,10000,10000,8000]
    survcolors = [(0,75,8),(26,92,2),(72,109,5),(126,122,8),(143,90,13),(160,48,19)]
    leveljump = [0,20,40,60,80,100]
    clock = pygame.time.Clock()



    # 0 - 1/12
    # 1 - 0/2
    # 2 - 0/12
    # 3 - 0/12
    # 4 - 0/2

grid = []


def randombrick(order):
    newbrick = [[0, 0]]

    if order > 11:
        while len(newbrick) != order:
            possiblesq = newbrick[random.randint(0, len(newbrick) - 1)]
            direction = random.randint(1, 4)

            if direction == 1:
                if [possiblesq[0] + 1, possiblesq[1]] not in newbrick:
                    newbrick.append([possiblesq[0] + 1, possiblesq[1]])

            elif direction == 2:
                if [possiblesq[0], possiblesq[1] + 1] not in newbrick:
                    newbrick.append([possiblesq[0], possiblesq[1] + 1])

            elif direction == 3:
                if [possiblesq[0], possiblesq[1] - 1] not in newbrick:
                    newbrick.append([possiblesq[0], possiblesq[1] - 1])

            elif direction == 4:
                if [possiblesq[0] - 1, possiblesq[1]] not in newbrick:
                    newbrick.append([possiblesq[0] - 1, possiblesq[1]])

        minimum_x = min([i[0] for i in newbrick])
        minimum_y = min([i[1] for i in newbrick])

        newbrick = [(i[0] - minimum_x, i[1] - minimum_y) for i in newbrick]

        return sorted(newbrick)

    else:
        if polylist[order] == "FOUR OH FOUR":
            while len(newbrick) != order + 1:
                possiblesq = newbrick[random.randint(0, len(newbrick) - 1)]
                direction = random.randint(1, 4)

                if direction == 1:
                    if [possiblesq[0] + 1, possiblesq[1]] not in newbrick:
                        newbrick.append([possiblesq[0] + 1, possiblesq[1]])

                elif direction == 2:
                    if [possiblesq[0], possiblesq[1] + 1] not in newbrick:
                        newbrick.append([possiblesq[0], possiblesq[1] + 1])

                elif direction == 3:
                    if [possiblesq[0], possiblesq[1] - 1] not in newbrick:
                        newbrick.append([possiblesq[0], possiblesq[1] - 1])

                elif direction == 4:
                    if [possiblesq[0] - 1, possiblesq[1]] not in newbrick:
                        newbrick.append([possiblesq[0] - 1, possiblesq[1]])

            minimum_x = min([i[0] for i in newbrick])
            minimum_y = min([i[1] for i in newbrick])

            newbrick = [(i[0] - minimum_x, i[1] - minimum_y) for i in newbrick]

            return sorted(newbrick)

        return polylist[order][random.randint(0, len(polylist[order]) - 1)]


def div_round_up(a, b):
    return (a + (-a % b)) // b


def rotate_poly(brick, numrots):
    newbrick = [i for i in brick]

    newbrick = [[i[0] - min([i[0] for i in newbrick]), i[1] - min([i[1] for i in newbrick])] for i in newbrick]

    boxsize = max(max([i[0] for i in newbrick]),max([i[1] for i in newbrick]))

    length_x = max([i[0] for i in newbrick]) - min([i[0] for i in newbrick])
    length_y = max([i[1] for i in newbrick]) - min([i[1] for i in newbrick])

    x_shift = (boxsize - length_x) // 2
    y_shift = (boxsize - length_y) // 2

    newbrick = [[i[0] + x_shift, i[1] + y_shift] for i in newbrick]

    shift = boxsize / 2

    newbrick = [[i[0] - shift, i[1] - shift] for i in newbrick]


    for i in range(numrots):
        newbrick = [[i[1], -i[0]] for i in newbrick]

    newbrick = [[i[0] + shift, i[1] + shift] for i in newbrick]

    newbrick = [[int(round(i[0])), int(round(i[1]))] for i in newbrick]

    #newbrick = [[i[0] - min([i[0] for i in newbrick]), i[1] - min([i[1] for i in newbrick])] for i in newbrick]


    return sorted(newbrick)


def imprint(brick, rowz, colz):
    global grid

    for i in brick:
        grid[rowz + i[1]][colz + i[0]] = 1


def lineclearpoints(clears, level):
    if clears == 0: return 0

    if clears == 1:
        return 40 * (level + 1)

    elif clears == 2:
        return 100 * (level + 1)

    elif clears == 3:
        return 300 * (level + 1)

    elif clears == 4:
        return 1200 * (level + 1)

    elif clears == 5:
        return 3500 * (level + 1)

    elif clears == 6:
        return 6000 * (level + 1)

    elif clears == 7:
        return 9200 * (level + 1)

    elif clears == 8:
        return 13700 * (level + 1)

    elif clears == 9:
        return 23000 * (level + 1)

    elif clears == 10:
        return 50000 * (level + 1)

    elif clears == 11:
        return 100000 * (level + 1)

    elif clears == 12:
        return 200000 * (level + 1)


def checkifcollision(brick, rowz, colz, dir=0):
    global grid

    if dir == 0:
        for square in brick:
            if rowz + 1 + square[1] == height:
                return True
            elif grid[rowz + square[1] + 1][colz + square[0]] == 1:
                return True
        return False

    elif dir == 1:
        for square in brick:
            if colz + square[0] + 1 == width:
                return True

            elif grid[rowz + square[1]][colz + square[0] + 1] == 1:
                return True

        return False

    elif dir == -1:
        for square in brick:
            if (colz + square[0]) - 1 <= -1:
                return True
            elif grid[rowz + square[1]][colz + square[0] - 1] == 1:
                return True
        return False

    elif dir == 2:
        for square in brick:
            if rowz + square[1] >= height or colz + square[0] >= width: return True

            if grid[rowz + square[1]][colz + square[0]] == 1:
                return True
        return False


def intWithCommas(x):
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


def expandgrid(newheight, newwidth):
    global grid, height, width

    while len(grid) < newheight:
        grid = [[0 for i in range(width)]] + grid

    for i in grid:
        while len(i) < newwidth:
            i.append(0)

    height = len(grid)
    width = len(grid[0])


def flatten(brick):
    candidates = [rotate_poly(brick, i) for i in range(4)]

    currentmin = 999

    for i in range(4):
        possiblemin = max([j[1] for j in candidates[i]])

        if possiblemin <= currentmin:
            currentmin = possiblemin
            choice = i

    return candidates[choice]


def randomvalue():
    value = random.randint(0, 11)
    while enabledpoly[value] != 1:
        value = random.randint(0, 11)

    return value


def shift_poly(brick, x, y):
    return [[i[0] + x, i[1] + y] for i in brick]


def mstog(gravity):
    if gravity == "0":
        return "∞"
    else:
        return round(120 / gravity, 2)


def addgarbage(difficulty):
    global grid

    grid = [grid[i] for i in range(1,len(grid))]

    grid.append(grid[-1])

    if difficulty >= 3:
        shuffler = grid[-1][:]
        random.shuffle(shuffler) #the truffle shuffle
        grid[-1] = shuffler[:]


def draw(gamemode):
    global color

    screen.fill((0, 0, 0))

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    if gamemode == 0:

        ver = smallfont.render("Ver. " + version, True, (0, 0, 204))
        screen.blit(ver, (30, 30))

        title = bigfont.render("Polytris", True, (0, 0, 204))
        screen.blit(title, (415, 100))

        title = smallfont.render("Enabled Polyominoes", True, (0, 0, 204))
        screen.blit(title, (105, 200))

        title = smallfont.render("Board Size", True, (0, 0, 204))
        screen.blit(title, (105, 250))

        title = smallfont.render("Speed Multiplier", True, (0, 0, 204))
        screen.blit(title, (105, 300))

        title = smallfont.render("Starting Level", True, (0, 0, 204))
        screen.blit(title, (105, 350))

        title = smallfont.render("Gametype", True, (0, 0, 204))
        screen.blit(title, (105, 500))

        if gametype == 1:
            title = smallfont.render("Difficulty",True,(0,0,204))
            screen.blit(title,(105,550))

        title = font.render("Press Enter to Begin", True, (0, 0, 204))
        screen.blit(title, ((screen_width - title.get_width()) // 2, 600))

        title = smallfont.render(statsstring, True, (204, 204, 0))
        screen.blit(title, (300, 10))

        title = smallfont.render(resultstring, True, (204, 204, 0))
        screen.blit(title, (300, 30))

        title = smallfont.render(resultstring2, True, (204, 204, 0))
        screen.blit(title, (300, 50))

        title = smallfont.render(resultstring3, True, (204, 204, 0))
        screen.blit(title, (300, 70))


        #enabled poly
        cord = 330
        for i in range(12):
            if enabledpoly[i] == 1:
                numbertxt = smallfont.render(str(i + 1), True, (0, 204, 0))
            else:
                numbertxt = smallfont.render(str(i + 1), True, (204, 0, 0))

            if polynum == i + 1 and polysettings == 0:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (cord, 225))

            screen.blit(numbertxt, (cord, 200))

            cord = cord + 30 + numbertxt.get_width()

        #boardsizes
        for i in range(3):
            sizes = [[(maxpoly + 2) * 2, (maxpoly + 1) * 5 + 2], [(maxpoly + 2) * 3, (maxpoly + 1) * 6 + 2],
                     [(maxpoly + 2) * 4, (maxpoly + 1) * 7 + 2]]

            if i != boardsize:
                sizetxt = smallfont.render(str(sizes[i][0]) + "x" + str(sizes[i][1]), True, (204, 0, 0))
            else:
                sizetxt = smallfont.render(str(sizes[i][0]) + "x" + str(sizes[i][1]), True, (0, 204, 0))

            if polysettings == 1 and i == polynum:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (330 + 90 * i, 275))

            screen.blit(sizetxt, (330 + 80 * i, 250))


        #speed multiplier
        cord = 330
        for i in range(13):
            multiplier = 1 + (i / 4)
            if speedmult == i:
                multtxt = smallfont.render(str(multiplier) + str("x"), True, (0, 204, 0))
            else:
                multtxt = smallfont.render(str(multiplier) + str("x"), True, (204, 0, 0))

            if polynum == i and polysettings == 2:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (cord, 325))

            screen.blit(multtxt, (cord, 300))

            cord = cord + 10 + multtxt.get_width()

        #starting level
        cord = 330
        for i in range(13):
            startlvl = 50 * i
            if startinglevel == startlvl:
                lvltxt = smallfont.render(str(startlvl), True, (0, 204, 0))
            else:
                lvltxt = smallfont.render(str(startlvl), True, (204, 0, 0))

            if polynum == i and polysettings == 3:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (cord, 375))

            screen.blit(lvltxt, (cord, 350))

            cord = cord + 15 + lvltxt.get_width()

        #gametype
        types = ["Simple","Survival","Doubles (NYI)"]
        colors = [(204,0,0) for i in types]
        colors[gametype] = (0,204,0)

        cord = 330

        for n,name in enumerate(types):
            typetxt = smallfont.render(name,True,colors[n])
            screen.blit(typetxt,(cord,500))

            if polysettings == 9 and polynum == n:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (cord, 525))

            cord = cord + 30 + typetxt.get_width()

        if gametype == 1:
            difflevels = ["Easy","Normal","Hard","Insane","Ludicrous","Devil"]
            colors = [(204,0,0) for i in difflevels]
            colors[difficulty] = (0,204,0)

            cord = 330

            for n,name in enumerate(difflevels):
                difftxt = smallfont.render(name,True,colors[n])
                screen.blit(difftxt, (cord, 550))

                cord = cord + 30 + difftxt.get_width()

                if polysettings == 10 and polynum - 1 == n:
                    arrow = font.render("^", True, (204, 204, 204))
                    screen.blit(arrow, (cord, 575))

            if polysettings == 10 and polynum == 0:  # For some reason, the above loop doesn't draw this case ¯\_(ツ)_/¯
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (330, 575))

                cord = cord + 15 + difftxt.get_width()

    if gamemode == 1 or gamemode == -1 or gamemode == 99:


        #timer = smallfont.render(str(gametimer % garbagelist[difficulty]),True,(0,204,0))
        #screen.blit(timer,(30,30))


        squaresize = min((screen_width // 2) // width, (screen_height - 60) // height)

        horizshift = (screen_width - (width * squaresize)) / 2
        vertshift = (screen_height - (height * squaresize)) + 30

        scoretxt = smallfont.render("Score: " + intWithCommas(score), True, (0, 204, 0))
        screen.blit(scoretxt, (30, 100))

        leveltxt = smallfont.render("Level: " + str(level), True, (0, 204, 0))
        screen.blit(leveltxt, (30, 130))

        gravitytxt = smallfont.render("Gravity: " + str(mstog(gravity)) + "G", True, (0, 204, 0))
        screen.blit(gravitytxt, (30, 160))

        locktxt = smallfont.render("Lock Delay: " + str(lockspeed) + " Ticks", True, (0, 204, 0))
        screen.blit(locktxt, (30, 190))

        linestxt = smallfont.render("Lines Cleared: " + str(lines), True, (0, 204, 0))
        screen.blit(linestxt, (30, 220))

        if gametype == 0:
            word = "Mode: Simple"
        elif gametype == 1:
            word = "Mode: Survival [" + ["Easy","Normal","Hard","Insane","Ludicrous","Devil"][difficulty] + "]"
        elif gametype == 2:
            word = "Mode: Doubles"

        modetxt = smallfont.render(word,True,(0,204,0))
        screen.blit(modetxt,(30,280))

        rect = (horizshift - 50, 0, 100 + (width * squaresize), 9999)

        pygame.draw.rect(screen, rectcolor, rect)

        rect = (horizshift, 60, squaresize * (width), squaresize * (height))
        pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        if gamemode == 99:
            color = (70, 70, 70)
        else:
            color = (50, 0, 0)

        for row in range(height):
            for col in range(width):
                rect = (horizshift + col * squaresize, 60 + squaresize * row, squaresize, squaresize)
                if grid[row][col] == 1:
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        if gamemode != 99:
            for brick in ghostpoly:
                rect = (horizshift + (colz + brick[0]) * squaresize, 60 + squaresize * (rowzg + brick[1]), squaresize,
                        squaresize)
                pygame.draw.rect(screen, (128, 128, 128), rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        for brick in currentpoly:
            rect = (
            horizshift + (colz + brick[0]) * squaresize, 60 + squaresize * (rowz + brick[1]), squaresize, squaresize)
            pygame.draw.rect(screen, (0, 0, 50), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        if gamemode != 99:

            x_cord = horizshift + 75 + (width * squaresize)
            squaresize = 18
            y_cord = 125 + squaresize
            if maxpoly >= 9: squaresize = 9

            nexttxt = smallfont.render("Next", True, (0, 204, 0))
            screen.blit(nexttxt, (x_cord, 100))

            for poly in nextpoly:
                maxes = (max([i[0] for i in poly]), max([i[1] for i in poly]))  # col,row

                for brick in poly:
                    rect = (x_cord + (brick[0] * squaresize), y_cord + squaresize * brick[1], squaresize, squaresize)
                    pygame.draw.rect(screen, (50, 50, 0), rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)

                y_cord += squaresize * (maxes[1] + 2)

            holdtxt = smallfont.render("Hold", True, (0, 204, 0))
            screen.blit(holdtxt, (x_cord, y_cord))

            y_cord += squaresize
            y_cord += 25

            for brick in heldpoly:
                rect = (x_cord + (brick[0] * squaresize), y_cord + squaresize * brick[1], squaresize, squaresize)
                pygame.draw.rect(screen, (50, 0, 50), rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        if gamemode == 99:
            x_cord = horizshift + 65 + (width * squaresize)
            gameovertxt = smallfont.render("Game Over!", True, (0, 0, 0))
            screen.blit(gameovertxt, ((screen_width - gameovertxt.get_width()) // 2, 15))

            endtxt = smallfont.render("Press SPACE to Return to Menu", True, (0, 0, 0))
            screen.blit(endtxt, ((screen_width - endtxt.get_width()) // 2, 30))

        rect = (3)




while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        exit()

    if event.type == pygame.KEYUP:

        key = event.key

        if gamemode == 1 or gamemode == -1:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                softdrop = False

        if key == pygame.K_LEFT or key == pygame.K_a:
            automove[0] = 0

        if key == pygame.K_RIGHT or key == pygame.K_d:
            automove[1] = 0

    if event.type == pygame.MOUSEBUTTONDOWN:
        pressed = pygame.mouse.get_pressed()
        if gamemode == 1 or gamemode == -1:

            if pressed[0] == 1 and currentpoly:
                rot = 3

            if pressed[2] == 1 and currentpoly:
                rot = 1

    if event.type == pygame.KEYDOWN:

        key = event.key

        if key == pygame.K_ESCAPE:
            gamemode = 0

        if gamemode == 0:

            if key == pygame.K_LEFT and polynum != minpolyvalue[polysettings]:
                polynum -= 1

            if key == pygame.K_RIGHT and polynum != maxpolyvalue[polysettings]:
                polynum += 1

            if key == pygame.K_UP and polysettings != 0:
                if polysettings == 9:
                    polysettings = 3
                else:
                    polysettings -= 1


                if polysettings == 0: polynum = polynum + 1
                if polysettings == 1: polynum = (polynum - 1) % 3
                if polysettings == 9: polynum = 0

            if key == pygame.K_DOWN and (polysettings != 9 or (gametype == 1 and polysettings != 10)):
                if polysettings == 3:
                    polysettings = 9
                else:
                    polysettings += 1

                if polysettings == 1: polynum = (polynum - 1) % 3
                if polysettings == 2: polynum = polynum + 1
                if polysettings == 9: polynum = 1


            if key == pygame.K_SPACE:
                if polysettings == 0 and (enabledpoly[polynum - 1] == 0 or enabledpoly.count(1) != 1):
                    enabledpoly[polynum - 1] = (enabledpoly[polynum - 1] + 1) % 2
                if polysettings == 1 and (boardsize != polynum):
                    boardsize = polynum
                if polysettings == 2 and (speedmult != polynum):
                    speedmult = polynum
                if polysettings == 3 and (startinglevel / 50 != polynum):
                    startinglevel = 50 * polynum
                if polysettings == 9 and gametype != polynum:
                    gametype = polynum
                if polysettings == 10 and difficulty != polynum:
                    difficulty = polynum

            if key == pygame.K_RETURN:
                if gametype == 1:
                    gamemode = 1
                    enabledpoly = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    maxpoly = 3
                    boardsize = 0
                    speedmult = 0
                    expandat = expandatlist[difficulty]
                else:
                    gamemode = -1
                    level = startinglevel
                    difficulty = 0
                grid = [[0 for i in range((maxpoly + 2) * (2 + boardsize))] for j in
                        range((maxpoly + 1) * (5 + boardsize) + 2)]
                height = len(grid)
                width = len(grid[0])
                currentpoly = []

        elif gamemode == 1 or gamemode == -1:
            if key == pygame.K_g:  # REMOVE THIS IN RELEASE VERSION TODO
                value = random.randint(0, 11)
                while enabledpoly[value] != 1:
                    value = random.randint(0, 11)
                currentpoly = randombrick(value)

                candidates = [rotate_poly(currentpoly, i) for i in range(4)]

                currentmin = 999

                for i in range(4):
                    possiblemin = max([j[1] for j in candidates[i]])

                    if possiblemin <= currentmin:
                        currentmin = possiblemin
                        choice = i

                currentpoly = candidates[choice]

                max_col = max([i[0] for i in currentpoly])
                max_row = max([i[1] for i in currentpoly])

                rowz = 1
                colz = (width - max_col) // 2

            if key == pygame.K_r:
                grid = [[0 for i in range(width)] for j in range(height)]
                currentpoly = []

            if key == pygame.K_LEFT or key == pygame.K_a:
                if not checkifcollision(currentpoly, rowz, colz, -1):
                    colz -= 1
                    automove[0] = 1
                    autotime = gametimer

            if key == pygame.K_RIGHT or key == pygame.K_d:
                if not checkifcollision(currentpoly, rowz, colz, 1):
                    colz += 1
                    automove[1] = 1
                    autotime = gametimer

            if key == pygame.K_DOWN or key == pygame.K_s:
                softdrop = True

            if key == pygame.K_UP or key == pygame.K_w and currentpoly != []:
                rot = 1

            if key == pygame.K_z and currentpoly != []:
                rot = 3

            if key == pygame.K_h:

                polyswap = [currentpoly[:], heldpoly[:]]

                heldpoly = polyswap[0][:]

                currentpoly = polyswap[1][:]

                if currentpoly == []:
                    currentpoly = nextpoly[0][:]
                    nextpoly[0] = nextpoly[1][:]
                    nextpoly[1] = nextpoly[2][:]
                    nextpoly[2] = nextpoly[3][:]
                    nextpoly[3] = nextpoly[4][:]

                    for i in range(6):
                        nextpoly[4] = flatten(randombrick(randomvalue()))

                        if nextpoly[4] not in [nextpoly[i] for i in [0,1,2]]:
                            break

                    currentpoly = flatten(currentpoly)

                max_col = max([i[0] for i in currentpoly])
                max_row = max([i[1] for i in currentpoly])

                rowz = 1
                rowzg = 1
                colz = (width - max_col) // 2

                candidates = [rotate_poly(currentpoly, i) for i in range(3)]

                if checkifcollision(currentpoly, rowz, colz, 2):
                    for candidate in candidates:
                        max_col = max([i[0] for i in candidate])
                        max_row = max([i[1] for i in candidate])

                        rowz = 1
                        colz = (width - max_col) // 2

                        if not checkifcollision(candidate, rowz, colz, 2):
                            currentpoly = candidate[:]

                    if checkifcollision(currentpoly, rowz, colz, 2): gamemode = 99

                ghostpoly = currentpoly[:]

            if key == pygame.K_SPACE:
                while not checkifcollision(currentpoly, rowz, colz, 2):
                    rowz += 1
                rowz -= 1
                lockspeed = 0
                harddrop = True

            if key == pygame.K_l:
                level += 1

            if key == pygame.K_p:
                level += 10

            if key == pygame.K_o:
                level += 100

        elif gamemode == 99:
            if key == pygame.K_SPACE:
                enabledpoly = [0 for i in range(12)]
                enabledpoly[3] = 1
                boardsize = 0
                speedmult = 0
                gametimer = 0
                currentpoly = []
                score = 0
                softdrop = False
                lockdelay = -1
                level = 0
                score = 0
                gravity = 120
                harddrop = False
                ghostpoly = []
                startinglevel = 0
                nextpoly = [[] for i in range(5)]
                heldpoly = []
                gamemode = 0
                lines = 0


    #survival mode exclusive things
    if gamemode == 1:
        stage = level // expandat + 3

        enabledpoly = [0 for i in range(12)]

        for i in range(12):
            if stage >= i:
                enabledpoly[i] = 1

        maxpoly = 0
        for i in range(12):
            if enabledpoly[i] == 1:
                maxpoly = i

        if ((maxpoly + 1) * 5 + 2) > height:
            expandgrid(((maxpoly + 1) * 5 + 2), ((maxpoly + 2) * 2))


        if difficulty != 0 and level > 200:
            if gametimer % garbagelist[difficulty] == 0:
                if grid[0] != [0 for i in grid[0]]:
                    gamemode = 99
                else:
                    addgarbage(difficulty)


    maxpoly = 0
    for i in range(12):
        if enabledpoly[i] == 1:
            maxpoly = i

    if gamemode == 1 or gamemode == -1:
        gametimer += 1

        if gamemode == 1: countedlevel = level + leveljump[difficulty]
        if gamemode == -1: countedlevel = level

        if countedlevel <= 609: gravity = int((120 * 1 / ((259 / 256) ** countedlevel)) * 1 / (1 + (speedmult / 4)))
        if gravity == 0: gravity = 1
        if countedlevel > 609: gravity = "0"

        if countedlevel <= 609: lockspeed = int(120 * 40 / 60)
        if countedlevel > 609: lockspeed = int(120 * (40 / (1 + 3 / 256 * (countedlevel - 609))) / 60)

        if rotations >= 20:
            while not checkifcollision(currentpoly, rowz, colz, 2):
                rowz += 1
            rowz -= 1
            lockspeed = 0
            harddrop = True
            rotations = 0

        if harddrop == True: lockspeed = 0

        nextpoly = [flatten(randombrick(randomvalue())) if i == [] else i for i in nextpoly]

        if currentpoly == []:
            rotations = 0

            currentpoly = nextpoly[0][:]
            nextpoly[0] = nextpoly[1][:]
            nextpoly[1] = nextpoly[2][:]
            nextpoly[2] = nextpoly[3][:]
            nextpoly[3] = nextpoly[4][:]

            for i in range(6):
                nextpoly[4] = flatten(randombrick(randomvalue()))

                if nextpoly[4] not in [nextpoly[i] for i in [0, 1, 2]]:
                    break

            currentpoly = flatten(currentpoly)

            max_col = max([i[0] for i in currentpoly])
            max_row = max([i[1] for i in currentpoly])

            rowz = 1
            rowzg = 1
            colz = (width - max_col) // 2

            candidates = [rotate_poly(currentpoly, i) for i in range(3)]

            if checkifcollision(currentpoly, rowz, colz, 2):
                for candidate in candidates:
                    max_col = max([i[0] for i in candidate])
                    max_row = max([i[1] for i in candidate])

                    rowz = 1
                    colz = (width - max_col) // 2

                    if not checkifcollision(candidate, rowz, colz, 2):
                        currentpoly = candidate[:]

                if checkifcollision(currentpoly, rowz, colz, 2): gamemode = 99

            ghostpoly = currentpoly[:]

        if (gametimer - autotime) % (240 // width) == 0:
            if automove[0] and not automove[1]:
                if not checkifcollision(currentpoly, rowz, colz, -1):
                    colz -= 1

            if automove[1] and not automove[0]:
                if not checkifcollision(currentpoly, rowz, colz, 1):
                    colz += 1

        if rot != 0:
            if not checkifcollision(rotate_poly(currentpoly, rot), rowz, colz, 2):
                currentpoly = rotate_poly(currentpoly, rot)
                max_col = max([i[0] for i in currentpoly])
                max_row = max([i[1] for i in currentpoly])
                ghostpoly = currentpoly[:]
                rotations += 1

            elif not checkifcollision(shift_poly(rotate_poly(currentpoly, rot), -1, 0), rowz, colz, 2):
                colz -= 1
                currentpoly = rotate_poly(currentpoly, rot)
                max_col = max([i[0] for i in currentpoly])
                max_row = max([i[1] for i in currentpoly])
                ghostpoly = currentpoly[:]
                rotations += 1

            elif not checkifcollision(shift_poly(rotate_poly(currentpoly, rot), 1, 0), rowz, colz, 2):
                colz += 1
                currentpoly = rotate_poly(currentpoly, rot)
                max_col = max([i[0] for i in currentpoly])
                max_row = max([i[1] for i in currentpoly])
                ghostpoly = currentpoly[:]
                rotations += 1

            elif not checkifcollision(shift_poly(rotate_poly(currentpoly, rot), 0, -1), rowz, colz, 2):
                rowz -= 1
                currentpoly = rotate_poly(currentpoly, rot)
                max_col = max([i[0] for i in currentpoly])
                max_row = max([i[1] for i in currentpoly])
                ghostpoly = currentpoly[:]
                rotations += 1

        rot = 0

        if rowz + max_row + 1 != height and softdrop == True and gametimer % int(
                        100 / 60) == 0 and not checkifcollision(currentpoly, rowz, colz):
            rowz += 1

        if gravity != "0" and gametimer % gravity == 0 and softdrop == False and not checkifcollision(currentpoly, rowz,
                                                                                                      colz):
            rowz += 1

        if gravity == "0":
            while not checkifcollision(currentpoly, rowz, colz, 2):
                rowz += 1
            rowz -= 1

        rowzg = rowz

        ghostpoly = currentpoly[:]
        while not checkifcollision(ghostpoly, rowzg, colz, 2):
            rowzg += 1
        rowzg -= 1

        if colz < 0: colz = 0

        if checkifcollision(currentpoly, rowz, colz):
            if lockdelay == -1:
                lockdelay = gametimer

            if gametimer - lockdelay >= lockspeed:
                imprint(currentpoly, rowz, colz)
                currentpoly = []
                ghostpoly = []

                level += 1

                lineclears = 0

                for line in range(height):
                    if grid[line].count(0) == 0:
                        lineclears += 1
                        grid[line] = [0 for i in range(width)]
                        for row in range(line - 1, -1, -1):
                            for col in range(width - 1, -1, -1):
                                if grid[row][col] == 1 and row != height - 1:
                                    if grid[row + 1][col] == 0:
                                        grid[row + 1][col] = 1
                                        grid[row][col] = 0
                lockdelay = -1
                score += lineclearpoints(lineclears, level)
                level += lineclears
                lines += lineclears
                harddrop = False


        else:
            lockdelay = -1




    if gamemode == -1: rectcolor = (5,31,169)
    if gamemode == 1: rectcolor = survcolors[difficulty]

    draw(gamemode)

    clock.tick(120)
    print(clock.get_fps())


    pygame.display.flip()

