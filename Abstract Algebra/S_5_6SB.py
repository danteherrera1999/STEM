import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

# This script generates the Cayley table for an abelian six element subgroup of S_5
# exercise B4 of chapter 7 of Charles Pinter's "A Book Of Abstract Algebra"

I = np.identity(5).astype(int) # This is the neutral element of the group representing a function that maps A directly to A with no transformation
f = I[:,(1,0,2,3,4)] # This is the first generator of the group representing a rotation of the first 2 elements
g = I[:,(0,1,3,4,2)] # This is the second generator of the group representing a rotation of the last 3 elements
h = I[:,(1,0,3,4,2)] 
k = I[:,(0,1,4,2,3)] 
l = I[:,(1,0,4,2,3)] 
o = lambda x,y : np.matmul(x,y).astype(int) # This combines the generators

invert = lambda x: inv(x).astype(int)

S = {'e':I,'f':f,'g':g,'h':h,'k':k,'l':l}

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
