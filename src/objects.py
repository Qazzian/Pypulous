#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Native populous imports
#from populous import *
import populous

# Externl modules
import random

class PopObject:
	file_name = ''
	def __init__(self, world, x=0, y=0, team=None):
		self.id = 0
		self.x = x
		self.y = y
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
			populous.log( "Created an object without a team.", self)
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
		populous.log(( self, "killed by ", cause))

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
			populous.log( "Idol.join ", newLeader, "\n")
			self.team.setLeader(newLeader)

	def isEnemy(self, other):
		return False


class Native(PopObject):
	def __init__ (self, world, x=0, y=0, team=None):
		self.health = 100 # percent
		self.strength = 1 # max 100 except the leader and knights
		self.is_leader = False
		self.is_knight = False
		PopObject.__init__(self, world, x, y, team)
		self.team_goal = None  # A text field.
		self.goal = None       # A grid square or PopObject to aim for
		self.in_action = 0     # Number of ticks for action to compleate
		self.rand = populous.getRandom()
		self.file_name = "native_%(id)d.png" % {'id': self.team.id}
		# used with in_action to move the image smoothly between actions
		self.x_dir, self.y_dir = 0, 0

	def __repr__(self):
		s = "<%(type)s id: %(id)d T:%(team)d L:%(leader)s K:%(knight)s>" % {
					'type':'Native', 'id': self.id , 'team': self.team.id,
					'leader':(self.is_leader and 'L' or '-'), 'knight':(self.is_knight and 'K' or '-')}
		return s

	# Priorities in order: Leader, build, fight.
	def decideGoal(self):
		if not self.team_goal or self.team_goal != self.team.goal:
			tg = self.team_goal = self.team.goal
		else:
			tg = self.team_goal
		if tg == 'build':
			self.goal = self.findNearestEmptyLand()
		elif tg == 'fight':
			self.goal = self.findNearestEnemy()
		elif tg == 'leader':
			if not self.is_leader:
				self.goal = self.findLeader()
			else: self.goal = self.team.idol
		if not self.goal:
			self.decideOwnGoal()
		populous.log(self, "has found goal", self.goal, "\n")

	def decideOwnGoal(self):
		land = self.findNearestEmptyLand()
		enemy = self.findNearestEnemy()
		leader = self.findLeader()
		# TODO: Goal is the closest of the above.
		goal = self.world.closest(self, land, enemy)
		self.goal = goal
		return goal

	def checkTeamGoal(self):
		if self.team == None:
			populous.log( "Native", self.id, self.x, self.y, "Has no Team")
		if self.team_goal != self.team.goal:
			self.team_goal = self.team.goal
			return False
			#populous.log( "changed goal to", self.goal)
		else: return True

	def checkMyGoal(self):
		"""Ensures that the curent goal is still valid. Returns False if not."""
		if self.goal == None:
			#populous.log( "There is no goal")
			return False
		#if not self.checkTeamGoal():
			#populous.log( "team goal is bad")
			#return False
		if isinstance(self.goal, PopObject):
			if not self.goal.is_alive:
				#populous.log( "Goal has died")
				return False
		if isinstance(self.goal, populous.GridSqr):
			if not self.goal.isBuildable():
				#populous.log( "Goal no longer buildable")
				return False
		return True

	# return True if acted
	def act(self):
		if self.in_action > 0:
			self.in_action -= 1
			return False
		if self.state == 'fighting' and self.checkMyGoal():
			self.attack(self.goal)
			return True
		self.state = 'thinking'
		# If on top of an enemy interrupt goal
		foe = self.isNearEnemy()
		if foe:
			self.goal = foe
		if not self.checkMyGoal():
			#populous.log( "need a new goal")
			self.goal = None
			self.decideGoal()
		# act on goal
		if not self.goal:
			raise Exception("object has no Goal")
		if self.x != self.goal.x or self.y != self.goal.y:
			self.state = 'moving'
			self.move(self.goal.x, self.goal.y)
		elif isinstance(self.goal, PopObject):
			if self.goal.team.id == self.team.id:
				self.state = 'joining'
				self.goal.join(self)
				self.goal = None
			else:
				self.state = 'fighting'
				self.attack(self.goal)
		elif isinstance(self.goal, populous.GridSqr):
			if self.team_goal == 'build':
				self.state = 'building'
				self.build()
		return True

	def findLeader(self, idol_ok = True):
		obj = self.team.leader
		if not obj and idol_ok:
			obj = self.team.idol
		return obj

	def join(self, other):
		if (self.x, self.y) == (other.x, other.y):
			if self.health < 100:
				self.health += self.rand.randint(int(other.health*0.25),int(other.health*0.95))
				if self.health > 100: self.health = 100
			self.strength += self.rand.randint(int(other.strength*0.25), int(other.strength*0.85))
			if not self.is_leader and self.strength > 100: self.strength = 100
			other.die('Joined with friend')

	def findNearestEmptyLand(self):
		def matchBuildableLand(pos):
			if isinstance(pos, populous.GridSqr):
				return pos.isBuildable()
		return self.world.findNearestPosFromFunction(self, matchBuildableLand)

	def findNearestEnemy(self):
		return self.world.findNearestObjFromFunction(self, self.matchEnemy)

	def matchEnemy(self, obj):
		if (isinstance(obj, House) or isinstance(obj, Native)) and obj.team.id != self.team.id:
			return True

	def findNearestEnemyHouse(self):
		def matchEnemyHouse(obj):
			if isinstance(obj, House) and obj.team.id != self.team.id:
				return True
		return self.world.findNearestObjFromFunction(self, matchEnemyHouse)

	def isNearEnemy(self):
		pos = self.getPos()
		my_enemy = pos.hasEnemy(self)
		attack_chance = populous.getRandomPercent()
		if (my_enemy and attack_chance > 10):
			return my_enemy
		else:
			for xy in self.world.getAjoiningPos(pos.x, pos.y):
				my_enemy = xy.hasEnemy(self)
				attack_chance = populous.getRandomPercent()
				if (my_enemy and attack_chance > 66):
					return my_enemy
		return False

	def move(self, x, y):
		if x > self.x:
			new_x = self.x+ 1
			self.x_dir = 1
		elif x < self.x:
			new_x = self.x - 1
			self.x_dir = -1
		else:
			new_x = x
			self.x_dir = 0
		if y > self.y:
			new_y = self.y + 1
			self.y_dir = 1
		elif y < self.y:
			new_y = self.y - 1
			self.y_dir = -1
		else:
			new_y = y
			self.y_dir = 0
		self.world.moveObj(self.id, new_x, new_y)
		self.in_action = 10

	# Called when this is attacking another Object
	def attack(self, foe):
		if not foe.is_alive:
			self.goal = None
			return
		if self.x == foe.x and self.y == foe.y:
			score = self.getAttackStrength()
			#populous.log(( self, "attacks", foe, "with score %(s)d" % {'s':score}))
			foe.defend(self, score)
			if not foe.is_alive:
				populous.log(( self, 'killed', foe))
				self.goal = None
		else :
			self.move(foe.x, foe.y)

	# Called when another is attacking me
	def defend(self, foe, f_score):
		self.state = 'fighting'
		self.goal = foe
		s_score = self.getAttackStrength()
		#populous.log(( self, "defends against", foe, "with score %(s)d" % {'s':s_score}))
		cause = "fighting"
		if f_score > s_score:
			self.wound(f_score, cause)
		elif s_score > f_score:
			foe.wound(s_score, cause)
		else:
			self.wound(f_score / 2, cause)
			foe.wound(s_score / 2, cause)
		if not foe.is_alive:
			populous.log(( self, 'killed', foe))
			self.goal = None

	def getAttackStrength(self):
		limit = self.strength * self.health / 100
		score = self.rand.randint(0, limit)
		return score

	def wound(self, score, cause=None):
		self.health -= score
		if self.health <= 0:
			self.die(cause)
		return self.is_alive

	def joinWithLeader(self):
		# if team.leader
			# get leader pos
		# else get idol pos
		# if not same pos
			# move towards leader
		#else (leader/idol).join(self)
			# (Want a bell curve probability rather than linier)
			# Up to a max of the leaders strength?
			# self.delete()
		pass

	def build(self):
		if self.x != self.goal.x or self.y != self.goal.y:
			self.move(self.goal.x,self.goal.y)
		elif not self.goal.isBuildable():
			self.decideGoal()
		else:
			house = House(self.world, self.x, self.y, self.team)
			house.join(self)
			return True

class House(PopObject):
	def __init__ (self, world, x=0, y=0, team=None):
		PopObject.__init__(self, world, x, y, team)
		self.health = 100 # percent
		self.strength = self.findStrength()
		self.growth = 0 # (growth rate depends on available land/strength)
		self.file_name = "house_%(id)d.png" % {'id': self.team.id}
		self.is_leader = False
		self.rand = populous.getRandom()
		if (self.strength > 95):
			self.size = 3
		else:
			self.size = 1

	def findStrength(self):
		# strength depends on available land max of 25 squares around the house.
		# if there are 25 squares then the house can become a castle.
		strength = 1
		# iter from pos, up to 2 levels
			# for each pos,
				# if harvestable by self()
					# add 1 to strength
					# mark havestable(self)
		strength = 9
		return strength

	def act(self):
		# All house actions are dependant on its strength.
		self.strength = self.findStrength()
		# Might be better to change strength when the land changes rather than
		# checking each house each loop iteration.
		self.grow()
		if self.growth >= 100:
			self.growth = 100
			self.spawn()
		#elif self.rand.randint(0, 100) <= 25: # 25% chance of
		#	self.spawn()
		return True

	def spawn(self):
		#populous.log( "building is spawning.", self.x, self.y, self.team)
		man = Native(self.world, self.x, self.y, self.team)
		man.strength = self.strength * (self.growth / 100)
		if self.is_leader:
			self.team.replaceLeader(self, newLeader)
		self.growth = 0
		return man

	def grow(self, strength=None):
		# populous.log( self.strength, self.growth,)
		self.growth += 1
		# populous.log( new_growth, self.growth)

	def defend(self, foe, f_score):
		self.state = 'fighting'
		self.goal = foe
		s_score = self.getAttackStrength()
		populous.log(( self, "defends against", foe, "with score %(s)d" % {'s':s_score}))
		cause = "fight"
		if f_score > s_score:
			self.wound(f_score, cause)
		elif s_score > f_score:
			foe.wound(s_score, cause)
		else:
			self.wound(f_score / 2, cause)
			foe.wound(s_score / 2, cause)
		if not foe.is_alive:
			populous.log( self, 'killed', foe)
			self.goal = None


	def getAttackStrength(self):
		limit = self.strength * self.health / 100
		score = self.rand.randint(0, limit)
		return score

	def wound(self, score, cause=None):
		self.health -= score
		if self.health <= 0:
			self.die(cause)
		return self.is_alive

	def join(self, man):
		if not isinstance(man, Native):
			return False
		elif man.team.id != self.team.id:
			raise Exception("Man joining with Another teams house.")
		elif man.is_knight:
			man.goal = None
			return False
		else:
			man_strength = man.strength + man.health
			needed_health = 100 - self.health
			if man_strength < needed_health:
				self.health += man_strength
			else:
				self.health = 100
				man_strength -= needed_health
				self.grow(man_strength)
			# take some of the man's strength/health
			# left overs can be added to growth
			was_leader = man.is_leader
			man.die("Joined with House %(house)s" % {'house':self})
			if was_leader:
				self.team.setLeader(self)

	def __repr__(self):
		s = "<%(type)s id:%(id)d H:%(health)d S:%(strength)d G:%(growth)d>" % {
		        'type':'HOUSE', 'id': self.id, 'health':self.health,
						'strength':self.strength, 'growth':self.growth }
		return s


class InHisOwnWorldError(Exception):
	pass