import math
import sys
import struct
import json
from fractions import Fraction
from collections import Counter

from . import *

PREFIXES = {
	'Y': (24,'yotta'),
	'Z': (21,'zetta'),
	'E': (18,'exa'),
	'P': (15,'peta'),
	'T': (12,'tera'),
	'G': (9,'giga'),
	'M': (6,'mega'),
	'k': (3,'kilo'),
	'h': (2,'hecto'),
	'da': (1,'deca'),
	None: (0, ''),
	'd': (-1,'deci'),
	'c': (-2,'centi'),
	'm': (-3,'milli'),
	'u': (-6,'micro'),
	'n': (-9,'nano'),
	'p': (-12,'pico'),
	'f': (-15,'femto'),
	'a': (-18,'atto'),
	'z': (-21,'zepto'),
	'y': (-24,'yocto')
}

REV_PREFIX = dict([(k[1], (k[0], v)) for v, k in PREFIXES.iteritems()])
REV_OFFSET = dict([(k[0], (k[1], v)) for v, k in PREFIXES.iteritems()])

_PF_PRIME = 19
class BaseUnits:
	_ = Fraction(1)
	m = Fraction(2)
	g = Fraction(3)
	s = Fraction(5)
	A = Fraction(7)
	K = Fraction(11)
	mol = Fraction(13)
	cd = Fraction(17)
	PF = Fraction(_PF_PRIME)

class DerivedUnits:
	Hz = Fraction(BaseUnits._, BaseUnits.s)
	N = Fraction(BaseUnits.m * BaseUnits.g * BaseUnits.s * BaseUnits.s,
				 BaseUnits._)
	J = Fraction(N * BaseUnits.m, BaseUnits._)
	W = Fraction(J, BaseUnits.s)
	V = Fraction(W, BaseUnits.A * BaseUnits.PF)
	VA = Fraction(W, BaseUnits.PF)

def model_dc_power():
	BaseUnits.PF = BaseUnits._
	DerivedUnits.V = Fraction(DerivedUnits.W, BaseUnits.A)
	DerivedUnits.__dict__['VA'] = BaseUnits._

def model_ac_power():
	BaseUnits.PF = Fraction(_PF_PRIME)
	DerivedUnits.V = Fraction(DerivedUnits.W, BaseUnits.A * BaseUnits.PF)
	DerivedUnits.__dict__['VA'] = Fraction(DerivedUnits.W, BaseUnits.PF)


def significant(x, sig=2):
	if x == 0:
		return 0
	return round(x, sig-int(math.floor(math.log10(math.fabs(x))))-1)


def find_unit_string(unit):
	if unit == BaseUnits._:
		return ''

	unit_dict = dict(BaseUnits.__dict__)
	unit_dict.update(DerivedUnits.__dict__)

	for k in unit_dict:
		if unit == unit_dict[k]:
			return k

	raise UnitError("Unknown Unit")


def get_factors(i):
	i = int(i)
	ret = Counter()
	unit_list = [int(BaseUnits.__dict__[x]) for x in BaseUnits.__dict__ if
				 isinstance(BaseUnits.__dict__[x], Fraction) and
				 BaseUnits.__dict__[x] != 1]

	unit_list.sort(reverse=True)

	for f in unit_list:
		while i % f == 0:
			ret[f] += 1
			i /= f

	return ret


def describe_unit(u):
	ret = ''
	num = get_factors(u.numerator)
	denom = get_factors(u.denominator)

	num.subtract(denom)

	for f in num:
		cur_unit = find_unit_string(f)
		if num[f] != 1:
			cur_unit += '^{}'.format(num[f])
		ret += cur_unit

	return ret


class Measure:
	BIN_STRUCT = struct.Struct("!dbII")
	def __init__(self, value, prefix=None, unit=None, sig=sys.float_info.dig):
		self.value = significant(float(value), sig)
		self.sig = sig

		try:
			self.prefix = PREFIXES[prefix]
		except KeyError, e:
			raise PrefixError("Invalid SI Prefix", prefix)

		if unit is None:
			self.unit = BaseUnits._
		else:
			self.unit = Fraction(unit)

	def to_base_prefix(self):
		baseval = self.value * (10 ** self.prefix[0])
		return Measure(baseval, unit=self.unit, sig=self.sig)

	def binarize(self):
		return self.BIN_STRUCT.pack(self.value, self.prefix[0],
									self.unit.numerator, self.unit.denominator)

	def json(self):
		return json.dumps({'v': self.value,
						   'si': self.prefix[0],
						   'un': self.unit.numerator,
						   'ud': self.unit.denominator})

	@staticmethod
	def from_binary(bin_str):
		val, pre, num, den = Measure.BIN_STRUCT.unpack(bin_str)

	@staticmethod
	def from_json(json_str):
		vals = json.loads(json_str)
		val = vals['v']
		pre = vals['si']
		num = vals['un']
		den = vals['ud']

		return Measure(val, REV_OFFSET[pre][1], Fraction(num, den))

	def __str__(self):
		prefix = REV_PREFIX[self.prefix[1]][1]
		if prefix is None:
			prefix = ''

		try:
			unit = find_unit_string(self.unit)
		except UnitError:
			unit = describe_unit(self.unit)

		return "{} {}{}".format(self.value, prefix, unit)

	def __eq__(self,other):
		if not isinstance(other, Measure):
			other = Measure(other)
		lhs = self.to_base_prefix()
		rhs = other.to_base_prefix()

		if lhs.unit != rhs.unit:
			raise UnitError("Incompatible units")

		return lhs.value == rhs.value

	def __ne__(self,other):
		if not isinstance(other, Measure):
			other = Measure(other)
		if self.unit != other.unit:
			raise UnitError("Incompatible units")

		return not(self == other)

	def __add__(self,other):
		if not isinstance(other, (Measure, NonStandard)):
			other = Measure(other)
		lhs = self.to_base_prefix()
		rhs = other.to_base_prefix()
		sig = min(self.sig, other.sig)

		if lhs.unit != rhs.unit:
			raise UnitError("Incompatible units")

		prefix = self.prefix
		value = (lhs.value + rhs.value) * (10 ** (prefix[0] * -1))
		return Measure(value, REV_OFFSET[prefix[0]][1], lhs.unit, sig=sig)

	def __radd__(self, other):
		return Measure(other) + self

	def __sub__(self,other):
		if not isinstance(other, (Measure, NonStandard)):
			other = Measure(other)
		if self.unit != other.unit:
			raise UnitError("Incompatible units")

		return self + -other

	def __rsub__(self, other):
		return Measure(other) + -self

	def __mul__(self,other):
		if not isinstance(other, (Measure, NonStandard)):
			other = Measure(other)
		lhs = self.to_base_prefix()
		rhs = other.to_base_prefix()
		sig = min(self.sig, other.sig)

		prefix = self.prefix
		value = (lhs.value * rhs.value) * (10 ** (prefix[0] * -1))
		return Measure(value, REV_OFFSET[prefix[0]][1],
					  lhs.unit * rhs.unit, sig=sig)

	def __rmul__(self, other):
		return Measure(other) * self

	def __div__(self,other):
		if not isinstance(other, (Measure, NonStandard)):
			other = Measure(other)
		return self * ~other

	def __rdiv__(self, other):
		return Measure(other) * ~self

	def __pow__(self,other):
		return Measure(self.value ** other, REV_OFFSET[self.prefix[0]][1],
					  self.unit ** other, sig=self.sig)

	def __pos__(self):
		return Measure(self.value, REV_OFFSET[self.prefix[0]][1],
					  self.unit, sig=self.sig)

	def __neg__(self):
		return Measure(-self.value, REV_OFFSET[self.prefix[0]][1],
					  self.unit, sig=self.sig)

	def __abs__(self):
		return Measure(abs(self.value), REV_OFFSET[self.prefix[0]][1],
					  self.unit, sig=self.sig)

	def __invert__(self):
		return self.__inv__()

	def __inv__(self):
		unit = Fraction(self.unit.denominator, self.unit.numerator)
		return Measure(1.0/self.value, REV_OFFSET[-self.prefix[0]][1],
					  unit, sig=self.sig)


class NonStandard(object):
	def __init__(self, unit=None):
		self._value = Measure(0, unit=unit)

	def to_base_prefix(self):
		return self._value.to_base_prefix()

	@property
	def metric(self):
		return self._value

	@metric.setter
	def metric(self, value):
		self._value = value

	@property
	def sig(self):
		return self.metric.sig

	@property
	def unit(self):
		return self.metric.unit

	def __add__(self, other):
		ret = self.__class__()
		ret.metric = (self.to_base_prefix() + other.to_base_prefix())
		return ret

	def __pos__(self): return self

	def __neg__(self):
		ret = self.__class__()
		ret.metric = -self.metric
		return ret

	def __sub__(self, other):
		return self + -other

	def __mul__(self, other):
		ret = self.__class__()
		ret.metric = (self.to_base_prefix() * other.to_base_prefix())
		return ret

	def __invert__(self):
		ret = self.__class__()
		ret.metric = ~self.metric
		return ret

	def __div__(self, other):
		return self * ~other


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
		return self._value.value / self.M_PER_YARD

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