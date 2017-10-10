



class problem_table:

	def __init__(self,streams):
		#streams should be a list of streams
		self.streams = streams

	def calc_vals(self,streams = []):
		if not streams:
			streams = self.streams
		temps = []
		for stream in streams:
			temps.append(stream.shifted_Ts)
			temps.append(stream.shifted_Tf)
		sorted_temps = []
		for temp in temps:
				if temp not in sorted_temps:
					sorted_temps.append(temp)
		sorted_temps.sort(reverse=True)
		

		intervals = [(sorted_temps[i],sorted_temps[i+1]) for i in range(len(sorted_temps)-1)]
		print("Temperature Intervals: ", intervals)
		interval_cps = [0 for i in intervals]
		for i,interval in zip(range(len(intervals)),intervals):
			for stream in streams: 
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

		interval_deltaHs = [(intervals[i][0] - intervals[i][1])*interval_cps[i] for i in range(len(intervals))]
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
			if cascade == 0:
				i = interval_deltaHs.index(delta_h)
				pinch = intervals[i][1]
			Qc_min = cascade

		

		print("Qc_min: {}			Qh_min:	{}			Pinch T: {}		".format(Qc_min,Qh_min,pinch))

		return [Qc_min, Qh_min,pinch]


class stream:
	
	def __init__(self,T_supply,T_final,Cp):
		delta_T = 10
		self.Ts = T_supply
		self.Tf = T_final
		self.Cp = Cp
		if self.Ts < self.Tf: 
			self.type = "Cold"
		elif self.Ts > self.Tf:
			self.type = "Hot"
		else:
			self.type = "Column"

		if self.type == "Cold":
			self.shifted_Ts = self.Ts + delta_T / 2
			self.shifted_Tf = self.Tf + delta_T / 2
		if self.type == "Hot":
			self.shifted_Ts = self.Ts - delta_T / 2
			self.shifted_Tf = self.Tf - delta_T / 2




