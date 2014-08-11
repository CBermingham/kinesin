import csv
import scipy.stats
import pylab
import matplotlib.pyplot as plt
import numpy as np
import math
import os, sys


path = raw_input("Location of stepdata.csv files to analyse: ")
dirs = os.listdir(path)

amplitude = []
load = []
dwell=[]
steptype=[]
rows=[]

for filename in dirs:
	if 'stepdata' in filename:
		f = open(path + '/' + filename, 'rU')
		reader = csv.reader(f, None) 
		next(reader, None)
		for row in reader:
			load.append(float(row[4]))
			amplitude.append(float(row[3]))
			steptype.append(row[5])
			dwell.append(row[1])
		del dwell[-1]
		f.close()


for i in dwell:
	i=float(i)

bload=[]
fload=[]
famplitude=[]
bamplitude=[]
damplitude=[]
bdwell=[]
fdwell=[]

#The following lists omit values with load less than 1pN
amplitude2=[]
load2=[]
steptype2=[]
fdwell2=[]
bdwell2=[]
dwell2=[]

#Go through columns, creating new lists only containing those with load greater than 1pN
for z in range(0, len(amplitude)):
	if abs(load[z])>=1:
		amplitude2.append(amplitude[z])
		load2.append(load[z])
		steptype2.append(steptype[z])

#Go through lists with load greater than 1 and create two lists for forward and back
#steps for amplitude, load and dwell
for x in range(0, len(amplitude2)):
	if steptype2[x]=='b':
		bamplitude.append(-amplitude2[x])
		bload.append(load2[x])

	if steptype2[x]=='f':
		famplitude.append(amplitude2[x])
		fload.append(load2[x])

	if steptype2[x]=='d':
		damplitude.append(amplitude2[x])


load3=[]
bload3=[]
fload3=[]
for z in range(0, len(dwell)):
	if abs(load[z])>=1:
		load3.append(load[z])
		dwell2.append(dwell[z])

for x in range(0, len(dwell2)-1):
	if steptype2[x]=='b':
		bdwell.append(dwell2[x])
		bload3.append(load2[x])

	if steptype2[x]=='f':
		fdwell.append(dwell2[x])
		fload3.append(load2[x])


dwelltot=[[] for i in range(15)]

for j in range(0, len(fload3)):
 	for i in range(0, 15):
 		if fload3[j]>=i and fload3[j]<i+1:
 			dwelltot[i].append(float(fdwell[j]))

dwellave=[]
dwellsem=[]
dwellaveload=[]
logdwellave=[]

for i in range(0,len(dwelltot)):
  	if len(dwelltot[i]) != 0:
  		dwellaveload.append(i+0.5)
  		dwellave.append(np.mean(dwelltot[i]))
  		dwellsem.append(np.std(dwelltot[i], ddof=1)/math.sqrt(len(dwelltot[i])))

for i in dwellave:
	logdwellave.append(math.log(i))

p_coeff=np.polyfit(dwellaveload, logdwellave, 1)
dwellavefit=[]
for f in range(0, len(dwellaveload)):
 	dwellavefit.append(math.exp(p_coeff[1]) * math.exp(p_coeff[0] * dwellaveload[f]))

print 'Dwell = %f * exp(%f * load)' % (math.exp(p_coeff[1]), p_coeff[0])

bsum=[]
fsum=[]
sizesum=[0]*15
bampvalues_foreachload=[[] for i in range(15)]
fampvalues_foreachload=[[] for i in range(15)]
ampvalues_foreachload=[[] for i in range(15)]

for x in range(0, len(bload)):
	for i in range(0,15):
		if bload[x]>=i and bload[x]<i+1:
			bampvalues_foreachload[i].append(bamplitude[x])
			ampvalues_foreachload[i].append(bamplitude[x])

bsum[:]=[len(bampvalues_foreachload[x]) for x in range(0,15)]

for x in range(0, len(fload)):
	for i in range(0,15):
		if fload[x]>=i and fload[x]<i+1:
			fampvalues_foreachload[i].append(famplitude[x])
			ampvalues_foreachload[i].append(famplitude[x])

fsum[:]=[len(fampvalues_foreachload[x]) for x in range(0,15)]


#Velocity (mean amplitude / mean dwell for each bin)
loadbins_velocity=[]
velocity=[]

for i in range(0,len(ampvalues_foreachload)):
  	if len(dwelltot[i]) != 0:
  		velocity.append(np.mean(ampvalues_foreachload[i]) / np.mean(dwelltot[i]))



for x in bamplitude:
	for i in range(0,15):
		if abs(x)>=i and abs(x)<i+1:
			sizesum[i]=sizesum[i]+1


for x in famplitude:
	for i in range(0,15):
		if x>=i and x<i+1:
			sizesum[i]=sizesum[i]+1


for x in damplitude:
	for i in range(0,15):
		if abs(x)>=i and abs(x)<i+1:
			sizesum[i]=sizesum[i]+1


ratio=[]
for i in range(0,15):
	if bsum[i]==0:
		ratio.append(0)
	else:
		ratio.append(float(fsum[i]/bsum[i]))

ampbins=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5]


ratio2=[]
loadbins=[]

for i in range(0,len(ratio)):
	if ratio[i]!=0:
		ratio2.append(ratio[i])
		loadbins.append(i+0.5)
ratio=ratio2


x=[]
y=[]
for i in range(0,len(loadbins)):
	x.append(loadbins[i])
	b=math.log(ratio[i])
	y.append(b)

p_coeff=np.polyfit(x, y, 1)
A=math.exp(p_coeff[1])
b=p_coeff[0]
print 'Ratio = %f * exp(%f * load)' % (A, b)

fit=[]
for f in range(0, len(x)):
	v=A*math.exp(b*x[f])
	fit.append(v)

stall=-math.log(A)/b

print 'Stall force = ',stall, 'pN'

aveamp=(sum(famplitude)-sum(bamplitude))/(len(famplitude)+len(bamplitude))
print 'Average step amplitude =', aveamp, 'nm'

fig1 = plt.figure()
plt.scatter(fload, famplitude, s=1, color='r', label='Forward steps')
plt.scatter(bload, bamplitude, s=1, color='b', label='Backward steps')
plt.ylabel("Amplitude / nm", fontsize=18)
plt.xlabel("Load / pN", fontsize=18)
plt.axhline(y=0, xmin=0, xmax=1, linewidth=1, color='k')
plt.ylim(ymin=-12, ymax=12)
plt.yticks([-12,-8,-4,0,4,8,12])

savefilename = path + '_amplitude.png'
plt.savefig(savefilename)

fig2 = plt.figure()
plt.scatter(fload3, fdwell, s=1, color='r', label='Forward steps')
plt.scatter(bload3, bdwell, s=1, color='b', label='Backward steps')
plt.errorbar(dwellaveload, dwellave, yerr=dwellsem, linestyle='', marker='o', markersize=5, mfc='r', color='r')
plt.plot(dwellaveload, dwellavefit, color='r')
plt.xlabel("Load / pN", fontsize=18)
plt.ylabel("Dwell time / s", fontsize=18)
plt.yscale('log')
plt.ylim(ymin=0.001)
plt.xlim(xmin=0)

savefilename = path + '_dwell.png'
plt.savefig(savefilename)

fig3 = plt.figure()
plt.scatter(loadbins, ratio)
plt.plot(x, fit)
plt.xlabel("Load / pN", fontsize=18)
plt.ylabel("Step ratio", fontsize=18)
plt.axhline(y=1, xmin=0, xmax=1, linewidth=1, color='k')
plt.yscale('log')
plt.xlim(xmin=0)

savefilename = path + '_ratio.png'
plt.savefig(savefilename)

fig4 = plt.figure()
plt.bar(ampbins, sizesum)
plt.xlabel("Step amplitude / nm", fontsize=18)
plt.ylabel("Frequency", fontsize=18)
plt.xlim(xmin=0, xmax=16)

savefilename = path + '_amp_histogram.png'
plt.savefig(savefilename)

fig5 = plt.figure()
plt.scatter(dwellaveload, velocity)
plt.xlabel("Load / pN", fontsize=18)
plt.ylabel("Velocity / nm / s", fontsize=18)
plt.xlim(xmin=0)

savefilename = path + '_velocity.png'
plt.savefig(savefilename)

plt.show()

