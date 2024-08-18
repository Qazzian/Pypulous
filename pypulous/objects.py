#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pypulous.lib.logger import log

class PopObject:
	file_name = ''
	def __init__(self, world, x=0, y=0, team=None, type=""):
		self.id = 0
		self.x = x
		self.y = y
		self.type = ""
		self.is_alive = True # if not is_alive, remove from game
		self.killed_by = None # text description
		self.world = world
		if world == None:
			raise InHisOwnWorldError("Objects need to be in the real world.")
		else:
			world.addObject(self)
		self.team = team
		if team != None:
			team.addObject(self)
		else:
			log( "Created an object without a team.", self)
			raise Exception('no team')
		self.file_name = ''
		self.state = None

	def getPos(self):
		if not self.world:
			raise Exception('Object not in a world')
		pos = self.world.getPos(self.x, self.y)
		return pos

	# act will need to be overridden by actors (natives, houses, etc.)
	def act(self):
		return False

	def die(self, cause=None):
		self.is_alive = False
		self.killed_by = cause or self.state
		self.state = 'dead'
		log(( self, "killed by ", cause))

	def isEnemy(self, other):
		if isinstance(other, PopObject):
			# TODO: Need to check for idols.
			if self.team and other.team:
				return self.team.isEnemy(other.team)
		return False

	def __repr__(self):
		s = "<%(type)s id: %(id)d Team: %(team)d>" % {'type':self.__class__, 'id': self.id, 'team':self.team.id }
		return s

# somehow bestowes leadership
class Idol(PopObject):
	def __init__ (self, world, x=0, y=0, team=None):
		PopObject.__init__(self, world, x, y, team)
		self.file_name = "idol.gif"

	def join(self, newLeader):
		if self.x == newLeader.x and self.y == newLeader.y:
			log( "Idol.join ", newLeader, "\n")
			self.team.setLeader(newLeader)

	def isEnemy(self, other):
		return False







class InHisOwnWorldError(Exception):
	pass