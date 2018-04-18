## PSYC493 - Directed Studies
## Jack 'jryzkns' Zhou 2018
## code used for calculations and mathematical modelling

from math import sqrt

def norm(vi):
	acc=0
	for entry in vi:
		acc+=entry**2
	return sqrt(acc)

def dist(v1,v2):
	if (len(v1) != len (v2)):
		print("ERROR: input vectors are not of the same dimension!")
		return
	diffvector=[]
	for i in range(len(v1)):
		diffvector.append(v1[i]-v2[i])
	return norm(diffvector)

## TOP

## Estimating arclength for turning tile route:
## Turning tile is a 400x400 grid with the route starting at (0,100) and ends at (300,400)
## It contains a 90 degrees turn that is somewhat difficult to calulate
## For this, we take a upper bound estimate and a lower bound estimate
end = (1200,1700)
midpoint = (967.4,1631)

upperboundest = 2*dist(end,midpoint)
lowerboundest = 400+100*sqrt(2)

print("The lowerbound distance is", upperboundest)
print("The upperbound distance is", lowerboundest)

print("A reasonable guess of the actual value of the curvature should be the average of the two,\n which in this case would be the average of the bounds:", (upperboundest+lowerboundest)/2)

