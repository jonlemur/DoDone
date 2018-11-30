import pygame
from pygame.locals import *
from Task import Task
from DynamicLabel import DynamicLabel
import json
import tempfile
import os
import random

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((300, 500))
pygame.display.set_caption("DoDone")
done = False

bgColor = pygame.Color(30, 30, 30, 0)

all_tasks = pygame.sprite.Group()
labels = pygame.sprite.Group()

wWidth, wHeight = pygame.display.get_surface().get_size()

color1 = pygame.Color(20, 40, 20, 0)

# LABELS
doLbl = DynamicLabel("DO",bgColor,100,15)
doLbl.rect.center = (wWidth*0.25,20)
labels.add(doLbl)

doneLbl = DynamicLabel("DONE",bgColor,100,15)
doneLbl.rect.center = (wWidth*0.75,20)
labels.add(doneLbl)


prevFont = pygame.font.SysFont('Verdana', 12)
textColor = pygame.Color(200, 200, 200)
taskText = ''
prevText = prevFont.render(taskText , 1, textColor)


def sortTasks():
    wWidth, wHeight = pygame.display.get_surface().get_size()
    tYPosDO = []
    tYPosDONE = []
    doTasks = []
    doneTasks = []
    for t in all_tasks.sprites():
        if t.rect.center[0] < wWidth/2:
            tYPosDO.append(t.rect.center[1])
            doTasks.append(t)
        else:
            tYPosDONE.append(t.rect.center[1])
            doneTasks.append(t)

    tYPosDO.sort()
    tYPosDONE.sort()

    setY = 15
    for p in tYPosDO:
        for t in doTasks:
            if t.rect.center[1] == p:
                setY +=67
                t.rect.center = (wWidth*0.25+2,setY)
                t.setColor(False)
                break

    setY = 15
    for p in tYPosDONE:
        for t in doneTasks:
            if t.rect.center[1] == p:
                setY +=67
                t.rect.center = (wWidth*0.75-2,setY)
                t.setColor(True)
                break


def createTask(text,done=False):

    rColor = pygame.Color(random.randint(20,150), random.randint(20,150), random.randint(20,150), 0)
    wWidth, wHeight = pygame.display.get_surface().get_size()
    t = Task(text, rColor, wWidth / 2 - 10, 60)
    if done==True:
        t.rect.center = (wWidth*0.75+2,30)
    else:
        t.rect.center = (wWidth * 0.25 + 2, 30)
    all_tasks.add(t)
    sortTasks()


saveFile = tempfile.gettempdir() + '\\dodone.json'

def loadTasks():
    if os.path.isfile(saveFile):
        doneList = []
        doList = []
        with open(saveFile,'r') as openFile:
            save = json.load(openFile)
            doneList = save['done']
            doList = save['do']

        for t in doList:
            createTask(t)

        for t in doneList:
            createTask(t,True)



def saveToSaveFile():
    wWidth, wHeight = pygame.display.get_surface().get_size()
    tYPosDO = []
    tYPosDONE = []
    doList = []
    doneList = []
    for t in all_tasks.sprites():
        if t.rect.center[0] < wWidth/2:
            tYPosDO.append(t.rect.center[1])
            doList.append(t)
        else:
            tYPosDONE.append(t.rect.center[1])
            doneList.append(t)

    tYPosDO.sort()
    tYPosDONE.sort()

    doListOrdered = []
    doneListOrdered = []

    for p in reversed(tYPosDO):
        for t in doList:
            if t.rect.center[1] == p:
                doListOrdered.append(t.text)

    for p in reversed(tYPosDONE):
        for t in doneList:
            if t.rect.center[1] == p:
                doneListOrdered.append(t.text)

    saveDict = {
        'do':doListOrdered,
        'done':doneListOrdered
    }

    print saveFile
    with open(saveFile, 'w') as outfile:
        json.dump(saveDict, outfile)



loadTasks()
sortTasks()

timer = 0 # for deticting double clicks
dt = 0.0




while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if timer == 0.0:  # First mouse click.
                    timer = 0.01  # Start the timer.
                # Click again before 0.5 seconds to double click.
                elif timer < 0.5:
                    print('double click')
                    for t in all_tasks.sprites():
                        t.setEvent(event, True)
                    timer = 0.0
            for t in all_tasks.sprites():
                t.setEvent(event)
        elif event.type == pygame.MOUSEMOTION:
            for t in all_tasks.sprites():
                t.setEvent(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            for t in all_tasks.sprites():
                t.setEvent(event)
            sortTasks()
            saveToSaveFile()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(taskText)
                if taskText != '':
                    createTask(taskText)
                    saveToSaveFile()
                taskText = ''
            elif event.key == pygame.K_BACKSPACE:
                taskText = taskText[:-1]
            else:
                taskText += event.unicode

            prevText = prevFont.render(taskText, 1, textColor)

    screen.fill(bgColor)
    all_tasks.update()
    all_tasks.draw(screen)
    labels.draw(screen)

    screen.blit(prevText,(wWidth/2-prevText.get_width()/2,30))

    # double click timer
    if timer != 0.0:
        timer += dt
        # Reset after 0.5 seconds.
        if timer >= 0.5:
            timer = 0.0

    pygame.display.flip()
    dt = clock.tick(60)/1000.0
    #print dt




'''
elif event.type == VIDEORESIZE:

    screen = pygame.display.set_mode(event.dict['size'])
    wWidth, wHeight = pygame.display.get_surface().get_size()
    tasks = all_tasks.sprites()
    for t in tasks:
        if t.rect.center<wWidth:
            t.rect.center = (wWidth * 0.25, 30)
        else:
            t.rect.center = (wWidth * 0.75, 30)
        t.resize(wWidth / 2-10, 60)

    sortTasks()
    doLbl.rect.center = (wWidth * 0.25, 20)
    doneLbl.rect.center = (wWidth * 0.75, 20)
'''