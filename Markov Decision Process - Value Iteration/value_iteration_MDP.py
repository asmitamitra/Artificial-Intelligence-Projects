import os
import sys
import math
import numpy as np
class GridMDP:
	def __init__(self, grid, terminals, actions, gamma):
		self.terminals = terminals
		self.actionlist = actions
		self.gamma = gamma
		self.reward = {}
		self.states = set()
		self.size = len(grid)
		# self.MDP = MDP(actions, terminals, gamma)
		for x in range(len(grid)):#rows
			for y in range(len(grid)):
				self.reward[x,y] = grid[x][y]
				if(grid[x][y] != None):
					self.states.add((x,y))
		#print(self.reward)
		#print(self.states)

	def R(self,state):
		return self.reward[state]
	
	def actions(self,state):
		#set of actions which can be performed.
		# print("in actions," , self.terminals, self.actionlist)
		if state in self.terminals:
			return [None]
		return self.actionlist
	def P(self, state, action):
		#P(s' |s,a)
		if(action == None):
			return [(state, 0.0)] #resultant state and probability of going there
		else:
			placesCanGo = []
			for i in self.actionlist:
				if(i != action):
					placesCanGo.append((self.go(state, i), 0.1))
			placesCanGo.append((self.go(state, action), 0.7))
			# print("possible places returning",placesCanGo)
			return placesCanGo
	def go(self, state, action):
		#return state that results if do action
		result = None
		if(action == 'r'):
			right = (0,1) #right i,j+1
			result = tuple(map(lambda x,y: x+y, right, state))
		elif(action == 'l'):
			left = (0,-1) #left i,j-1
			result = tuple(map(lambda x,y: x+y, left, state))
		elif(action == 'u'):
			up = (-1,0) #right i-1,j
			result = tuple(map(lambda x,y: x+y, up, state))
		elif(action == 'd'):
			down = (1,0) #right i+1,j
			result = tuple(map(lambda x,y: x+y, down, state))
		if(result[0] <0 or result[0]>=self.size or result[1]<0 or result[1]>=self.size):
			return state #boundary states. 
		else:
			return result	
def value_iteration(grid, epsilon):
	done = 1
	numberofIteration = 0
	U1 = dict([(s,0) for s in grid.states])
	gamma = grid.gamma
	reward = grid.reward
	
	while done :
		countstate = 0
		numberofIteration+=1
		U = U1.copy()
		delta = 0
		#print("old_iteration\n", U)
		for s in grid.states:
			# for a in grid.actions(s):
			# 	directionVal = sum([p * U[s1] for (s1, p) in grid.P(s, a)])
			U1[s] = grid.R(s) + gamma * max([sum([p * U[s1] for (s1, p) in grid.P(s, a)])
                                        for a in grid.actions(s)])
			#print("new util",U1[s])
			if(abs(U1[s] - U[s]) > delta):
				delta = abs(U1[s] - U[s])
			#print("delta", delta)
			if(delta < (epsilon *(1-gamma)/gamma)):
				countstate+=1
		if(delta < (epsilon *(1-gamma)/gamma) and countstate == len(grid.states)):
			done = 0;
	#print ("===", numberofIteration)
	return U
def expected_utility(grid, U, a,s):
	# print(a)
	return sum([p*U[s] for (s, p) in grid.P(s,a)])
def policy_matrix(grid, U):
	pi = {}
	for s in grid.states:
		max = float("-inf")
		maxAction = None
		for a in grid.actions(s):
			d = expected_utility(grid, U, a, s)
			if(max<d):
				max = d
				maxAction = a
		pi[s] = maxAction
	return pi
def turn_left(action):
	if(action == 'r'):
		return 'u'
	elif action == 'u':
		return 'l'
	elif action == 'l':
		return 'd'
	else:
		return 	'r'
def turn_right(action):
	if action == 'r':
		return 'd'
	elif action == 'd':
		return 'l'
	elif action == 'l':
		return 'u'
	else:
		return 'r'
def simulation(grid, U, pi, start, terminal):
	cost = 0
	#print(start)
	for j in range(10):
		peritercost = cost
		state = start
		np.random.seed(j)
		swerve = np.random.random_sample(1000000)
		k = 0
		if(state == terminal):
			cost+=100
		while(state != terminal):
			action = pi[state]
			if(swerve[k]>0.7):
				if(swerve[k]>0.8):
					if(swerve[k]>0.9):
						action = turn_left(turn_left(action))
					else:
						action = turn_left(action)
				else:
					action = turn_right(action)
			# print('moving:', action)
			state = grid.go(state, action)
			# print(state, grid.R(state))
			cost += grid.R(state)
			k+=1
		#print("iteration: ", j, "cost:", cost-peritercost)
	return math.floor(cost/10)
if __name__ == "__main__":
	target = open("output.txt", "w")
	with open("input.txt") as fp:
		s = int(fp.readline())#size of grid
		n = int(fp.readline())#no of cars
		o = int(fp.readline())#no of obstacles
		grid = [-1] * s
		for i in range(s):
			grid[i] = [-1] * s
		for i in range(o):
			obs = fp.readline().split(',')
			grid[int(obs[0])][int(obs[1])] += -100
		startLocations = []
		endLocations = []
		for i in range(n):
			startLocations.append(fp.readline());
		for i in range(n):
			endLocations.append(fp.readline());
		actions = ['l', 'r', 'd', 'u']
		for i in range(n):
			#for every car goal state is different. 
			score = -1
			startlocs = startLocations[i].split(',')
			endlocs = endLocations[i].split(',')
			grid[int(endlocs[0])][int(endlocs[1])] += 100
			#print("terminals", int(endlocs[0]),int(endlocs[1]))
			terminals = []
			terminals.append((int(endlocs[0]),int(endlocs[1])))
			#print(grid)
			# grid = np.array(grid)
			# grid.transpose(1,0)
			# print(grid)
			problem = GridMDP(grid, terminals, actions, 0.9)
			utility = value_iteration(problem, 0.1)
			#print("utility =====\n",utility)
			utilitymatrix = [-1] * s
			pi = policy_matrix(problem, utility)
			#print(pi)
			matrix = [-1] * s
			#print(matrix)
			#now start from initial position, and do simulation 10 times. 
			start = (int(startlocs[0]),int(startlocs[1]))
			#print("start",start)
			#print("terminals",terminals[0])
			simulation1 = simulation(problem, utility, pi, start, terminals[0])
			#print(simulation1)
			target.write(str(int(simulation1)) + '\n')
			#finally remove +100 when going for other cars
			grid[int(endlocs[0])][int(endlocs[1])] -= 100			
