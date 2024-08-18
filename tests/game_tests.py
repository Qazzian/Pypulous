#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.poptest.py

# import tests.poptest

import unittest
import random
import time

from pypulous.populous import Populous

############
# Populous #
############

class PopulousTest(unittest.TestCase):
	def testNew(self):
		game = Populous()
		self.assertTrue(game)

	def testStartGame(self):
		game = Populous()
		game.startGame()
		self.assertEqual(len(game.teams), 3, "Default team count.")
		self.assertTrue(game.world, "No World")
		pass # check world and teams

def getAllTests(suiteClass=unittest.TestSuite):
	s = unittest.makeSuite(PopulousTest, suiteClass=suiteClass)
	s.setShortDescription("PopulousTest")
	return s