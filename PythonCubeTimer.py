import datetime
import csv
import os
import configparser
import plot
from collections import OrderedDict
from math import ceil, floor, sqrt
from tkinter import *
from tkinter import ttk
from time import sleep, perf_counter


def writeTime(time):
	with open("times.csv", "a", newline="") as times:
		writer = csv.writer(times)
		writer.writerow([time, "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())])


def readTimes():
	times = []
	with open("times.csv", newline = "") as saveFile:
		reader = csv.reader(saveFile, delimiter=",")
		for row in reader:
			times.append(row[0])

	times = [float(time) for time in times]
	return times


class application():
	def __init__(self):
		self.root = Tk()
		self.root.title("Cubing Timer")
		self.root.option_add("*tearOff", False)
		self.initGUI()
		self.root.config(menu = self.menuBar)
		self.root.resizable(0, 0)
		self.root.mainloop()
	
	
	def calcStats(self, times):
		self.solves.set("Solves: " + str(len(times)))
	
		last3Times = times[-3:]
		sumLast3Times = sum(last3Times)
		self.ao3.set("Ao3: " + str(round(sumLast3Times / len(last3Times), 3)))
	
		last5Times = times[-5:]
		sumLast5Times = sum(last5Times)
		self.ao5.set("Ao5: " + str(round(sumLast5Times / len(last5Times), 3)))
		
		last12Times = times[-12:]
		last12Times.pop(last12Times.index(max(last12Times)))
		last12Times.pop(last12Times.index(min(last12Times)))
		sumLast12Times = sum(last12Times)
		self.ao12.set("Ao12: " + str(round(sumLast12Times / len(last12Times), 3)))
	
		last50Times = times[-50:]
		sumLast50Times = sum(last50Times)
		self.ao50.set("Ao50: " + str(round(sumLast50Times / len(last50Times), 3)))
	
		last100Times = times[-100:]
		sumLast100Times = sum(last100Times)
		self.ao100.set("Ao100: " + str(round(sumLast100Times / len(last100Times), 3)))
	
		last1000Times = times[-1000:]
		sumLast1000Times = sum(last1000Times)
		self.ao1000.set("Ao1000: " + str(round(sumLast1000Times / len(times), 3)))
		
		totalTime = sum(times)
		self.average.set("Average: " + str(round(totalTime / len(times), 3)))
		
		sortedTimes = sorted(times)
		if len(sortedTimes) % 2 == 0:
			median = round(sortedTimes[ceil(len(sortedTimes) / 2)], 3)
		else:
			median = round((sortedTimes[floor(len(sortedTimes) / 2)] + sortedTimes[ceil(len(sortedTimes) / 2)]) / 2, 3)
	
		self.median.set("Median: " + str(median))
	
		average = sum(times) / len(times)
		deviations = [(x - average) ** 2 for x in times]
		variance = sum(deviations) / len(deviations)
		standardDeviation = sqrt(variance)
		self.standardDeviation.set("SD: " + str(round(standardDeviation, 3)))
	
		self.best.set("Best: " + str(min(times)))
		
		self.worst.set("Worst: " + str(max(times)))
	
		self.latest.set("Latest: " + str(times[-1]))
	
	
	def updateTimer(self):
		self.elapsedTime = int(floor(perf_counter() - self.start))
		self.minutes, self.seconds = divmod(self.elapsedTime, 60)
		self.timerLabel.configure(text = "%02d:%02d" % (self.minutes, self.seconds))
		self.root.after(1000, self.updateTimer)
	
	
	def updateImage(self, times):
		plot.plot(times)
		self.image = PhotoImage(file = "plot.png")
		self.plotImage.configure(image = self.image)
	
	
	def timer(self):
		self.start = perf_counter()
		self.timerWindow = Toplevel(self.root)
		self.timerWindow.title("Timer")
		self.timerWindow.resizable(0, 0)
		
		self.timerLabel = ttk.Label(self.timerWindow, text = "00:00", font = ("Courier", 64))
		self.timerLabel.grid(column = 0, row = 0, sticky = (N, E, S, W))
		
		self.startButton = ttk.Button(self.timerWindow, text = "START", width = 40, command = self.updateTimer)
		self.startButton.grid(column = 0, row = 1, sticky = (S))
	

	def initGUI(self):
		self.mainframe = ttk.Frame(self.root, padding = "3 3 3 3")
		self.mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
		self.mainframe.columnconfigure(0, weight = 1)
		self.mainframe.rowconfigure(0, weight = 1)
		
		self.menuBar = Menu(self.root)
		self.menuBar.add_command(label = "Quit", command = self.root.quit)
		
		self.solves = StringVar()
		self.ao3 = StringVar()
		self.ao5 = StringVar()
		self.ao12 = StringVar()
		self.ao50 = StringVar()
		self.ao100 = StringVar()
		self.ao1000 = StringVar()
		self.average = StringVar()
		self.median = StringVar()
		self.best = StringVar()
		self.worst = StringVar()
		self.latest = StringVar()
		self.standardDeviation = StringVar()
		
		self.solvesLabel = ttk.Label(self.mainframe, textvariable = self.solves)
		self.solvesLabel.grid(column = 1, row = 1, sticky = (E))
		self.ao3Label = ttk.Label(self.mainframe, textvariable = self.ao3)
		self.ao3Label.grid(column = 1, row = 2, sticky = (E))
		self.ao5Label = ttk.Label(self.mainframe, textvariable = self.ao5)
		self.ao5Label.grid(column = 1, row = 3, sticky = (E))
		self.ao12Label = ttk.Label(self.mainframe, textvariable = self.ao12)
		self.ao12Label.grid(column = 1, row = 4, sticky = (E))
		self.ao50Label = ttk.Label(self.mainframe, textvariable = self.ao50)
		self.ao50Label.grid(column = 1, row = 5, sticky = (E))
		self.ao100Label = ttk.Label(self.mainframe, textvariable = self.ao100)
		self.ao100Label.grid(column = 1, row = 6, sticky = (E))
		self.ao1000Label = ttk.Label(self.mainframe, textvariable = self.ao1000)
		self.ao1000Label.grid(column = 1, row = 7, sticky = (E))
		self.averageLabel = ttk.Label(self.mainframe, textvariable = self.average)
		self.averageLabel.grid(column = 1, row = 8, sticky = (E))
		self.medianLabel = ttk.Label(self.mainframe, textvariable = self.median)
		self.medianLabel.grid(column = 1, row = 9, sticky = (E))
		self.standardDeviationLabel = ttk.Label(self.mainframe, textvariable = self.standardDeviation)
		self.standardDeviationLabel.grid(column = 1, row = 10, sticky = (E))
		self.bestLabel = ttk.Label(self.mainframe, textvariable = self.best)
		self.bestLabel.grid(column = 1, row = 11, sticky = (E))
		self.worstLabel = ttk.Label(self.mainframe, textvariable = self.worst)
		self.worstLabel.grid(column = 1, row = 12, sticky = (E))
		self.latestLabel = ttk.Label(self.mainframe, textvariable = self.latest)
		self.latestLabel.grid(column = 1, row = 13, sticky = (E))
		
		times = readTimes()
		plot.plot(times, 1, 1, 1)
		self.image = PhotoImage(file = "plot.png")
		self.plotImage = ttk.Label(self.mainframe, image = self.image)
		self.plotImage.grid(column = 2, row = 1, rowspan = 13, sticky = (E))
		
		self.lowerFrame = ttk.Frame(self.mainframe, padding = "3 3 3 3")
		self.lowerFrame.grid(column = 1, columnspan = 2, row = 14, sticky = (N, S))
		
		self.timerButton = ttk.Button(self.lowerFrame, text = "TIMER", width = 160, command = self.timer)
		self.timerButton.grid(column = 0, row = 0, sticky = (W, E))
		
		for child in self.mainframe.winfo_children():
			child.grid_configure(padx = 2, pady = 2)
		
		self.calcStats(times)
	
	
application = application()