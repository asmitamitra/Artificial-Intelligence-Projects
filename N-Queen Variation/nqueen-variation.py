import os
import sys
from operator import itemgetter
import math

def get_board(n):
	board = [0] * n
	for i in range(n):
		board[i] = [0] * n
	return board
def boardInitialState(board):
	for i in range(n):
		for j in range(n):
			board[i][j] = 0
	return board
def isValidPosition(row,col, board):
	for i in range(n):
		if(board[row][i] == 1):
			return False
	for i in range(n):
		if(board[i][col] == 1):
			return False

	ix = row
	iy = col
	while(ix>=0 and iy>=0):
		if(board[ix][iy]):
			return False
		ix-=1
		iy-=1
	ix = row
	iy = col
	while(ix<n and iy<n):
		if(board[ix][iy] == 1):
			return False
		ix+=1
		iy+=1
	ix = row
	iy = col
	while(ix<n and iy>=0):
		if(board[ix][iy] == 1):
			return False
		ix+=1
		iy-=1
	ix = row
	iy = col
	while(ix>=0 and iy<n):
		if(board[ix][iy] == 1):
			return False
		ix-=1
		iy+=1
	return True

def checking(j, p, p1, listScooter, stack, board, sum):
	#print("In checling")
	while(j<len(listScooter) and p1<p):
		if(board[listScooter[j]["pos_i"]][listScooter[j]["pos_j"]] != 1 and isValidPosition(listScooter[j]["pos_i"], listScooter[j]["pos_j"], board)):
			p1+=1
			board[listScooter[j]["pos_i"]][listScooter[j]["pos_j"]] = 1
			sum += listScooter[j]["point"]
			stack.append(listScooter[j])
		j+=1
	return {"sum": sum, "stack": stack, "p1": p1, "board": board}

def calculateScore2(board, listScooter, p):
	max_sum1 = 0
	i = 0
	pos_max1 = 0
	while(i<=((n/2)+1)):
		board = boardInitialState(board)
		j = 0
		stack = []
		p1 = 1
		sum = listScooter[i]["point"]
		board[listScooter[i]["pos_i"]][listScooter[i]["pos_j"]] = 1
		stack.append(listScooter[i])
		while(p1<p):
			res = checking(j, p, p1, listScooter, stack, board, sum)
			#print("response", res)
			board = res["board"]
			sum = res["sum"]
			p1 = res["p1"]
			stack = res["stack"]
			if(p1<p):
				#print("p1<p")
				if(not len(stack)):
					break
				s1 = stack.pop()
				p1 -= 1
				j1 = listScooter.index(s1)
				sum -= listScooter[j1]["point"] 
				board[listScooter[j1]["pos_i"]][listScooter[j1]["pos_j"]] = 0
				j = j1 + 1
		#print("p1: ", p1)
		if(p1 >= p):
			#print("stack: ", stack, "len_stack: ", len(stack))
			if(max_sum1<sum):
				max_sum1 = sum
		i+=1
	i = 0
	max_sum2 = 0
	pos_max2 = 0
	while(i<=((n/2)+1)):
		board = boardInitialState(board)
		j = i
		stack = []
		p1 = 0
		sum = 0
		while(p1<p):
			res = checking(j, p, p1, listScooter, stack, board, sum)
			#print("response", res)
			board = res["board"]
			sum = res["sum"]
			p1 = res["p1"]
			stack = res["stack"]
			if(p1<p):
				#print("p1<p")
				if(not len(stack)):
					break
				s1 = stack.pop()
				p1 -= 1
				j1 = listScooter.index(s1)
				sum -= listScooter[j1]["point"] 
				board[listScooter[j1]["pos_i"]][listScooter[j1]["pos_j"]] = 0
				j = j1 + 1
		#print("p1: ", p1)
		if(p1 >= p):
			#print("stack: ", stack, "len_stack: ", len(stack))
			if(max_sum2<sum):
				max_sum2 = sum
		i+=1
	
	if(max_sum1<=max_sum2):
		return max_sum2
	else: 
		return max_sum1
	#print("max: ", max_sum, "array: ", actualArray[pos_max])			
	#return max_sum

def sortBoxes(scooterBoard):
	listScooter = []
	for i in range(n):
		for j in range(n):
			s1 = {"pos_i": i, "pos_j": j, "point": scooterBoard[i][j]}
			listScooter.append(s1)
	newList = sorted(listScooter, key = itemgetter("point"), reverse = True)
	return newList

if __name__ == "__main__":
	global n
	#listScooter = []
	with open("input.txt") as fp:
		n = int(fp.readline())
		p = int(fp.readline())
		s = int(fp.readline())
		scooterBoard = get_board(n)
		board = get_board(n)
		line = fp.readline()
		while line:
			ax = line.split(",")
			sx = int(ax[0])
			sy = int(ax[1])
			scooterBoard[sx][sy] += 1
			line = fp.readline()
		#print(scooterBoard)

		#sort points
		listScooter = sortBoxes(scooterBoard)

		#calculate and return max sum
		target = open("output.txt", "w")
		target.write(str(calculateScore2(board, listScooter, p)))
