from random import random
import numpy as np

total_steps = 0
run_lengths = []

#Range sets the number of runs. b is a random number corresponding to the time taken
#for the rear, bound head to detach and f the same for the forward, free head to bind. 
#If b>f then the forward head binds before the back head detaches and a step is made.
for i in range(0, 100000):
	b = 0.0175
	f = 0.001
	total_steps = 0
	while b>f:
		b = 0.0175 + (random()-0.5)*0.02
		f = 0.001 + (random()-0.5)*0.02
		total_steps += 1
	run_lengths.append(total_steps*8)

print 'Average run length =', np.mean(run_lengths), '+/-', np.std(run_lengths), 'nm'