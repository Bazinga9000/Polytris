import json, random, pygame, pathlib, Polyominoes, math




polylist = []

#sets up this list
for i in range(1, 13):
    if pathlib.Path(str("Poly Order " + str(i) + ".txt")).is_file():
        with open(str("Poly Order " + str(i) + ".txt"), "r") as savefile:
            polylist.append(json.loads(savefile.read()))
    else:
        polylist.append("FOUR OH FOUR")


pygame.init()
screen = pygame.display.set_mode((1000, 760))



        # RED 1
        # BLUE 2
        # GREEN 3
        # ORANGE 4
        # YELLOW 5
        # PURPLE 6
        # CYAN 71


polycolorlist = [
("NaN","NaN","NaN"),
(155,   0,   0),
(  0,   0, 155),
(  0, 155,   0),
(239, 121, 34),
(155, 155, 0),
(155, 0, 155),
( 48,  199, 239),
    (139, 69, 19)

]

#fonts
if True:
    font = pygame.font.SysFont("Trebuchet MS", 25)
    bigfont = pygame.font.SysFont("Trebuchet MS", 45)
    smallfont = pygame.font.SysFont("Trebuchet MS", 18)

#important variables
if True:
    enabledpoly = [0 for i in range(12)]

    enabledpoly[3] = 1
    boardsize = 0
    speedmult = 0
    gametimer = 0
    startinglevel = 0
    gravitytype = 0
    speedcurve = 0

    controls = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_DOWN, pygame.K_UP]
    controlslist = {"Left" : 0,"Right" : 1,"Rotate Left" : 2,"Rotate Right" : 3, "Hold" : 4, "Soft Drop" : 5, "Hard Drop" : 6}



    
    gamemode = 0
    version = "2.0.0"
    gametype = 0
    difficulty = 0
    settingvalue = 0
    settingindex = 0
    clock = pygame.time.Clock()

    minsetvalue = [1,0,0,0,0,"X","X","X","X",0,0]
    maxsetvalue = [12,2,12,12,1,"X","X","X","X",1,5]

    automove = [0, 0]
    dastime = 99999


#survival mode stuff
if True:
    expandatlist = [75,60,55,50,40,30]
    garbagelist = ["X",120 * 20,120 * 15,120 * 12,120 * 12,120 * 10]
    survcolors = [(0,75,8),(26,92,2),(72,109,5),(126,122,8),(143,90,13),(160,48,19)]
    leveljump = [0,20,40,60,80,100]




#if it ain't broke
def draw(gamemode):
    global color

    screen.fill((0, 0, 0))

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    fps = smallfont.render(str(round(clock.get_fps())) + "FPS", True, (0,0,204))
    screen.blit(fps, (screen_width - fps.get_width() - 30, 30))

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

        title = smallfont.render("Gravity Type", True, (0, 0, 204))
        screen.blit(title, (105, 400))

        title = smallfont.render("Gametype", True, (0, 0, 204))
        screen.blit(title, (105, 500))

        if gametype == 1:
            title = smallfont.render("Difficulty",True,(0,0,204))
            screen.blit(title,(105,550))

        title = font.render("Press Enter to Begin", True, (0, 0, 204))
        screen.blit(title, ((screen_width - title.get_width()) // 2, 600))
        

        #enabled poly
        cord = 330
        for i in range(12):
            if enabledpoly[i] == 1:
                numbertxt = smallfont.render(str(i + 1), True, (0, 204, 0))
            else:
                numbertxt = smallfont.render(str(i + 1), True, (204, 0, 0))

            if settingvalue == i + 1 and settingindex == 0:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (cord, 225))

            screen.blit(numbertxt, (cord, 200))

            cord = cord + 30 + numbertxt.get_width()

        #boardsizes
        for i in range(3):
            if i != boardsize:
                sizetxt = smallfont.render(str(sizes[i][0]) + "x" + str(sizes[i][1]), True, (204, 0, 0))
            else:
                sizetxt = smallfont.render(str(sizes[i][0]) + "x" + str(sizes[i][1]), True, (0, 204, 0))

            if settingindex == 1 and i == settingvalue:
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

            if settingvalue == i and settingindex == 2:
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

            if settingvalue == i and settingindex == 3:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (cord, 375))

            screen.blit(lvltxt, (cord, 350))

            cord = cord + 15 + lvltxt.get_width()

        #gravitytype
        types = ["Naive", "Recursive"]
        colors = [(204, 0, 0) for i in types]
        colors[gravitytype] = (0, 204, 0)

        cord = 330

        for n, name in enumerate(types):
            typetxt = smallfont.render(name, True, colors[n])
            screen.blit(typetxt, (cord, 400))

            if settingindex == 4 and settingvalue == n:
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (cord, 425))

            cord = cord + 30 + typetxt.get_width()

        #gametype
        types = ["Simple","Survival","Doubles (NYI)"]
        colors = [(204,0,0) for i in types]
        colors[gametype] = (0,204,0)

        cord = 330

        for n,name in enumerate(types):
            typetxt = smallfont.render(name,True,colors[n])
            screen.blit(typetxt,(cord,500))

            if settingindex == 9 and settingvalue == n:
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

                if settingindex == 10 and settingvalue - 1 == n:
                    arrow = font.render("^", True, (204, 204, 204))
                    screen.blit(arrow, (cord, 575))

            if settingindex == 10 and settingvalue == 0:  # For some reason, the above loop doesn't draw this case ¯\_(ツ)_/¯
                arrow = font.render("^", True, (204, 204, 204))
                screen.blit(arrow, (330, 575))

                cord = cord + 15 + difftxt.get_width()

    if gamemode in [1,99]:

        squaresize = min((screen_width // 2) // width, (screen_height - 60) // height)

        horizshift = (screen_width - (width * squaresize)) / 2
        vertshift = (screen_height - (height * squaresize)) + 30


        gametimertxt = smallfont.render(str(gametimer) + "|" + str(dastime),True,(204,204,0))
        screen.blit(gametimertxt,(30,30))


        scoretxt = smallfont.render("Score: " + intWithCommas(score), True, (0, 204, 0))
        screen.blit(scoretxt, (30, 100))

        leveltxt = smallfont.render("Level: " + str(level), True, (0, 204, 0))
        screen.blit(leveltxt, (30, 130))


        gravitytxt = smallfont.render("Gravity: " + str(round(1/gravity, 2)) + "G", True, (0, 204, 0))
        screen.blit(gravitytxt, (30, 160))

        locktxt = smallfont.render("Lock Delay: " + str(lockspeed) + " Frames", True, (0, 204, 0))
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
                if grid[row][col] != 0:

                    if gamemode == 1:
                        colortuple = polycolorlist[grid[row][col]]
                    else:
                        colortuple = (50, 50, 50)

                    pygame.draw.rect(screen, colortuple, rect)
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


            pygame.draw.rect(screen, polycolorlist[polycolor], rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        if gamemode != 99:

            x_cord = horizshift + 75 + (width * squaresize)
            squaresize = 18
            y_cord = 125 + squaresize
            if maxpoly >= 9: squaresize = 9

            nexttxt = smallfont.render("Next", True, (0, 204, 0))
            screen.blit(nexttxt, (x_cord, 100))

            for num, poly in enumerate(nextpoly):
                maxes = (max([i[0] for i in poly]), max([i[1] for i in poly]))  # col,row

                for brick in poly:
                    rect = (x_cord + (brick[0] * squaresize), y_cord + squaresize * brick[1], squaresize, squaresize)
                    pygame.draw.rect(screen, polycolorlist[colorlist[num]], rect)
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

def intWithCommas(x):
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)

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

def randomvalue():
    value = random.randint(0, 11)
    while enabledpoly[value] != 1:
        value = random.randint(0, 11)

    return value

def calculategravity(level,curve):
    if curve == 0:
        return 60 / (259/256)**level

        # blocks per frame = (259/256)^n / 60
        # frames per block = 60 / (256/256)^n

def calculatelockdelay(level,curve):
    if curve == 0:
        return int(80/(1 + 3/256 * (level - 609)))

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

    else:
        return sum([2 * lineclearpoints(clears-m, level) for m in [1,2,3]])


while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        exit()



    if event.type == pygame.KEYDOWN:
        key = event.key

        if gamemode == 0:

            if key == pygame.K_UP and settingindex != 0:
                if settingindex == 9:
                    settingindex = 4
                else:
                    settingindex -= 1
                    
                if settingvalue not in range(minsetvalue[settingindex],maxsetvalue[settingindex] + 1):
                    settingvalue = 0
                    
                    if settingvalue not in range(minsetvalue[settingindex], maxsetvalue[settingindex] + 1):
                        settingvalue = 1
                        
            if key == pygame.K_DOWN and (settingindex != 9 or (gametype == 1 and settingindex != 10)):
                if settingindex == 4:
                    settingindex = 9
                else:
                    settingindex += 1

                if settingvalue not in range(minsetvalue[settingindex], maxsetvalue[settingindex] + 1):
                    settingvalue = 0

                    if settingvalue not in range(minsetvalue[settingindex], maxsetvalue[settingindex] + 1):
                        settingvalue = 1


            if key == pygame.K_LEFT and settingvalue != minsetvalue[settingindex]:
                settingvalue -= 1

            if key == pygame.K_RIGHT and settingvalue != maxsetvalue[settingindex]:
                settingvalue += 1

            if key == pygame.K_SPACE:
                if settingindex != 0:
                    if settingindex == 1 and settingvalue != boardsize: boardsize = settingvalue
                    if settingindex == 2 and settingvalue != speedmult: speedmult = settingvalue
                    if settingindex == 3 and settingvalue != startinglevel / 50: startinglevel = 50 * settingvalue
                    if settingindex == 4 and settingvalue != gravitytype: gravitytype = settingvalue

                    if settingindex == 9 and settingvalue != gametype: gametype = settingvalue
                    if settingindex == 10 and settingvalue != difficulty: difficulty = settingvalue
                elif not (enabledpoly.count(1) == 1 and enabledpoly[settingvalue - 1] == 1):
                    enabledpoly[settingvalue - 1] = (enabledpoly[settingvalue - 1] + 1) % 2

            if key == pygame.K_RETURN:
                currentpoly = []
                score = 0
                softdrop = False
                lockdelay = -1
                level = startinglevel
                gravity = 120
                harddrop = False
                nextpoly = [[] for i in range(5)]
                nextpoly = [randombrick(randomvalue()) if i == [] else i for i in nextpoly]
                colorlist = [Polyominoes.color(nextpoly[i]) for i in range(5)]
                nextpoly = [Polyominoes.flatten(i) for i in nextpoly]
                heldpoly = []
                ghostpoly = []
                rotations = 0
                automove = [0, 0]
                lines = 0
                rot = 0
                gamemode = 1

                if gametype == 1:
                    level,speedmult,gravitytype,boardsize = 0,0,0,0
                    enabledpoly = [0 for i in range(12)]
                    enabledpoly[3] = 1
                    speedcurve = 0

                maxpoly = 0
                for i in range(12):
                    if enabledpoly[i] == 1:
                        maxpoly = i

                sizes = [[(maxpoly + 2) * 2, (maxpoly + 1) * 5 + 2],
                         [(maxpoly + 3) * 2, (maxpoly + 2) * 5 + 2],
                         [(maxpoly + 4) * 2, (maxpoly + 3) * 5 + 2]]

                grid = [[0 for i in range(sizes[boardsize][0])] for j in range(sizes[boardsize][1])]
                height = len(grid)
                width = len(grid[0])

        if gamemode == 1:

            if key == controls[controlslist["Hold"]]:
                polyswap = [currentpoly[:], heldpoly[:]]

                heldpoly = polyswap[0][:]

                currentpoly = polyswap[1][:]

                if currentpoly == []:
                    rotations = 0

                    currentpoly = nextpoly[0][:]
                    nextpoly[0] = nextpoly[1][:]
                    nextpoly[1] = nextpoly[2][:]
                    nextpoly[2] = nextpoly[3][:]
                    nextpoly[3] = nextpoly[4][:]

                    polycolor = colorlist[0]
                    colorlist[0] = colorlist[1]
                    colorlist[1] = colorlist[2]
                    colorlist[2] = colorlist[3]
                    colorlist[3] = colorlist[4]

                    for i in range(6):
                        nextpoly[4] = randombrick(randomvalue())
                        colorlist[4] = Polyominoes.color(nextpoly[4])

                        nextpoly[4] = Polyominoes.flatten(nextpoly[4])

                        if nextpoly[4] not in [nextpoly[i] for i in [0, 1, 2]]:
                            break

                    currentpoly = Polyominoes.flatten(currentpoly)

                    rowz = 1
                    rowzg = 1
                    colz = (width - max_col) // 2

                    ghostpoly = currentpoly[:]

                    max_col = max([i[0] for i in currentpoly])
                    max_row = max([i[1] for i in currentpoly])


                if Polyominoes.checkifcollision(currentpoly, grid, 0, 0, colz, rowz):
                    gamemode = 99

            if key == controls[controlslist["Left"]]:
                if not Polyominoes.checkifcollision(Polyominoes.shift_poly(currentpoly,-1,0),grid,0,0,colz,rowz):
                    colz -= 1
                    dastime = gametimer + 60
                    automove[0] = 1

            if key == controls[controlslist["Right"]]:
                if not Polyominoes.checkifcollision(Polyominoes.shift_poly(currentpoly,1,0),grid,0,0,colz,rowz):
                    colz += 1
                    dastime = gametimer + 60
                    automove[1] = 1

            if key == controls[controlslist["Rotate Left"]] and currentpoly != []:

                for i in [[0,0],[0,1],[0,-1],[1,0]]:
                    if not Polyominoes.checkifcollision(Polyominoes.rotate_poly(currentpoly,3),grid,i[0],i[1],colz,rowz):
                        rowz += i[1]
                        colz += i[0]
                        currentpoly = Polyominoes.rotate_poly(currentpoly,3)
                        break

            if key == controls[controlslist["Rotate Right"]] and currentpoly != []:

                for i in [[0,0],[0,1],[0,-1],[1,0]]:
                    if not Polyominoes.checkifcollision(Polyominoes.rotate_poly(currentpoly,1),grid,i[0],i[1],colz,rowz):
                        rowz += i[1]
                        colz += i[0]
                        currentpoly = Polyominoes.rotate_poly(currentpoly,1)
                        break

            if key == controls[controlslist["Hard Drop"]]:
                harddrop = True

            if key == pygame.K_l:
                level += 1

            if key == pygame.K_o:
                level += 10

            if key == pygame.K_p:
                level += 100

        if gamemode == 99:
            if key == pygame.K_SPACE:
                gamemode = 0

    pressedkeys = pygame.key.get_pressed()

    if gamemode == 1 and pressedkeys[controls[controlslist["Soft Drop"]]]:
        softdrop = True
    else:
        softdrop = False


    if pressedkeys[controls[controlslist["Left"]]] == 0:
        automove[0] = 0

    if pressedkeys[controls[controlslist["Right"]]] == 0:
        automove[1] = 0


    maxpoly = 0
    for i in range(12):
        if enabledpoly[i] == 1:
            maxpoly = i

    sizes = [[(maxpoly + 2) * 2, (maxpoly + 1) * 5 + 2],
             [(maxpoly + 3) * 2, (maxpoly + 2) * 5 + 2],
             [(maxpoly + 4) * 2, (maxpoly + 3) * 5 + 2]]

    if gamemode == 1:


        gametimer += 1

        if gametype == 1:
            stage = level // expandatlist[difficulty] + 3

            enabledpoly = [0 for i in range(12)]

            for i in range(12):
                if stage >= i:
                    enabledpoly[i] = 1

            maxpoly = 0
            for i in range(12):
                if enabledpoly[i] == 1:
                    maxpoly = i

            sizes = [[(maxpoly + 2) * 2, (maxpoly + 1) * 5 + 2],
                     [(maxpoly + 3) * 2, (maxpoly + 2) * 5 + 2],
                     [(maxpoly + 4) * 2, (maxpoly + 3) * 5 + 2]]

            if sizes[0][1] > height:

                grid = Polyominoes.expandgrid(grid,sizes[0][1],sizes[0][0])

                height = len(grid)
                width = len(grid[0])

            if difficulty != 0 and level > 200:
                if gametimer % garbagelist[difficulty] == 0:
                    if grid[0] != [0 for i in grid[0]]:
                        gamemode = 99
                    else:
                        grid = Polyominoes.addgarbage(grid, difficulty)


        if gametype == 1: countedlevel = level + leveljump[difficulty]
        if gametype == 0: countedlevel = level

        gravity = calculategravity(countedlevel, speedcurve)

        if speedcurve == 0:

            #DO NOT QUESTION THE MATH
            if level >= int((math.log(60 * (height - 2)))/(-8 * math.log(2) + math.log(7) + math.log(37))):
                lockspeed = calculatelockdelay(level, speedcurve)
            else:
                lockspeed = 80

        if currentpoly == []:
            rotations = 0

            currentpoly = nextpoly[0][:]
            nextpoly[0] = nextpoly[1][:]
            nextpoly[1] = nextpoly[2][:]
            nextpoly[2] = nextpoly[3][:]
            nextpoly[3] = nextpoly[4][:]

            polycolor = colorlist[0]
            colorlist[0] = colorlist[1]
            colorlist[1] = colorlist[2]
            colorlist[2] = colorlist[3]
            colorlist[3] = colorlist[4]

            for i in range(6):
                nextpoly[4] = randombrick(randomvalue())
                colorlist[4] = Polyominoes.color(nextpoly[4])

                nextpoly[4] = Polyominoes.flatten(nextpoly[4])

                if nextpoly[4] not in [nextpoly[i] for i in [0, 1, 2]]:
                    break

            currentpoly = Polyominoes.flatten(currentpoly)

            max_col = max([i[0] for i in currentpoly])
            max_row = max([i[1] for i in currentpoly])

            rowz = 1
            rowzg = 1
            colz = (width - max_col) // 2

            if Polyominoes.checkifcollision(currentpoly,grid,0,0,colz,rowz):
                gamemode = 99

            ghostpoly = currentpoly[:]

        if gametimer > dastime:

            if gametimer % (80//width) == 0:

                if automove[0] and not automove[1] and not Polyominoes.checkifcollision(currentpoly,grid,-1,0,colz,rowz):
                    colz -= 1
                if automove[1] and not automove[0] and not Polyominoes.checkifcollision(currentpoly,grid,1,0,colz,rowz):
                    colz += 1

        if harddrop == True:
            while not Polyominoes.checkifcollision(currentpoly,grid,0,1,colz,rowz):
                rowz += 1

        if gravity >= 1 and gametimer % int(gravity) == 0 and softdrop == False and not (
                Polyominoes.checkifcollision(currentpoly,grid,0,1,colz,rowz)):
            rowz += 1


        if gravity < 1 and softdrop == False:
            for i in range(int(1/gravity)):
                if not Polyominoes.checkifcollision(currentpoly,grid,0,1,colz,rowz):
                    rowz += 1

                else:
                    break

        if softdrop == True and gametimer % 2 == 0 and gravity >= 2:
            if not Polyominoes.checkifcollision(currentpoly,grid,0,1,colz,rowz):
                rowz += 1

        ghostpoly = currentpoly[:]
        colzg = colz
        rowzg = rowz

        while not Polyominoes.checkifcollision(ghostpoly,grid,0,1,colzg,rowzg):
            rowzg += 1


        if Polyominoes.checkifcollision(currentpoly,grid,0,1,colz,rowz):
            if lockdelay == -1:
                lockdelay = gametimer

            if harddrop == True: lockspeed = 0

            if gametimer - lockdelay >= lockspeed:
                Polyominoes.imprint(currentpoly, rowz, colz, grid, polycolor)
                currentpoly = []
                ghostpoly = []

                level += 1

                lineclears = 0

                if gravitytype == 0:
                    for line in range(height):
                        if grid[line].count(0) == 0:
                            lineclears += 1
                            grid[line] = [0 for i in range(width)]

                            if gravitytype == 0:
                                for row in range(line - 1, -1, -1):
                                    for col in range(width - 1, -1, -1):
                                        if grid[row][col] != 0 and row != height - 1:
                                            if grid[row + 1][col] == 0:
                                                grid[row + 1][col] = grid[row][col]
                                                grid[row][col] = 0


                elif gravitytype == 1:
                    for line in range(height):
                        if grid[line].count(0) == 0:
                            lineclears += 1
                            grid[line] = [0 for i in range(width)]

                    if lineclears != 0:

                        for row in range(height - 1, -1, -1):
                            if row == [0 for i in range(width)]:
                                pass
                            else:
                                for col in range(width):
                                    if grid[row][col] != 0:
                                        for i in range(row + 1, height):

                                            if grid[i][col] == 0:
                                                grid[i][col] = grid[i-1][col]
                                                grid[i-1][col] = 0

                                            else:
                                                break

                        while Polyominoes.haslineclear(grid):

                            for line in range(height):
                                if grid[line].count(0) == 0:
                                    lineclears += 1
                                    grid[line] = [0 for i in range(width)]

                            for row in range(height - 1, -1, -1):
                                if row == [0 for i in range(width)]:
                                    pass
                                else:
                                    for col in range(width):
                                        if grid[row][col] != 0:
                                            for i in range(row + 1, height):

                                                if grid[i][col] == 0:
                                                    grid[i][col] = grid[i - 1][col]
                                                    grid[i - 1][col] = 0

                                                else:
                                                    break




                lockdelay = -1
                score += lineclearpoints(lineclears, level)
                level += lineclears
                lines += lineclears
                harddrop = False




    # <,>,L,R,H,S,D
    if gametype == 0: rectcolor = (5,31,169)
    if gametype == 1: rectcolor = survcolors[difficulty]


    draw(gamemode)
    pygame.display.flip()
    clock.tick(120)
