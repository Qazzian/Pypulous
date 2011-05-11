
import tests
import tests.poptest

import lib
import lib.t

from lib.t import timed_queue_tests


def runAllTests():
	print "Package:",__package__

def addAllSuites(runner, suiteClass=tests.poptest.ProveSuite):
	runner.addSuite(lib.t.timed_queue_tests.getAllTests(suiteClass=suiteClass))
