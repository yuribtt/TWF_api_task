import copy

#just call the minCost function passing the product quantities


# representation of the map in an adjacenci matrix, L1=0, C1=1, ..., C3=3
graph = [[0,3,2.5,2],
		  [3,0,4,-1],
		  [2.5,4,0,3],
		  [2,-1,3,0]]

# values of the problem
weights = [3,2,8,12,25,15,0.5,0.8,1]
costDistance = [10,18,25,30,34,37,39,40]
pickCost = 10
dropCost = 5

# cost to move from source to target with the weight in cargo
def costDistanceWeight(cargo, source, target):
	weight = sum([i*j for i,j in zip(cargo,weights)])
	pos = 0
	if weight != 0:
		pos = min(int((weight - 0.1) // 5), 7)
	return costDistance[pos] * graph[source][target]

# what centers we still have to pass in order to pick
def centersLeft(order):
	result = []
	if sum(order[:3]) > 0:
		result.append(1)
	if sum(order[3:6]) > 0:
		result.append(2)
	if sum(order[6:9]) > 0:
		result.append(3)
	return result

# from a certain state, what centers we can go?
# assuming that we don't go to any center with nothing to pick
def centersPossible(left, state):
	possible = [0]
	for center in left:
		if graph[state][center] > 0:
			possible += [center]
	return possible

def uptadeOrder(order, cargo, state):
	pos = (state - 1) * 3
	newOrder = copy.copy(order)
	newCargo = copy.copy(cargo)
	for i in range(pos,pos+3):
		newCargo[i] = order[i]
		newOrder[i] = 0
	return newOrder, newCargo

# recursive function, take order, cargo, state and actual cost. Returns the best path
def calc(order, cargo, state, cost):

	# if nothing to pick
	if (sum(order) == 0):
		# move to L1 and drop (if we're already in L1 costDistanceWeight == 0)
		cost = cost + costDistanceWeight(cargo,state,0)
		return " -> L1 (drop and finish)", cost + dropCost

	# calculating the centers we still have to pick products
	left = centersLeft(order)

	# if we're in L1, drop items or just pass?
	if state == 0:

		# search for the best path after just pass
		minPass =  min([calc(order,cargo,center,cost+costDistanceWeight(cargo,state,center)) for center in left], key=lambda x: x[1])

		# search for the best path dropping
		# set default value to drop path cost
		minDrop = (" -> L1 (empty)", 1000000)
		if sum(cargo) > 0:
			newCargo = [0,0,0,0,0,0,0,0,0]
			minDrop =  min([calc(order,newCargo,center,cost+costDistanceWeight(newCargo,state,center)+dropCost) for center in left], key=lambda x: x[1])

		# compare paths
		if minPass[1] < minDrop[1]:
			return " -> L1 (pass)"+minPass[0], minPass[1]
		return " -> L1 (drop)"+minDrop[0], minDrop[1]

	# if we're not in L1 and have products to pick
	else:

		# update cargo and order
		newOrder, newCargo = uptadeOrder(order, cargo, state)
		# where can we go?
		possible = centersPossible(left, state)
		# search minimum path
		minPath = min([calc(newOrder,newCargo,center,cost+costDistanceWeight(newCargo,state,center)+pickCost) for center in possible], key=lambda x: x[1])
		return " -> C"+str(state)+" (pick)"+minPath[0], minPath[1]

def minCost(a=0,b=0,c=0,d=0,e=0,f=0,g=0,h=0,i=0):
	order = [a,b,c,d,e,f,g,h,i]
	cargo = [0,0,0,0,0,0,0,0,0]
	path, cost = min([calc(order, cargo, state, 0) for state in range(1,4)], key=lambda x: x[1])
	print("Path: (start)"+path)
	print("Cost: " + str(cost))

#minCost(1,1,1,1,1,1,1,1,1)
#minCost(2,5,7,0,0,0,20,30,40)