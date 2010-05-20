#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Implimentation notes

# dictionaries of PopObject's should use the object id as the key name

# Native populous imports
from objects import *

# Externl modules
import random
import Queue
import math

# Define some constants:
GRID_SQUARE_SIZE = 30 # px
FRAMES_PER_SECOND = 30
NATIVE_SPEED = 15 # pixels per second (pps)
# Times in seconds
NATIVE_SQUR_TRAVEL_TIME = GRID_SQUARE_SIZE / NATIVE_SPEED
NATIVE_BUILD_TIME = 1
NATIVE_THINK_TIME = 1
NATIVE_JOIN_TIME = 0

NATIVE_DROWN_TIME_WATER = 15
NATIVE_DROWN_TIME_SWAMP = 15

INFINIT = 999999

DEBUG = False

def set_debug(level=False):
	DEBUG = level

class Populous:
	def __init__ (self):
		self.update_interval = 25
		self.fps = 25
		# world settings
		self.world_width = 5
		self.world_height = 4
		self.team_count = 2 # not including the neutral team (id:0)
		self.teams = []
		self.world = None
		self.random = getRandom()

	def startGame(self):
		self.world = World(width=self.world_width, height=self.world_height)
		for i in range(self.team_count + 1):
			new_team = Team(i)
			self.teams.append(new_team)
		self.world.generateWorld(self.teams)

	# doLoop. Needs to be in a seperate thread?
	def doLoop(self):
		# Get queued user commands
		# for each object: object.act()
		# update display
		pass

	def getWinner(self):
		team_count = 0
		winner = None
		for t in self.teams:
			if not t.hasLost:
				team_count += 1
				winner = t.id
		if team_count > 1:
			return False
		else:
			return winner

	def endGame(self):
		pass

	def mouseToGameCoords(self, x, y):
		x -= x % GRID_SQUARE_SIZE
		gx = x / GRID_SQUARE_SIZE
		y -= y % GRID_SQUARE_SIZE
		gy = y / GRID_SQUARE_SIZE
		return (gx, gy)

	def queueCommand(self):
		pass


class GridSqr:
	def __init__ (self, x, y, world):
		self.x = x
		self.y = y
		self.world = world
		self.objects = dict() # object_id : object
		self.builders = dict() # team_id: native_id natives that aim to build on this place

	def __repr__(self):
		state = (self.hasHouse() and 'H') or (not self.isBuildable() and 'O') or 'E'
		s = '<Position %(x)d,%(y)d> Objects: %(count)d, state: %(state)s' % {
			'x':self.x, 'y':self.y, 'count':len(self.objects), 'state':state
		}
		return s

	def append(self, obj):
		if isinstance(obj, PopObject):
			if isinstance(obj, House):
				if self.hasHouse():
					raise Exception, "Position already has a house! %(self)s" % {'self':self}
				self.builders = dict() # clear list of builders.
			self.objects[obj.id] = obj
		else:
			s = "Object %(type)s is not a subclass of PopObject " % {'type':obj.__class__}
			raise TypeError, s

	def remove(self, obj):
		# TODO: fix me.
		removed_obj = self.objects.pop(obj.id)
		populous.log(( "removed", removed_obj, "From %d,%d" % (self.x, self.y)))
		populous.log("Now has objects: ", self.inspect())
		return removed_obj

	def targeted(self, native):
		""" Record who's trying to get here by team
		    Want to make natives from the same team don't all go for the same place."""
		pass

	def isBuildable(self):
		if self.hasHouse():
			return False
		else:
			for neighbours in self.world.getAjoiningPos(self.x, self.y):
				if neighbours.hasHouse():
					return False
		return True

	def hasHouse(self):
		for i in self.objects:
			if isinstance(self.objects[i], House):
				return self.objects[i]
		return False

	def hasEnemy(self, native):
		for i in self.objects:
			if isinstance(self.objects[i], Native) and self.objects[i].isEnemy(native):
				return self.objects[i]
			if isinstance(self.objects[i], House) and self.objects[i].isEnemy(native):
				return self.objects[i]
		return False

	def inspect(self):
		s = self.__repr__() + "\n"
		for o in self.objects:
			s += self.objects[o].__repr__() + "\n"
		return s

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
				print y.objects,
			print '\n',

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
			populous.log(( "Removed object %(id)s" % {'id': obj}))
		except KeyError:
			populous.log(( "Error Removing object %(id)d" % {'id': id}))
			populous.log(( "\nObject List\n", self.objects, "\n\nGrid State\n"))
			self.printGrid()
			raise KeyError
		else:
			(x, y) = (obj.x, obj.y)
			self.grid[y][x].remove(obj)
			return obj

	def kill(self, obj):
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



class IterGrid:
	def __init__(self, world):
		self.world = world
		self.next_index = 0
		self.next_x = 0
		self.next_y = 0

	def next(self):
		if self.next_y >= self.world.height:
			raise StopIteration
		else:
			pos = self.world.getPos(self.next_x, self.next_y)
			self.next_x += 1
			if self.next_x >= self.world.width:
				self.next_x = 0
				self.next_y += 1
			return pos

	def __iter__(self):
		return self

class IterFromPoint:
	def __init__(self, source, world, radius_limit=None):
		self.world = world
		self.radius_limit = radius_limit
		self.source = source
		self.index = 0
		self.current_radius = 0
		self.x = self.x_min = self.x_max = source.x
		self.y = self.y_min = self.y_max = source.y

	def next(self):
		pos = self.getNextPos()
		self.index += 1
		return pos

	def getNextPos(self):
		if (self.radius_limit and self.current_radius > self.radius_limit):
			raise StopIteration
		if (self.x_min < 0 and self.x_max >= self.world.width and
				self.y_min < 0 and self.y_max >= self.world.height):
			raise StopIteration
		pos = self.world.getPos(self.x, self.y)
		if (self.x == self.x_max and self.y == self.y_max):
			self.current_radius += 1
			self.x_min = self.source.x - self.current_radius
			self.x = self.x_max = self.source.x + self.current_radius
			self.y_min = self.source.y - self.current_radius
			self.y = self.y_max = self.source.y + self.current_radius
		if (self.y == self.y_max and self.x > self.x_min):
			self.x -= 1
		elif (self.x == self.x_min and self.y > self.y_min):
			self.y -= 1
		elif (self.y == self.y_min and self.x < self.x_max):
			self.x += 1
		elif (self.x == self.x_max and self.y < self.y_max):
			self.y += 1
		if not pos:
			pos = self.getNextPos()
		return pos

	def __iter__(self):
		return self



default_team_settings = [
		{'name':'neutral', 'colour':"#cccccc"},
		{'name':'Player',  'colour':"#0000ff"},
		{'name':'CPU',     'colour':"#ff0000"},
		{'name':'unknown', 'colour':"#00ff00"},
		{'name':'unknown', 'colour':"#00ffff"},
		{'name':'unknown', 'colour':"#ff00ff"},
		{'name':'unknown', 'colour':"#ffff00"},
	]

class Team:
	def __init__(self, id = 0):
		# Settings
		self.id = id
		self.name = default_team_settings[id]['name']
		self.colour = default_team_settings[id]['colour']
		# Objects
		self.objects = dict()
		self.natives = dict()
		self.leader = None
		self.knights = dict()
		self.homes = dict()
		self.idol = None
		# other
		self.hasLost = False

	def __repr__(self):
		s = "<Team %(id)d >" % {'id': self.id }
		return s

	def addObject(self, obj):
		self.objects[obj.id] = obj
		if isinstance(obj, Native):
			self.natives[obj.id] = obj
			if obj.is_knight:
				self.knights[obj.id] = obj
			elif obj.is_leader:
				self.leader = obj
		elif isinstance(obj, House):
			self.homes[obj.id] = obj
		elif isinstance(obj, Idol):
			self.idol = obj
		obj.team = self

	def removeObject(self, id):
		obj = self.objects.pop(id)
		if isinstance(obj, Native):
			self.natives.pop(id)
			if obj.is_knight:
				self.knights.pop(id)
			elif obj.is_leader:
				self.removeLeader(obj)
		elif isinstance(obj, House):
			self.homes.pop(id)
		obj.team = None

	def setLeader(self, newLeader):
		if not self.leader and self.id == newLeader.team.id:
			self.leader = newLeader
			newLeader.is_leader = True
			return True
		else: return False

	def replaceLeader(self, oldLeader, newLeader):
		""" Replaces the old leader with the current.
		    you need a handle of the old one to allow you to replace him. """
		if self.removeLeader(oldLeader):
			if self.setLeader(newLeader):
				return True
		return False

	def removeLeader(self, oldLeader):
		""" removeLeader takes leadership off the current leader. e.g. he is knighted. """
		if self.leader.id == oldLeader.id:
			self.leader = None
			return True
		else:
			return False

	def isEnemy(self, team2):
		if self.id == 0 or team2.id == 0:
			return False
		if self.id == team2.id:
			return False
		return True

#################
# Utility methods
#################

def getRandom():
	rand = random.Random()
	rand.seed = 10
	return rand

def getRandomPercent():
	return getRandom().randint(0, 100)

def log(msg, *args):
	if DEBUG:
		print msg
		for i in args:
			print i
	pass