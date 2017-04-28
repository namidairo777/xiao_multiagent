# mapAbstraction.py
# 2017.4.27
# XIAO TANG
# tangxiao.dalian@gmail.com
"""
Map -> Node -> abstract
"""
class Node(object):
	"""A node is representative for a position"""
	def __init__(self, level):
		self.x = 0 				# coordinate x
		self.y = 0				# coordinate y
		self.level = level      # abstraction level
		self.isAbstracted = False    # abtracted or not
		self.neighbors = []		# neighbor nodes
		self.children = []		# child nodes ( abtraction level - 1)

	def addNeighbors(self, node):
		"""
		Append neighbor to current node's neighbors list
		"""
		self.neighbor.append(node)



