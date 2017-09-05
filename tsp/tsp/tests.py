import unittest
from tsp import tsp 

class TestTSP(unittest.TestCase):
 
	def setUp(self):
		pass
 
	def testInitialization(self):
		with self.assertRaises(TypeError):
			tsp([[12]],'test',23.4) #tests temp
		with self.assertRaises(TypeError):
			tsp([[12]],12,'test') #tests beta
		with self.assertRaises(TypeError):
			tsp({'hi':12,'no':12},23.523,1) #tests distance matrix 
		with self.assertRaises(IndexError):
			tsp([12.2,31,2,3],1,24.3) #tests for list of lists

if __name__ == '__main__':
	unittest.main()
