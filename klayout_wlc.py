#################################################
##File:           klayout_wlc.py
##Author:         Jaspreet Jhoja
##Python Interface for analysing output text data file from KLayout Software

import pygame
import pygame._view

load_profile = open('data.txt', "r")
read_it = load_profile.read()
Lines = []
paths = []
datapoints = []
finaldata = []
redundant =[]
drawpoints = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

colors = [BLACK, BLUE, GREEN, RED]

for line in read_it.splitlines():
    Lines.append(line)
    
#first new variables
def width():
    global paths
    for i in Lines:
        if "SNAME " in i:
            a = i.replace("SNAME ","")
            indexval = Lines.index(i)
            indexval = indexval+7
            wdata = Lines[indexval]
            split= wdata.split(" ")
            
            for i in split:
                if "w=" in i:
                    fdata = i.replace("w=","")
                    fdata = float(fdata)
            pdata = [a,fdata]
            paths.append(pdata)
            
def cdata():
    global datapoints
    global drawpoints
    for j in paths:
        foundit = 0
        rawdata=[]
        rawdata1 = []
        pathname = ""
        endpt = 'ENDEL '
        startindex = 0
        for i in Lines:
            pathname = "STRNAME "+j[0] 
            if pathname == i and foundit==0:
                foundit = 1
                indexval = Lines.index(pathname)
                indexval = indexval+5
                startpt = Lines[indexval]
                startpt = startpt.replace("XY ","")
                a = startpt.split(': ')
                b = [float(a[0])/1000,float(a[1])/1000]
                z = [float(a[0])/1500,float(a[1])/1500]
                rawdata.append(b)
                rawdata1.append(z)
                startindex = indexval
        while True:
            startindex = startindex + 1
            if(Lines[startindex] == endpt):
                break
            a = Lines[startindex]
            a = a.split(': ')
           # print a
            b = [float(a[0])/1000, float(a[1])/1000]
            z = [float(a[0])/1500,float(a[1])/1500]
            rawdata.append(b)
            rawdata1.append(z)
        datapoints.append(rawdata)
        drawpoints.append(rawdata1)
#    print datapoints

def parea(corners): #calculates the polygon area
    n = len(corners)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def finalstep():
    global finaldata
    for i in range(len(paths)):
        Area = parea(datapoints[i])
        Name = paths[i][0]
        Width = paths[i][1]
        data = [Name, Width, Area/Width]
        finaldata.append(data)
width()
cdata()
finalstep()

#Draw polygon in pygame
def drawpoly():
    pygame.init()
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("waveguides lengths")
    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(WHITE)
        add = 100
        for i in range(len(paths)):
            a = 0
            b = 0

            for j in range(len(drawpoints[i])):
                a = j
                if (a == len(drawpoints[i])-1):
                    b = a
                else:
                    b = a+1
                pygame.draw.line(screen, colors[i], [(drawpoints[i][a][0]), ((drawpoints[i][a][1]))+add], [drawpoints[i][b][0], drawpoints[i][b][1]+add] , 1)

            c = drawpoints[i]
            #write data stats
            xlimit = c[0][0]
            ylimit = c[0][1]
            for k in range(len(drawpoints[i])):
                if (xlimit<= drawpoints[i][k][0]):
                    xlimit = drawpoints[i][k][0]
                if (ylimit<= drawpoints[i][k][1]):
                    ylimit = drawpoints[i][k][1]
            if (i == 0):
                ylimit = ylimit/2 +100
            elif(i == 1):
                ylimit = (ylimit/2)+200
            elif(i == 2):
                ylimit = (ylimit/2)+300
            elif (i == 3):
                ylimit = (ylimit/2)+400
            elif (i == 4):
                ylimit = (ylimit/2)+500
            elif (i ==5):
                ylimit = (ylimit/2) + 600
                
            font = pygame.font.SysFont('Calibri', 12, True, False)
            text1 = font.render("wg_label = "+str(finaldata[i][0]), True, BLACK)
            screen.blit(text1, [xlimit+30, ylimit])
            text2 = font.render("width = "+str(finaldata[i][1])+ " um", True, BLACK)
            screen.blit(text2, [xlimit+30, ylimit+15])    
            text3 = font.render("wg_length = "+str(finaldata[i][2])+ " um", True, BLACK)
            screen.blit(text3, [xlimit+30, ylimit+30])    
            add = add+100
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

drawpoly()
