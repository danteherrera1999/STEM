import numpy as np
import matplotlib.pyplot as plt

# This script generates the symmetric group of 3 elements as shown in the 
# first exercise of chapter 7 of Charles Pinter's "A Book Of Abstract Algebra"

I = np.identity(3).astype(int) # This is the neutral element of the group representing a function that maps A to A with no transformation
a = I[:,(1,0,2)] # This is the first generator of the group representing swapping the first 2 elements of the set
b = I[:,(1,2,0)] # This is the second generator of the group representing rolling all elements 1 position
o = lambda x,y : np.matmul(x,y).astype(int) # This combines the generators
S = {'ε':I,'α':o(a,b),'β':o(b,b),'γ':a,'δ':b,'κ':o(b,a)}

print('  '+" ".join(S.keys()))

for i in S.keys():
	temp = []
	for j in S.values():
		temp.append([key for key in S.keys() if np.all(S[key] == o(S[i],j))][0])
	print(i+' '+' '.join(temp))

