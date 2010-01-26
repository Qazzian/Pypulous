from threading import Thread
from time import sleep

pop_main_menu = [
	{ 'name' : "Start Game", 'function' : 'start' },
	{ 'name' : "Fibonacci", 'function' : 'do_fib'},
	{ 'name' : "Pickle", 'function' : 'do_pickle' },
	{ 'name' : "Quit", 'function' : 'quit' }
]

class PopUI:
		def __init__(self, commQueue):
			self.comms = commQueue
			self.main_menu = Menu(pop_main_menu)

		def getCommand(self):
			option = self.main_menu.doMenu()
			if 0 <= option < len(pop_main_menu):
				self.comms.put(pop_main_menu[option]['function'])
			else:
				self.main_menu.setError('NotRecognised')
				option = 'Error'


class Menu():
	"""A functional menu for consol use.

	Takes a list of options and prints them to the screen	Then askes for the user
	to choose what to do, calling the function associated with the option.
	Options should be passed as a list of dictonaries. Each  dictonary must
	contain the keys 'name' which will be printed in the menu, and 'function'
	which will be called when the user selects that option.
	Options are printed to the screen in the order found.
	USers select options by index value of the option.
	-1 is used to return from the menu function.	"""
	messages = {
		'Generic' : "There was an error with your command",
		'NotRecognised' : "The command was not recognised.",
		'InvalidInput' : "Please enter the number in front of your chosen option."
	}

	def __init__(self, menu_entries):
		self.name = "\nMenu"
		self.prompt = "Enter your choice: "
		self.error_message = ''
		self.menu_entries = menu_entries

	def printMenu(self):
		print self.name
		for i, v in enumerate(self.menu_entries):
			# py <= 2.5
			print "%(index)3d. %(name)s" % { 'index':i, 'name':v['name'] }
			# py >= 2.6
			#print "{0:3}. {1}".format(i, v['name])

	def getInput(self):
		try:
			user_choice = int(raw_input(self.prompt))
		except ValueError:
			user_choice = len(self.menu_entries)
		except KeyboardInterrupt:
			user_choice = -1
		return user_choice

	def doMenu(self):
		self.printErrorMessage()
		self.printMenu()
		return self.getInput()

	def printErrorMessage(self):
		if self.error_message:
			print self.error_message
			self.error_message = ''

	def setError(self, error):
		if (Menu.messages[error]):
			self.error_message = Menu.messages[error]
		else:
			self.error_message = Menu.messages['Generic']

class UIThread (Thread):
	def __init__(self, commQueue, delay):
		Thread.__init__(self)
		self.cq = commQueue
		self.ui = PopUI(cq)
		self.delay = delay
		self.die = False

	def run(self):
		while not self.die:
			self.ui.getCommand()
			sleep(self.delay)
		if __name__ == '__main__':
			print 'Exiting ui thread'

	def exit(self):
		self.die = True

if __name__ == '__main__':
	import Queue
	class QueueReader(Thread):
		def __init__(self, commQueue):
			Thread.__init__(self)
			self.cq = commQueue
			self.die = False

		def run(self):
			while not self.die:
				try:
					command = self.cq.get()
					self.cq.task_done()
					print command
				except Queue.Empty:
					print 'Nothing to do.'
				else:
					if command == 'quit':
						self.exit()

		def exit(self):
			self.die = True

	cq = Queue.Queue()
	ui = UIThread(cq, 0.2)
	qr = QueueReader(cq)
	ui.start()
	qr.start()
	qr.join()
	ui.exit()
