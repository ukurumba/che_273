import random
import math
class tsp:



    def __init__(self,distance_matrix,init_temp,beta,debug = False):
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
            self.end_run = False
            self.debug = debug
            

    def find_path_sa(self, num_its = 100,end_run_its = 200):
        '''This function finds the shortest path in the travelling salesman problem by implementing the simulated annealing algorithm. Number of iterations defaults to 100 but can be modified by passing in the num_its argument (i.e. tspInstance.find_path_sa(num_its = 1000)).

        Returns: List of shortest path.'''

        self.path = self.generate_random_path()
        self.cost = self.calc_cost()
        for k in range(num_its):
            try:
                self.k = k
                self.modify_path(self.choose_nodes())
            except Exception as error:
                raise error

        self.end_run = True
        self.debug = False #never debug end run.
        if self.debug:
            print("\n \n \nBEGINNING END RUN ----------------------------------------------------")
        for k in range(end_run_its):
            try:
                self.k = k
                self.modify_path(self.choose_nodes())
            except Exception as error:
                raise error
        return self.path

    def find_path_random(self, num_its=1000):
        '''This function finds the shortest path length in the TSP problem by just randomly generating paths and keeping track of the shortest.'''
        self.path = self.generate_random_path()
        # print(self.path)
        # print(self.dist_mat)
        self.cost = self.calc_cost()
        for i in range(num_its):
            self.temppath = self.path
            self.tempcost = self.cost
            self.path = self.generate_random_path()
            self.cost = self.calc_cost()
            if self.tempcost < self.cost:
                self.path = self.temppath
                self.cost = self.tempcost
        
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
        if self.debug:
            print(self.path, " <--- path before update_path")
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

        if self.debug:
            print(self.path, " <--- Path after update_path")

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

        if new_cost - self.cost < 0: #if new path better than old 
            if self.debug:
                print("\nbetter path used")
            self.update_path(node1,node2)
            self.cost = new_cost

        else:
            T = self.calc_temp(self.k)
            prob_of_switch = self.calc_prob_of_switch(new_cost - self.cost,T)
            if random.uniform(0,1) <= prob_of_switch: #randomly get number to see whether to switch or not
                if self.debug:
                    print("\nworse path used. Prob switch: " + str(prob_of_switch))
                self.update_path(node1,node2)
                self.cost = new_cost
            else:
                if self.debug:
                    print("\nworse path not used. Prob switch: " + str(prob_of_switch))

    def calc_cost(self,path=[]):
        if not path:
            path = list(self.path)
        cost = 0
        for i in range(len(path)-1):
            cost += self.dist_mat[path[i]][path[i+1]]
        return cost
        

    def calc_prob_of_switch(self,delta,T):
        # delta = new minus old
        #calclates the probability you should switch to the more expensive path
        if self.end_run == True: #if we're doing the final burnoff that is a greedy algorithm. 
            return -1
        else:
            try:
                return math.exp(-1*delta / T)
            except OverflowError:
                if self.debug:
                    print("Overflow Error")
                return 0 #if there's an overflow then prob is so small it is effectively 0
    def calc_temp(self,k):
        return (max(0.0000000001,self.init_temp + self.beta * k)) #Temperature will never go negative


    

            


    
            
    
        



