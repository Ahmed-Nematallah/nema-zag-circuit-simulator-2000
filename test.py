import itertools
nodes = []
#a=[]
#b= []
c = [[8, 6], [8, 55], [3, 55], [9, 10],[10,11],[11,40]]
for a,b in itertools.combinations(c,2):
	out = set(a).intersection(b)
	if out != set():
		if len(nodes) >0:	
			for i in nodes:
				if b in i:
					i.append(a)
				elif a in i:
					i.append(b)
				elif (b not in i )and( a not in i):
					nodes.append([a,b])
		else:
			nodes.append([a,b])
print(nodes)