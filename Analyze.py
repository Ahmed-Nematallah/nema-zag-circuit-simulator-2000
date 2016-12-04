import re
import numpy as np
import math
import random
import copy

def getComponentValue(componentValue):
	if(componentValue.lower().endswith('k')):
		val = complex(componentValue[:-1]) * 1000
	elif(componentValue.lower().endswith('meg')):
		val = complex(componentValue[:-3]) * 1000000
	elif(componentValue.lower().endswith('g')):
		val = complex(componentValue[:-1]) * 1000000000
	elif(componentValue.lower().endswith('t')):
		val = complex(componentValue[:-1]) * 1000000000000
	elif(componentValue.lower().endswith('m')):
		val = complex(componentValue[:-1]) / 1000
	elif(componentValue.lower().endswith('u')):
		val = complex(componentValue[:-1]) / 1000000
	elif(componentValue.lower().endswith('n')):
		val = complex(componentValue[:-1]) / 1000000000
	elif(componentValue.lower().endswith('p')):
		val = complex(componentValue[:-1]) / 1000000000000
	elif(componentValue.lower().endswith('f')):
		val = complex(componentValue[:-1]) / 1000000000000000
	else:
		val = complex(componentValue)

	return val

def getNodes(nodeValue):
	return nodeValue[1:-1].lower().split(';')

def getPhase(complexNumber):
	if (complexNumber.real == 0):
		if (complexNumber.imag == 0):
			phase = 0
		else:
			phase = math.pi / 2 * 180 / math.pi

	elif (complexNumber.imag == 0):
		phase = 0
	
	else:
		phase = math.atan(complexNumber.imag / complexNumber.real) * 180 / math.pi

	if (complexNumber.real < 0):
		phase = phase + math.pi * 180 / math.pi

	return phase

def getMagnitude(complexNumber):
	return abs(complexNumber)

# netlist = """.DC OP
# .GND N0
# R R1 (N1;N0) 1k
# R R2 (N2;N0) 1k
# R R3 (N4;N2) 1k
# R R4 (N3;N2) 1k
# R R5 (N4;N3) 1k
# R R6 (N3;N0) 1k
# V V1 (N2;N1) 10"""
# netlist = """.DC OP
# R R1 N1 N2 1k
# R R2 N3 N0 1k
# L L1 N2 N3 1m
# V V1 N1 N0 10"""
# netlist = """.DC OP
# V V1 N1 N0 10
# R R1 N2 N1 10k
# R R2 N2 N0 10k
# R R3 N4 N3 10k
# OPAMP3 A1 N2 N3 N4"""
# netlist = """.AC OP
# V V1 N1 N0 10 1k
# G G1 N1 N2 6.28318530718m
# C C1 N2 N0 1u
# R R1 N1 N0 1k"""
# netlist = """.AC OP
# V V1 N1 N0 10 500
# V V2 N2 N0 5 200
# R R1 N0 N2 1k
# C C1 N2 N1 1u
# OPAMP3 A1 N2 N3 N4
# R R2 N3 N4 1k
# R R3 N3 N0 1k"""
# netlist = """.AC op
# V V1 N1 N0 10 500
# V V2 N2 N0 10 0
# C C1 N1 N2 1u
# R R1 N1 N2 1k
# R R2 N1 N0 1k"""
netlist = """.AC op
.GND N0
V V1 (N1;N0) 10 180
R R1 (N1;N2) 4.7k
R R2 (N2;N3) 6.8k
R R3 (N5;N4) 1.0k
R R4 (N4;N0) 6.8k
R R5 (N5;N6) 4.7k
R R6 (N6;N7) 6.8k
R R7 (N9;N8) 6.8k
R R8 (N8;N0) 5.6k
C C1 (N2;N5) 0.22u
C C2 (N3;N0) 0.1u
C C3 (N6;N9) 0.22u
C C4 (N7;N0) 0.1u
OPAMP3 A1 (N3;N4;N5)
OPAMP3 A2 (N7;N8;N9)"""


i = 0
simulationDomain = ""
simulationFrequencies = []
simulationParameters = []
commands = netlist.splitlines()
nodeList = []
nodeListNatural = []
voltageSources = 0
groundNode = "n0"
for i in range(len(commands)):
	commandtext = commands[i].split(' ')
	if (commandtext[0].lower() == ".dc"):
		simulationDomain = "DC"
		simulationParameters = copy.copy(commandtext)
	elif (commandtext[0].lower() == ".ac"):
		simulationDomain = "AC"
		simulationParameters = copy.copy(commandtext)

	if (commandtext[0].lower() == ".gnd"):
		groundNode = commandtext[1].lower()

	if ((commandtext[0].lower() == "v") | (commandtext[0].lower() == "i")):
		if (len(commandtext) > 4):
			if (getMagnitude(getComponentValue(commandtext[4])) not in simulationFrequencies):
				simulationFrequencies.append(getMagnitude(getComponentValue(commandtext[4])))

	if not(commands[i].startswith('.')):
		localNodes = getNodes(commandtext[2])
		for i in range(len(localNodes)):
			if localNodes[i] not in nodeList:
				nodeList.append(localNodes[i])
				nodeListNatural.append(commandtext[2][1:-1].split(';')[i])

simulationFrequencies.sort()
simulationFrequency = 0
nodeCount = len(nodeList) - 1
nodeListNatural = [x for (y,x) in sorted(zip(nodeList,nodeListNatural), key=lambda pair: pair[0])]
nodeList.sort()
admittanceMatrix = [[0 for j in range(nodeCount)] for i in range(nodeCount)]
knownMatrix = [0 for i in range(nodeCount)]
unknownMatrix = ["V(" + nodeListNatural[i + 1] + ")" for i in range(nodeCount)]

groundNodeIndex = nodeList.index(groundNode)
if (groundNodeIndex > 0):
	nodeList[groundNodeIndex] = nodeList[0]
	nodeList[0] = groundNode

def formAdmittanceMatrix():
	global voltageSources
	for i in range(len(commands)):
		commandtext = commands[i].split(' ')
		if not(commands[i].startswith('.')):
			nodes = getNodes(commandtext[2])
		# nodesAndValues = re.findall(r"\(([A-Za-z0-9_,. ]*)\)", commands[i])
		# if (nodesAndValues != []):
		# 	nodes = nodesAndValues[0].split(', ')

		if(commandtext[0].lower() == 'r'):
			componentValue = getComponentValue(commandtext[3])
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			componentAdmittance = 1/componentValue
			if(node1 != 0):
				admittanceMatrix[node1 - 1][node1 - 1] += componentAdmittance
			if((node1 != 0) & (node2 != 0)):
				admittanceMatrix[node1 - 1][node2 - 1] -= componentAdmittance
				admittanceMatrix[node2 - 1][node1 - 1] -= componentAdmittance
			if(node2 != 0):
				admittanceMatrix[node2 - 1][node2 - 1] += componentAdmittance

		elif(commandtext[0].lower() == 'g'):
			componentValue = getComponentValue(commandtext[3])
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			componentAdmittance = componentValue
			if(node1 != 0):
				admittanceMatrix[node1 - 1][node1 - 1] += componentAdmittance
			if((node1 != 0) & (node2 != 0)):
				admittanceMatrix[node1 - 1][node2 - 1] -= componentAdmittance
				admittanceMatrix[node2 - 1][node1 - 1] -= componentAdmittance
			if(node2 != 0):
				admittanceMatrix[node2 - 1][node2 - 1] += componentAdmittance
			
		elif(commandtext[0].lower() == 'l'):
			componentValue = getComponentValue(commandtext[3])
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			if((simulationDomain == "DC") | (simulationFrequency == 0)):	#Consider it a short circuit, or a 0V voltage source, neat, heh?
				for i in range(len(admittanceMatrix)):
					admittanceMatrix[i].append(0)
					if (i == (node1 - 1)):
						admittanceMatrix[i][nodeCount + voltageSources] += 1
					if (i == (node2 - 1)):
						admittanceMatrix[i][nodeCount + voltageSources] -= 1
				columnSliceTranspose = [row[-1] for row in admittanceMatrix]
				columnSliceTranspose.append(0)
				admittanceMatrix.append(columnSliceTranspose)
				voltageSources += 1
				unknownMatrix.append("I(" + commandtext[1] + ")")
				knownMatrix.append(0)

			elif(simulationDomain == "AC"):
				componentAdmittance = (-1j)/(2*math.pi*simulationFrequency*componentValue)
				if(node1 != 0):
					admittanceMatrix[node1 - 1][node1 - 1] += componentAdmittance
				if((node1 != 0) & (node2 != 0)):
					admittanceMatrix[node1 - 1][node2 - 1] -= componentAdmittance
					admittanceMatrix[node2 - 1][node1 - 1] -= componentAdmittance
				if(node2 != 0):
					admittanceMatrix[node2 - 1][node2 - 1] += componentAdmittance

		elif(commandtext[0].lower() == 'c'):
			componentValue = getComponentValue(commandtext[3])
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			if((simulationDomain == "DC") | (simulationFrequency == 0)):
				for i in range(len(admittanceMatrix)):
					admittanceMatrix[i].append(0)
				columnSliceTranspose = [0 for i in range(len(admittanceMatrix))]
				columnSliceTranspose.append(1)
				admittanceMatrix.append(columnSliceTranspose)
				voltageSources += 1
				unknownMatrix.append("I(" + commandtext[1] + ")")
				knownMatrix.append(0)

			elif(simulationDomain == "AC"):
				componentAdmittance = (1j)*(2*math.pi*simulationFrequency*componentValue)
				if(node1 != 0):
					admittanceMatrix[node1 - 1][node1 - 1] += componentAdmittance
				if((node1 != 0) & (node2 != 0)):
					admittanceMatrix[node1 - 1][node2 - 1] -= componentAdmittance
					admittanceMatrix[node2 - 1][node1 - 1] -= componentAdmittance
				if(node2 != 0):
					admittanceMatrix[node2 - 1][node2 - 1] += componentAdmittance
			
		elif(commandtext[0].lower() == 'v'):
			if(simulationDomain == "DC"):
				if (len(commandtext) == 4):
					componentValue = getComponentValue(commandtext[3])
					node1 = nodeList.index(nodes[0])
					node2 = nodeList.index(nodes[1])
					for i in range(len(admittanceMatrix)):
						admittanceMatrix[i].append(0)
						if (i == (node1 - 1)):
							admittanceMatrix[i][nodeCount + voltageSources] += 1
						if (i == (node2 - 1)):
							admittanceMatrix[i][nodeCount + voltageSources] -= 1
					columnSliceTranspose = [row[-1] for row in admittanceMatrix]
					columnSliceTranspose.append(0)
					admittanceMatrix.append(columnSliceTranspose)
					voltageSources += 1
					unknownMatrix.append("I(" + commandtext[1] + ")")
					knownMatrix.append(componentValue)
				else:
					node1 = nodeList.index(nodes[0])
					node2 = nodeList.index(nodes[1])
					for i in range(len(admittanceMatrix)):
						admittanceMatrix[i].append(0)
						if (i == (node1 - 1)):
							admittanceMatrix[i][nodeCount + voltageSources] += 1
						if (i == (node2 - 1)):
							admittanceMatrix[i][nodeCount + voltageSources] -= 1
					columnSliceTranspose = [row[-1] for row in admittanceMatrix]
					columnSliceTranspose.append(0)
					admittanceMatrix.append(columnSliceTranspose)
					voltageSources += 1
					unknownMatrix.append("I(" + commandtext[1] + ")")
					knownMatrix.append(0)
			if(simulationDomain == "AC"):
				if (len(commandtext) == 5):
					componentValue = getComponentValue(commandtext[3])
					node1 = nodeList.index(nodes[0])
					node2 = nodeList.index(nodes[1])
					if(getComponentValue(commandtext[4]) == simulationFrequency):
						for i in range(len(admittanceMatrix)):
							admittanceMatrix[i].append(0)
							if (i == (node1 - 1)):
								admittanceMatrix[i][nodeCount + voltageSources] += 1
							if (i == (node2 - 1)):
								admittanceMatrix[i][nodeCount + voltageSources] -= 1
						columnSliceTranspose = [row[-1] for row in admittanceMatrix]
						columnSliceTranspose.append(0)
						admittanceMatrix.append(columnSliceTranspose)
						voltageSources += 1
						unknownMatrix.append("I(" + commandtext[1] + ")")
						knownMatrix.append(componentValue)
					else:
						for i in range(len(admittanceMatrix)):
							admittanceMatrix[i].append(0)
							if (i == (node1 - 1)):
								admittanceMatrix[i][nodeCount + voltageSources] += 1
							if (i == (node2 - 1)):
								admittanceMatrix[i][nodeCount + voltageSources] -= 1
						columnSliceTranspose = [row[-1] for row in admittanceMatrix]
						columnSliceTranspose.append(0)
						admittanceMatrix.append(columnSliceTranspose)
						voltageSources += 1
						unknownMatrix.append("I(" + commandtext[1] + ")")
						knownMatrix.append(0)
				else:
					node1 = nodeList.index(nodes[0])
					node2 = nodeList.index(nodes[1])
					for i in range(len(admittanceMatrix)):
						admittanceMatrix[i].append(0)
						if (i == (node1 - 1)):
							admittanceMatrix[i][nodeCount + voltageSources] += 1
						if (i == (node2 - 1)):
							admittanceMatrix[i][nodeCount + voltageSources] -= 1
					columnSliceTranspose = [row[-1] for row in admittanceMatrix]
					columnSliceTranspose.append(0)
					admittanceMatrix.append(columnSliceTranspose)
					voltageSources += 1
					unknownMatrix.append("I(" + commandtext[1] + ")")
					knownMatrix.append(0)

		elif(commandtext[0].lower() == 'i'):
			if(simulationDomain == "DC"):
				if(len(commandtext) == 4):
					componentValue = getComponentValue(commandtext[3])
					node1 = nodeList.index(nodes[0])
					node2 = nodeList.index(nodes[1])
					if(node1 > 0):
						knownMatrix[node1 - 1] += componentValue
					if(node2 > 0):
						knownMatrix[node2 - 1] -= componentValue

			elif(simulationDomain == "AC"):
				if (len(commandtext) == 5):
					if(getComponentValue(commandtext[5]) == simulationFrequency):
						componentValue = getComponentValue(commandtext[3])
						node1 = nodeList.index(nodes[0])
						node2 = nodeList.index(nodes[1])
						if(node1 > 0):
							knownMatrix[node1 - 1] += componentValue
						if(node2 > 0):
							knownMatrix[node2 - 1] -= componentValue

		elif(commandtext[0].lower() == 'diffamp3'):
			componentValue = getComponentValue(commandtext[3])
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			node3 = nodeList.index(nodes[2])
			for i in range(len(admittanceMatrix)):
				admittanceMatrix[i].append(0)
				if (i == (node3 - 1)):
					admittanceMatrix[i][nodeCount + voltageSources] += 1
			columnSliceTranspose = [row[-1] for row in admittanceMatrix]
			columnSliceTranspose.append(0)
			admittanceMatrix.append(columnSliceTranspose)
			for i in range(len(admittanceMatrix)):
				if (i == (node1 - 1)):
					admittanceMatrix[nodeCount + voltageSources][i] += componentValue
				if (i == (node2 - 1)):
					admittanceMatrix[nodeCount + voltageSources][i] -= componentValue
			voltageSources += 1
			unknownMatrix.append("I(" + commandtext[1] + ")")
			knownMatrix.append(0)

		elif(commandtext[0].lower() == 'opamp3'):
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			node3 = nodeList.index(nodes[2])
			for i in range(len(admittanceMatrix)):
				admittanceMatrix[i].append(0)
				if (i == (node3 - 1)):
					admittanceMatrix[i][nodeCount + voltageSources] += 1
			columnSliceTranspose = [0 for i in range(len(admittanceMatrix))] #No longer the transpose
			columnSliceTranspose.append(0)
			admittanceMatrix.append(columnSliceTranspose)
			for i in range(len(admittanceMatrix)):
				if (i == (node1 - 1)):
					admittanceMatrix[nodeCount + voltageSources][i] += 1
				if (i == (node2 - 1)):
					admittanceMatrix[nodeCount + voltageSources][i] -= 1
			voltageSources += 1
			unknownMatrix.append("I(" + commandtext[1] + ")")
			knownMatrix.append(0)


def performAnalysis():
	global admittanceMatrix
	global knownMatrix
	formAdmittanceMatrix()
	admittanceMatrix = np.array(admittanceMatrix)
	knownMatrix = np.array(knownMatrix)
	admittanceMatrixInvert = np.linalg.inv(admittanceMatrix)
	solutionMatrix = np.dot(admittanceMatrixInvert, knownMatrix)
	solutionMatrix = solutionMatrix.tolist()

	for i in range(len(commands)):
		commandtext = commands[i].split(' ')
		if not(commands[i].startswith('.')):
			nodes = getNodes(commandtext[2])
		if ((commandtext[0].lower() == 'r') | (commandtext[0].lower() == 'g') | (commandtext[0].lower() == 'l') | \
			(commandtext[0].lower() == 'c')):
			componentValue = getComponentValue(commandtext[3])
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
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
			componentAdmittance = (-1j)/(2*math.pi*simulationFrequency*componentValue)
			unknownMatrix.append("I(" + commandtext[1] + ")")
			solutionMatrix.append(voltageAcross * componentAdmittance)

		elif(commandtext[0].lower() == 'c'):
			componentAdmittance = (1j)*(2*math.pi*simulationFrequency*componentValue)
			unknownMatrix.append("I(" + commandtext[1] + ")")
			solutionMatrix.append(voltageAcross * componentAdmittance)

	for i in range(len(solutionMatrix)):
		#print(unknownMatrix[i] + " = " + str(solutionMatrix[i]))
		if (getPhase(solutionMatrix[i]) < 180):
			print(unknownMatrix[i] + " = " + str(getMagnitude(solutionMatrix[i])) + "[" + str(getPhase(solutionMatrix[i])) + "]")
		else:
			print(unknownMatrix[i] + " = -" + str(getMagnitude(solutionMatrix[i])) + "[" + str(getPhase(solutionMatrix[i]) - 180) + "]")


if (simulationParameters[1].lower() == "op"):
	if(simulationDomain == "DC"):
		admittanceMatrix = [[0 for j in range(nodeCount)] for i in range(nodeCount)]
		knownMatrix = [0 for i in range(nodeCount)]
		voltageSources = 0
		print("Results for DC :")
		performAnalysis()
	elif (simulationDomain == "AC"):
		for i in simulationFrequencies:
			admittanceMatrix = [[0 for j in range(nodeCount)] for i in range(nodeCount)]
			knownMatrix = [0 for i in range(nodeCount)]
			voltageSources = 0
			simulationFrequency = i
			print("Results for frequency " + str(simulationFrequency) + " :")
			performAnalysis()
