import pygame
import populous
# from Buildings import House
from objects import PopObject
from lib.random import getRandom, getRandomPercent
from lib.logger import log

class Native(PopObject):
	def __init__ (self, world, x=0, y=0, team=None):
		self.health = 100 # percent
		self.strength = 1 # max 100 except the leader and knights
		self.is_leader = False
		self.is_knight = False
		PopObject.__init__(self, world, x, y, team, "Native")
		self.team_goal = None  # A text field.
		self.goal = None       # A grid square or PopObject to aim for
		self.in_action = 0     # Number of ticks for action to compleate
		self.rand = getRandom()
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
		log(self, "has found goal", self.goal, "\n")

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
			log( "Native", self.id, self.x, self.y, "Has no Team")
		if self.team_goal != self.team.goal:
			self.team_goal = self.team.goal
			return False
			#log( "changed goal to", self.goal)
		else: return True

	def checkMyGoal(self):
		"""Ensures that the curent goal is still valid. Returns False if not."""
		if self.goal == None:
			#log( "There is no goal")
			return False
		#if not self.checkTeamGoal():
			#log( "team goal is bad")
			#return False
		if isinstance(self.goal, PopObject):
			if not self.goal.is_alive:
				#log( "Goal has died")
				return False
		if isinstance(self.goal, populous.GridSqr):
			if not self.goal.isBuildable():
				#log( "Goal no longer buildable")
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
			#log( "need a new goal")
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
		if (isinstance(obj, PopObject) or isinstance(obj, Native)) and obj.team.id != self.team.id:
			return True

	def findNearestEnemyHouse(self):
		def matchEnemyHouse(obj):
			if isinstance(obj, PopObject) and obj.team.id != self.team.id:
				return True
		return self.world.findNearestObjFromFunction(self, matchEnemyHouse)

	def isNearEnemy(self):
		pos = self.getPos()
		my_enemy = pos.hasEnemy(self)
		attack_chance = getRandomPercent()
		if (my_enemy and attack_chance > 10):
			return my_enemy
		else:
			for xy in self.world.getAjoiningPos(pos.x, pos.y):
				my_enemy = xy.hasEnemy(self)
				attack_chance = getRandomPercent()
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
			#log(( self, "attacks", foe, "with score %(s)d" % {'s':score}))
			foe.defend(self, score)
			if not foe.is_alive:
				log(( self, 'killed', foe))
				self.goal = None
		else :
			self.move(foe.x, foe.y)

	# Called when another is attacking me
	def defend(self, foe, f_score):
		self.state = 'fighting'
		self.goal = foe
		s_score = self.getAttackStrength()
		#log(( self, "defends against", foe, "with score %(s)d" % {'s':s_score}))
		cause = "fighting"
		if f_score > s_score:
			self.wound(f_score, cause)
		elif s_score > f_score:
			foe.wound(s_score, cause)
		else:
			self.wound(f_score / 2, cause)
			foe.wound(s_score / 2, cause)
		if not foe.is_alive:
			log(( self, 'killed', foe))
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
			pygame.event.post(pygame.event.Event("build_house", {"x": self.x, "y": self.y, "team": self.team}))
			pygame.event.post(pygame.event.Event("join_house", {"native": self}))
			# house = House(self.world, self.x, self.y, self.team)
			# house.join(self)
			return True