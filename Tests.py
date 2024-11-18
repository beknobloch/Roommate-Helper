import unittest

class Test(unittest.TestCase):
    
    def testCase1(self):
        self.assertTrue(True)

if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()