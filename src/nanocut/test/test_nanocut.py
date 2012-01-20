import unittest
import io
import numpy
import glob
import subprocess

class NanocutTestCase(unittest.TestCase):

    _tests = []

    def errormsg(self, filename, line):
        return "ERROR in File: " + filename + " in line: " + str(line)

    def testTags(self):
        for filename in self._tests:
            print(filename)
            subprocess.call(["python", "../../../bin/nanocut", "-w", "current_result.dat", filename])
            result_file = open('current_result.dat', 'r')
            result = result_file.readlines()
            orig_file = open(filename+'.dat','r')
            orig_content = orig_file.readlines()
            ii = 0
            for line in orig_content:
                line_split = line.split(' ')
                result_line = result[ii]
                if ii != 0 and ii != 1:
                    result_line_split = result_line.split()
                    result_line_split = [x for x in result_line_split if len(x) > 0]
                    line_split = [x for x in line_split if len(x) > 0]
                    for jj in range(len(result_line_split)):
                        result_line_split[jj] = result_line_split[jj].strip()
                    for jj in range(len(line_split)):
                        line_split[jj] = line_split[jj].strip()
                    self.assertEqual(result_line_split[0], line_split[0], self.errormsg(filename, ii))
                    for coord_index in range(1,4):
                        if(numpy.abs(float(result_line_split[coord_index])) < 10E-8):
                            diff = float(result_line_split[coord_index]) - float(line_split[coord_index])
                            self.assertTrue(diff < 10E-8, self.errormsg(filename, ii))
                        else:
                            diff = (float(result_line_split[coord_index]) - float(line_split[coord_index]))/(float(result_line_split[coord_index]))
                            self.assertTrue(numpy.abs(diff) < 10E-2, self.errormsg(filename, ii))
                elif (ii==0):
                    self.assertTrue(result_line == line)
                else:
                    pass
                ii = ii + 1
class SimpleTestCase(NanocutTestCase):
    _tests = glob.glob("orig_results/*.ini")

def getsuites():
    """Returns the test suites defined in the module."""
    return [ unittest.makeSuite(SimpleTestCase, 'test')]

if __name__ == "__main__": 
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestSuite(getsuites()))
