import sys
from problem_table import stream,problem_table

streams = []
print("Inputs: ")
with open(sys.argv[1],'r') as file:
	for line in file:
		vals = line.split(',')
		vals2 = [float(val) for val in vals]

		print(vals2)
		new_stream = stream(vals2[0],vals2[1],vals2[2])
		streams.append(new_stream)

pt = problem_table(streams)
Qc,Qh,pinch = pt.calc_vals()
