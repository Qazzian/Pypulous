#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.object_tests.py

import poptest

import unittest
import random
import time

import populous


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


###############
# IterFromPos #
###############

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



def getAllTests(suiteClass=unittest.TestSuite):
	suite = poptest.ProveSuite()
	suite.setShortDescription("WorldTests")
	suite.addTest(unittest.makeSuite(WorldTests, suiteClass=suiteClass))
	suite.addTest(unittest.makeSuite(IterFromPosTest, suiteClass=suiteClass))
	suite.addTest(unittest.makeSuite(IterGridTests, suiteClass=suiteClass))
	return suite
