import numpy as np

# Simple demonstration of a non Abelian group from Charles Pinter's "A Book Of Abstract Algebra"

m = lambda a,b,c,d: np.array([[a,b],[c,d]])
M = {'I':m(1,0,0,1),
	'A':m(0,1,1,0),
	'B':m(0,1,-1,-1),
	'C':m(-1,-1,0,1),
	'D':m(-1,-1,1,0),
	'K':m(1,0,-1,-1)}

mm = lambda a,b: [x for x in M.keys() if (M[x]==np.matmul(M[a],M[b])).all()][0]

print("  " + " ".join(M.keys()))
for i in M.keys():
	temp = [i]
	for j in M.keys():
		temp.append(mm(i,j))
	print(" ".join(temp))

