print("Importing pyplot...")
import matplotlib.pyplot as pyplot
print("Done!\nImporting scipy...")
from scipy.stats import linregress
print("Done!\nImporting csv...")
import csv
print("Done!")


def readTimes():
	times = []
	with open("times.csv", newline = "") as saveFile:
		reader = csv.reader(saveFile, delimiter=",")
		for row in reader:
			times.append(row[0])

	times = [float(time) for time in times]
	return times


def plot(times, slope, intercept):
	pyplot.rcParams["figure.figsize"] = (16, 9)
	print("Plotting...")
	pyplot.scatter(times.index(max(times)), max(times), color = "r", lw = 3.0)
	pyplot.scatter(times.index(min(times)), min(times), color = "r", lw = 3.0)
	pyplot.annotate("Worst time: " + str(max(times)), xy = (times.index(max(times)), max(times)), xytext = (times.index(max(times)) + times.index(max(times)) / 100, max(times) + max(times) / 100))
	pyplot.annotate("Best time: " + str(min(times)), xy = (times.index(min(times)), min(times)), xytext = (times.index(min(times)), min(times) - min(times) / 30))
	pyplot.plot(range(len(times)), times, lw = 2.0, color = "#0099ff")
	trend = [slope * i + intercept for i in [-1, len(times)]]
	pyplot.plot([-1, len(times)], trend, lw = 2.0, color = "r", label = "Trend")
	pyplot.axis([-1, len(times), min(times) - (min(times) / 10), max(times) + (max(times) / 10)])
	pyplot.xlabel("Solves")
	pyplot.ylabel("Seconds")
	print("Done!\nSaving...")
	pyplot.savefig("plot.png", bbox_inches = "tight", dpi = 200)
	print("Done!")
	#pyplot.show()


times = readTimes()
slope, intercept, r_value, p_value, std_err = linregress(range(len(times)), times)
plot(times, slope, intercept)