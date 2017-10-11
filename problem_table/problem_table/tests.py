import unittest
from problem_table import problem_table,stream

class TestTSP(unittest.TestCase):
 	

	def setUp(self):
		pass

	def test_stream(self):
		S1 = stream(100,150,2)
		self.assertTrue(S1.type == "Cold")
		self.assertTrue(S1.shifted_Ts== 105)

	def test_problem_table(self):
		S1 = stream(20,135,2)
		S2 = stream(170,60,3)
		S3 = stream(80,140,4)
		S4 = stream(150,30,1.5)
		pt = problem_table([S1,S2,S3,S4])
		Qc,Qh,pinch = pt.calc_vals()
		self.assertEqual(Qc,60)
		self.assertEqual(Qh,20)
		self.assertEqual(pinch,85)

	
 





		




if __name__ == '__main__':
	unittest.main()
