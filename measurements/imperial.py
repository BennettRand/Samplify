from si import *


class ImperialDistance(NonStandard):
	M_PER_YARD = 0.9144
	def __init__(self, thous=0, inches=0, feet=0, yards=0, chains=0, furlongs=0,
				 miles=0):
		NonStandard.__init__(self, BaseUnits.m)
		self.yards = yards
		self.feet += feet
		self.inches += inches
		self.thous += thous
		self.chains += chains
		self.furlongs += furlongs
		self.miles += miles

	@property
	def yards(self):
		return (self._value.to_base_prefix().value / self.M_PER_YARD)

	@yards.setter
	def yards(self, y):
		self._value = Measure(y * self.M_PER_YARD, unit=BaseUnits.m)

	@property
	def feet(self):
		return self.yards * 3.0

	@feet.setter
	def feet(self, f):
		self.yards = f / 3.0

	@property
	def inches(self):
		return self.feet * 12.0

	@inches.setter
	def inches(self, i):
		self.feet = i / 12.0

	@property
	def thous(self):
		return self.inches * 1000.0

	@thous.setter
	def thous(self, t):
		self.inches = t / 1000.0

	@property
	def chains(self):
		return self.yards / 22.0

	@chains.setter
	def chains(self, c):
		self.yards = c * 22.0

	@property
	def furlongs(self):
		return self.chains / 10.0

	@furlongs.setter
	def furlongs(self, f):
		self.chains = f * 10.0

	@property
	def miles(self):
		return self.furlongs / 8.0

	@miles.setter
	def miles(self, m):
		self.furlongs = m * 8.0
