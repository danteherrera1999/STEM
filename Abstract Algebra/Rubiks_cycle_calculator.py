import numpy as np
import matplotlib.pyplot as plt


"""
This code takes a rubiks cube sequence (in Singmaster notation) and calculates the number of repititions of that sequence required to return to a solved cube
"""

# The entire set of permutations can be found with U, x, and z
I = np.identity(9*6).astype(int)
U = I[:,(6,3,0,7,4,1,8,5,2,18,19,20,12,13,14,15,16,17,27,28,29,21,22,23,24,25,26,36,37,38,30,31,32,33,34,35,9,10,11,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53)]
x = I[:,(9,10,11,12,13,14,15,16,17,45,46,47,48,49,50,51,52,53,24,21,18,25,22,19,26,23,20,8,7,6,5,4,3,2,1,0,38,41,44,37,40,43,36,39,42,35,34,33,32,31,30,29,28,27)]
z = I[:,(42,39,36,43,40,37,44,41,38,15,12,9,16,13,10,17,14,11,6,3,0,7,4,1,8,5,2,29,32,35,28,31,34,27,30,33,51,48,45,52,49,46,53,50,47,24,21,18,25,22,19,26,23,20)]
A = np.arange(54).astype(int)
inv = lambda M: np.linalg.inv(M)
# Recursive matmul for successive transformations
mm = lambda *args: np.matmul(args[0],(mm(*args[1:]) if len(args)>2 else args[1]))
moves = {
	"e":I,
	"U":U,
	"U'":inv(U),
	"D":mm(x,x,U,inv(x),inv(x)),
	"D'":mm(x,x,inv(U),inv(x),inv(x)),
	"L":mm(z,U,inv(z)),
	"L'":mm(z,inv(U),inv(z)),
	"R":mm(inv(z),U,z),
	"R'":mm(inv(z),inv(U),z),
	"F":mm(x,U,inv(x)),
	"F'":mm(x,inv(U),inv(x)),
	"B":mm(inv(x),U,x),
	"B'":mm(inv(x),inv(U),x)
}

def generate_PM(sequence):
	return mm(*[moves[s] for s in sequence.split(',')])
def generate_arr(sequence):
	return np.matmul(A,generate_PM(sequence)).astype(int)

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

def get_cycle_length(seq):
	cycle_pms = [x for x,y in PM(generate_arr(seq)+1)[:-1]]
	cycle_lengths = [cyc.size for cyc in cycle_pms]
	return np.lcm.reduce(cycle_lengths)

seq = "U,L',U',L,R,L',R'"
#seq = "U,U"
cl = get_cycle_length(seq)

print(cl)








