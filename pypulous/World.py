from pypulous.GridSqr import GridSqr
from pypulous.IterFromPoint import IterFromPoint
from pypulous.lib.logger import log
from pypulous.objects import PopObject

import math

INFINIT = 999999


class World:
	def __init__ (self, width=5, height=4, name=None):
		self.next_id = 0
		self.width = width
		self.height = height
		self.name = name
		self.objects = dict()
		self.dead_objects = dict()
		self.newGrid()

	def newGrid(self):
		self.grid = []
		for y in range(self.height):
			self.grid.append([])
			for x in range(self.width):
				self.grid[y].append([])
				self.grid[y][x] = GridSqr(x,y,self)

	def printGrid(self):
		for x in self.grid:
			for y in x:
				print( y.objects),
			print ('\n'),

	def checkObjects(self):
		print (self.objects)
		for i, o in dict(self.objects).items():
			if not o.is_alive:
				self.removeObject(o)
		pass

	def addObject(self, obj):
		if isinstance(obj, PopObject):
			obj.id = self.next_id
			self.next_id += 1
			self.objects[obj.id ] = (obj)
			pos = self.grid[obj.y][obj.x]
			pos.append(obj)

	def getPos(self, x, y):
		if (0 <= x < self.width) and (0 <= y < self.height):
			return self.grid[y][x]
		else:
			return None

	def getAjoiningPos(self, x, y):
		pos = self.getPos(x, y)
		pos_list = []
		for ys in range(y-1, y+2):
			for xs in range(x-1, x+2):
				if not (xs == x and ys == y):
					pos2 = self.getPos(xs, ys)
					if pos2:
						pos_list.append(pos2)
		return pos_list

	def getObjFromID(self, id):
		try:
			obj = self.objects[id]
		except IndexError:
			pass
		else:
			return obj

	def closest(self, s, *objects):
		result = False
		shortest_distance = INFINIT
		for o in objects:
			if (not hasattr(o, 'x')):
				continue # TODO: Check me
			so_x = s.x - o.x
			so_y = math.copysign(so_x, s.y - o.y)
			so_h = so_x * so_x + so_y * so_y
			if (so_h <= shortest_distance):
				result = o
				shortest_distance = so_h
		return result

	def findNearestPosFromFunction(self, source, matchFunc):
		closest_pos = None
		for p in IterFromPoint(source, self):
			if matchFunc(p):
				return p

	def findNearestObjFromFunction(self, source, matchFunc):
		#populous.log(( source, matchFunc))
		closest_obj = None
		for i in self.objects:
			obj = self.objects[i]
			if matchFunc(obj):
				if not closest_obj:
					closest_obj = obj
				else:
					closest_obj = self.closest(source, closest_obj, obj)
		return closest_obj

	# TODO: Some checks
	def moveObj(self, id, x, y):
		obj = self.getObjFromID(id)
		self.grid[y][x].append(obj)
		self.grid[obj.y][obj.x].remove(obj)
		obj.x = x
		obj.y = y

	def removeObject(self, obj):
		return self.removeObjectWithID(obj.id)

	def removeObjectWithID(self, id):
		try:
			obj = self.objects.pop(id)
			log(( "Removed object %(id)s" % {'id': obj}))
		except KeyError:
			log(( "Error Removing object %(id)d" % {'id': id}))
			log(( "\nObject List\n", self.objects, "\n\nGrid State\n"))
			self.printGrid()
			raise KeyError()
		else:
			(x, y) = (obj.x, obj.y)
			self.grid[y][x].remove(obj)
			return obj

	def kill(self, obj):
		if obj.is_alive:
			return obj.die()
		removed_obj = self.removeObject(obj)
		self.dead_objects[removed_obj.id ] = (removed_obj)
		if not removed_obj.killed_by:
			removed_obj.killed_by = "unknown"
		return removed_obj

	def generateWorld(self, teams, native_count=3):
		"""Sets up the world.

		Input:
			teams: List of teams to add objects to. The first one is taken as the neautral team. Minimum of 3, max of len(default_team_settings)
			native_count: The number of natives to give to each team. Defaults to 3, Minimum is 1.
		"""
		self.newGrid()
			# try to keep teams seperated
				# split the grid into equal parts for each player (neutral zone?)
				# Choose a random location.
				# Put the leader there
			# create random land with hills
				# Start where there are natives
				# put random objects accross the land, (trees, rocks)
			# Place remaining natives
				# put other natives around leader.
				# Use an expanding radius based on number of natives to add
				# Ensure on land, within grid bounds, not on top of another native, not too far from another native (how far is too far)

	def inspectPos(self, x, y):
		grid_sq = self.getPos(x, y)
		return grid_sq.inspect()