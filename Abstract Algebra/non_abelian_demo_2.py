import numpy as np

# Chapter 3 problem E of Charles Pinter's "A Book Of Abstract Algebra" showing the non Abelian 
# group of transformations in a game involving two coins

m = lambda a,b,c,d: np.array([[a,b],[c,d]])

I = m(1,0,0,1) # Do nothing
M1 = m(-1,0,0,1) # Flip coin at position A
M2 = m(1,0,0,-1) # Flip coin at position B
M4 = m(0,1,1,0) # Switch the two coins

M = {'I ':I,
	'M1':M1,
	'M2':M2,
	'M3':np.matmul(M1,M2),
	'M4':M4,
	'M5':np.matmul(M1,M4),
	'M6':np.matmul(M2,M4),
	'M7':np.matmul(np.matmul(M1,M2),M4)}

mm = lambda a,b: [x for x in M.keys() if (M[x]==np.matmul(M[a],M[b])).all()][0]

print("*  " + " ".join(M.keys()))
for i in M.keys():
	temp = [i]
	for j in M.keys():
		temp.append(mm(i,j))
	print(" ".join(temp))

