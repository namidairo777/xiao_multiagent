# graphicsDisplay.py
# 2016.11.29
# XIAO TANG
# tangxiao.dalian@gmail.com

from graphicsUtils import *
import math, time
from game import Directions

###############################
#   graphics display code
###########################

DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = formatColor(1.0, 1.0, 1.0)
OBSTACLE_COLOR = formatColor(0.0, 0.0, 0.0)
INFO_PANE_COLOR = formatColor(.1, .1, 0)
SCORE_COLOR = formatColor(.9, .9, .9)
TARGET_COLOR = formatColor(1.0, 0, 0)
PURSUER_COLOR = formatColor(0.0, .8, .8)

TARGET_SCALE = 0.5
PURSUER_SCALE = 0.5

OBSTACLE_SCALE = 0.5

class InfoPane:
    def __init__(self, layout, gridSize):
        self.gridSize = gridSize
        self.width = (layout.width) * gridSize
        self.base = (layout.height + 1) * gridSize
        self.height = INFO_PANE_HEIGHT
        self.fontSize = 24
        self.textColor = TARGET_COLOR
        self.drawPane()

    def toScreen(self, pos, y = None):
        """
        Translates a point relative from the bottom left of the game
        """
        if y == None:
            x, y = pos
        else:
            x = pos

        x = self.gridSize + x
        y = self.base + y
        return x, y

    def drawPane(self):
        self.scoreText = text(self.toScreen(0, 0), self.textColor, "TURNS:  0", "TIMES", self.fontSize, "bold")

    def initializePursuerDistances(self, distances):
        self.pursuerDistanceText = []

        size = 20
        if self.width < 240:
            size = 12
        if self.width < 160:
            size = 10

        for i, d in enumerate(distances):
            t = text(self.toScreen(self.width/2, self.width/8 * i, 0), PURSUER_COLOR, d, "TIMES", size, "bold")
            self.pursuerDistanceText.append(t)

    def updateScore(self, score):
        changeText(self.scoreText, "TURNS: % 4d" % score)

    # def setTeam()

    def updatePursuerDistances(self, distances):
        if len(distances) == 0: return
        if "pursuerDistanceText" not in dir(self): self.initializePursuerDistances(distances)
        else:
            for i, d in enumerate(distances):
                changeText(self.pursuerDistanceText[i], d)


class MultiAgentGraphics:
    def __init__(self, zoom = 1.0, frameTime = 30.0, capture = False):
        self.have_window = 0
        self.currentPursuerImages = {}
        self.pursuerImage = None
        self.zoom = zoom
        self.gridSize = DEFAULT_GRID_SIZE * zoom
        self.capture = capture
        self.frameTime = frameTime

    def checkNullDisplay(self):
        return False

    def initialize(self, state, isBlue = False):
        self.isBlue = isBlue
        self.startGraphics(state)

        # self.drawDistributions(state)
        self.distributionImages = None 
        self.drawStaticObjects(state)
        
        self.drawAgentObjects(state)
        time.sleep(1)
        # information
        self.previousState = state
        

    def startGraphics(self, state):
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = InfoPane(layout, self.gridSize)
        self.currentState = layout

    def drawDistributions(self, state):
        obstacles = state.layout.obstacles
        dist = []
        for x in range(obstacles.width):
            distx = []
            dist.append(distx)
            for y in range(obstacles.height):
                ( screen_x, screen_y ) = self.to_screen( (x, y) )
                block = square( (screen_x, screen_y),
                                0.5 * self.gridSize,
                                color = BACKGROUND_COLOR,
                                filled = 1, behind=2)
                distx.append(block)
        self.distributionImages = dist    

    def drawStaticObjects(self, state):
        layout = self.layout
        self.drawObstacles(layout.obstacles)
        
        refresh()

    def drawAgentObjects(self, state):
        self.agentImages = []
        for index, agent in enumerate(state.agentStates):
            if agent.isTarget:
                image = self.drawTarget(agent, index)
                self.agentImages.append((agent, image))
            else:
                image = self.drawPursuer(agent, index)
                self.agentImages.append((agent, image))
        refresh()

    def update(self, newState, agentIndex):
        
        agentIndex = agentIndex
        agentState = newState.agentStates[agentIndex]
        print newState.agentStates[1]

        # if self.agentImages[agentIndex][0].isTarget != agentState.isTarget: self.swapImages(agentIndex, agentState)
        prevState, prevImage = self.agentImages[agentIndex]
        # print "before move agents"
        if agentIndex == 0:
            time.sleep(1/self.frameTime )
        self.moveAgent(agentState, prevState, prevImage)
        
        # print "after update.move"
        self.agentImages[agentIndex] = (agentState, prevImage)

        self.infoPane.updateScore(newState.score)
        if 'pursuerDistances' in dir(newState):
            self.infoPane.updatePursuerDistances(newState.pursuerDistances)


    def make_window(self, width, height):
        grid_width = width * self.gridSize
        grid_height = height * self.gridSize
        screen_width = grid_width
        screen_height = 2 * self.gridSize + grid_height + INFO_PANE_HEIGHT

        begin_graphics(screen_width,
                       screen_height,
                       BACKGROUND_COLOR,
                       "Multi-Agent-Moving-Target-Pursuit")

    def drawTarget(self, target, index):
        position = self.getPosition(target)
        screen_point = self.to_screen(position)

        return agent_circle(screen_point, TARGET_SCALE * self.gridSize, TARGET_COLOR)

    
    def getEndpoints(self, direction, position=(0,0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi* pos)

        delta = width / 2
        if (direction == 'West'):
            endpoints = (180+delta, 180-delta)
        elif (direction == 'North'):
            endpoints = (90+delta, 90-delta)
        elif (direction == 'South'):
            endpoints = (270+delta, 270-delta)
        else:
            endpoints = (0+delta, 0-delta)
        return endpoints

    def moveAgent(self, newState, prevState, image):
        newPosition = newState.getPosition()
        screenPosition = self.to_screen(newPosition)
        moveAgent(image, screenPosition)

        refresh()

    def animateTarget(self, target, prevTarget, image):
        # if frameTime < 0
        self.moveTarget(self.getPosition(target), self.getDirection(target), image)
        refresh()

    def drawPursuer(self, pursuer, agentIndex):
        position = self.getPosition(pursuer)
        screen_point = self.to_screen(position)

        return agent_circle(screen_point, PURSUER_SCALE * self.gridSize, PURSUER_COLOR)

    def movePursuer(self, pursuer, pursuerIndex, pervPursuer, image):
        screenPosition = self.to_screen(self.getPosition(pursuer))
        endpoints = self.getEndpoints(self.getDirection(pursuer), self.getPosition(pursuer))
        r = PURSUER_SCALE * self.gridSize
        moveAgent(image[0], screenPosition)
        #moveCircle(image[0], screenPosition, r, endpoints)
        refresh()

    def getPosition(self, agentState):
        if agentState.configuration == None: return (-1000, -1000)
        return agentState.getPosition()

    def getDirection(self, agentState):
        if agentState.configuration == None: return Directions.STOP
        return agentState.configuration.getDirection()

    def finish(self):
        end_graphics()

    def to_screen(self, point):
        # print "beginning of to_screen"
        (x, y) = point
        x = x * self.gridSize
        y = (self.height - y) * self.gridSize
        return (x, y)
    # def to_screen()

    def drawObstacles(self, obstacleMatrix):
        obstacleColor = OBSTACLE_COLOR
        for xNum, x in enumerate(obstacleMatrix):
            for yNum, cell in enumerate(x):
                if cell:
                    pos = (xNum, yNum)
                    screenPosition = self.to_screen(pos)
                    rect(screenPosition, self.gridSize, OBSTACLE_COLOR)
        

    def isObstacle(self, x, y, obstacles):
        if x < 0 or y < 0:
            return False
        if x > obstacles.width or y >= obstacles.height:
            return False
        return obstacles[x][y]

    # def updateDistributions



def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

# Saving graphical output

SAVE_POSTSCRIPT = False
POSTSCRIPT_OUTPUT_DIR = "frames"
FRAME_NUMBER = 0
import os
def saveFrame():
    "save current"