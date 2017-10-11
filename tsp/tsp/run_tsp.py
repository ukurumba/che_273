from tsp import tsp

dist_mat = [[200,2,300,400],[500,600,2,800],[900,100,110,12],[13,142,153,116]]
init_temp = 900
beta = -1.1
debug = False
tsp1 = tsp(dist_mat,init_temp,beta,debug=debug)
shortest_path = tsp1.find_path_sa()
cost = tsp1.calc_cost(shortest_path)
print("Shortest Path")
print(shortest_path)
print("Cost")
print(cost)
