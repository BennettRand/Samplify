from si import *

class Energy(NonStandard):
	def __init__(self, joules=0, watthours=0, kilowatthours=0, electronvolts=0,
				 calories=0):
		NonStandard.__init__(self, DerivedUnits.J)
		self.joules = joules
		self.watthours += watthours
		self.kilowatthours += kilowatthours
		self.electronvolts += electronvolts
		# self.calories += calories

	@property
	def joules(self):
		return self._value.to_base_prefix().value

	@joules.setter
	def joules(self, j):
		self._value = Measure(j, unit=DerivedUnits.J)

	@property
	def watthours(self):
		return self.joules / 3600.0

	@watthours.setter
	def watthours(self, wh):
		self.joules = wh * 3600.0

	@property
	def kilowatthours(self):
		return self.watthours / 1000.0

	@kilowatthours.setter
	def kilowatthours(self, kwh):
		self.watthours = kwh * 1000.0

	@property
	def electronvolts(self):
		return self.metric.to_prefix('a').value / 0.160217733

	@electronvolts.setter
	def electronvolts(self, ev):
		self.metric = Measure(ev * 0.160217733, 'a', DerivedUnits.J)
