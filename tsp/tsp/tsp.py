import random
import math
class tsp:



    def __init__(self,distance_matrix,init_temp,beta):
        ''' The tsp class is initialized by specifying as inputs:

        Distance matrix: list of lists.
        Initial temperature: int or float
        Beta: int or float

        ex. tspInstance = tsp(adj_mat,init_temp,beta)'''

        if type(init_temp) != int and type(init_temp) != float:
            raise TypeError("Initial temperature must be an integer or float.")
        elif type(beta) != int and type(beta) != float:
            raise TypeError("Beta must be an integer or float.")
        if type(distance_matrix) != list:
            raise TypeError("Distance matrix must be a list of lists.")
        elif not isinstance(distance_matrix[0],list):
            raise IndexError("Distance matrix must be two dimensional.")
        else:
            self.dist_mat = distance_matrix
            self.num_nodes = len(self.dist_mat[0])
            self.init_temp = init_temp
            self.beta = beta
            

    def find_path_sa(self, num_its = 100):
        '''This function finds the shortest path in the travelling salesman problem by implementing the simulated annealing algorithm. Number of iterations defaults to 100 but can be modified by passing in the num_its argument (i.e. tspInstance.find_path_sa(num_its = 1000)).

        Returns: List of shortest path.'''

        self.path = self.generate_random_path()
        self.cost = calc_cost()
        for k in range(num_its):
            try:
                self.path = self.modify_path()
            except Exception as error:
                raise error
        return self.path

    def generate_random_path(self):
        available_nodes = [i for i in range(self.num_nodes)]
        path = []
        while available_nodes:
            next_node = random.choice(available_nodes)
            path.append(next_node)
            available_nodes.remove(next_node)
        path.append(path[0])
        return path

    def choose_nodes(self):
        #chooses one node, removes it from the available choices, then chooses the next node
        node1 = random.choice(self.path)
        temp_path = list(self.path)
        if node1 == temp_path[0]:
            temp_path = temp_path[1:-1]
        else:
            temp_path.remove(node1)
        node2 = random.choice(temp_path)
        return (node1,node2)

    def update_path(self,node1,node2):

        node1_index = self.path.index(node1)
        node2_index = self.path.index(node2)

        if node1_index != 0 and node2_index != 0:
            self.path[node1_index] = node2
            self.path[node2_index] = node1

        elif node1_index == 0:
            self.path[0] = node2
            self.path[-1] = node2
            self.path[node2_index] = node1
        elif node2_index == 0:
            self.path[0] = node1
            self.path[-1] = node1
            self.path[node1_index] = node2


    def modify_path(self,nodes):
        node1,node2 = nodes
        #randomly chooses node to modify. updates cost and decides whether or not to keep new path
        node1_index = self.path.index(node1)
        node2_index = self.path.index(node2)
        temp_path = list(self.path)

        if node1_index != 0 and node2_index != 0:
            
            temp_path[node1_index] = node2
            temp_path[node2_index] = node1
            new_cost = self.calc_cost(path=temp_path)

        elif node1_index == 0:
            
            temp_path[0] = node2
            temp_path[-1] = node2
            temp_path[node2_index] = node1
            new_cost = self.calc_cost(path=temp_path)

        elif node2_index == 0:
            temp_path[0] = node1
            temp_path[-1] = node1
            temp_path[node1_index] = node2
            new_cost = self.calc_cost(path=temp_path)

        if self.cost - new_cost > 0: #if new path better than old path
            self.update_path(node1,node2)
            self.cost = new_cost

        else:
            T = self.calc_temp(k)
            prob_of_switch = self.calc_prob_of_switch(self.cost - new_cost,T)
            if random.uniform(0,1) <= prob_of_switch: #randomly get number to see whether to switch or not
                self.update_path(node1,node2)
                self.cost = new_cost

    def calc_cost(self,path=[]):
        if not path:
            path = list(self.path)
        cost = 0
        for i in range(len(path)-1):
            cost += self.dist_mat[path[i]][path[i+1]]
        return cost
        

    def calc_prob_of_switch(self,delta,T):
        #calclates the probability you should switch to the more expensive path
        return math.exp(-1*delta / T)
    def calc_temp(self,k):
        return (self.init_temp + self.beta * k)


    

            


    
            
    
        



