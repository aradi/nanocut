import unittest
import test_nanocut

runner = unittest.TextTestRunner()
runner.run(unittest.TestSuite(test_nanocut.getsuites()))
