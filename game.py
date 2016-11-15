#2016-07-29
#Developed by XIAO TANG
#tangxiao.dalian@gmail.com

#game.py
#

from util import *
import time, os
import traceback
import sys

######################
#                    #
######################

class Agent:
	"""
	An agent must define a getAction method

	"""
	def __init__(self, index=0):
		self.index = index

	def getAction(self, state):

		raiseNotDefined()

class Directions:
	"""
	Left and right corresponds to four Directions (north, south, east, west)
	"""
	NORTH = 'North'
	SOUTH = 'South'
	EAST = 'East'
	WEST = 'West'
	STOP = 'Stop'

	LEFT = {NORTH: WEST,
			SOUTH: EAST,
			EAST: NORTH,
			WEST: SOUTH,
			STOP: STOP}

	RIGHT = dict([(y,x) for x, y in LEFT.items()])

	REVERSE = {NORTH: SOUTH,
				SOUTH: WEST,
				EAST: WEST,
				WEST: EAST,
				STOP: STOP}

class Configuration:
	"""
	A Configuration holds the (x,y) coordinate of a character, along with its traveling direction.

	"""
	
	def __init__(self, pos, direction):
		self.pos = pos
		self.direction = direction

	def getPosition(self):
		return (self.pos)

	def getDirection(self):
		return self.direction

	def isInteger(self):
		x, y = self.pos
		return x == int(x) and y == int(y)

	def __eq__(self, other):
		if other == None: return False
		return (self.pos == other.pos and self.direction == other.direction)

	def __hash__(self):
		x = hash(self.pos)
		y = hash(self.direction)
		return hash(x + 13 * y)

	def __str__(self):
		return "(x,y)="+str(self.pos)+", "+str(self.direction)

	def generateSuccssor(self, vector):
		"""
		Generate a new Configuration reached by translating the current configuration by the action vector. 
		This is a low-level call and does not attempt to respect the legality of the movement
		Actions are movement vectors.
		"""

		x, y = self.pos
		dx, dy = vector
		direction == Actions.vectorToDirection(vector)
		if direction == Directions.STOP:
			direction = self.direction
		return Configuration((x + dx, y + dy), direction)

class AgentState:
	"""
	AgentStates hold the state of an agent (configuration, speed, scared, etc)

	"""

	def __init__(self, startConfiguration, is Pacman):
		self.start = startConfiguration
		self.configuration = startConfiguration
		self.isPacman = isPacman
		self.scaredTimer = 0
		self.numCarrying = 0
		self.numReturned = 0

	def __str__(self):
		if self.isPacman:
			return "Pacman: "+str( self.configuration)
		else:
			return "Ghost: "+str(self.configuration)

	def __eq__(self, other):
		if other == None:
			return False
		return self.configuration == other.configuration and self.scaredTimer == other.scaredTimer

	def __hash__(self):
		state = AgentState(self.start, self.isPacman)
		state.configuration = self.configuration
		state.scaredTimer = self.scaredTimer
		state.numCarrying = self.numCarrying
		state.numReturned = self.numReturned
		return state

	def getPosition(self):
		if self.configuration == None: return None
		return self.configuration.getPosition()

	def getDirection(self):
		return self.configuration.getDirection()
		



















