import numpy as np
import matplotlib.pyplot as plt

"""
This script generates the Cayley table for the subgroup of S_6 
that corresponds to the symmetries of a regular hexagon
This is exercise 7F from Charles Pinter's "A Book Of Abstract Algebra"
"""

I = np.identity(6).astype(int)
G = {
	'R0' : I,
	'R1' : np.roll(I,-1,axis=1), # Rotation Symmetries
	'R2' : np.roll(I,-2,axis=1),
	'R3' : np.roll(I,-3,axis=1),
	'R4' : np.roll(I,-4,axis=1),
	'R5' : np.roll(I,-5,axis=1),
	'RA' : I[:,(4,3,2,1,0,5)], # Reflection Symmetries
	'RB' : I[:,(5,4,3,2,1,0)],
	'RC' : I[:,(0,5,4,3,2,1)],
	'RD' : I[:,(1,0,5,4,3,2)],
	'RE' : I[:,(2,1,0,5,4,3)],
	'RF' : I[:,(3,2,1,0,5,4)]
}

# Recursive matmul for successive transformations
mm = lambda *args: np.matmul(args[0],(mm(*args[1:]) if len(args)>2 else args[1]))

# Compose transformations and search for corresponding transformation from the set
c = lambda *args: [key for key in G.keys() if np.all(G[key] == mm(*args))][0]

print('   ' +' '.join(G.keys()))
for i in G.keys():
	print(i+' '+' '.join([c(G[i],G[key]) for key in G.keys()]))

"""
OUTPUT:

   R0 R1 R2 R3 R4 R5 RA RB RC RD RE RF
R0 R0 R1 R2 R3 R4 R5 RA RB RC RD RE RF
R1 R1 R2 R3 R4 R5 R0 RB RC RD RE RF RA
R2 R2 R3 R4 R5 R0 R1 RC RD RE RF RA RB
R3 R3 R4 R5 R0 R1 R2 RD RE RF RA RB RC
R4 R4 R5 R0 R1 R2 R3 RE RF RA RB RC RD
R5 R5 R0 R1 R2 R3 R4 RF RA RB RC RD RE
RA RA RF RE RD RC RB R0 R5 R4 R3 R2 R1
RB RB RA RF RE RD RC R1 R0 R5 R4 R3 R2
RC RC RB RA RF RE RD R2 R1 R0 R5 R4 R3
RD RD RC RB RA RF RE R3 R2 R1 R0 R5 R4
RE RE RD RC RB RA RF R4 R3 R2 R1 R0 R5
RF RF RE RD RC RB RA R5 R4 R3 R2 R1 R0

"""