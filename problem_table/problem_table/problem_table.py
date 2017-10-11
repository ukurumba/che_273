



class problem_table:

	def __init__(self,streams):
		#streams should be a list of streams
		self.streams = streams

	def calc_vals(self,streams = []):
		if not streams:
			streams = self.streams
		temps = []
		sorted_temps = []
		for stream in streams:
			if stream.type != "Column":
				temps.append(stream.shifted_Ts)
				temps.append(stream.shifted_Tf)
			else:
				sorted_temps.append(stream.shifted_Ts)
				sorted_temps.append(stream.shifted_Tf)
		
		for temp in temps:
				if temp not in sorted_temps:
					sorted_temps.append(temp)
		sorted_temps.sort(reverse=True)
		

		intervals = [(sorted_temps[i],sorted_temps[i+1]) for i in range(len(sorted_temps)-1)]
		print("Temperature Intervals: ", intervals)
		interval_cps = [0.0 for i in intervals]
		interval_deltaHs = [0.0 for i in intervals]
		for i,interval in zip(range(len(intervals)),intervals):
			for stream in streams: 
				if stream.type == "Column":
					if stream.shifted_Ts == interval[0] and stream.shifted_Ts == interval[1]: #if this is the column interval
						interval_deltaHs[i] += stream.load #add the load directly
				else:
					if stream.shifted_Ts >= interval[0] and interval[1] >= stream.shifted_Tf:
						if stream.type == "Hot":
							interval_cps[i] += stream.Cp
						elif stream.type == "Cold":
							interval_cps[i] -= stream.Cp
					elif stream.shifted_Tf >= interval[0] and interval[1] >= stream.shifted_Ts:
						if stream.type == "Hot":
							interval_cps[i] += stream.Cp
						elif stream.type == "Cold":
							interval_cps[i] -= stream.Cp

		print("Cp per interval: ", interval_cps)

		for i in range(len(intervals)):
			interval_deltaHs[i] += (intervals[i][0] - intervals[i][1])*interval_cps[i] 
		print("Delta H per interval: ", interval_deltaHs)

		cascade = 0
		most_negative = 0
		for delta_h in interval_deltaHs:
			cascade += delta_h
			if cascade < most_negative:
				most_negative = cascade

		cascade = most_negative
		Qh_min = -1 * cascade
		pinch = -1000
		Qc_min = 0

		cascade = Qh_min 
		for delta_h in interval_deltaHs:

			cascade += delta_h
			if abs(cascade) < .0000001: #rounding error
				i = interval_deltaHs.index(delta_h)
				pinch = intervals[i][1]
			Qc_min = cascade

		
		cascade_for_print = Qh_min
		print("Temp   CP    deltaH    Cascade(Feasible)")
		print(intervals[0][0])
		for i in range(len(intervals)):
			interval = intervals[i][1]
			cp = interval_cps[i]
			dH = interval_deltaHs[i]
			cascade_for_print += interval_deltaHs[i] 
			print("{}   {:.3}   {:.3}   {:.3}   {:.3} ".format(interval,cp,dH, cascade_for_print - Qh_min,cascade_for_print))
			

		print("Qc_min Qh_min T_pinch")
		print(Qc_min,Qh_min,pinch)
		return [Qc_min, Qh_min,pinch]


class stream:
	
	def __init__(self,T_supply,T_final,Cp):
		#Cp is CP if normal stream, load if column
		#load is positive for condensers, negative for reboilers 
		delta_T = 10
		self.Ts = T_supply
		self.Tf = T_final
		
		if self.Ts < self.Tf: 
			self.type = "Cold"
			self.Cp = Cp
		elif self.Ts > self.Tf:
			self.type = "Hot"
			self.Cp = Cp
		else:
			self.type = "Column"
			self.load = Cp
			if self.load < 0: #reboiler i.e. cold stream
				self.shifted_Ts = self.Ts + delta_T / 2
				self.shifted_Tf = self.Tf + delta_T / 2
			elif self.load > 0:
				self.shifted_Ts = self.Ts - delta_T / 2
				self.shifted_Tf = self.Tf - delta_T / 2


		if self.type == "Cold":
			self.shifted_Ts = self.Ts + delta_T / 2
			self.shifted_Tf = self.Tf + delta_T / 2
		if self.type == "Hot":
			self.shifted_Ts = self.Ts - delta_T / 2
			self.shifted_Tf = self.Tf - delta_T / 2




