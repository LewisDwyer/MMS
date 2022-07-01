import unittest
from nextSmallestNumber import nextSmallest
import random
import time
#Test arrays
arr = [ 3, 4, 6, 10, 12, 14, 15, 17, 19, 21, 22 ]

arr2 = [random.randrange(-32768, 32768) for i in range(32768)]
arr2.sort()

class TestNextSmallestBasic(unittest.TestCase):
    
    def test_given(self):
        result = nextSmallest(arr, 12)
        self.assertEqual(12, 12)

    def test_given2(self):
        result = nextSmallest(arr, 13)
        self.assertEqual(result, 12)

    def test_error(self):
        result = nextSmallest(arr, "asd")
        self.assertEqual(result, -1)

    def test_max (self):
        result = nextSmallest(arr, 23)
        self.assertEqual(result, 22)
        
    def test_time (self):
        x = random.randrange(-32768, 32768)
        start_time = time.time()
        result = nextSmallest(arr2, x)
        print(result)
       


if __name__ == '__main__':
    t = unittest.TestLoader().loadTestsFromTestCase(TestNextSmallestBasic)
    unittest.TextTestRunner(verbosity=2).run(t)