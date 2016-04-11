from . import imperial
from . import si

def run_all_tests():
	imperial.test_all()
	si.test_all()
	return

if __name__ == "__main__":
	run_all_tests()
