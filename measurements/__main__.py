import bz2
import zlib
import random
import time

from . import *
from si import *
from imperial import *
from energy import *
from timeseries import *
import util

def examples():
	print "SI".center(60, '-')
	count = Measure(5)
	distance = Measure(8, 'k', BaseUnits.m)
	mass = Measure(13, unit=BaseUnits.g)
	time_ = Measure(19, unit=BaseUnits.s)
	current = Measure(1.2, unit=BaseUnits.A)
	print "distance", distance
	print "distance meters", distance.to_prefix()
	print "mass", mass
	print "time_", time_
	print "current", current
	speed = distance / time_
	print "speed", speed
	print "2 x speed > speed", 2 * speed > speed
	# print "2 x speed >= speed", 2 * speed >= speed
	# print "2 x speed < speed", 2 * speed < speed
	# print "2 x speed <= speed", 2 * speed <= speed
	# print "speed > speed x 2", speed > speed * 2
	print "speed >= speed x 2", speed >= speed * 2
	# print "speed < speed x 2", speed < speed * 2
	# print "speed <= speed x 2", speed <= speed * 2
	# print "speed > speed", speed > speed
	# print "speed >= speed", speed >= speed
	print "speed < speed", speed < speed
	# print "speed <= speed", speed <= speed
	acceleration = distance / (time_ ** 2)
	acceleration2 = (1 / (time_ ** 2)) * distance
	print "acceleration", acceleration
	print "acceleration2", acceleration2
	print "acceleration == acceleration2 ", acceleration == acceleration2
	frequency = 100 / time_
	print "frequency", frequency

	print "ImperialDistance".center(60, '-')
	yard = ImperialDistance(yards = 1)
	print "2 yards =", (yard+yard).metric
	print "2 yards =", (yard+yard).miles, "miles"
	print "2 yards > yard", (yard + yard) > yard
	print "2 yards < yard", (yard + yard) < yard

	print "Energy".center(60, '-')
	print "1 J =", Energy(joules = 1).watthours, "wh"
	print "1 wh =", Energy(watthours = 1).joules, "J"
	print "1 kwh =", Energy(kilowatthours = 1).joules, "J"
	print "1 kwh =", Energy(kilowatthours = 1).watthours, "wh"
	print "1000 eV =", Energy(electronvolts = 1000).joules, "J"
	print "1 J =", Energy(joules = 1).electronvolts, "eV"
	print "1 J =", Energy(joules = 1).calories, "cal"
	print "1 kwh =", Energy(kilowatthours = 1).calories, "cal"

	print "Timeseries".center(60, '-')
	ts = Timeseries()
	sampcnt = 10000
	print "Generating {} samples...".format(sampcnt)
	power_read = 1000.0
	for _ in xrange(sampcnt):
		power_read = max(power_read + random.uniform(-10.0,10.0), 0.0)
		ts.append(Energy(kilowatthours=power_read))
		if _ % (sampcnt // 40) == 0:
			print ".",
	print ""

	bindat = ts.binarize()
	zlib_t = time.time()
	cmpdat = ts.compress(zlib.compress)
	zlib_t = time.time() - zlib_t
	bz2_t = time.time()
	cmpdat2 = ts.compress()
	bz2_t = time.time() - bz2_t
	cmpperc = float(len(cmpdat)) / len(bindat) * 100.0
	cmpperc2 = float(len(cmpdat2)) / len(bindat) * 100.0
	strdat = ts.stringify()
	strperc = float(len(cmpdat)) / len(strdat) * 100.0

	print "The following is based on {} samples".format(sampcnt).center(60, '-')
	print "Zlib Compression reduced data to {:.4f}% binary size".format(cmpperc)
	print "Zlib Compression took {} seconds".format(zlib_t)
	print "Bz2 Compression reduced data to {:.4f}% binary size".format(cmpperc2)
	print "Bz2 Compression took {} seconds".format(bz2_t)
	print "Stringify reduced data to {:.4f}% binary size".format(strperc)

	ds_t = time.time()
	from_string = Timeseries.destringify(strdat)
	ds_t = time.time() - ds_t
	print "Destringify took {} seconds".format(ds_t)
	print random.choice(from_string)[0], random.choice(from_string)[1]

	pt_a = random.choice(from_string)
	pt_b = random.choice(from_string)

	from_a_to_b = from_string.timeslice(min(pt_a[0], pt_b[0]),
										max(pt_a[0], pt_b[0]))

	print "There are {} datapoints between {} and {}."\
		  .format(from_a_to_b.length,min(pt_a[0], pt_b[0]),
				  max(pt_a[0], pt_b[0]))

	pt_a = random.choice(from_string)
	pt_b = random.choice(from_string)

	from_a_to_b = from_string.valueslice(min(pt_a[1], pt_b[1]),
										 max(pt_a[1], pt_b[1]))

	print "There are {} datapoints between {} and {}."\
		  .format(from_a_to_b.length,min(pt_a[1], pt_b[1]),
				  max(pt_a[1], pt_b[1]))


	util.plot_timeseries_with_pyplot(from_string)
	return

if __name__ == "__main__":
	examples()
