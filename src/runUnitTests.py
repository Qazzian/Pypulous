#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tests
from tests import poptest, game_tests, world_tests, object_tests, house_tests, native_tests

import lib
import lib.t
import lib.t.runtests

def runAllTests():
	runner = tests.poptest.SuiteRunner()
	addAllSuites(runner)
	results = runner.run()
	return results

def addAllSuites(runner):
	""" Create a list of poptest.ProveSuite's """
	runner.addSuite(tests.game_tests.getAllTests(suiteClass=tests.poptest.ProveSuite))
	runner.addSuite(tests.world_tests.getAllTests(suiteClass=tests.poptest.ProveSuite))
	runner.addSuite(tests.object_tests.getAllTests(suiteClass=tests.poptest.ProveSuite))
	runner.addSuite(tests.house_tests.getAllTests(suiteClass=tests.poptest.ProveSuite))
	runner.addSuite(tests.native_tests.getAllTests(suiteClass=tests.poptest.ProveSuite))
	lib.t.runtests.addAllSuites(runner, suiteClass=tests.poptest.ProveSuite)



if __name__ == '__main__':
	runAllTests()
	#lib.t.runtests.runAllTests()