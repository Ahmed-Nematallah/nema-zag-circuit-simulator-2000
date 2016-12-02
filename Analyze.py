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
	return int(nodeValue[1:])

netlist = """.DC
R R1 (N1, N0) (1k)
R R2 (N2, N0) (1k)
R R3 (N4, N2) (1k)
R R4 (N3, N2) (1k)
R R5 (N4, N3) (1k)
R R6 (N3, N0) (1k)
V V1 (N2, N1) (10)"""

i = 0
simulationDomain = ""
simulationFrequency = 0
simulationParameters = []
commands = netlist.splitlines()
maxNode = 0
voltageSources = 0
for i in range(len(commands)):
	if (commands[i].startswith == ".DC"):
		simulationDomain = "DC"
	if (commands[i].startswith == ".AC"):
		simulationDomain = "AC"
		simulationFrequency = getComponentValue(commands[i].split(' ')[1])

	nodesAndValues = re.findall(r"\(([A-Za-z0-9_, ]+)\)", commands[i])
	if (nodesAndValues != []):
		nodes = nodesAndValues[0].split(', ')
		node1 = getNodeValue(nodes[0])
		node2 = getNodeValue(nodes[1])
		if (node1 > maxNode):
			maxNode = node1
		if (node2 > maxNode):
			maxNode = node2

admittanceMatrix = [[0 for j in range(maxNode)] for i in range(maxNode)]
knownMatrix = [0 for i in range(maxNode)]
unknownMatrix = ["V(N" + str(i + 1) + ")" for i in range(maxNode)]

for i in range(len(commands)):
	commandtext = commands[i].split(' ')
	nodesAndValues = re.findall(r"\(([A-Za-z0-9_, ]*)\)", commands[i])
	if (nodesAndValues != []):
		nodes = nodesAndValues[0].split(', ')
	
	if(commandtext[0].lower() == 'r'):
		componentValue = getComponentValue(nodesAndValues[1])
		node1 = getNodeValue(nodes[0]) - 1
		node2 = getNodeValue(nodes[1]) - 1
		if(node1 != -1):
			admittanceMatrix[node1][node1] += 1/componentValue
		if((node1 != -1) & (node2 != -1)):
			admittanceMatrix[node1][node2] -= 1/componentValue
			admittanceMatrix[node2][node1] -= 1/componentValue
		if(node2 != -1):
			admittanceMatrix[node2][node2] += 1/componentValue

	elif(commandtext[0].lower() == 'g'):
		componentValue = getComponentValue(nodesAndValues[1])
		node1 = getNodeValue(nodes[0]) - 1
		node2 = getNodeValue(nodes[1]) - 1
		if(node1 != -1):
			admittanceMatrix[node1][node1] += componentValue
		if((node1 != -1) & (node2 != -1)):
			admittanceMatrix[node1][node2] -= componentValue
			admittanceMatrix[node2][node1] -= componentValue
		if(node2 != -1):
			admittanceMatrix[node2][node2] += componentValue
		
	elif(commandtext[0].lower() == 'l'):
		componentValue = getComponentValue(nodesAndValues[1])
		node1 = getNodeValue(nodes[0]) - 1
		node2 = getNodeValue(nodes[1]) - 1
		if(simulationDomain == "DC"):
			pass
		elif(simulationDomain == "AC"):
			pass

	elif(commandtext[0].lower() == 'c'):
		componentValue = getComponentValue(nodesAndValues[1])
		node1 = getNodeValue(nodes[0]) - 1
		node2 = getNodeValue(nodes[1]) - 1
		if(simulationDomain == "DC"):
			pass
		elif(simulationDomain == "AC"):
			pass
		
	elif(commandtext[0].lower() == 'v'):
		componentValue = getComponentValue(nodesAndValues[1])
		node1 = getNodeValue(nodes[0]) - 1
		node2 = getNodeValue(nodes[1]) - 1
		for i in range(len(admittanceMatrix)):
			admittanceMatrix[i].append(0)
			if (i == node1):
				admittanceMatrix[i][maxNode + voltageSources] += 1
			if (i == node2):
				admittanceMatrix[i][maxNode + voltageSources] -= 1
		columnSliceTranspose = [row[-1] for row in admittanceMatrix]
		columnSliceTranspose.append(0)
		admittanceMatrix.append(columnSliceTranspose)
		voltageSources += 1
		unknownMatrix.append("I(" + commandtext[1] + ")")
		knownMatrix.append(componentValue)

	elif(commandtext[0].lower() == 'i'):
		componentValue = getComponentValue(nodesAndValues[1])
		node1 = getNodeValue(nodes[0]) - 1
		node2 = getNodeValue(nodes[1]) - 1
		if(node1 > -1):
			knownMatrix[node1] += componentValue
		if(node2 > -1):
			knownMatrix[node2] -= componentValue

#Merge Nodes
if (simulationDomain == "DC"):
	for i in range(len(commands)):
		commandtext = commands[i].split(' ')
		nodesAndValues = re.findall(r"\(([A-Za-z0-9_, ]*)\)", commands[i])
		if (nodesAndValues != []):
			nodes = nodesAndValues[0].split(', ')
		
		if(commandtext[0].lower() == 'l'):
			componentValue = getComponentValue(nodesAndValues[1])
			node1 = getNodeValue(nodes[0]) - 1
			node2 = getNodeValue(nodes[1]) - 1


admittanceMatrix = np.array(admittanceMatrix)
knownMatrix = np.array(knownMatrix)


admittanceMatrixInvert = np.linalg.inv(admittanceMatrix)
solutionMatrix = np.dot(admittanceMatrixInvert, knownMatrix)
solutionMatrix = solutionMatrix.tolist()

for i in range(len(commands)):
	commandtext = commands[i].split(' ')
	nodesAndValues = re.findall(r"\(([A-Za-z0-9_, ]*)\)", commands[i])
	mergeRows = [-1 for j in range(maxNode)]
	if (nodesAndValues != []):
		nodes = nodesAndValues[0].split(', ')
		componentValue = getComponentValue(nodesAndValues[1])
		node1 = getNodeValue(nodes[0]) - 1
		node2 = getNodeValue(nodes[1]) - 1
		voltageAcross = 0
		if ((node1 == -1) & (node2 == -1)):
			voltageAcross = 0
		elif(node1 == -1):
			voltageAcross = -solutionMatrix[node2]
		elif(node2 == -1):
			voltageAcross = solutionMatrix[node1]
		else:
			voltageAcross = solutionMatrix[node1] - solutionMatrix[node2]
	
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
