import unittest

from measurements import *
from measurements import si
from measurements import imperial
from measurements import energy

class SITest(unittest.TestCase):
	def setUp(self):
		return

	def test_prefix_comparisons(self):
		self.assertEqual(si.Measure(1), si.Measure(1000, 'm'))
		self.assertEqual(si.Measure(1000), si.Measure(1, 'k'))
		self.assertEqual(si.Measure(1000000, 'm'), si.Measure(1, 'k'))
		self.assertEqual(si.Measure(1), si.Measure(1).to_prefix('y'))

		self.assertNotEqual(si.Measure(1), si.Measure(1, 'm'))
		self.assertNotEqual(si.Measure(1), si.Measure(2))
		self.assertNotEqual(si.Measure(1, 'y'), si.Measure(1, 'Y'))

	def test_math(self):
		one = si.Measure(1)
		two = si.Measure(2)
		ten = si.Measure(1, 'da')

		self.assertEqual(one + one, 2 * one)
		self.assertEqual(two, 2 * one)
		self.assertEqual(two / 2, one)
		self.assertEqual(two * 5, ten)
		self.assertEqual(two - one, one)
		self.assertEqual(two - one, 1)
		self.assertEqual(two - 1, one)
		self.assertEqual(ten - two, 8)

	def test_comparators(self):
		one = si.Measure(1)
		two = si.Measure(2)
		ten = si.Measure(1, 'da')

		self.assertEqual(one, one)
		self.assertNotEqual(one, two)
		self.assertGreater(two, one)
		self.assertGreaterEqual(two, one)
		self.assertGreaterEqual(one, one)
		self.assertLess(one, ten)
		self.assertLessEqual(one, ten)
		self.assertLessEqual(ten, ten)

	def test_unit_math(self):
		G = si.Measure(9.81, unit=si.BaseUnits.m) /\
					   (si.Measure(1, unit=si.BaseUnits.s) ** 2)
		dist = si.Measure(49.05, unit=si.BaseUnits.m)
		time_ = si.Measure(5, 'd', unit=si.BaseUnits.s)
		time2 = si.Measure(10, unit=si.BaseUnits.s)
		speed1 = G * time2
		speed2 = dist / time_
		volts = si.Measure(120, unit=si.DerivedUnits.V)
		amps = si.Measure(2, unit=si.BaseUnits.A)
		powerfactor = si.Measure(9, 'd', unit=si.BaseUnits.PF)
		newton = si.Measure(1, unit=si.DerivedUnits.N)
		power = (newton * dist) / time2
		voltamps = volts * amps
		power2 = voltamps * powerfactor

		self.assertEqual(speed1, speed2)

		with self.assertRaises(UnitError):
			_ = time_ + dist

		with self.assertRaises(UnitError):
			_ = dist - G

		_ = time_ + time2
		self.assertEqual(_.unit, si.BaseUnits.s)

		_ = speed1 + speed2
		self.assertEqual(_.unit, si.BaseUnits.m / si.BaseUnits.s)

		self.assertEqual(power.unit, power2.unit)
		self.assertEqual(power.unit, si.DerivedUnits.W)
		self.assertEqual(voltamps.unit, si.DerivedUnits.VA)
		self.assertNotEqual(power.unit, si.DerivedUnits.VA)

		return

	def tearDown(self):
		return

def test_all():
	runner = unittest.TextTestRunner(verbosity=2)
	test_suite = unittest.TestLoader().loadTestsFromTestCase(SITest)
	# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase())
	runner.run(test_suite)
	return

if __name__ == "__main__":
	test_all()
