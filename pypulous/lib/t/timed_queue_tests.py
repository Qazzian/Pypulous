#! /usr/bin/python

import tests
import tests.poptest

import unittest


class TimedQueueNodeTest(unittest.TestCase):
	def testNew(self):
		self.assertTrue(1)


def getAllTests(suiteClass=unittest.TestSuite):
	s = unittest.makeSuite(TimedQueueNodeTest, suiteClass=suiteClass)
	s.setShortDescription("TimedQueueNodeTests")
	return s