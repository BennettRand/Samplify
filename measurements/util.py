from si import *
import logging

def plot_timeseries_with_pyplot(ts):
	try:
		import matplotlib.pyplot as plt
	except ImportError:
		logging.error("pyplot could not be imported")
		return

	serieses = set([x[1].pre_str() + unit_find(x[1].unit)
					for x in ts.datapoints])
	serieses = {s:([],[]) for s in serieses}

	for d in ts.datapoints:
		u = d[1].pre_str() + unit_find(d[1].unit)
		serieses[u][0].append(d[0])
		serieses[u][1].append(d[1].value)

	for s in serieses:
		plt.plot(*serieses[s])

	plt.legend(serieses.keys())
	plt.show()
	return
