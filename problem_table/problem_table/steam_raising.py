import sys
from problem_table import stream,problem_table
import matplotlib.pyplot as plt 
import numpy as np
plt.style.use('seaborn')

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
Qc,Qh,pinch, deltaHs, intervalTemps= pt.calc_vals(debug=False,gcc=True)

#engineering toolbox
dHvap = 2250.76
Cps = 1.895
Cpw = 4.20
Tf = 398-273
Tsat = 378-273
Tstart = 303-273


tHpoints = []
tHpoints.append((intervalTemps[0][0],Qh))
cascade = Qh
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


def Hwater(T,H_start): #calculates the enthalpy of the water at a specific pt using eqs from paper
	return H_start - Mw * Cpw * (T-Tstart) 

def Hstart(Hwsat,Mw): #calculates starting enthalpy based on given vals
	return Mw * Cpw * (Tsat-Tstart) + Hwsat

def Mw_calc(Hwsat):
	return Hwsat / dHvap * (1-Cps * (Tf-Tsat) / (dHvap + Cps * (Tf-Tsat)))

def Hsteam(T,Mw):
	return Mw * Cps * (Tf - T) 

def gcc_crossed(Hwsat,Mw):
	H_start = Hstart(Hwsat,Mw)
	for pt in relevant_tH:
		if Hwater(pt[0],H_start) > pt[1]:
			return True
	return False

temps = [i[0] for i in tHpoints]
enthalpies = [i[1] for i in tHpoints]


# Hssat_init = Qc
# Mw = 1 / Cps * Hssat_init / (Tf-Tsat)
# Hwsat = dHvap * Mw + Hssat_init
Hwsat = Qc
Mw = Mw_calc(Hwsat)
# print("hssat_init",Hssat_init)
# print("init of its",Hwsat)


while gcc_crossed(Hwsat,Mw):
	Hwsat -= .1
	Mw = Mw_calc(Hwsat)

print(Hwsat)
print(Mw_calc(Hwsat)) 
Mw = Mw_calc(Hwsat)


Tpoints = np.linspace(Tstart,Tsat,100)
H_start = Hstart(Hwsat,Mw_calc(Hwsat))
Hpoints = Hwater(Tpoints,H_start)

TpointsSteam = np.linspace(Tsat,Tf,100)
HpointsSteam = Hsteam(TpointsSteam,Mw)

Htransition = np.linspace(Hpoints[-1],HpointsSteam[0],100)
Ttransition = [Tsat for i in range(100)]

# plt.style('ggplot')
plt.annotate('Hwsat',xy=(Hwsat,105),xytext=(Hwsat+200,110), arrowprops=dict(facecolor='black',arrowstyle='-|>'))
plt.annotate('Hssat',xy=(HpointsSteam[0],105),xytext=(HpointsSteam[0],60), arrowprops=dict(facecolor='black',arrowstyle='-|>'))
plt.annotate('Hstart',xy=(H_start,30),xytext=(H_start-400,35), arrowprops=dict(facecolor='black',arrowstyle='-|>'))


plt.plot(enthalpies,temps)
plt.plot(Hpoints,Tpoints,'r')
plt.plot(HpointsSteam,TpointsSteam,'r')
plt.plot(Htransition,Ttransition,'r')
plt.xlabel("Enthalpy (kW)")
plt.ylabel("Temperature (Celsius)")
plt.title("Steam raising plot and GCC")
plt.savefig("steam_raising.jpg")
plt.show()





