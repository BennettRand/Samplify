import sys
import unittest

from measurements import si
from measurements import imperial

class ImperialTest(unittest.TestCase):
	def setUp(self):
		self.foot = imperial.ImperialDistance(feet = 1)
		self.foot_in_cm = si.Measure(30.48, 'c',si.BaseUnits.m)
		self.foot_in_inches = imperial.ImperialDistance(inches = 12)
		self.foot_in_thous = imperial.ImperialDistance(thous = 12000)
		self.yard_in_feet = imperial.ImperialDistance(feet = 3)
		self.yard = imperial.ImperialDistance(yards = 1)
		self.yards_in_mile = imperial.ImperialDistance(yards = 1760)
		self.chains_in_mile = imperial.ImperialDistance(chains = 80)
		self.furlongs_in_mile = imperial.ImperialDistance(furlongs = 8)
		self.mile = imperial.ImperialDistance(miles = 1)
		return

	def test_metric_conversion(self):
		self.assertEqual(self.foot_in_cm, self.foot)
		self.assertEqual(self.foot_in_cm, self.foot.metric)
		self.assertEqual(self.foot, self.foot_in_cm)
		self.assertEqual(self.foot.metric, self.foot_in_cm)

	def test_conversions(self):
		self.assertEqual(self.foot_in_inches, self.foot)
		self.assertEqual(self.foot_in_thous, self.foot)
		self.assertEqual(self.yard_in_feet, self.yard)
		self.assertEqual(self.yards_in_mile, self.mile)
		self.assertEqual(self.chains_in_mile, self.mile)
		self.assertEqual(self.furlongs_in_mile, self.mile)

	def tearDown(self):
		return

def test_all():
	runner = unittest.TextTestRunner(verbosity=2)
	test_suite = unittest.TestLoader().loadTestsFromTestCase(ImperialTest)
	# test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase())
	runner.run(test_suite)
	return

if __name__ == "__main__":
	test_all()
