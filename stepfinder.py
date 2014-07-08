import scipy.stats
import pylab
import matplotlib.pyplot as plt
import numpy as np
import csv
import os, sys, datetime, time

path = raw_input("Location of files: ")
dirs = os.listdir(path)

timestamp = time.time() 
value = datetime.datetime.fromtimestamp(timestamp)
currenttime = value.strftime('%Y%m%d_%H%M%S')

report = open('/Users/chlorite/Desktop/Dropbox/Code/Test data/Analysed data/' + currenttime + '_report', "w")
report.write(currenttime + '\n')

threshold = int(raw_input("Threshold: "))
report.write('Threshold = ' + str(threshold) + '\n')

width = int(raw_input("Width: "))
a=w=width
report.write('width of data samples = ' + str(width) + '\n')

for file in dirs:
	if '.csv' in file:
		datafile = path + '/' + file
		datafilename = file.strip(".csv")
		report.write(datafilename + '\n')
		noisefile = datafile.replace(".csv", "noise.txt")

	posbase=[]

	f = open(noisefile, 'r')
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

	#set the width of the samples of data to compare in the t test in number of samples
	
	pos1=[]
	pos2=[]
	steps=[]
	timeswtvalue=[]
	tvalue=[]
	stepnumber=[]
	times=[]
	#all the times from (time) which have a t value outside threshold
	position=[]

	#set the t test threshold (could be calculated by finding the number of degrees of
	#freedom which is number of samples*2 - 2 then looking up in a table)
	
	#Go through all samples creating a list of w samples before (pos1) and w samples 
	#after (pos2) then comparing the sample lists using the t test. Determine if the t value is above
	#the threshold and if so assign the time value to either a list of forward steps (fsteps)
	#or backsteps (bsteps) and save the index of the step in the main (time) array as an array
	#called (stepnumber). (Steps) contains the index and time of each detected value outside the 
	#t threshold in the (time) array.

	#Create a list of all the time values and position values that have a corresponding t value (timeswtvalue) 
	#and a list of all the t values (tvalue). Empty the t test sample arrays (pos1 and pos2)
	for k in range(0, len(pos)-(2*w+2)):
		for i in range(a-w, a):
			pos1.append(float(pos[i]))
		for j in range(a+1, a+w+1):
			pos2.append(float(pos[j]))
		t, prob = scipy.stats.ttest_ind(pos1, pos2, equal_var=True)
		if t>0 and t>threshold:
			times.append(time[a])
			stepnumber.append(a)
		if t<0 and t<-threshold:
			times.append(time[a])
			stepnumber.append(a)
		steps=[stepnumber, times]
		timeswtvalue.append(time[a])
		tvalue.append(float(t))
		position.append(float(pos[a]))
		del pos1[:]
		del pos2[:]
		a=a+1
	a=w=width

	time[:] = [x - time[0] for x in time]

	#plot the t value at each time
	f1=plt.figure("t test")
	plt.plot(timeswtvalue,tvalue)
	plt.axhline(threshold, linewidth=0.5, color='r')
	plt.axhline(-threshold, linewidth=0.5, color='r')
	plt.xlabel("Time / s", fontsize=18)
	plt.ylabel("t value", fontsize=18)
	a1=time[0]
	a2=time[-1]
	plt.xlim(xmin=a1, xmax=a2)

	savefilename1 = '/Users/chlorite/Desktop/Dropbox/Code/Test data/Analysed data/' + datafilename + 'ttest.png'
	plt.savefig(savefilename1)
	plt.clf()

	stepstarts=[]
	#the time values form (time) at which step is first detected (first t value above threshold)
	stepends=[]
	#the time values form (time) at which steps is last detected (next value has t under threshold)
	stepstartspos=[]
	stependpos=[]


	#set the first step start time in (stepstarts) as the first value in (times) 
	#then go through the values in (times) and if the next time value in the forward 
	#step times list differs by more than 0.001s from the previous value, this next value is 
	#also added to (stepstarts) and the previous value is added to (stepends). Result is
	#arrays containing the start and end of each part of t sequence outside threshold. Step
	#position is maximum between these values. Stepstartspos and stependpos contain the 
	#indices of the time values in the main array (time). 

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
	stop=len(stepstarts)
	for y in range(0,stop):
		b=stepstartspos[y]-w
		c=stependpos[y]-w
		maximum = max(tvalue[b:c+1])
		maxpos = tvalue.index(maximum)
		inpos.append(maxpos+w)
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

	pos[:] = [x - baseline for x in pos]
	filtered[:]=[x - baseline for x in filtered]

	for i in range(0, len(avepos)):
		avepos[i]=avepos[i]-baseline

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

	rows = zip(steppos, length, avepos, distance, force, direction)
	rows2 = zip(time, filtered)


	stepdatafile = '/Users/chlorite/Desktop/Dropbox/Code/Test data/Analysed data/' + datafilename + 'stepdata.csv'

	import csv
	writer = csv.writer(open(stepdatafile, "wb"))
	writer.writerow(["Step time / s", "Step length / s", "Average position / m", "Step length / nm", "Average force / pN", "Forward/Backward (f/b)"])
	for row in rows:
	    writer.writerow(row)
	
	tracedatafile = '/Users/chlorite/Desktop/Dropbox/Code/Test data/Analysed data/' + datafilename + 'trace.csv'

	import csv
	writer = csv.writer(open(tracedatafile, "wb"))
	writer.writerow(["Time / s", "filtered / m"])
	for row in rows2:
	    writer.writerow(row)

	#plot the position at each time
	
	f2=plt.figure("Step trace")
	plt.plot(time, filtered, 'b')
	plt.xlabel("Time / s", fontsize=18)
	plt.ylabel("Position / m", fontsize=18)
	for i in range(0, len(steppos)-1):
		start=(steppos[i]-time[0])/(time[-1]-time[0])
		end=(steppos[i+1]-time[0])/(time[-1]-time[0])
		plt.axhline(y=avepos[i], xmin=start, xmax=end, linewidth=1, color='r')
	start = (steppos[-1]-time[0])/(time[-1]-time[0])
	plt.axhline(y=avepos[-1], xmin=start, xmax=1, linewidth=1, color='r')
	a1=time[0]
	a2=time[-1]
	plt.xlim(xmin=a1, xmax=a2)

	savefilename2 = '/Users/chlorite/Desktop/Dropbox/Code/Test data/Analysed data/' + datafilename + 'trace.png'
	plt.savefig(savefilename2)
	plt.clf()

report.close()
	

	




	