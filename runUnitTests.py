#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tests import poptest, game_tests, world_tests, object_tests, house_tests, native_tests

from pypulous.lib.t import runtests

def runSingle(test_name):
	pass

def runAllTests():
	runner = poptest.SuiteRunner()
	addAllSuites(runner)
	results = runner.run()
	return results

def addAllSuites(runner):
	""" Create a list of poptest.ProveSuite's """
	runner.addSuite(game_tests.getAllTests(suiteClass=poptest.ProveSuite))
	runner.addSuite(world_tests.getAllTests(suiteClass=poptest.ProveSuite))
	runner.addSuite(object_tests.getAllTests(suiteClass=poptest.ProveSuite))
	runner.addSuite(house_tests.getAllTests(suiteClass=poptest.ProveSuite))
	runner.addSuite(native_tests.getAllTests(suiteClass=poptest.ProveSuite))
	runtests.addAllSuites(runner, suiteClass=poptest.ProveSuite)


if __name__ == '__main__':
	import sys
	print("ARGS: ",len(sys.argv))
	if len(sys.argv) > 1:
		runSingle(sys.argv[1])
	else:
		runAllTests()