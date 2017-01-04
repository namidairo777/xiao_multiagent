# layout.py
# created in 2016/11/27
# created by XIAO TANG
# update date: 2016/11/27

from util import manhattanDistance
from game import Grid
import os
import random

class Layout:
	"""
	A layout manages the static information about the game board

	"""
	def __init__(self, layoutText):
		self.width = len(layoutText[0])
		self.height = len(layoutText)
		self.obstacles = Grid(self.width, self.height, False)
		self.agentPositions = []
		self.numPursuers = 0
		self.processLayoutText(layoutText)
		self.layoutText = layoutText

	def getNumPursuers(self):
		return self.numPursuers

	# def initializeVisibilityMatrix
	def isObstacle(self, pos):
		x, y = pos
		return self.obstacles[x][y]

	# def getRandomLegalPosition
	# def getRandomCorner
	# def getFurthestCorner
	# def isVisibleFrom
	def __str__(self):
		return "\n".join(self.layoutText)

	def deepCopy(self):
		return Layout(self.layoutText[:])

	def processLayoutText(self, layoutText):
		"""
		The shape of the map.
		Each character represents a different type of object
		% - Obstacle
		T - Target
		P - Pursuer
		"""
		# print layoutText
		randomFlag = False
		maxY = self.height - 1
		for y in range(self.height):
			for x in range(self.width):
				layoutChar = layoutText[maxY - y][x]
				self.processLayoutChar(x, y, layoutChar)
		if self.numPursuers == 0:
			self.randomPosition()
		
		self.agentPositions.sort()
		self.agentPositions = [(i == 0, pos) for i, pos in self.agentPositions]

	def randomPosition(self):
		"""
		For small map, we use 2 pursuers
		For Big map, use 3.
		"""


		import random
		# Random target
		vacancy = []
		for x in range(self.width):
			for y in range(self.height):
				if self.obstacles[x][y] == False:
					vacancy.append((x, y))
		# Shuffle it and give these position to agent
		random.shuffle(vacancy)
		for index in range(4):
			if index == 0:
				self.agentPositions.append((0, vacancy[index]))
			else:
				self.numPursuers += 1
				self.agentPositions.append((self.numPursuers, vacancy[index]))



	def processLayoutChar(self, x, y, layoutChar):
		#print self.height, self.width
		
		if layoutChar == '%':
			self.obstacles[x][y] = True
			
		elif layoutChar == 'T':
			self.agentPositions.append((0, (x, y)))
			
		elif layoutChar == 'P':
			self.numPursuers += 1
			self.agentPositions.append((self.numPursuers, (x, y)))
			
		
		# print self.numPursuers
def getLayout(name, back = 2):
	if name == "random":
		return getRandomMap()
	if name.endswith('.lay'):
		layout = tryToLoad('layouts/' + name)
		if layout == None: layout = tryToLoad(name)
	else:
		layout = tryToLoad('layouts/' + name + '.lay')
		if layout == None: layout = tryToLoad(name + '.lay')
	if layout == None and back >= 0:
		curdir = os.path.abspath('.')
		os.chdir('..')
		layout = getLayout(name, back - 1)
		os.chdir(curdir)
	return layout

def tryToLoad(fullname):
	if(not os.path.exists(fullname)): return None
	f = open(fullname)
	try: return Layout([line.strip() for line in f])
	finally: f.close()

def getRandomMap():
	return 0
