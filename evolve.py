'''
This file is where the evolving of the AIs happen
'''

#make an individual
#from ai_rule import AIRule
import mvc

from deap import algorithms, base, tools, creator

def fitness_function(ai_team):
	'''
	evaluating fitness in terms of:
	- difference between number of units on each team
	- how close units are to flag
	- how close units are to other team units
	- once unit has flag, how close it is to base
	'''
	unit_list = mvc.Model.unit_list
	flag_list = mvc.Model.flag_list

	ai_strength = 0
	ai_distance_flag = 0

	opposite_flag = ''

	# find the opposite team's flag
	for flag in flag_list:
		if flag.team != ai_team:
			opposite_flag = flag

	#loop through all of the units
	for unit in unit_list:
		# if on the same team, then add one to ai_strenght
		if unit.team == ai_team:
			ai_strength += 1
			ai_distance_flag += (unit.pos[0]**2+unit.pos[1]**2)**(1/2)
		else:
			ai_strength -= 1

	fitness = (ai_strength, ai_distance_flag)
	return(fitness)


def evaluate_ai(ai):
	'''
	Given an AI, returns the fitness of it
	'''
	ai_team = ai.team
	fitness = fitness_function(ai_team)
	return(fitness)

def mutate():
	'''
	change the weights of the AI randomly
	'''
	pass

def mate():
	'''
	simulate mating between two individuals
	might be able to use DEAP stuff
	'''
	pass

def get_toolbox():
	pass

def evolve_ai():
	'''
	mostly going to be DEAP library
	'''

	pass

'''
class FitnessMinimize(base.Fintess):
	weights = (-1.0,)
'''
