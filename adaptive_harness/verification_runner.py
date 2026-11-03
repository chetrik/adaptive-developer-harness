"""Internal unittest observer, executed only by an explicitly authorized verification run.

Application tests are executable code, not sandboxed by this file. No user commands
are evaluated; the host must authorize the selected test suite and its permissions.
"""
import hashlib
import json
import sys
import unittest

class Observed(unittest.TestResult):
    def __init__(self):super().__init__();self.passed=[];self.seen=[]
    def startTest(self,test):super().startTest(test);self.seen.append(test.id())
    def addSuccess(self,test):super().addSuccess(test);self.passed.append(test.id())

def main():
    sys.path.insert(0,'.')
    suite=unittest.defaultTestLoader.discover(sys.argv[1],pattern=sys.argv[2])
    result=Observed();suite.run(result)
    payload={'count':result.testsRun,'passed':result.passed,'seen':result.seen,
        'failures':[t.id() for t,_ in result.failures], 'errors':[t.id() for t,_ in result.errors],
        'skipped':[t.id() for t,_ in result.skipped],
        'unexpected_successes':[t.id() for t in result.unexpectedSuccesses],
        'expected_failures':[t.id() for t,_ in result.expectedFailures],
        'failure_digest':hashlib.sha256(''.join(s for _,s in result.failures+result.errors).encode()).hexdigest()}
    print('\n_ADH_TEST_RESULT_'+json.dumps(payload),flush=True)
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
