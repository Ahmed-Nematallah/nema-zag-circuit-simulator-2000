import re
import numpy as np
import random

def getComponentValue(componentValue):
	if(componentValue.lower().endswith('k')):
		val = float(componentValue[:-1]) * 1000
	elif(componentValue.lower().endswith('meg')):
		val = float(componentValue[:-3]) * 1000000
	elif(componentValue.lower().endswith('g')):
		val = float(componentValue[:-1]) * 1000000000
	elif(componentValue.lower().endswith('t')):
		val = float(componentValue[:-1]) * 1000000000000
	elif(componentValue.lower().endswith('m')):
		val = float(componentValue[:-1]) / 1000
	elif(componentValue.lower().endswith('u')):
		val = float(componentValue[:-1]) / 1000000
	elif(componentValue.lower().endswith('n')):
		val = float(componentValue[:-1]) / 1000000000
	elif(componentValue.lower().endswith('p')):
		val = float(componentValue[:-1]) / 1000000000000
	elif(componentValue.lower().endswith('f')):
		val = float(componentValue[:-1]) / 1000000000000000
	else:
		val = float(componentValue)

	return val

def getNodeValue(nodeValue):
	if(nodeValue.lower().startswith("n")):
		return int(nodeValue[1:])
	else:
		return -1

# netlist = """.DC
# R R1 N1 N0 1k
# R R2 N2 N0 1k
# R R3 N4 N2 1k
# R R4 N3 N2 1k
# R R5 N4 N3 1k
# R R6 N3 N0 1k
# V V1 N2 N1 10"""
# netlist = """.DC
# R R1 N1 N2 1k
# R R2 N3 N0 1k
# L L1 N2 N3 1m
# V V1 N1 N0 10"""
netlist = """.DC
V V1 N1 N0 10
R R1 N2 N1 10k
R R2 N2 N0 10k
R R3 N4 N3 10k
DIFFAMP3 A1 N2 N3 N4 100k"""


i = 0
simulationDomain = ""
simulationFrequency = 0
simulationParameters = []
commands = netlist.splitlines()
maxNode = 0
voltageSources = 0
for i in range(len(commands)):
	commandtext = commands[i].split(' ')
	if (commandtext[0].lower() == ".dc"):
		simulationDomain = "DC"
	elif (commandtext[0].lower() == ".ac"):
		simulationDomain = "AC"

	for i in range(1, len(commandtext)):
		currentNode = getNodeValue(commandtext[i])
		if(currentNode > maxNode):
			maxNode = currentNode

admittanceMatrix = [[0 for j in range(maxNode)] for i in range(maxNode)]
knownMatrix = [0 for i in range(maxNode)]
unknownMatrix = ["V(N" + str(i + 1) + ")" for i in range(maxNode)]

for i in range(len(commands)):
	commandtext = commands[i].split(' ')
	# nodesAndValues = re.findall(r"\(([A-Za-z0-9_,. ]*)\)", commands[i])
	# if (nodesAndValues != []):
	# 	nodes = nodesAndValues[0].split(', ')

	if(commandtext[0].lower() == 'r'):
		componentValue = getComponentValue(commandtext[4])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		if(node1 != 0):
			admittanceMatrix[node1 - 1][node1 - 1] += 1/componentValue
		if((node1 != 0) & (node2 != 0)):
			admittanceMatrix[node1 - 1][node2 - 1] -= 1/componentValue
			admittanceMatrix[node2 - 1][node1 - 1] -= 1/componentValue
		if(node2 != 0):
			admittanceMatrix[node2 - 1][node2 - 1] += 1/componentValue

	elif(commandtext[0].lower() == 'g'):
		componentValue = getComponentValue(commandtext[4])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		if(node1 != 0):
			admittanceMatrix[node1 - 1][node1 - 1] += componentValue
		if((node1 != 0) & (node2 != 0)):
			admittanceMatrix[node1 - 1][node2 - 1] -= componentValue
			admittanceMatrix[node2 - 1][node1 - 1] -= componentValue
		if(node2 != 0):
			admittanceMatrix[node2 - 1][node2 - 1] += componentValue
		
	elif(commandtext[0].lower() == 'l'):
		componentValue = getComponentValue(commandtext[4])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		if(simulationDomain == "DC"):		#Consider it a short circuit, or a 0V voltage source, neat, heh?
			for i in range(len(admittanceMatrix)):
				admittanceMatrix[i].append(0)
				if (i == (node1 - 1)):
					admittanceMatrix[i][maxNode + voltageSources] += 1
				if (i == (node2 - 1)):
					admittanceMatrix[i][maxNode + voltageSources] -= 1
			columnSliceTranspose = [row[-1] for row in admittanceMatrix]
			columnSliceTranspose.append(0)
			admittanceMatrix.append(columnSliceTranspose)
			voltageSources += 1
			unknownMatrix.append("I(" + commandtext[1] + ")")
			knownMatrix.append(0)

		elif(simulationDomain == "AC"):
			pass

	elif(commandtext[0].lower() == 'c'):
		componentValue = getComponentValue(commandtext[4])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		if(simulationDomain == "DC"):
			pass
		elif(simulationDomain == "AC"):
			pass
		
	elif(commandtext[0].lower() == 'v'):
		componentValue = getComponentValue(commandtext[4])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		for i in range(len(admittanceMatrix)):
			admittanceMatrix[i].append(0)
			if (i == (node1 - 1)):
				admittanceMatrix[i][maxNode + voltageSources] += 1
			if (i == (node2 - 1)):
				admittanceMatrix[i][maxNode + voltageSources] -= 1
		columnSliceTranspose = [row[-1] for row in admittanceMatrix]
		columnSliceTranspose.append(0)
		admittanceMatrix.append(columnSliceTranspose)
		voltageSources += 1
		unknownMatrix.append("I(" + commandtext[1] + ")")
		knownMatrix.append(componentValue)

	elif(commandtext[0].lower() == 'i'):
		componentValue = getComponentValue(commandtext[4])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		if(node1 > -1):
			knownMatrix[node1 - 1] += componentValue
		if(node2 > -1):
			knownMatrix[node2 - 1] -= componentValue

	elif(commandtext[0].lower() == 'diffamp3'):
		componentValue = getComponentValue(commandtext[5])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		node3 = getNodeValue(commandtext[4])
		for i in range(len(admittanceMatrix)):
			admittanceMatrix[i].append(0)
			if (i == (node3 - 1)):
				admittanceMatrix[i][maxNode + voltageSources] += 1
		columnSliceTranspose = [row[-1] for row in admittanceMatrix]
		columnSliceTranspose.append(0)
		admittanceMatrix.append(columnSliceTranspose)
		for i in range(len(admittanceMatrix)):
			if (i == (node1 - 1)):
				admittanceMatrix[maxNode + voltageSources][i] += componentValue
			if (i == (node2 - 1)):
				admittanceMatrix[maxNode + voltageSources][i] -= componentValue
		voltageSources += 1
		unknownMatrix.append("I(" + commandtext[1] + ")")
		knownMatrix.append(0)


admittanceMatrix = np.array(admittanceMatrix)
knownMatrix = np.array(knownMatrix)

# print(admittanceMatrix)
# print(knownMatrix)
# print(unknownMatrix)

admittanceMatrixInvert = np.linalg.inv(admittanceMatrix)
solutionMatrix = np.dot(admittanceMatrixInvert, knownMatrix)
solutionMatrix = solutionMatrix.tolist()

for i in range(len(commands)):
	commandtext = commands[i].split(' ')
	if (len(commandtext) == 5):           #Bad solution, should check type of component
		componentValue = getComponentValue(commandtext[4])
		node1 = getNodeValue(commandtext[2])
		node2 = getNodeValue(commandtext[3])
		voltageAcross = 0
		if ((node1 == 0) & (node2 == 0)):
			voltageAcross = 0
		elif(node1 == 0):
			voltageAcross = -solutionMatrix[node2 - 1]
		elif(node2 == 0):
			voltageAcross = solutionMatrix[node1 - 1]
		else:
			voltageAcross = solutionMatrix[node1 - 1] - solutionMatrix[node2 - 1]
	
	if(commandtext[0].lower() == 'r'):
		unknownMatrix.append("I(" + commandtext[1] + ")")
		solutionMatrix.append(voltageAcross / componentValue)

	elif(commandtext[0].lower() == 'g'):
		unknownMatrix.append("I(" + commandtext[1] + ")")
		solutionMatrix.append(voltageAcross * componentValue)

	elif(commandtext[0].lower() == 'l'):
		pass

	elif(commandtext[0].lower() == 'c'):
		pass

for i in range(len(solutionMatrix)):
	print(unknownMatrix[i] + " = " + str(solutionMatrix[i]))
