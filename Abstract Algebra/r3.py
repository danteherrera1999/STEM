import numpy as np
import matplotlib.pyplot as plt


"""
This code takes a rubiks cube sequence (in Singmaster notation) and calculates the number of repititions of that sequence required to return to a solved cube
The entire set of legal rubiks cube moves can be built with U, x, and z. That is to say, the subgroup of S_54 that is isomorphic to the rubik's cube is generated by the singmaster moves U, x, and z.
In fact, since 6 facets never move (the center facet of each face), the rubik's group can also be thought of as a subgroup of S_48. The fact that each possible permutation is cyclic is a natural consequence
of the fact that the group is finite. Since a group must contain all powers and products of its elements, an infinite ordered element would necessitate an infinite ordered group. It can be concluded then
that each element in the rubiks group is of finite order, and thus every possible permutation has some power which equals the neutral element.
"""
I = np.identity(9*6).astype(int)
U = I[:,(6,3,0,7,4,1,8,5,2,18,19,20,12,13,14,15,16,17,27,28,29,21,22,23,24,25,26,36,37,38,30,31,32,33,34,35,9,10,11,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53)]
x = I[:,(9,10,11,12,13,14,15,16,17,45,46,47,48,49,50,51,52,53,24,21,18,25,22,19,26,23,20,8,7,6,5,4,3,2,1,0,38,41,44,37,40,43,36,39,42,35,34,33,32,31,30,29,28,27)]
z = I[:,(42,39,36,43,40,37,44,41,38,15,12,9,16,13,10,17,14,11,6,3,0,7,4,1,8,5,2,29,32,35,28,31,34,27,30,33,51,48,45,52,49,46,53,50,47,24,21,18,25,22,19,26,23,20)]
A = np.arange(54).astype(int)
inv = lambda M: np.linalg.inv(M)
# Recursive matmul for successive transformations
mm = lambda *args: np.matmul(args[0],(mm(*args[1:]) if len(args)>2 else args[1]))
colors = {
	'w': np.arange(9),
	'r': np.arange(9) + 9,
	'b': np.arange(9) + 18,
	'o': np.arange(9) + 27,
	'g': np.arange(9) + 36,
	'y': np.arange(9) + 45
}
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

from random import randint
def run_random_sequence(N): # This generates a random sequence and calculates the cycle length of that seuqence
	keys= list(moves.keys())
	seq = ",".join([keys[randint(0,len(keys)-1)] for i in range(N)])
	print("SEQUENCE: "+seq)
	print(f"Cycle Length: {get_cycle_length(seq)}")
	return seq

def run_seq(seq): # This caculates the cycle time for the specified sequence in the following comma delimited singmaster format: "U,U',L',L,R,B,F'"
	print("----------------------------")
	print("SEQUENCE: "+seq)
	print(f"Cycle Length: {get_cycle_length(seq)}")

def color_translate(pos): # This converts a position array into a matrix of colors and faces
	carray = [key for n in pos for key in colors.keys() if n in colors[key]]
	return np.array(carray).reshape(6,3,3)

def color_decode(carray):
	""" Due to the geometry of a rubiks cube, no two block segments have the same number and colors of exposed facets, this means that, while there are an infinite number of ways to achieve a certain permutation, there is only one
	unique and physically realizable permutation that matches a given color layout across all 6 faces. This can be exploited to determine the permutation of the cube solely from the positions and colors of the facets
	"""
	cmap = { 
		(0,29,36):("w","o","g"),
		(1,28):("w","o"),
		(2,20,27):("w","b","o"),
		(3,37):("w","g"),
		(4,):("w",),
		(5,19):("w","b"),
		(6,9,38):("w","r","g"),
		(7,10):("w","r"),
		(8,11,18):("w","r","b"),
		(12,41):("r","g"),
		(13,):("r",),
		(14,21):("r","b"),
		(15,44,45):("r","g","y"),
		(16,46):("r","y"),
		(17,24,47):("r","b","y"),
		(22,):("b",),
		(23,30):("b","o"),
		(25,50):("b","y"),
		(26,33,53):("b","o","y"),
		(31,):("o",),
		(32,39):("o","g"),
		(34,52):("o","y"),
		(35,42,51):("o","g","y"),
		(40,):("g",),
		(43,48):("g","y"),
		(49,):("y",)
	}
	colors = carray.flatten()
	numbers = np.arange(54)
	for k1,v1 in cmap.items(): # All block positions
		v1p = colors[list(k1)] # Actual block colors
		for k2,v2 in [(x,y) for (x,y) in cmap.items() if len(y) == len(v1p)]: # Search for block that matches, filter out blocks that have a different number of exposed facets
			if np.all(np.sort(v1p) == np.sort(v2)): # If the block colors are the same
				numbers[list(k1)] = [k2[v2.index(c)] for c in v1p]
	print(numbers)
	print(print(f"Error Sum: {np.sum(np.sort(numbers)-np.arange(54))}"))



seq = run_random_sequence(10)
vec = generate_arr(seq)
carr = color_translate(vec)
print(carr)
color_decode(carr)





