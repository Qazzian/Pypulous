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