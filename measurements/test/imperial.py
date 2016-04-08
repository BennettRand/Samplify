import sys
import unittest

from measurements import si
from measurements import imperial

class ImperialTest(unittest.TestCase):
	def setUp(self):
		return

	def test_metric_conversion(self):
		foot = imperial.ImperialDistance(feet = 1)
		foot_in_cm = si.Measure(30.48, 'c',si.BaseUnits.m)

		self.assertEqual(foot_in_cm, foot)
		self.assertEqual(foot_in_cm, foot.metric)
		self.assertEqual(foot, foot_in_cm)
		self.assertEqual(foot.metric, foot_in_cm)

	def test_conversions(self):
		foot = imperial.ImperialDistance(feet = 1)
		foot_in_inches = imperial.ImperialDistance(inches = 12)
		foot_in_thous = imperial.ImperialDistance(thous = 12000)
		yard_in_feet = imperial.ImperialDistance(feet = 3)
		yard = imperial.ImperialDistance(yards = 1)
		yards_in_mile = imperial.ImperialDistance(yards = 1760)
		chains_in_mile = imperial.ImperialDistance(chains = 80)
		furlongs_in_mile = imperial.ImperialDistance(furlongs = 8)
		mile = imperial.ImperialDistance(miles = 1)

		self.assertEqual(foot_in_inches, foot)
		self.assertEqual(foot_in_thous, foot)
		self.assertEqual(yard_in_feet, yard)
		self.assertEqual(yards_in_mile, mile)
		self.assertEqual(chains_in_mile, mile)
		self.assertEqual(furlongs_in_mile, mile)

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
