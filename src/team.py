# Native populous imports
from objects import *

# Externl modules
import random
import Queue
import math



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
		# state
		self.goal = None
		self.hasLost = False

	def __repr__(self):
		s = "<Team %(id)d >" % {'id': self.id }
		return s

	def checkHasLost(self):
		print self, "Object count: ", len(self.objects)
		# TODO there are objects not being cleared up.

	def checkTeamGoal(self):
		if (self.leader):
			self.goal = 'build'
		else:
			self.goal = 'leader'

	def addObject(self, obj):
		obj.team = self
		if isinstance(obj, Idol):
			self.idol = obj
		else:
			self.objects[obj.id] = obj
			if isinstance(obj, House):
				self.homes[obj.id] = obj
			elif isinstance(obj, Native):
				self.natives[obj.id] = obj
				if obj.is_knight:
					self.knights[obj.id] = obj
				elif obj.is_leader:
					self.leader = obj
		return

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

