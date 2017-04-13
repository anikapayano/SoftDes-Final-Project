import numpy as np
import force_calculator as fc

calc = fc.Calculator()

screen_x = 1840
screen_y = 920

# information stored as [x, y, team (1 or 2), discovered (0 undiscovered, 1 discovered), exists (0 does not, 1 does)] per unit
information_sample1 = [[screen_x-1500, screen_y - 750, 1, 1, 1], [screen_x-1500, screen_y - 550, 1, 1, 1], [screen_x-1500, screen_y - 350, 1, 1, 1],
			 [screen_x-300, screen_y - 750, 2, 1, 1], [screen_x-300, screen_y - 550, 2, 1, 1], [screen_x-300, screen_y - 350, 2, 1, 1],
			 [screen_x-1700, screen_y/2, 1, 1, 1], [screen_x-140, screen_y/2, 2, 1, 1]]

information_sample2 = [[screen_x-1300, screen_y - 550, 1, 1, 1], [screen_x-1500, screen_y - 250, 1, 1, 1], [screen_x-500, screen_y - 650, 1, 1, 1],
			 [screen_x-100, screen_y - 750, 2, 1, 1], [screen_x-1300, screen_y - 400, 2, 1, 1], [screen_x-900, screen_y - 150, 2, 1, 1],
			 [screen_x-1700, screen_y/2, 1, 1, 1], [screen_x-140, screen_y/2, 2, 1, 1]]

def single_list(lists):
	return([item for sublist in lists for item in sublist])

def nonlin(x,deriv=False):
	if(deriv==True):
		return x*(1-x)

	return 1/(1+np.exp(-x))

#input data
X = np.array([single_list(information_sample1),
	single_list(information_sample2)])

y = np.array([calc.sum_forces_all(information_sample1),
	calc.sum_forces_all(information_sample2)])

np.random.seed(1)

syn0 = 2*np.random.random((40,4)) -1
syn1 = 2*np.random.random((4,12)) -1

for j in range(50000):
	l0 = X
	l1 = nonlin(np.dot(l0,syn0))
	l2 = nonlin(np.dot(l1,syn1))

	l2_error = y - l2

	if(j % 10000) == 12:
		print("Error: " + str(np.mean(np.abs(l2_error))))

	l2_delta = l2_error*nonlin(l2, deriv=True)
	l1_error = l2_delta.dot(syn1.T)
	l1_delta = l1_error*nonlin(l1,deriv=True)

	syn1 += l1.T.dot(l2_delta)
	syn0 += l0.T.dot(l1_delta)


print(l2)
