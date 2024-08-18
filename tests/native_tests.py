#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.object_tests.py

import unittest
import random
import time

from pypulous.Native import Native
from pypulous.populous import Populous
from pypulous.Buildings import House

from pypulous.objects import PopObject, Idol

##########
# Native #
##########

class NativeTest(unittest.TestCase):
	def setUp(self):
		self.game = Populous()
		self.game.startGame()
		self.world = self.game.world
		self.teams = self.game.teams

	def testNew(self):
		man = Native(self.world, team=self.teams[1])
		self.assertTrue(man)
		self.assertEqual((man.x, man.y, man.strength, man.health), (0, 0, 1, 100))

	def setupWorld(self):
		world = self.world
		team1 = self.teams[1]
		team2 = self.teams[2]
		man1 = Native(world, 0, 1, team1)
		home1 = House(world, 0, 0, team1)
		idol1 = Idol(world, 4, 3, team1)
		# Team 2
		man2 = Native(world, world.width-1, world.height-2, team2)
		home2 = House(world, world.width-1, world.height-1, team2)
		idol2 = Idol(world, world.width-5, world.height-3, team2)
		return (man1, home1, idol1) , (man2, home2, idol2)

	def testFindNearestEnemy(self):
		(t1, t2) = self.setupWorld()
		foe = t1[0].findNearestEnemy()
		#print self.world
		#print t1, t2
		self.assertTrue(t1[0].matchEnemy(t2[0]), "matchEnemy not working")
		self.assertTrue(foe, "Cannot find any enemies")

	"""
	How does this work?
	1) decide based on team goals.
		a. team goal = build
		b. team goal = fight
		c. team goal = leader
			i. I am leader = decide my self
			ii. team has leader = find leader
			iii. team does not have leader = find idol
		d. else decide for myself.
	2) decide for my self
		for pos in iterFromPos(no_limit)
			a. if has enemy: goal = fight enemy
			b. if is buildable: goal = build on pos

	"""
	def testDecideGoal(self):
		house = House(self.world, self.game.world_width -2, self.game.world_height -2, self.teams[2])
		man = Native(self.world, self.game.world_width-1, self.game.world_height-1, self.teams[1])
		goal = man.decideOwnGoal()
		self.assertTrue(goal, "Native can't decide what to do")
		self.assertEqual(goal, house, "Native found unexpected goal.")



def getAllTests(suiteClass=unittest.TestSuite):
	s = unittest.makeSuite(NativeTest, suiteClass=suiteClass)
	s.setShortDescription("NativeTest")
	return s
