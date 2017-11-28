import sys
from problem_table import stream,problem_table
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import numpy as np

dHvap = 2250.76
Cps = 1.895
Cpw = 4.20
Tf = 398-273
Tsat = 378-273
Tstart = 303-273

streams = []
unstreamed_values = []
print("Inputs: ")
with open(sys.argv[1],'r') as file:
	for line in file:
		vals = line.split(',')
		vals2 = [float(val) for val in vals]
		unstreamed_values.append(vals2)

capitals = []
energies = []
savings = []


def objective(dTmin):
	streams = []
	for val_set in unstreamed_values:
		new_stream = stream(val_set[0],val_set[1],val_set[2],delta_T=dTmin)
		streams.append(new_stream)
	pt = problem_table(streams) 
	Qc,Qh,pinch,deltaHs,intervalTemps = pt.calc_vals(gcc=True)
	energy_cost = 300 * 3.6 * 10* (Qh+2832) #energy cost in $ 2832 is the KW from the unintegrated reboiler that must be considered
	capital_cost = 12.5*10**6 / (dTmin**.05) #capital cost in $
	saved_cost = saved(Qc,Qh,deltaHs,intervalTemps)
	total_cost = energy_cost + capital_cost - saved_cost
	#print("dtmin: {} Total cost: {} Saved Cost: {} Energy Cost: {}".format(dTmin,total_cost,saved_cost,energy_cost))
	capitals.append(capital_cost)
	energies.append(energy_cost)
	savings.append(saved_cost)

	return total_cost


def steam_raising(Qc,Qh,deltaHs,intervalTemps):

	def Hwater(T,H_start): #calculates the enthalpy of the water at a specific pt using eqs from paper
		return H_start - Mw * Cpw * (T-Tstart) 

	def Hstart(Hwsat,Mw): #calculates starting enthalpy based on given vals
		return Mw * Cpw * (Tsat-Tstart) + Hwsat

	def Mw_calc(Hwsat):
		return Hwsat / dHvap * (1-Cps * (Tf-Tsat) / (dHvap + Cps * (Tf-Tsat)))

	def Hsteam(T,Mw):
		return Mw * Cps * (Tf - T) 

	tHpoints = []
	tHpoints.append((intervalTemps[0][0],Qh))
	cascade = Qh*10
	Qc *= 10
	deltaHs = [i*10 for i in deltaHs]
	for i in range(len(intervalTemps)):
		cascade += deltaHs[i]
		tHpoints.append((intervalTemps[i][1],cascade))


	topPt = []
	botPt = []
	for i in range(len(tHpoints)):
		if Tf >= tHpoints[i][0]:
			topPt = i
			break
	for i in range(len(tHpoints)-1,0,-1):
		if tHpoints[i][0] >= Tstart:
			botPt = i
			break

	relevant_tH = tHpoints[topPt:botPt]




	temps = [i[0] for i in tHpoints]
	enthalpies = [i[1] for i in tHpoints]


	# Hssat_init = Qc
	# Mw = 1 / Cps * Hssat_init / (Tf-Tsat)
	# Hwsat = dHvap * Mw + Hssat_init
	Hwsat = Qc
	Mw = Mw_calc(Hwsat)
	# print("hssat_init",Hssat_init)
	# print("init of its",Hwsat)




	def gcc_crossed(Hwsat,Mw):
		H_start = Hstart(Hwsat,Mw)
		for pt in relevant_tH:
			if Hwater(pt[0],H_start) > pt[1]:
				return True
		return False


	while gcc_crossed(Hwsat,Mw):
		Hwsat -= 1
		Mw = Mw_calc(Hwsat)
	 
	Mw = Mw_calc(Hwsat)
	H_sr = Cpw * Mw * (Tsat-Tstart) + dHvap * Mw + Cps * Mw * (Tsat-Tstart)

	Tpoints = np.linspace(Tstart,Tsat,100)
	H_start = Hstart(Hwsat,Mw_calc(Hwsat))
	Hpoints = Hwater(Tpoints,H_start)

	TpointsSteam = np.linspace(Tsat,Tf,100)
	HpointsSteam = Hsteam(TpointsSteam,Mw)

	Htransition = np.linspace(Hpoints[-1],HpointsSteam[0],100)
	Ttransition = [Tsat for i in range(100)]

	# plt.style('ggplot')
	# plt.annotate('Hwsat',xy=(Hwsat,105),xytext=(Hwsat+200,110), arrowprops=dict(facecolor='black',arrowstyle='-|>'))
	# plt.annotate('Hssat',xy=(HpointsSteam[0],105),xytext=(HpointsSteam[0],60), arrowprops=dict(facecolor='black',arrowstyle='-|>'))
	# plt.annotate('Hstart',xy=(H_start,30),xytext=(H_start-400,35), arrowprops=dict(facecolor='black',arrowstyle='-|>'))


	# plt.plot(enthalpies,temps)
	# plt.plot(Hpoints,Tpoints,'r')
	# plt.plot(HpointsSteam,TpointsSteam,'r')
	# plt.plot(Htransition,Ttransition,'r')
	# plt.xlabel("Enthalpy (kW)")
	# plt.ylabel("Temperature (Celsius)")
	# plt.show()

	# raise ValueError("Fuck my life")



	return H_sr,Mw

def saved(Qc,Qh,deltaHs,intervalTemps):
	H_sr,Mw = steam_raising(Qc,Qh,deltaHs,intervalTemps)
	#print("H_sr",H_sr,"Qc",Qc*10,"Qh",Qh)
	Work_carnot = 21.141 * (1/44.01) * Mw / 1000 #j / mol * mol / kg * kg/s * kj / j
	return (H_sr + Work_carnot) * 300 * 3.6





dTmin_array = np.linspace(3,40,1000)
costs = []
for i in dTmin_array:
	costs.append(objective(i))

print("Min Delta T: ",dTmin_array[costs.index(min(costs))], "Min Cost: ", min(costs))


plt.plot(dTmin_array,costs,label='total costs')
plt.xlabel('Delta T Min (K)')
plt.ylabel('Total Cost (* 10 mil $)')
plt.title('Effect of Delta T Min on total cost',y=1.08)
plt.savefig('overall_total_cost_with_steam_raising_total_only.jpg')
plt.show()




