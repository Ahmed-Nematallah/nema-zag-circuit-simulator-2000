"""Module for analyzing the netlist."""

# import re
import numpy as np
import math
# import random
import copy
import matplotlib.pyplot as plt

def getComponentValue(componentValue):
	"""Convert component value suffix to floatinv value."""
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

def rect2pol(complexNumber):
	"""Rectangular to plar coordinates."""
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

	return (abs(complexNumber), phase)

def pol2rect(magnitude, phase):
	"""Polar to rectangular coordinates."""
	complexNumber = complex(magnitude * math.cos(phase), magnitude * math.sin(phase))
	return complexNumber

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
# R R1 (N1;N2) 1k
# R R2 (N3;N0) 1k
# L L1 (N2;N3) 1m
# V V1 (N1;N0) 10"""
# netlist = """.DC OP
# V V1 (N1;N0) 10
# R R1 (N2;N1) 10k
# R R2 (N2;N0) 10k
# R R3 (N4;N3) 10k
# OPAMP3 A1 (N2;N3;N4)"""
# netlist = """.AC SWEEP FREQ V1 10 10000 N2
# .GRAPH N1 N2
# V V1 (N1;N0) 10 1
# G G1 (N1;N2) 6.28318530718m
# C C1 (N0;N2) 1u
# R R1 (N1;N0) 1k"""
# netlist = """.AC OP
# .GRAPH N1 N4
# V V1 (N1;N0) 10 500
# V V2 (N2;N0) 5 200
# R R1 (N0;N2) 1k
# C C1 (N2;N1) 1u
# OPAMP3 A1 (N2;N3;N4)
# R R2 (N3;N4) 1k
# R R3 (N3;N0) 1k"""
# netlist = """.AC op
# .GRAPH N1 N2
# V V1 (N1;N0) 10 500
# V V2 (N2;N0) 10 0
# C C1 (N1;N2) 1u
# R R1 (N1;N2) 1k
# R R2 (N1;N0) 1k"""
# netlist = """.AC op
# .GND N0
# .GRAPH Input Output
# V V1 (Input;N0) 10 180
# R R1 (Input;N2) 4.7k
# R R2 (N2;N3) 6.8k
# R R3 (N5;N4) 1.0k
# R R4 (N4;N0) 6.8k
# R R5 (N5;N6) 4.7k
# R R6 (N6;N7) 6.8k
# R R7 (Output;N8) 6.8k
# R R8 (N8;N0) 5.6k
# C C1 (N2;N5) 0.22u
# C C2 (N3;N0) 0.1u
# C C3 (N6;Output) 0.22u
# C C4 (N7;N0) 0.1u
# *First opamp
# OPAMP3 A1 (N3;N4;N5)
# OPAMP3 A2 (N7;N8;Output) *Second opamp"""
# netlist = """.DC op
# .GND N0
# V V1 (N1;N0) 100
# R R1 (N1;N2) 100
# D D1 (N2;N0)
# R R2 (N1;N3) 100
# D D2 (N0;N3)
# D D3 (N1;N4)
# R R3 (N4;N0) 100"""
netlist = """.DC OP
.GND N0
OPAMP3 O0 (N3;N2;N1) 
V V0 (N2;N0) 10.0
R R1 (N3;N0) 1000.0
R R2 (N3;N1) 1000.0
"""

sweepit = 0
satCurrent = 10**-14
thermalVoltage = 0.026
magList = [0 for i in range(100)]
phaList = [0 for i in range(100)]
i = 0
vCriticalDiode = thermalVoltage * math.log1p(thermalVoltage / (math.sqrt(2) * satCurrent))
simulationDomain = ""
simulationFrequencies = []
simulationParameters = []
toGraph = []
commands = []
nodeList = []
nodeListNatural = []
voltageSources = 0
groundNode = "n0"
nodeCount = 0
admittanceMatrix = []
currentMatrix = []
groundNodeIndex = []
voltageMatrixLabels = []
simulationFrequency = 0
def analyzeFile():
	global commands
	global simulationDomain
	global simulationFrequencies
	global simulationParameters
	global nodeList
	global nodeListNatural
	global nodeCount
	global admittanceMatrix
	global currentMatrix
	global groundNodeIndex
	global voltageMatrixLabels
	global simulationFrequency

	commands = netlist.splitlines()
	commands = list(filter(None, commands))
	for i in range(len(commands)):
		commandtext = commands[i].split(' ')
		if ('*' in commands[i]):
			temp = commands[i][0:commands[i].index('*')]
			if not(temp is ''):
				commands[i] = temp
				commandtext = commands[i].split(' ')
			else:
				commands[i] = ''
				continue
		commandtext = list(filter(None, commandtext))

		if (commandtext[0].lower() == ".dc"):
			simulationDomain = "DC"
			simulationParameters = copy.copy(commandtext)
		elif (commandtext[0].lower() == ".ac"):
			simulationDomain = "AC"
			simulationParameters = copy.copy(commandtext)
		elif (commandtext[0].lower() == ".gnd"):
			groundNode = commandtext[1].lower()
		elif (commandtext[0].lower() == ".graph"):
			toGraph.append(commandtext[1].lower())
			toGraph.append(commandtext[2].lower())

		if ((commandtext[0].lower() == "v") | (commandtext[0].lower() == "i")):
			if (len(commandtext) > 4):
				if (rect2pol(getComponentValue(commandtext[4]))[0] not in simulationFrequencies):
					simulationFrequencies.append(rect2pol(getComponentValue(commandtext[4]))[0])

		if not(commands[i].startswith('.')):
			localNodes = getNodes(commandtext[2])
			for i in range(len(localNodes)):
				if localNodes[i] not in nodeList:
					nodeList.append(localNodes[i])
					nodeListNatural.append(commandtext[2][1:-1].split(';')[i])

	commands = list(filter(None, commands))
	simulationFrequencies.sort()
	simulationFrequency = 0
	nodeCount = len(nodeList) - 1
	nodeListNatural = [x for (y, x) in sorted(zip(nodeList, nodeListNatural), key=lambda pair: pair[0])]
	nodeList.sort()
	admittanceMatrix = [[0 for j in range(nodeCount)] for i in range(nodeCount)]
	currentMatrix = [0 for i in range(nodeCount)]

	groundNodeIndex = nodeList.index(groundNode)
	if (groundNodeIndex > 0):
		nodeList[groundNodeIndex] = copy.copy(nodeList[0])
		nodeList[0] = groundNode

		temp = copy.copy(nodeListNatural[groundNodeIndex])
		nodeListNatural[groundNodeIndex] = copy.copy(nodeListNatural[0])
		nodeListNatural[0] = temp

	voltageMatrixLabels = ["V(" + nodeListNatural[i + 1] + ")" for i in range(nodeCount)]

def plot2sine(mag1, phase1, mag2, phase2):
	"""Plot magnitude and phase of two complex numbers."""
	t = np.arange(0.0, 1.01, 0.01)
	figure1 = plt.figure(1)
	fig = figure1.add_subplot(111)
	fig.plot(t, mag1 * np.sin(4 * np.pi * t + phase1 * (180 / np.pi)))
	fig.plot(t, mag2 * np.sin(4 * np.pi * t + phase2 * (180 / np.pi)))
	fig.set_ylim((-max(mag1, mag2), max(mag1, mag2)))
	fig.set_ylabel('Magnitude')
	fig.set_title('phase difference')
	plt.show()

def displaymagphase(array1, array2, array3, array4):
	# array1=[1,2,3,4,5,6]
	# array2=[0.5,2,3,4,5,6]
	figure1 = plt.figure(1)
	up = figure1.add_subplot(211)
	up.plot(array1, array2)
	up.set_ylim(min(array2), max(array2))
	up.set_ylabel('magnitude')
	up.set_title('magnitude')
	down = figure1.add_subplot(212)
	down.plot(array3, array4)
	down.set_ylim(min(array4), max(array4))
	down.set_ylabel('phase')
	down.set_title('phase')
	plt.show()

def formAdmittanceMatrix():
	"""Form the base admittance matrix for analysis."""
	global voltageSources
	global admittanceMatrix
	global simulationFrequency
	global currentMatrix
	admittanceMatrix = [[0 for j in range(nodeCount)] for i in range(nodeCount)]
	currentMatrix = [0 for i in range(nodeCount)]
	for i in range(len(commands)):
		commandtext = commands[i].split(' ')
		commandtext = list(filter(None, commandtext))
		if not(commands[i].startswith('.')):
			nodes = getNodes(commandtext[2])
		# nodesAndValues = re.findall(r"\(([A-Za-z0-9_,. ]*)\)", commands[i])
		# if (nodesAndValues != []):
		# 	nodes = nodesAndValues[0].split(', ')

		if(commandtext[0].lower() == 'r'):
			componentValue = getComponentValue(commandtext[3])
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			componentAdmittance = 1 / componentValue
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
			if((simulationDomain == "DC") | (simulationFrequency == 0)):  # Consider it a short circuit,
				for i in range(len(admittanceMatrix)):					  # or a 0V voltage source, neat, heh?
					admittanceMatrix[i].append(0)
					if (i == (node1 - 1)):
						admittanceMatrix[i][nodeCount + voltageSources] += 1
					if (i == (node2 - 1)):
						admittanceMatrix[i][nodeCount + voltageSources] -= 1
				columnSliceTranspose = [row[-1] for row in admittanceMatrix]
				columnSliceTranspose.append(0)
				admittanceMatrix.append(columnSliceTranspose)
				voltageSources += 1
				voltageMatrixLabels.append("I(" + commandtext[1] + ")")
				currentMatrix.append(0)

			elif(simulationDomain == "AC"):
				componentAdmittance = (-1j) / (2 * math.pi * simulationFrequency * componentValue)
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
				voltageMatrixLabels.append("I(" + commandtext[1] + ")")
				currentMatrix.append(0)

			elif(simulationDomain == "AC"):
				componentAdmittance = (1j) * (2 * math.pi * simulationFrequency * componentValue)
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
					voltageMatrixLabels.append("I(" + commandtext[1] + ")")
					currentMatrix.append(componentValue)
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
					voltageMatrixLabels.append("I(" + commandtext[1] + ")")
					currentMatrix.append(0)
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
						voltageMatrixLabels.append("I(" + commandtext[1] + ")")
						currentMatrix.append(componentValue)
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
						voltageMatrixLabels.append("I(" + commandtext[1] + ")")
						currentMatrix.append(0)
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
					voltageMatrixLabels.append("I(" + commandtext[1] + ")")
					currentMatrix.append(0)

		elif(commandtext[0].lower() == 'i'):
			if(simulationDomain == "DC"):
				if(len(commandtext) == 4):
					componentValue = getComponentValue(commandtext[3])
					node1 = nodeList.index(nodes[0])
					node2 = nodeList.index(nodes[1])
					if(node1 > 0):
						currentMatrix[node1 - 1] += componentValue
					if(node2 > 0):
						currentMatrix[node2 - 1] -= componentValue

			elif(simulationDomain == "AC"):
				if (len(commandtext) == 5):
					if(getComponentValue(commandtext[4]) == simulationFrequency):
						componentValue = getComponentValue(commandtext[3])
						node1 = nodeList.index(nodes[0])
						node2 = nodeList.index(nodes[1])
						if(node1 > 0):
							currentMatrix[node1 - 1] += componentValue
						if(node2 > 0):
							currentMatrix[node2 - 1] -= componentValue

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
			voltageMatrixLabels.append("I(" + commandtext[1] + ")")
			currentMatrix.append(0)

		elif(commandtext[0].lower() == 'opamp3'):
			node1 = nodeList.index(nodes[0])
			node2 = nodeList.index(nodes[1])
			node3 = nodeList.index(nodes[2])
			for i in range(len(admittanceMatrix)):
				admittanceMatrix[i].append(0)
				if (i == (node3 - 1)):
					admittanceMatrix[i][nodeCount + voltageSources] += 1
			columnSliceTranspose = [0 for i in range(len(admittanceMatrix))]  # No longer the transpose
			columnSliceTranspose.append(0)
			admittanceMatrix.append(columnSliceTranspose)
			for i in range(len(admittanceMatrix)):
				if (i == (node1 - 1)):
					admittanceMatrix[nodeCount + voltageSources][i] += 1
				if (i == (node2 - 1)):
					admittanceMatrix[nodeCount + voltageSources][i] -= 1
			voltageSources += 1
			voltageMatrixLabels.append("I(" + commandtext[1] + ")")
			currentMatrix.append(0)


def performAnalysis():
	"""Perform the analysis."""
	global magList
	global phaList
	global sweepit
	global admittanceMatrix
	global currentMatrix
	result = ""
	formAdmittanceMatrix()
	admittanceMatrix = np.array(admittanceMatrix)
	currentMatrix = np.array(currentMatrix)
	basecurrentMatrix = copy.deepcopy(currentMatrix)
	voltageMatrix = [0 for i in currentMatrix]
	# voltageMatrixOld = [0 for i in currentMatrix]
	voltageAcrossOld = 0
	conv = 100000
	while conv > 10**-20:
		nlJacobian = [[0 for j in i] for i in admittanceMatrix]
		currentMatrix = copy.deepcopy(basecurrentMatrix)
		# form currentMatrix & complete nlJacobian
		for i in commands:
			commandtext = i.split(' ')
			if not(i.startswith('.')):
				nodes = getNodes(commandtext[2])
			if (commandtext[0].lower() == 'd'):
				print(commandtext[1])
				node1 = nodeList.index(nodes[0])
				node2 = nodeList.index(nodes[1])
				voltageAcross = 0
				if ((node1 == 0) & (node2 == 0)):
					voltageAcross = 0
				elif(node1 == 0):
					voltageAcross = -voltageMatrix[node2 - 1]
				elif(node2 == 0):
					voltageAcross = voltageMatrix[node1 - 1]
				else:
					voltageAcross = voltageMatrix[node1 - 1] - voltageMatrix[node2 - 1]

				if (voltageAcrossOld < vCriticalDiode):
					pass
				else:
					voltageAcross = voltageAcrossOld + thermalVoltage *  \
						math.log1p((((voltageAcross - voltageAcrossOld) / thermalVoltage) + 1).real)

				diodeCurrent = satCurrent * (math.e ** (voltageAcross / thermalVoltage) - 1)
				print(voltageAcross)
				if node1 != 0:
					currentMatrix[node1 - 1] -= diodeCurrent
					nlJacobian[node1 - 1][node1 - 1] += -diodeCurrent / thermalVoltage
				if node2 != 0:
					currentMatrix[node2 - 1] += diodeCurrent
					nlJacobian[node2 - 1][node2 - 1] += -diodeCurrent / thermalVoltage
				if((node1 != 0) & (node2 != 0)):
					nlJacobian[node1 - 1][node2 - 1] += diodeCurrent / thermalVoltage
					nlJacobian[node2 - 1][node1 - 1] += diodeCurrent / thermalVoltage

		Jacobian = admittanceMatrix - nlJacobian
		voltageMatrix2 = np.dot(np.linalg.inv(Jacobian), -np.dot(nlJacobian, voltageMatrix) + currentMatrix)
		conv = 0
		for i in range(len(voltageMatrix)):
			conv += (voltageMatrix[i] - voltageMatrix2[i])**2

		for i in range(len(voltageMatrix)):
			if ((voltageMatrix[i] - voltageMatrix2[i]) > 10):
				voltageMatrix2[i] = voltageMatrix[i] - 10
			elif ((voltageMatrix2[i] - voltageMatrix[i]) > 10):
				voltageMatrix2[i] = voltageMatrix[i] + 10
		voltageMatrix = copy.copy(voltageMatrix2)
	# admittanceMatrixInvert = np.linalg.inv(admittanceMatrix)
	# solutionMatrix = np.dot(admittanceMatrixInvert, currentMatrix)
	# solutionMatrix = solutionMatrix.tolist()
	solutionMatrix = voltageMatrix.tolist()

	for i in range(len(commands)):
		commandtext = commands[i].split(' ')
		if not(commands[i].startswith('.')):
			nodes = getNodes(commandtext[2])
		if ((commandtext[0].lower() == 'r') | (commandtext[0].lower() == 'g') |
			(commandtext[0].lower() == 'l') | (commandtext[0].lower() == 'c') |
			(commandtext[0].lower() == 'd')):
			if not(commandtext[0].lower() == 'd'):
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
			voltageMatrixLabels.append("I(" + commandtext[1] + ")")
			solutionMatrix.append(voltageAcross / componentValue)

		elif(commandtext[0].lower() == 'g'):
			voltageMatrixLabels.append("I(" + commandtext[1] + ")")
			solutionMatrix.append(voltageAcross * componentValue)

		elif(commandtext[0].lower() == 'l'):
			if (simulationDomain == "AC"):
				componentAdmittance = (-1j) / (2 * math.pi * simulationFrequency * componentValue)
				voltageMatrixLabels.append("I(" + commandtext[1] + ")")
				solutionMatrix.append(voltageAcross * componentAdmittance)

		elif(commandtext[0].lower() == 'c'):
			if (simulationDomain == "AC"):
				componentAdmittance = (1j) * (2 * math.pi * simulationFrequency * componentValue)
				voltageMatrixLabels.append("I(" + commandtext[1] + ")")
				solutionMatrix.append(voltageAcross * componentAdmittance)

		elif(commandtext[0].lower() == 'd'):
			voltageMatrixLabels.append("I(" + commandtext[1] + ")")
			solutionMatrix.append(satCurrent * (math.e ** (voltageAcross / thermalVoltage) - 1))

	for i in range(len(solutionMatrix)):
		# print(voltageMatrixLabels[i] + " = " + str(solutionMatrix[i]))
		print(voltageMatrixLabels[i] + " = " + str(rect2pol(solutionMatrix[i])[0]) + "[" + str(rect2pol(solutionMatrix[i])[1]) + "]")
		result += voltageMatrixLabels[i] + " = " + str(rect2pol(solutionMatrix[i])[0]) + "[" + str(rect2pol(solutionMatrix[i])[1]) + "]\n"
	if len(toGraph) > 0:
		a = rect2pol(solutionMatrix[nodeList.index(toGraph[0]) - 1])[0]
		b = rect2pol(solutionMatrix[nodeList.index(toGraph[0]) - 1])[1]
		c = rect2pol(solutionMatrix[nodeList.index(toGraph[1]) - 1])[0]
		d = rect2pol(solutionMatrix[nodeList.index(toGraph[1]) - 1])[1]
		if simulationParameters[1].lower() == "op":
			plot2sine(a, b, c, d)
		elif simulationParameters[1].lower() == "sweep":
			magList[sweepit] = rect2pol(solutionMatrix[nodeList.index(simulationParameters[6].lower()) - 1])[0]
			phaList[sweepit] = rect2pol(solutionMatrix[nodeList.index(simulationParameters[6].lower()) - 1])[1]
			sweepit += 1

	return result

def __main__():
	global netlist
	global voltageSources
	global simulationFrequency
	global admittanceMatrix
	global currentMatrix
	global voltageSources
	global voltageMatrixLabels
	global sweepit
	sweepit = 0
	f = open("circuit.net", 'r')
	netlist = f.read()
	analyzeFile()
	result = ""
	if (simulationParameters[1].lower() == "op"):
		if(simulationDomain == "DC"):
			voltageMatrixLabels = ["V(" + nodeListNatural[i + 1] + ")" for i in range(nodeCount)]
			admittanceMatrix = [[0 for j in range(nodeCount)] for i in range(nodeCount)]
			currentMatrix = [0 for i in range(nodeCount)]
			voltageSources = 0
			print("Results for DC :")
			result += "Results for DC :\n"
			result += performAnalysis()
		elif (simulationDomain == "AC"):
			for i in simulationFrequencies:
				voltageMatrixLabels = ["V(" + nodeListNatural[i + 1] + ")" for i in range(nodeCount)]
				admittanceMatrix = [[0 for j in range(nodeCount)] for i in range(nodeCount)]
				currentMatrix = [0 for i in range(nodeCount)]
				voltageSources = 0
				simulationFrequency = i
				print("Results for frequency " + str(simulationFrequency) + " :")
				result += "Results for frequency " + str(simulationFrequency) + " :\n"
				result += performAnalysis()
	elif (simulationParameters[1].lower() == "sweep"):
		if (simulationDomain == "AC"):
			if (simulationParameters[2].lower() == "freq"):
				for i in range(len(commands)):
					if commands[i].split(" ")[1] == simulationParameters[3]:
						a = float(simulationParameters[4])
						b = float(simulationParameters[5])
						for j in range(100):
							simulationFrequency = a + (b - a) * j / 100
							commands[i] = commands[i].split(" ")[0] + " " + commands[i].split(" ")[1] + " " + \
								commands[i].split(" ")[2] + " " + commands[i].split(" ")[3] + " " + str(simulationFrequency)
							voltageMatrixLabels = ["V(" + nodeListNatural[k + 1] + ")" for k in range(nodeCount)]
							admittanceMatrix = [[0 for k in range(nodeCount)] for i in range(nodeCount)]
							currentMatrix = [0 for l in range(nodeCount)]
							voltageSources = 0
							performAnalysis()
						displaymagphase(np.arange(a, b, (b-a)/100), magList, np.arange(a, b, (b-a)/100), phaList)

	return result

# __main__()
