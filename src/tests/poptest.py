#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.poptest.py

import unittest

import sys

class ProveSuite(unittest.TestSuite):
	def __init__(self, tests=(), name=None):
		unittest.TestSuite.__init__(self, tests)
		self._name = name

	def setShortDescription(self, desc):
		self._name = desc

	def getShortDescription(self):
		return self._name or self.__repr__()

	def __repr__(self):
		 return "<%s tests:%d>" % (self.__class__, self.countTestCases())

class ProveTextResult(unittest.TestResult):
	""" Test Result class to print test results based on a suite level

	Create a single result object per ProveSuite passing the output stream, suite description,
	and the verbosity.
	"""
	def __init__(self, stream, description, verbosity=1):
		""" Create a ProveTextRunner instance"""
		self.description = description
		self.stream = stream
		self.verbosity = verbosity


class SuiteRunner():

	def __init__(self, stream=sys.stderr):
		self.suites = []
		self.results = []
		self.tests_ran = 0
		self.passed = 0
		self.failed = 0
		self.errors = 0
		self.stream = stream

	def run(self):
		self.runAllSuites()

	def addSuite(self, suite=None, suites=None):
		if (suite != None):
			self.suites.append(suite)
		if (suites != None):
			self.suites.extend(suites)

	def runAllSuites(self):
		for suite in self.suites:
			result = self.makeResult()
			suite.run(result)
			self.results.append(result)
			self.printResult(result, suite)
		self.print_summery()
		return self.results

	def makeResult(self):
		""" Overload this method to use your own TestResult Class. """
		return unittest.TestResult()

	def printResult(self, result, suite):
		suite_name = suite.getShortDescription()
		test_count = result.testsRun
		tests_passed = test_count - (len(result.failures) + len(result.errors))
		pass_str = (test_count == tests_passed) and 'OK' or 'Fail'
		# update running totals
		self.tests_ran = self.tests_ran + test_count
		self.passed = self.passed + tests_passed
		self.failed = self.failed + len(result.failures)
		self.errors = self.errors + len(result.errors)
		# Print result
		result_str = "%s... %d/%d --- %s\n" % (suite_name, test_count, tests_passed, pass_str)
		self.stream.write(result_str)
		return result_str

	def print_summery(self):
		summery_str = 'TESTS=%d, PASSED=%d, FAILED=%d, ERRORS=%d\n' % (self.tests_ran, self.passed, self.failed, self.errors)

		if (self.tests_ran == 0):
			result_str = 'NOTESTS'
		elif (self.passed == self.tests_ran):
			result_str = 'PASSED'
		else:
			result_str = 'FAILED'

		summery_str = "%sResult:%s\n" % (summery_str, result_str)
		self.stream.write(summery_str)
		return summery_str


def runAllTests():
	runner = SuiteRunner()
	addAllSuites(runner)
	results = runner.run()
	return results

def addAllSuites(runner):
	""" Create a list of poptest.ProveSuite's """
	runner.addSuite(game_tests.getAllTests(suiteClass=ProveSuite))
	runner.addSuite(world_tests.getAllTests(suiteClass=ProveSuite))
	runner.addSuite(object_tests.getAllTests(suiteClass=ProveSuite))
	runner.addSuite(house_tests.getAllTests(suiteClass=ProveSuite))
	runner.addSuite(native_tests.getAllTests(suiteClass=ProveSuite))

