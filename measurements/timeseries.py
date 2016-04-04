import time
import zlib
import bz2
import struct
import base64
import datetime

# from . import *
from si import *

_EPOCH = datetime.datetime.utcfromtimestamp(0)

def epoch_secs(dt):
    return float((dt - _EPOCH).total_seconds())

class Timeseries(object):
	def __init__(self):
		self.datapoints = []

	def append(self, measure, timestamp=None):
		if timestamp is None:
			timestamp = datetime.datetime.utcnow()
		elif isinstance(timestamp, (int,float)):
			timestamp = datetime.datetime.utcfromtimestamp(timestamp)
		elif isinstace(timestamp, datetime.datetime):
			pass
		else:
			raise TypeError("Not a datetime, int, or float type")

		if isinstance(measure, Measure):
			self.datapoints.append((timestamp, measure))
		elif isinstance(measure, NonStandard):
			self.datapoints.append((timestamp, measure.metric))
		else:
			raise TypeError("Not a Measurement type")

	def get_timestamps(self):
		return [x[0] for x in self.datapoints]

	def get_measurements(self):
		return [x[1] for x in self.datapoints]

	def binarize_timestamps(self):
		return "".join([struct.pack("!d", epoch_secs(x)) for x in
						self.get_timestamps()])

	def binarize_measurements(self):
		return "".join([x.binarize() for x in self.get_measurements()])

	@property
	def length(self):
		return len(self.datapoints)

	def binarize(self):
		ret = struct.pack("!Q", self.length)
		ret += self.binarize_timestamps()
		ret += self.binarize_measurements()

		return ret

	def compress(self, compressor=bz2.compress, level=9):
		return compressor(self.binarize(), level)

	def stringify(self):
		return base64.b64encode(self.compress())

	@staticmethod
	def debinarize(data):
		ret = Timeseries()
		data_len = struct.unpack("!Q", data[:8])[0]

		ts_end = 8 + 8 * data_len

		timestamps = struct.unpack("!" + "d" * data_len, data[8:ts_end])

		measurement_bin = data[ts_end:]
		measurements = []
		for x in xrange(data_len):
			measurements.append(Measure.from_binary(\
								measurement_bin[x * Measure.BIN_STRUCT.size:\
								(x + 1) * Measure.BIN_STRUCT.size]))

		for ts, m in zip(timestamps, measurements):
			ret.append(m, ts)

		return ret

	@staticmethod
	def decompress(data, decompressor=bz2.decompress):
		return Timeseries.debinarize(decompressor(data))

	@staticmethod
	def destringify(data):
		return Timeseries.decompress(base64.b64decode(data))

	def timeslice(self, i, j):
		ret = Timeseries()

		for ts, m in self.datapoints:
			if i < ts < j:
				ret.append(m, ts)

		return ret

	def __getitem__(self, i):
		return self.datapoints[i]
