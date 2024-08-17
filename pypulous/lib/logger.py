

DEBUG = True

def log(msg, *args):
	if DEBUG:
		print (msg)
		for i in args:
			print (i)
	pass