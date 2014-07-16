from pylab import *
from matplotlib.widgets import Slider, Button, RadioButtons

#Plot initial threshold line
ax = subplot(211)
subplots_adjust(left=0.25, bottom=0.25)
t = range(-10, 11)
a0=10
s1 = [a0 for x in t]
s2 = [-a0 for x in t]
t_data = [x * 2 for x in t]
l, = plot(t,s1, lw=2, color='red')
m, = plot(t,s2, lw=2, color='red')
k, = plot(t, t_data, lw=2, color='blue')
axis([-10, 10, -20, 20])


vals_x=[]
vals_y=[]
ax = subplot(212)
for i in range(0, len(t)):
	if abs(t_data[i]) > a0:
		vals_x.append(t[i])
		vals_y.append(t_data[i])
n, = plot(vals_x, vals_y, 'bo')
axis([-10, 10, -20, 20])

# Defines the position and size of slider
axamp  = axes([0.25, 0.15, 0.65, 0.03])

#Set slider properties
samp = Slider(axamp, 'Threshold', 0.0, 20.0, valinit=a0)


newvals_y=[]
newvals_x = []
#Update slider function
def update(val):
	newvals_y=[]
	newvals_x=[]
	amp = samp.val
	l.set_ydata([amp for x in t])
	m.set_ydata([-amp for x in t])
	draw()
	for i in range(0, len(t)):
		if abs(t_data[i]) > amp:
			newvals_x.append(t[i])
			newvals_y.append(t_data[i])
			n.set_ydata(newvals_y)
			n.set_xdata(newvals_x)
			draw()
samp.on_changed(update)

#position and size of reset button
resetax = axes([0.8, 0.025, 0.1, 0.04])

#Reset when button pressed function
button = Button(resetax, 'Reset', hovercolor='0.975')
def reset(event):
    samp.reset()
button.on_clicked(reset)

show()