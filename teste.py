"""
O que quero é
D1 D2 D3

C1; D1 D2 D3
C2; D1 D2 D3
C3; D1 D2 D3
C4; D1 D2 D3

B1; C1; D1 D2 D3
B1; C2; D1 D2 D3
B1; C3; D1 D2 D3
B1; C4; D1 D2 D3

B2; C1; D1 D2 D3
B2; C2; D1 D2 D3
B2; C3; D1 D2 D3
B2; C4; D1 D2 D3

B3; C1; D1 D2 D3
B3; C2; D1 D2 D3
B3; C3; D1 D2 D3
B3; C4; D1 D2 D3

...

Mas o output ta

C1; D1 D2 D3 
C2; D1 D2 D3 
C3; D1 D2 D3 
C4; D1 D2 D3 
C5; D1 D2 D3 

B1; C1 C2 C3 C4 C5 
B2; C1 C2 C3 C4 C5 
B3; C1 C2 C3 C4 C5 
B1; D1 D2 D3 
B2; D1 D2 D3 
B3; D1 D2 D3 

A1; B1 B2 B3 
A2; B1 B2 B3 
A3; B1 B2 B3 
A4; B1 B2 B3 
A1; C1 C2 C3 C4 C5 
A2; C1 C2 C3 C4 C5 
A3; C1 C2 C3 C4 C5 
A4; C1 C2 C3 C4 C5 
A1; D1 D2 D3 
A2; D1 D2 D3 
A3; D1 D2 D3 
A4; D1 D2 D3 


"""
Matrix = [["A1", "A2", "A3", "A4"],
		  ["B1", "B2", "B3"],
		  ["C1", "C2", "C3", "C4", "C5"],
		  ["D1", "D2", "D3"]]

reversedMatrix = list(reversed(Matrix))

# o produto da lista funcionaria, mas como se eu clico em um dos elementos a Matrix muda, nao da para usar, mas a ideia é essa
# acessando cada elemento individualmente 

# import itertools
# for combo in itertools.product(*Matrix):
# 	print(combo)

def recursive_click(Matrix, row=0):
	if len(Matrix) > row:
		print("nova linha")
		print(row)
		print("Resto Matrix: %s" % Matrix[row:])
		for button in Matrix[row]:
			print(button, end=" ")
			recursive_click(Matrix, row+1)
	else:
		print()


Matrix = [["A1", "A2", "A3", "A4"],
    	  ["B1", "B2", "B3"],
    	  ["C1", "C2", "C3", "C4", "C5"],
    	  ["D1", "D2", "D3"]]

reversedMatrix = list(reversed(Matrix))

# o produto da lista funcionaria, mas como se eu clico em um dos elementos a Matrix muda, nao da para usar, mas a ideia é essa
# acessando cada elemento individualmente
recursive_click(Matrix)


