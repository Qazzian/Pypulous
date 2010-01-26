# poptest.py

import populous
import gui
import unittest
import random
import time


############
# Populous #
############

class PopulousTest(unittest.TestCase):
	def testNew(self):
		game = populous.Populous()
		self.assertTrue(game)

	def testStartGame(self):
		game = populous.Populous()
		game.startGame()
		self.assertEqual(len(game.teams), 3, "Default team count.")
		self.assertTrue(game.world, "No World")
		pass # check world and teams


#############
# PopObject #
#############

class PopObjectTest(unittest.TestCase):
	def setUp(self):
		self.game = populous.Populous()
		self.game.startGame()
		self.world = self.game.world
		self.teams = self.game.teams

	def tearDown(self):
		del(self.game)

	def testNew(self):
		obj = populous.PopObject(self.world, team=self.teams[0])
		self.assertTrue(obj, "Could not create PopObject.")

	def testGetPos(self):
		obj = populous.PopObject(self.world, team=self.teams[0])
		pos = obj.getPos()
		self.assertTrue(pos, "Could not get Objects Position.")
		self.assertEqual((pos.x, pos.y), (obj.x, obj.y), "Returned Position does not match objects x,y co-ords.")

	def testAct(self):
		obj = populous.PopObject(self.world, team=self.teams[0])
		self.failIf(obj.act(), "standard objects should not act.")

	def testDie(self):
		obj = populous.PopObject(self.world, team=self.teams[0])
		self.failUnless(obj.is_alive, "Objects should start alive.")
		obj.die("test")
		self.assertEqual((obj.is_alive, obj.killed_by), (False, "test"), "Object refused to die.")


#########
# World #
#########

class WorldTests(unittest.TestCase):
	def setUp(self):
		self.world_width = 15
		self.world_height = 10
		self.random = random.Random()
		self.team = populous.Team()
		pass

	def tearDown(self):
		pass

	def testNew(self):
		world = populous.World(width=self.world_width, height=self.world_height)
		self.assertEqual((self.world_width, self.world_height), (world.width, world.height))
		grid_y = len(world.grid)
		grid_x = len(world.grid[0])
		self.assertEqual((self.world_width, self.world_height), (grid_x, grid_y ))

	def testGetPos(self):
		world = populous.World(width=self.world_width, height=self.world_height)
		for i in range(self.random.randint(0, self.world_width)):
			rand_x = self.random.randint(0, self.world_width-1)
			rand_y = self.random.randint(0, self.world_height-1)
			pos = world.getPos(rand_x, rand_y)
			self.assertEqual((pos.x, pos.y), (rand_x, rand_y))
		# TODO: test no index errors
		x, y = -1, -1
		pos1 = world.getPos(x, y)
		self.assertEqual(pos1, None)
		x, y = self.world_width, self.world_height
		pos2 = world.getPos(x, y)
		self.assertEqual(pos2, None)

	def testGetAjoiningPos(self):
		world = populous.World(width=self.world_width, height=self.world_height)
		posList = world.getAjoiningPos(0, 0) # Test the corner
		self.assertEqual(len(posList), 3)
		posList = world.getAjoiningPos(1, 1) # middle
		self.assertEqual(len(posList), 8)
		posList = world.getAjoiningPos(1, 0) # side
		self.assertEqual(len(posList), 5)
		# far corner
		posList = world.getAjoiningPos(self.world_width-1, self.world_height-1)
		self.assertEqual(len(posList), 3)
		# 1 over the corner
		posList = world.getAjoiningPos(self.world_width, self.world_height)
		self.assertEqual(len(posList), 1)
		# out of range
		posList = world.getAjoiningPos(self.world_width + 3, self.world_height + 3)
		self.assertEqual(len(posList), 0)

	def testAddObject(self):
		pass

	def testGetObjFromID(self):
		pass

	# TODO: Try with a range of objects and distances.
	def testClosest(self):
		world = populous.World(width=self.world_width, height=self.world_height)
		source = populous.PopObject(x=3, y=3, world=world, team=self.team)
		a = populous.PopObject(x=2, y=-2, world=world, team=self.team)
		b = populous.PopObject(x=1, y=1, world=world, team=self.team)
		result = world.closest(source, a, b)
		self.assertTrue(result, "World.closest returned nothing.")
		self.assertEqual((result.x, result.y), (2, -2), "World.closest returned incorrect result.")

	def testFindNearestObjFromFunction(self):
		pass

class IterFromPosTest(unittest.TestCase):
	def setUp(self):
		self.game = populous.Populous()
		self.game.world_width = 10
		self.game.world_height = 10
		self.game.startGame()
		self.world = self.game.world
		self.teams = self.game.teams

	def doLoop(self, source, limit=None):
		count = 0
		for p in populous.IterFromPoint(source, self.world, limit):
			self.assertTrue(p)
			# print p.x, p.y
			count += 1
		return count

	def testRadiusLimit(self):
		pos = self.world.getPos(self.world.width / 2, self.world.height / 2)
		#print self.world.width, self.world.height, ':', pos.x, pos.y
		count = self.doLoop(pos, limit=1)
		self.assertEqual(count, 9)
		count = self.doLoop(pos, limit=2)
		self.assertEqual(count, 25)
		# test 1 away from the edge with limit 2
		pos = self.world.getPos(1, 2)
		count = self.doLoop(pos, limit=2)
		self.assertEqual(count, 20)

	def testFrom00(self):
		pos = self.world.getPos(0, 0)
		count = self.doLoop(pos, 1)
		self.assertEqual(count, 4)
		count = self.doLoop(pos)
		self.assertEqual(count, self.world.width * self.world.height)

	def testFromMid(self):
		pos = self.world.getPos(self.world.width / 2, self.world.height / 2)
		count = self.doLoop(pos)
		self.assertEqual(count, self.world.width * self.world.height)

	def testFromEnd(self):
		pos = self.world.getPos(self.world.width - 1, self.world.height - 1)
		count = self.doLoop(pos, 1)
		self.assertEqual(count, 4)
		count = self.doLoop(pos)
		self.assertEqual(count, self.world.width * self.world.height)

	def testEdge(self):
		pos = self.world.getPos(self.world.width - 1, self.world.height / 2)
		count = self.doLoop(pos, 1)
		self.assertEqual(count, 6)
		count = self.doLoop(pos)
		self.assertEqual(count, self.world.width * self.world.height)

############
# IterGrid #
############

class IterGridTests(unittest.TestCase):
	def setUp(self):
		self.game = populous.Populous()
		self.game.world_width = 10
		self.game.world_height = 10
		self.game.startGame()
		self.world = self.game.world
		self.teams = self.game.teams

	def testNew(self):
		my_iter = populous.IterGrid(self.world)
		count = 0
		self.assertTrue(my_iter, "Cannot make IterGrid object.")
		#print dir(my_iter)
		for i in my_iter:
			count += 1
		self.assertEqual(count, self.world.width * self.world.height, "Iter count does not match pos count.")


##########
# Native #
##########

class NativeTest(unittest.TestCase):
	def setUp(self):
		self.game = populous.Populous()
		self.game.startGame()
		self.world = self.game.world
		self.teams = self.game.teams

	def testNew(self):
		man = populous.Native(self.world, team=self.teams[1])
		self.assertTrue(man)
		self.assertEqual((man.x, man.y, man.strength, man.health), (0, 0, 1, 100))

	def setupWorld(self):
		world = self.world
		team1 = self.teams[1]
		team2 = self.teams[2]
		man1 = populous.Native(world, 0, 1, team1)
		home1 = populous.House(world, 0, 0, team1)
		idol1 = populous.Idol(world, 4, 3, team1)
		# Team 2
		man2 = populous.Native(world, world.width-1, world.height-2, team2)
		home2 = populous.House(world, world.width-1, world.height-1, team2)
		idol2 = populous.Idol(world, world.width-5, world.height-3, team2)
		return (man1, home1, idol1) , (man2, home2, idol2)

	def testFindNearestEnemy(self):
		(t1, t2) = self.setupWorld()
		foe = t1[0].findNearestEnemy()
		#print self.world
		#print t1, t2
		self.assertTrue(t1[0].matchEnemy(t2[0]), "matchEnemy not working")
		self.assertTrue(foe, "Cannot find any enemies")

	def notestDecideGoal(self):
		for p in populous.IterGrid(self.world):
			populous.House(self.world, p.x, p.y, self.teams[2])
		man = Native(self.world, p.x, p.y, self.teams[1])
		# TODO: Make the man kill a house
		# Look at the position with the killed house.
		# See if you can make the man build in the empty space.



#########
# House #
#########

class HouseTest(unittest.TestCase):
	def setUp(self):
		self.game = populous.Populous()
		self.game.startGame()
		self.world = self.game.world
		self.teams = self.game.teams

	def testNew(self):
		house = populous.House(self.world, team=self.teams[0])
		self.assertTrue(house)
		self.assertEqual((house.x, house.y, house.strength, house.health, house.growth), (0, 0, house.findStrength(), 100, 0))

	def testGrowth(self):
		house = populous.House(self.world, team=self.teams[0])
		house.strength = 16
		g1 = house.growth
		house.grow()
		g2 = house.growth
		self.assertTrue(g2 > g1, "House has not grown.")

	def testSpawn(self):
		house = populous.House(self.world, team=self.teams[0])
		house.growth = 100
		house.strength = 100
		man = house.spawn()
		self.assertTrue(man, "House did not spawn a man.")
		self.assertEqual(man.strength, house.strength, "House Strength not passed on to Man.")

	def testAct(self):
		house = populous.House(self.world, team=self.teams[0])
		obj_no = obj_no2 = len(self.world.objects)
		#print obj_no, '-', house.strength
		man = None
		while obj_no2 <= obj_no:
			house.act()
			obj_no2 = len(self.world.objects)
			#print obj_no2, ':', house.growth
		self.assertTrue(True, "House doesn't know ow to act.")

	def testFight(self):
		house = populous.House(self.world, team=self.teams[0])
		foe = populous.Native(self.world, house.x, house.y, self.teams[0])
		#print house.strength, house.health, foe.strength, foe.health
		house.defend(foe, 10)
		#print foe.health, house.health
		self.assertEqual(house.health, 90)

	def testWound(self):
		house = populous.House(self.world, team=self.teams[0])
		house.wound(50, "testing")
		self.assertEqual(house.health, 50)
		house.wound(51, "testing")
		self.assertFalse(house.is_alive)

#########
# Suite #
#########

def test_suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(PopulousTest))
	suite.addTest(unittest.makeSuite(WorldTests))
	suite.addTest(unittest.makeSuite(PopObjectTest))
	suite.addTest(unittest.makeSuite(IterFromPosTest))
	suite.addTest(unittest.makeSuite(IterGridTests))
	suite.addTest(unittest.makeSuite(HouseTest))
	suite.addTest(unittest.makeSuite(NativeTest))

	return suite

if __name__ == '__main__':
	unittest.main(defaultTest='test_suite')


