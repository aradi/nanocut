import unittest
import numpy as np
import glob
import subprocess

class NanocutTestCase(unittest.TestCase):

    _tests = []

    def errormsg(self, filename, line):
        return "ERROR in File: '" + filename + "' in line " + str(line)

    def testTags(self):
        for filename in self._tests:
            print(filename)
            subprocess.call([ "python", "../bin/nanocut", "--verbosity", "0",
                             filename, "current_result.xyz" ])
            result_file = open("current_result.xyz", "r")
            result = result_file.readlines()
            orig_file = open(filename[:-4] + ".xyz", "r")
            orig = orig_file.readlines()
            ii = 0
            for ii in range(len(orig)):
                origwords = orig[ii].split()
                resultwords = result[ii].split()                
                if ii == 0:
                    self.assertEqual(len(resultwords), 1)
                    self.assertEqual(int(origwords[0]), int(resultwords[0]))
                elif ii > 1:
                    self.assertEqual(len(resultwords), 4)
                    self.assertEqual(origwords[0].lower(),
                                     resultwords[0].lower())
                    origcoords = np.array(origwords[1:4], dtype=float)
                    resultcoords = np.array(resultwords[1:4], dtype=float)
                    diff = np.sqrt(np.sum((origcoords - resultcoords)**2))
                    self.assertTrue(diff < 1e-8, self.errormsg(filename, ii))

class SimpleTestCase(NanocutTestCase):
    _tests = glob.glob("nanocut/*.ini")

def getsuites():
    """Returns the test suites defined in the module."""
    return [ unittest.makeSuite(SimpleTestCase, 'test')]

if __name__ == "__main__": 
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestSuite(getsuites()))
