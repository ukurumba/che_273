import sys
from problem_table import stream,problem_table
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import numpy as np

streams = []
unstreamed_values = []
print("Inputs: ")
with open(sys.argv[1],'r') as file:
	for line in file:
		vals = line.split(',')
		vals2 = [float(val) for val in vals]
		unstreamed_values.append(vals2)


def objective(dTmin):
	streams = []
	for val_set in unstreamed_values:
		new_stream = stream(val_set[0],val_set[1],val_set[2],delta_T=dTmin)
		streams.append(new_stream)
	pt = problem_table(streams) 
	Qc,Qh,pinch = pt.calc_vals()
	energy_cost = 300 * 3.6 * 10* (Qh+2832) #energy cost in $ 2832 is the KW from the unintegrated reboiler that must be considered
	capital_cost = 12.5*10**6 / (dTmin**.05) #capital cost in $
	total_cost = energy_cost + capital_cost
	return total_cost




dTmin_array = np.linspace(3,40,500)
costs = []
for i in dTmin_array:
	costs.append(objective(i))

print("Min Delta T: ",dTmin_array[costs.index(min(costs))], "Min Cost: ", min(costs))


plt.plot(dTmin_array,costs,'bo')
plt.xlabel('Delta T Min (K)')
plt.ylabel('Total Cost (* 10 mil $)')
plt.title('Effect of Delta T Min on total cost on the range 10-40K',y=1.08)
plt.savefig('overall_total_cost.jpg')
plt.show()

dTmin_array = np.linspace(32.5,33,200)
costs = []
for i in dTmin_array:
	costs.append(objective(i))

plt.plot(dTmin_array,costs,'bo')
plt.xlabel('Delta T Min (K)')
plt.ylabel('Total Cost (* 10 mil $)')
plt.title('Zoom in on discontinous region of total cost function',y=1.08)
plt.savefig('zoomin.jpg')


	