import unittest

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
