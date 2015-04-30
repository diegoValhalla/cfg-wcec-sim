import sys
sys.path[0:0] = ['.', '..']

import unittest


suite = unittest.TestLoader().loadTestsFromNames(
    [
        'test_simple_case'
    ]
)

testresult = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if testresult.wasSuccessful() else 1)


