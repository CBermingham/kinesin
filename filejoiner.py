import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()

f = open(file_path, 'r')
lines=f.readlines()
f.close()

pos=[]
time=[]
filtered=[]

for l in lines:
	p = l.split()
	pos.append(float(p[7]))
	time.append(float(p[6]))
	filtered.append(float(p[9]))

endtime=time[-1]

var = raw_input("Add another file? (enter y or n) ")

while var == 'y':
	root = Tkinter.Tk()
	root.withdraw()
	file_path = tkFileDialog.askopenfilename()
	f = open(file_path, 'r')
	lines=f.readlines()
	f.close()
	del lines[0]
	for l in lines:
		p = l.split()
		pos.append(float(p[7]))
		time.append(endtime+float(p[6]))
		filtered.append(float(p[9]))
	endtime=time[-1]
	var = raw_input("Add another file? (enter y or n) ")

rows = zip(time, pos, filtered)

import csv
name = raw_input("Enter filename: ")
writer = csv.writer(open(name, "wb"))
for row in rows:
    writer.writerow(row)

