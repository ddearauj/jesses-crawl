"""
O que quero é

C1 D1 D2 D3
C2 D1 D2 D3
C3 D1 D2 D3
C4 D1 D2 D3

B1 C1 D1 D2 D3
B1 C2 D1 D2 D3
B1 C3 D1 D2 D3
B1 C4 D1 D2 D3

B2 C1 D1 D2 D3
B2 C2 D1 D2 D3
B2 C3 D1 D2 D3
B2 C4 D1 D2 D3

B3 C1 D1 D2 D3
B3 C2 D1 D2 D3
B3 C3 D1 D2 D3
B3 C4 D1 D2 D3

...

Mas o output ta

C1 D1 D2 D3 
C2 D1 D2 D3 
C3 D1 D2 D3 
C4 D1 D2 D3 
C5 D1 D2 D3 

B1 C1 C2 C3 C4 C5 
B2 C1 C2 C3 C4 C5 
B3 C1 C2 C3 C4 C5 
B1 D1 D2 D3 
B2 D1 D2 D3 
B3 D1 D2 D3 

A1 B1 B2 B3 
A2 B1 B2 B3 
A3 B1 B2 B3 
A4 B1 B2 B3 
A1 C1 C2 C3 C4 C5 
A2 C1 C2 C3 C4 C5 
A3 C1 C2 C3 C4 C5 
A4 C1 C2 C3 C4 C5 
A1 D1 D2 D3 
A2 D1 D2 D3 
A3 D1 D2 D3 
A4 D1 D2 D3 


"""
Matrix = [["A1", "A2", "A3", "A4"],
		  ["B1", "B2", "B3"],
		  ["C1", "C2", "C3", "C4", "C5"],
		  ["D1", "D2", "D3"]]

reversedMatrix = list(reversed(Matrix))

# o produto da lista funcionaria, mas como se eu clico em um dos elementos a Matrix muda, nao da para usar, mas a ideia é essa
# acessando cada elemento individualmente 

import itertools
for combo in itertools.product(*Matrix):
	print(combo)

# tirando da documentação do python

def product(*args, repeat=1):
	# product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
	# product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
	pools = [tuple(pool) for pool in args] * repeat
	result = [[]]
	for pool in pools:
		result = [x+[y] for x in result for y in pool]
		print(result)
	for prod in result:
		yield tuple(prod)




for i in range(4):
	for k in range(i-1, -1, -1):
		for ji in range(len(reversedMatrix[i])):
			print(reversedMatrix[i][ji], end=" ")
			for j in range(len(reversedMatrix[k])):
				print(reversedMatrix[k][j], end=" ")
			print()

	print()

