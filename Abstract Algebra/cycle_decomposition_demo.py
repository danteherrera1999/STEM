import numpy as np
import matplotlib.pyplot as plt

"""
Okay this is a bit of a doozy ngl. But basically its a visual aid to show how any permutation
of a set can be broken down into disjoint cycles. Its easy to see from this that any disjoint
cycles will commute with eachother, as they do not affect the same elements of the set.
The functions can be modified pretty easily to break a specific permutation into its constituent
cycles, but in its current form it generates a random permutation on the set of integers from 1->N
and then finds and plots the cycles of that random permutation.
"""

# Recursive matmul for successive transformations
mm = lambda *args: np.matmul(args[0],(mm(*args[1:]) if len(args)>2 else args[1]))

def gpm(I,c):
	pm = np.copy(I)
	pm[c] = pm[np.roll(c,1)]
	return pm

def cd(B):
	A = np.arange(len(B))
	B = np.array(B)-1
	cycles = []
	for i in A:
		cycle = [i]
		j = B[cycle[-1]]
		while j not in cycle:
			cycle.append(j)
			j = B[j]
		if not any(i+1 in sub for sub in cycles) and len(cycle)>=2:
			cycles.append(np.array([k+1 for k in cycle]))
	return cycles

def PM(B):
	I = np.identity(len(B)).astype(int)
	cycles = cd(B)
	cycle_pms = []
	for cycle in cycles:
		cycle_pm = gpm(I,cycle-1)
		cycle_pms.append([cycle,cycle_pm])
	PM_Total = mm(*[y for (x,y) in cycle_pms]) if len(cycle_pms)>1 else cycle_pms[0][1]
	return cycle_pms+[["Total",PM_Total]]

def generate_random_cycles(N):
	A = np.arange(N)
	B = np.copy(A)+1
	np.random.shuffle(B)
	cycle_pms = PM(B)
	return cycle_pms,B

def run_plots(N):
	A = np.arange(N)+1
	cycle_pms,B = generate_random_cycles(N)
	n = len(cycle_pms)
	#Order is automatically set to the longest time for any one cycle to return to itself
	steps = np.max([len(cycle_pm[0]) for cycle_pm in cycle_pms[:-1]])+1
	#Generate Data
	data =[]	
	for cycle_pm in cycle_pms:
		temp_data = [np.matmul(A,cycle_pm[1])]
		for step in range(1,steps):
			temp_data.append(np.matmul(temp_data[-1],cycle_pm[1]))
		data.append(temp_data)
	data = np.array(data)

	# PLOT DATA
	print(f"generating {n} plots")
	fig,axs = plt.subplots(n)
	for i in range(n):
		axs[i].plot(data[i])
		axs[i].set_ylabel(f'{cycle_pms[i][0]}',rotation=45)
	fig.suptitle(f'Cycle Decomposition of {A}->{B}')
	plt.show()
	


#SETUP PARAM
N = 10

run_plots(N)






