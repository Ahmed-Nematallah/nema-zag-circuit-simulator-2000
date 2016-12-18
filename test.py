import numpy as np
import math
import random

sati = 10**-14
gmat = [[0.01, -0.01, 1.0], [-0.01, 0.02, 0.0], [1.0, 0.0, 0.0]]
imat = [[0.0], [sati], [30.0]]
vmat = [[0], [0], [0]]
v2mat = np.array(vmat) - 100
err = 0
for i in range(len(vmat)):
	err += (vmat[i][0]-v2mat[i][0])**2

while err > 0:
	imat = [[0.0], [], [30.0]]
	f = np.dot(gmat, vmat) - imat
	abc = [[0.0, 0, 0], [0, -sati*(math.e**(vmat[1][0]/0.026) - 1)/0.026, 0], [0, 0.0, 0]]
	jmat = np.array(gmat) - abc
	v2mat = vmat - np.dot(np.linalg.inv(jmat), f)
	err = 0
	for i in range(len(vmat)):
		err += (vmat[i][0]-v2mat[i][0])**2
	vmat = v2mat

print(vmat)