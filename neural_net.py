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
	""" DOCSTRING
		Takes list of lists; rtrns list of items
		"""
	return([item for sublist in lists for item in sublist])


def sigmoid(x):
	""" DOCSTRING
		Takes dot product of two vectors; rtrns result from passing value into
		sigmoid function
		Video: https://www.youtube.com/watch?v=h3l4qz76JhQ&vl=en
		"""
    return(1/(1 + np.exp(-x)))
# derivative of sigmoid
# sigmoid(y) * (1.0 - sigmoid(y))
# the way we use this y is already sigmoided


def dsigmoid(y, deriv=True):
	""" DOCSTRING
		Takes dot product of two vectors & boolean; returns sigmoid / derivative
		 of sigmoid dependend on inputs
		 TODO: More Research
		"""
	y = sigmoid(y)
	return(y * (1 - y))


def nonlin(x,deriv=False):

	""" DOCSTRING
		Takes dot product of two vectors; returns sigmoid; breaks down into
		sigmoid() & dsigmoid
		TODO: More Research
		"""
	if (deriv == True):
		return(x*(1-x))

	return(1/(1+np.exp(-x)))

#input data
X = np.array([single_list(information_sample1),
	single_list(information_sample2)])

Y = np.array([calc.sum_forces_all(information_sample1),
	calc.sum_forces_all(information_sample2)])
print(Y)
np.random.seed(1)

syn0 = 50*np.random.random((40,5))-1
syn1 = 50*np.random.random((5,12))-1

for j in range(50000):
	l0 = X
	l1 = nonlin(np.dot(l0,syn0))
	l2 = nonlin(np.dot(l1,syn1))

	l2_error = Y - l2

	if(j % 10000) == 12:
		print("Error: " + str(np.mean(np.abs(l2_error))))

	l2_delta = l2_error*nonlin(l2, deriv=True)
	l1_error = l2_delta.dot(syn1.T)
	l1_delta = l1_error*nonlin(l1,deriv=True)

	if(j % 10000) == 12:
		#print("Error: " + str(np.mean(np.abs(l2_error))))
		print("syn1 old: " + str(nonlin((np.dot(l0,syn0)))))
	syn1 += l1.T.dot(l2_delta)
	syn0 += l0.T.dot(l1_delta)


print(l2)
