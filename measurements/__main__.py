from . import *
from si import *

if __name__ == "__main__":
	count = Measure(5)
	distance = Measure(8, 'k', BaseUnits.m)
	mass = Measure(13, unit=BaseUnits.g)
	time_ = Measure(19, unit=BaseUnits.s)
	current = Measure(1.2, unit=BaseUnits.A)
	print "distance", distance
	print "mass", mass
	print "time_", time_
	print "current", current
	speed = distance / time_
	print "speed", speed
	acceleration = distance / (time_ ** 2)
	acceleration2 = (1 / (time_ ** 2)) * distance
	print "acceleration", acceleration
	print "acceleration2", acceleration2
	print "acceleration == acceleration2 ", acceleration == acceleration2
	frequency = 100 / time_
	print "frequency", frequency

	yard = ImperialDistance(yards = 1)
	print (yard-yard).metric
