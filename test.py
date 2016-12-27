
import matplotlib.pyplot as plt

def displaymagphase(array1,array2,array3,array4):
	#array1=[1,2,3,4,5,6]
	#array2=[0.5,2,3,4,5,6]
	figure1 = plt.figure(1)
	up = figure1.add_subplot(211)
	up.plot(array1,array2)
	up.set_ylim((0,max(max(array1),max(array2))))
	up.set_ylabel('magnitude')
	up.set_title('magnitude')
	down = figure1.add_subplot(212)
	down.plot(array3,array4)
	down.set_ylim((0,max(max(array3),max(array4))))
	down.set_ylabel('phase')
	down.set_title('phase')
	plt.show()

displaymagphase(range(100), range(100), range(100), range(100))