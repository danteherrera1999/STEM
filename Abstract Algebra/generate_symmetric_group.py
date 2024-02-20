import numpy as np

"""
Generates permutation matrices for a symmetric group of order N
Mathematical best case scenario for this script is factorial runtime so... probably don't go above order 8ish
There are definitely more efficient ways to generate all of the permutations, but this simple method helped me 
visualize permutations in the symmetric group especially when learning about quotient groups and homomorphic images
"""

def GI(A):
	n = A.size
	if n == 1:
		return [A]
	else:
		return [np.append(x,np.roll(A,i)[-1]) for i in range(n) for x in GI(np.roll(A,i)[:-1])] # Recursively generate symetric group indices
def GSG(N):
	I = np.identity(N)
	return np.array([I[indices] for indices in GI(np.arange(N))]) # Generate permutation matrices from indices
	

N = 3 # Order


print(GSG(N).shape)

