import random

def getRandom():
	rand = random.Random()
	rand.seed = 10
	return rand

def getRandomPercent():
	return getRandom().randint(0, 100)
