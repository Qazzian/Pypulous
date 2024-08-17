from objects import PopObject
from Native import Native
from lib.random import getRandom
from lib.logger import log

class House(PopObject):
	def __init__ (self, world, x=0, y=0, team=None):
		PopObject.__init__(self, world, x, y, team, "House")
		self.health = 100 # percent
		self.strength = self.findStrength()
		self.growth = 0 # (growth rate depends on available land/strength)
		self.file_name = "house_%(id)d.png" % {'id': self.team.id}
		self.is_leader = False
		self.rand = getRandom()
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
			self.team.replaceLeader(self, man)
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
		log(( self, "defends against", foe, "with score %(s)d" % {'s':s_score}))
		cause = "fight"
		if f_score > s_score:
			self.wound(f_score, cause)
		elif s_score > f_score:
			foe.wound(s_score, cause)
		else:
			self.wound(f_score / 2, cause)
			foe.wound(s_score / 2, cause)
		if not foe.is_alive:
			log( self, 'killed', foe)
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