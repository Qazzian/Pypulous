#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.object_tests.py

import poptest

import unittest
import random
import time

import populous
import objects


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


def getAllTests(suiteClass=unittest.TestSuite):
	s = unittest.makeSuite(HouseTest, suiteClass=suiteClass)
	s.setShortDescription("HouseTest")
	return s



