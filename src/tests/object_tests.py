#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.object_tests.py

import poptest

import unittest
import random
import time

import populous
import objects

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


def getAllTests(suiteClass=unittest.TestSuite):
	s = unittest.makeSuite(PopObjectTest, suiteClass=suiteClass)
	s.setShortDescription("PopObjectTest")
	return s