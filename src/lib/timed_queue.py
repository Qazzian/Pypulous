

class TimedQueue():
	def __init__(self, max_size=None):
		pass

	def __iter__(self):
		return self

	def next(self):
		pass

	def put(self, obj, time_delay):
		pass

	def push(self, obj, time_delay):
		pass

	def pop(self):
		pass

	def peek(self):
		pass


class TimedQueueNode():
	def __init__(self, data, scheduled_time=0):
		self.data = data
		self.scheduled_time = scheduled_time

	## TODO overwrite less than, greater than, equal etc for efficient sorting
	# just def __cmp__(self, other)
	def __cmp__(self, other): #
		return self.scheduled_time - other.scheduled_time