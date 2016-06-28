"""
Project Euler - Problem 39

If p is the perimeter of a right angle triangle with integral length sides,
{a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p <= 1000, is the number of solutions maximised?
"""
maxSol=0
maxPer=0
for perimeter in range(3,1001):
	solutions=[]
	for a in range(1,perimeter/4+1):
		for b in range(perimeter/4-1,perimeter/2):
			c=perimeter-a-b
			if c*c==a*a+b*b:
				solutions.append((a,b,c))
	if len(solutions) > maxSol: 
		maxSol=len(solutions)
		maxPer=perimeter
		print "Found a maximum for perimeter of %d" % maxPer
print "Maximum solutions is %d for a perimeter of %d" % (maxSol, maxPer)

# output:
# Found a maximum for perimeter of 12
# Found a maximum for perimeter of 60
# Found a maximum for perimeter of 120
# Found a maximum for perimeter of 240
# Found a maximum for perimeter of 720
# Found a maximum for perimeter of 840
# Maximum solutions is 7 for a perimeter of 840