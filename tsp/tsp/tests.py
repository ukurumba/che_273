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
			tsp([12.2,31,2,3],1,24.3) #tests for list of 

	def testRandomPath(self):
		tsp1 = tsp([[12,13,14],[12,121,2],[1,2,3]],12,13)
		path = tsp1.generate_random_path()
		self.assertTrue(len(path) == 4 and path[0] == path[-1])

	def test_calc_cost(self):
		tsp1 = tsp1 = tsp([[12,13,14],[12,121,2],[1,2,3]],12,13)
		path = [0,1,2,0]
		self.assertEqual(tsp1.calc_cost(path=path),16)

	def test_choose_nodes(self):
		tspA = tsp([[12,13,14],[12,121,2],[1,2,3]],12,13)
		tspA.path = tspA.generate_random_path()
		node1,node2 = tspA.choose_nodes()
		truth = (node1==0 or node1 == 1 or node1 == 2) and (node2 == 0 or node2 == 1 or node2 == 2) and (node1 != node2)
		self.assertTrue(truth)

	def test_modify_path_first_node(self):

		tsp1 = tsp([[1,2,3,4],[5,6,7,8],[9,10,11,12],[200,14,15,16]],12,13)
		init_cost = 2 + 7 + 12 + 200
		tsp1.path = [0,1,2,3,0]
		nodes = (0,1)
		tsp1.cost = tsp1.calc_cost()

		tsp1.modify_path(nodes)
		new_cost = 5 + 3 + 12 + 14
		self.assertEqual(tsp1.cost, new_cost)
		self.assertEqual(tsp1.path,[1,0,2,3,1])


		tsp1 = tsp([[1,2,3,4],[5,6,7,8],[9,10,11,12],[200,14,15,16]],12,13)
		init_cost = 2 + 7 + 12 + 200
		tsp1.path = [0,1,2,3,0]
		nodes = (1,0)
		tsp1.cost = tsp1.calc_cost()

		tsp1.modify_path(nodes)
		new_cost = 5 + 3 + 12 + 14
		self.assertEqual(tsp1.cost, new_cost)
		self.assertEqual(tsp1.path,[1,0,2,3,1])

	def test_modify_path_interior_nodes(self):
		tsp1 = tsp([[1,2,3,4],[5,6,300,8],[9,10,11,12],[13,14,15,16]],12,13)
		init_cost = 2 + 300 + 12 + 13
		tsp1.path = [0,1,2,3,0]
		nodes = (1,2)
		tsp1.cost = tsp1.calc_cost()
		self.assertEqual(init_cost,tsp1.cost)

		tsp1.modify_path(nodes)
		new_cost = 3 + 10 + 8 + 13
		self.assertEqual(tsp1.cost, new_cost)
		self.assertEqual(tsp1.path,[0,2,1,3,0])



		




if __name__ == '__main__':
	unittest.main()
