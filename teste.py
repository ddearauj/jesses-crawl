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


"""
Matrix = [["A1", "A2", "A3", "A4"],
		  ["B1", "B2", "B3"],
		  ["C1", "C2", "C3", "C4", "C5"],
		  ["D1", "D2", "D3"]]

reversedMatrix = list(reversed(Matrix))

def getLine

for i in range(4):
	for k in range(i-1, -1, -1):
		for ji in range(len(reversedMatrix[i])):
			print(reversedMatrix[i][ji], end=" ")
			for j in range(len(reversedMatrix[k])):
				print(reversedMatrix[k][j], end=" ")
			print()

	print()

