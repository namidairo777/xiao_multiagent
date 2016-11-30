# text display 
# 2016/11/28

import time

DRAW_EVERY = 1
SLEEP_TIME = 0
DISPLAY_MOVES = False
QUIET = False

class NullGraphics:
	def initialize(self, state, isBlue = False):
		pass

	def update(self, state):
		pass

	def checkNullDisplay(self):
		return True

	def pause(self):
		time.sleep(SLEEP_TIME)

	def draw(self, state):
		print state

	def updateDistributions(self, dist):
		pass

	def finish(self):
		pass

class MultiAgentGraphics:
	def __init__(self, speed = None):
		if speed != None:
			global SLEEP_TIME
			SLEEP_TIME = speed

	def initialize(self, state, isBlue = False):
		self.draw(state)
		self.pause()
		self.turn = 0
		self.agentCounter = 0

	def update(self, state):
		numAgents = len(state.agentStates)
		self.agentCounter = (self.agentCounter + 1) % numAgents
		if self.agentCounter == 0:
			self.turn += 1
			if DISPLAY_MOVES:
				pursuers = [target.nearestPoint(state.getPursuerPosition(i)) for i in range(1, numAgents)]
				print "%4d) P: %-8s" % (self.turn, str(target.nearestPoint(state.getTaegetPosition()))), '| Score: %-5d' % state.score, '| Pursuer:', pursuers	
			if self.turn % DRAW_EVERY == 0:
				self.draw(state)
				self.pause()
		if state._win or state._lose:
			self.draw(state)

	def pause(self):
		time.sleep(SLEEP_TIME)

	def draw(self, state):
		print state

	def finish(self):
		pass

