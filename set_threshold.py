import scipy.stats
import pylab
import matplotlib.pyplot as plt
import numpy as np
import csv
import os, sys, datetime, time

datafolder = raw_input("Data folder: ")

datafile = raw_input("t-values datafile: ")

t_file = datafolder + "/" + datafile

analysedpath = "/Users/chlorite/Desktop/Dropbox/Data/140806/Graphs/"

cont = 'n'

while cont == 'n':

	threshold = int(raw_input("Threshold: "))
	thresh = str(threshold)

	timeswtvalue = []
	tvalue = []
	filtered = []
	pos = []

	with open(t_file, 'rU') as data:
	 	    reader = csv.reader(data)
	 	    next(reader, None)
	 	    for row in reader:
	 	    	timeswtvalue.append(float(row[0]))
	 	    	tvalue.append(float(row[1]))
	 	    	filtered.append(float(row[2]))
	 	    	pos.append(float(row[3]))

	overTtimes = []
	stepnumber = []


	for k in range(0, len(tvalue)):
		if abs(tvalue[k])>threshold:
			overTtimes.append(timeswtvalue[k])
			stepnumber.append(k)

	steps = [stepnumber, overTtimes]

	stepstarts=[]
	#the time values form (time) at which step is first detected (first t value above threshold)
	stepends=[]
	#the time values form (time) at which steps is last detected (next value has t under threshold)
	stepstartspos=[]
	stependpos=[]

	stepstarts.append(steps[1][0])
	stepstartspos.append(steps[0][0])
	prev=steps[1][0]

	times = steps[1][1:]
	for q in times:
		if q-prev>0.001:
			stepstarts.append(q)
			stepends.append(prev)
			i=times.index(q)
			stepstartspos.append(steps[0][i])
			j=times.index(prev)
			stependpos.append(steps[0][j])
		prev=q
	stepends.append(steps[1][-1])
	stependpos.append(steps[0][-1])

	maxpos=[]
	steppos=[]
	avepos=[]
	inpos=[]
	l=[]

	#maximum is the max t value of each t bump. (maxpos) is a list of the indices in tvalue where this occurs,
	#this corresponds to index of that plus w in the main (time) array. maxpos contains the position of each step 
	#(where t is maximum) in the list (tvalue). (steppos) is the times at which these steps occur. The index in 
	#(time) at which these occur will be maxpos+w, stored in (inpos)

	tvalue[:]=[abs(x) for x in tvalue]
	for y in range(0,len(stepstarts)):
		b=stepstartspos[y]
		c=stependpos[y]
		maximum = max(tvalue[b:c+1])
		maxpos = tvalue.index(maximum)
		inpos.append(maxpos)
		d=timeswtvalue[maxpos]
		steppos.append(d)


	for x in range (0, len(inpos)-1):
		h=inpos[x+1]
		g=inpos[x]
		l=pos[g:h]
		ave = float(sum(l)/len(l))
		avepos.append(ave)

	#avepos are the average positions of each step
	g=inpos[-1]
	l=pos[g:-1]
	ave=float(sum(l)/len(l))
	avepos.append(ave)

	#length is the time each step waits after the actual step up or down, i.e. the dwell time.
	#last step doesn't have one because no end
	length=[]
	for i in range(1, len(steppos)):
		l=steppos[i]-steppos[i-1]
		length.append(l)
	length.append(None)


	distance=[]
	direction=[]

	g=inpos[0]
	l=pos[0:g]
	startave=float(sum(l)/len(l))

	d=(avepos[0]-startave)*10**9
	if d<0 and abs(d)<12:
		direction.append("b")
	if d>0 and d<12:
		direction.append("f")
	if abs(d)>12:
		direction.append("d")
	d=abs(d)
	distance.append(d)

	for i in range(1, len(steppos)):
		d=(avepos[i]-avepos[i-1])*10**9
		if d<0 and abs(d)<12:
			direction.append("b")
		if d>0 and d<12:
			direction.append("f")
		if abs(d)>12:
			direction.append("d")
		d=abs(d)
		distance.append(d)

	force=[]
	for i in avepos:
		f=i*3*10**(-5)*10**12
		force.append(f)

	f2=plt.figure("Step trace")
	plt.plot(timeswtvalue, filtered, 'b')
	plt.xlabel("Time / s", fontsize=18)
	plt.ylabel("Position / m", fontsize=18)
	for i in range(0, len(steppos)-1):
		start=(steppos[i]-timeswtvalue[0])/(timeswtvalue[-1]-timeswtvalue[0])
		end=(steppos[i+1]-timeswtvalue[0])/(timeswtvalue[-1]-timeswtvalue[0])
		plt.axhline(y=avepos[i], xmin=start, xmax=end, linewidth=1, color='r')
	start = (steppos[-1]-timeswtvalue[0])/(timeswtvalue[-1]-timeswtvalue[0])
	plt.axhline(y=avepos[-1], xmin=start, xmax=1, linewidth=1, color='r')
	a1=timeswtvalue[0]
	a2=timeswtvalue[-1]
	plt.xlim(xmin=a1, xmax=a2)
	graphsavename = analysedpath + datafile.replace("t_values.csv", '_T') + thresh + '.png' 
	plt.savefig(graphsavename)
	plt.show()

	cont = raw_input("Threshold ok? (y/n): ")

plotdatafile = analysedpath + datafile.replace("t_values.csv", '_T') + thresh + '_plotdata.csv'
rows = zip(timeswtvalue, tvalue, filtered, pos)
writer = csv.writer(open(plotdatafile, "wb"))
writer.writerow(["Time / s", "t_value", "Filtered position / m", "Position / m"])
for row in rows:
    writer.writerow(row)



stepdatafile = analysedpath + datafile.replace("t_values.csv", "_T") + thresh + '_stepdata.csv'
rows2 = zip(steppos, length, avepos, distance, force, direction)
writer = csv.writer(open(stepdatafile, "wb"))
writer.writerow(["Step time / s", "Step length / s", "Average position / m", "Step length / nm", "Average force / pN", "Forward/Backward (f/b)"])
for row in rows2:
    writer.writerow(row)





	




	