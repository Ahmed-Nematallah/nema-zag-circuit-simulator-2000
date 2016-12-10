import itertools
nodes = []
a=[]
b= []
c = [[[125, 225], [225, 225]], [[225, 225], [225, 150]], [[225, 150], [350, 150]], [[350, 150], [350, 225]]]
for a,b in itertools.combinations(c,2):
	out = set(a).intersection(b)
	print(out)