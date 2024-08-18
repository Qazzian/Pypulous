from pypulous.lib.logger import log

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
		# TODO these checks should not be inside the gridSquare
		# if isinstance(obj, PopObject):
		# 	if isinstance(obj, House):
		# 		if self.hasHouse():
		# 			raise Exception("Position already has a house! %(self)s" % {'self':self})
		# 		self.builders = dict() # clear list of builders.
		self.objects[obj.id] = obj
		# else:
		# 	s = "Object %(type)s is not a subclass of PopObject " % {'type':obj.__class__}
		# 	raise TypeError(s)

	def remove(self, obj):
		# TODO: fix me.
		removed_obj = self.objects.pop(obj.id)
		log(( "removed", removed_obj, "From Grid %d,%d" % (self.x, self.y)))
		log("Now has objects: ", self.inspect())
		return removed_obj

	def targeted(self, native):
		""" Record who's trying to get here by team
			Want to make natives from the same team don't all go for the same place."""
		pass

	# def isBuildable(self):
	# 	if self.hasHouse():
	# 		return False
	# 	else:
	# 		for neighbours in self.world.getAjoiningPos(self.x, self.y):
	# 			if neighbours.hasHouse():
	# 				return False
	# 	return True

	# def hasHouse(self):
	# 	for i in self.objects:
	# 		if isinstance(self.objects[i], House):
	# 			return self.objects[i]
	# 	return False

	# def hasEnemy(self, native):
	# 	for i in self.objects:
	# 		if isinstance(self.objects[i], Native) and self.objects[i].isEnemy(native):
	# 			return self.objects[i]
	# 		if isinstance(self.objects[i], House) and self.objects[i].isEnemy(native):
	# 			return self.objects[i]
	# 	return False

	def inspect(self):
		s = self.__repr__() + "\n"
		for o in self.objects:
			s += self.objects[o].__repr__() + "\n"
		return s