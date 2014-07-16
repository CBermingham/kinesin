import scipy.stats
import pylab
import matplotlib.pyplot as plt
import numpy as np
import csv
import os, sys, datetime, time


path = raw_input("Location of raw data files: ")
dirs = os.listdir(path)

timestamp = time.time() 
value = datetime.datetime.fromtimestamp(timestamp)
currenttime = value.strftime('%Y%m%d_%H%M%S')

analysedpath = "/Users/chlorite/Desktop/Dropbox/Code/Test_data/Analysed_data/"

report = open(analysedpath + currenttime + '_report', "w")
report.write(currenttime + '\n')
report.write("Location of raw data files:" + path)

width = int(raw_input("Width: "))
a=w=width
report.write('width of data samples = ' + str(width) + '\n')

for file in dirs:
	if not file.startswith('.'):
		if '.csv' in file:
			datafile = path + '/' + file
			datafilename = file.strip(".csv")
			report.write(datafilename + '\n')
			noisefile = datafile.replace(".csv", "noise.txt")

 	posbase=[]

 	f = open(noisefile, 'rU')
 	lines=f.readlines()
 	f.close()

 	for l in lines:
 		b = l.split()
 		posbase.append(float(b[9]))

 	baseline=float(sum(posbase)/len(posbase))

 	pos=[]
 	time=[]
 	filtered=[]

 	with open(datafile, 'rU') as data:
 	    reader = csv.reader(data)
 	    for row in reader:
 	    	time.append(float(row[0]))
 	    	pos.append(float(row[1]))
 	    	filtered.append(float(row[2]))

 	pos[:] = [x - baseline for x in pos]
 	time[:] = [x - time[0] for x in time]
	filtered[:]=[x - baseline for x in filtered]	    	

 	pos1=[]
 	pos2=[]
	tvalue=[]

	#Create a list of all the time values and position values that have a corresponding t value (timeswtvalue) 
	#and a list of all the t values (tvalue). Empty the t test sample arrays (pos1 and pos2)
	for i in range(a-w, a):
		pos1.append(float(pos[i]))
	for j in range(a+1, a+w+1):
		pos2.append(float(pos[j]))

# Last point is 1000+len(pos)-(2*w+2) so the last point in the last pos2 array is len(pos)-1
	for k in range(0, len(pos)-(2*w+1)):
		t, prob = scipy.stats.ttest_ind(pos1, pos2, equal_var=True)
		tvalue.append(float(t))
		del pos1[0]
		del pos2[0]
		pos1.append(pos[a])
		pos2.append(pos[a+w+1])
		a=a+1
	a=w=width

	del pos[:1000]
	del pos[-1001:]
	del filtered[:1000]
	del filtered[-1001:]
	del time[:1000]
	del time[-1001:]

	t_valuedatafile = analysedpath + datafilename + 't_values.csv'

	rows = zip(time, tvalue, filtered, pos)
	writer = csv.writer(open(t_valuedatafile, "wb"))
	writer.writerow(["Time / s", "t_value", "Filtered position", "Position"])
	for row in rows:
	    writer.writerow(row)

report.close()