'''
This file is where the evolving of the AIs happen
'''

#make an individual
#from ai_rule import AIRule
import mvc
import random
import ai_rule as AI
import numpy
from deap import algorithms, base, tools, creator
import gods_of_capture as gods

# TODO: class fitness maximize, want to maximize ai_strength
# creates that represents fitness (it's the same as creating an object but
# weird looking becasue it's DEAP)
# weights are (1.0, -1.0, 1.0) because we want to maximize strength, minimize
# distance to the flag, and mazimize if the AI wins  (this if for the fitness
# tuple (ai_strength, distance, win))




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
		# if on the same team, then add one to ai_strength
		if unit.team == ai_team:
			ai_strength += 1
			ai_distance_flag += (unit.pos[0]**2+unit.pos[1]**2)**(1/2)
		else:
			ai_strength -= 1

	# TODO: I'm thinking that these numbers should be stats for an entire game and
	# we should add a value that's a 1 if the ai won and 0 if it lost
	# we also may want to consier other mearures of fitness
	# ideas: how many of their units died, how many of the other units they killed,
	# how many times they picked up the flag/their flag was picked up, etc.
	# In any case, I think we'll have to have the ai play an entire game and
	# evolve the weights off that.
	fitness = (ai_strength, ai_distance_flag)
	return(fitness)


def evaluate_ai(ai):
	'''
	Given an AI, returns the fitness of it
	'''
	game = gods.CaptureGame(ai, True)
	game.run()
	ai_team = ai.team
	current_state = ai.evaluate_state()
	#print(current_state)
	return(current_state)

def mutate(ai, probs_weights = 0.05):
	'''
	change the weights of the AI randomly
	usually mutation involves insertion, deletion, and substitution, but since
	AIRule.wieghts must be fixed length, we only use substitution
	'''
	
	#idk if we need this if statement yet, but i'll leave it
	# commented in case we do
	#if random.random() < probs_weights:
	
	# choose a random index in ai.weights
	i = random.randint(0, len(ai.weights)-1)
	# choose a random number between 0 and 10 to replace
	# the current weight value by
	char = random.randint(0, 10)
	char = float(char/10)
	# insert the new weight at the ith index
	ai.weights.insert(i, char)
	# return ai in a length 1 tuple (required by DEAP)
	return(AI.AIRule(1, ai.weights), )

def mate(ai1, ai2):
	'''
	simulate mating between two individuals
	might be able to use DEAP stuff
	'''
	
	toolbox = base.Toolbox()
	# this seems to do something with mating...
	i = 0
	while i < len(ai1.weights):
		if random.randint(0,1) == 0:
			new2_weight = ai1.weights[i] 
			new1_weight = ai2.weights[i]
			ai2.weights[i] = new2_weight
			ai1.weights[i] = new1_weight
		i += 1
	#toolbox.mate(ai1.weights, ai2.weights)
	return(ai1, ai2)
	# delete the current fitness values associated with the parents 



def get_toolbox():
	'''
	Return DEAP Toolbox configured given AI
	'''
	toolbox = base.Toolbox()

	# CREATE POLULATION TO BE EVOLVED
	
	# create individual (using the AIRule object for an individual we created outselves)
	toolbox.register("individual", AI.AIRule)
	# create a polution
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)
	# initialize genetic operators
	# evaluate using fit function
	toolbox.register("evaluate", evaluate_ai)
	# mate using two point crossover
	# TODO: figure out how this works/how we can mate AIRule.weights specifically
	toolbox.register("mate", mate)
	
	# mutate function written above (insertion only)
	toolbox.register("mutate", mutate)
	
	# selection method, tournsize: number of individuals participlatingin each
	# tournament
	toolbox.register("select", tools.selTournament, tournsize=3)
	return toolbox


def evolve_ai():
	'''
	use evolutionary algorithm to evolve ai object
	mostly going to be DEAP library
	'''
	# set random number generator seed so results are repeatable
	random.seed(4)

	# configure toolbox using get_toolbox
	toolbox = get_toolbox()

	# create a population or random ai objects
	pop = toolbox.population(n=10)

	# Collect statistics as the EA runs
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)
	# run evolutionary algorithm
	pop, log = algorithms.eaSimple(pop,
								   toolbox,
								   cxpb=1,  # Prob. of crossover (mating)
								   mutpb=1, # Prob of mutation
								   ngen=100,	  # number of generations to run
								   stats=stats)

	#print(stats)
	return pop, log


pop, log = evolve_ai()

