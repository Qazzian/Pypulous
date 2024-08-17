
import tests
import tests.poptest

from pypulous.lib.t import timed_queue_tests


def runAllTests():
	print ("Package:",__package__)

def addAllSuites(runner, suiteClass=tests.poptest.ProveSuite):
	runner.addSuite(timed_queue_tests.getAllTests(suiteClass=suiteClass))
