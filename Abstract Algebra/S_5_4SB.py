import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

# This script generates the Cayley table for an abelian four element subgroup of S_5
# exercise B3 of chapter 7 of Charles Pinter's "A Book Of Abstract Algebra"

I = np.identity(5).astype(int) # This is the neutral element of the group representing a function that maps A directly to A with no transformation
f = I[:,(0,2,3,4,1)] # This is a rotation of the last 4 elements
g = I[:,(0,3,4,1,2)]
h = I[:,(0,4,1,2,3)]
o = lambda x,y : np.matmul(x,y).astype(int) # This combines the generators

invert = lambda x: inv(x).astype(int)

S = {'e':I,'f':f,'g':o(f,f),'h':o(o(f,f),f)}

for s in S.values():
	print(np.matmul([1,2,3,4,5],s))

print('  '+" ".join(S.keys()))
for i in S.keys():
	temp = []
	for j in S.values():
		matches = [key for key in S.keys() if np.all(S[key] == o(S[i],j))]
		if len(matches)>0:
			temp.append(matches[0])
		else: temp.append("X")
	print(i+' '+' '.join(temp))
