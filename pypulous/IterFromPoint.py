from pypulous.lib.random import getRandom


class IterFromPoint:
	direction_masks = [
			[-1,-1], [0,-1], [1,-1], [-1,0], [1,0], [-1,1], [0,1], [1,1]
		]

	def __init__(self, source, world, radius_limit=None):
		self.world = world
		self.radius_limit = radius_limit
		self.source = source
		self.index = 0
		self.current_radius = 0
		self.x = self.x_min = self.x_max = source.x
		self.y = self.y_min = self.y_max = source.y
		rand_index = getRandom().randint(0, len(self.direction_masks) -1)
		self.start_direction = self.direction_masks[rand_index]
		self.current_radius_start_pos = [self.x, self.y]
		#print "\n\nStart direction: ", self.start_direction, " Start location: ",self.x,',',self.y

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
		if (self.x == self.current_radius_start_pos[0] and self.y == self.current_radius_start_pos[1]):
#			print "move out: current pos ", self.x, ",",self.y
			self.current_radius += 1
			self.x_min = self.source.x - self.current_radius
			self.x_max = self.source.x + self.current_radius
			self.x += self.start_direction[0]
			self.y_min = self.source.y - self.current_radius
			self.y_max = self.source.y + self.current_radius
			self.y += self.start_direction[1]
			self.current_radius_start_pos = [self.x, self.y]
			#print "new min: ", self.x_min,',',self.y_min,' New max: ',self.x_max,',',self.y_max
			#print "new location: ",self.x,',',self.y
		if (self.y == self.y_max and self.x > self.x_min):
			self.x -= 1
			#print "x -1 on index ", self.index, " with position: ", self.x,',',self.y
		elif (self.x == self.x_min and self.y > self.y_min):
			self.y -= 1
			#print "y -1 on index ", self.index, " with position: ", self.x,',',self.y
		elif (self.y == self.y_min and self.x < self.x_max):
			self.x += 1
			#print "x +1 on index ", self.index, " with position: ", self.x,',',self.y
		elif (self.x == self.x_max and self.y < self.y_max):
			self.y += 1
			#print "y +1 on index ", self.index, " with position: ", self.x,',',self.y
		if not pos:
			pos = self.getNextPos()
		return pos

	def __iter__(self):
		return self