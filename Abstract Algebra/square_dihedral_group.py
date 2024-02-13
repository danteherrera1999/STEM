import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

# This script generates the Cayley table for the square dihedral group as in
# second exercise of chapter 7 of Charles Pinter's "A Book Of Abstract Algebra"

I = np.identity(4).astype(int) # This is the neutral element of the group representing a function that maps A directly to A with no transformation
a = I[:,(1,2,3,0)] # This is the first generator of the group representing a counter-clockwise rotation of the square
b = I[:,(1,0,3,2)] # This is the second generator of the group representing a flip about the vertical axis of the square
o = lambda x,y : np.matmul(x,y).astype(int) # This combines the generators

invert = lambda x: inv(x).astype(int)

S = {'R0':I,'R1':a,'R2':o(a,a),'R3':invert(a),'R4':o(b,a),'R5':o(b,invert(a)),'R6':b,'R7':o(o(a,a),b)}

print('   '+" ".join(S.keys()))
for i in S.keys():
	temp = []
	for j in S.values():
		temp.append([key for key in S.keys() if np.all(S[key] == o(S[i],j))][0])
	print(i+' '+' '.join(temp))

