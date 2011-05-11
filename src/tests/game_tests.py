#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.poptest.py

import poptest

import unittest
import random
import time

import populous
import gui

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

def getAllTests(suiteClass=unittest.TestSuite):
	s = unittest.makeSuite(PopulousTest, suiteClass=suiteClass)
	s.setShortDescription("PopulousTest")
	return s