from .si import *

class Energy(NonStandard):
	def __init__(self, joules=0, watthours=0, kilowatthours=0, electronvolts=0,
				 calories=0, btu_iso=0, btu_15=0):
		NonStandard.__init__(self, DerivedUnits.J)
		self.joules = joules
		self.watthours += watthours
		self.kilowatthours += kilowatthours
		self.electronvolts += electronvolts
		self.calories += calories
		self.btu_iso += btu_iso
		self.btu_15 += btu_15

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

	@property
	def calories(self):
		return self.joules / 4.184

	@calories.setter
	def calories(self, c):
		self.joules = c * 4.184

	@property
	def btu_iso(self):
		return self.joules / 1055.056

	@btu_iso.setter
	def btu_iso(self, b):
		self.joules = b * 1055.056

	@property
	def btu_15(self):
		return self.joules / 1054.804

	@btu_15.setter
	def btu_15(self, b):
		self.joules = b * 1054.804
