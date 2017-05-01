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
from os.path import exists
import sys
from pickle import dump, load

# TODO: class fitness maximize, want to maximize ai_strength
# creates that represents fitness (it's the same as creating an object but
# weird looking becasue it's DEAP)
# weights are (1.0, -1.0, 1.0) because we want to maximize strength, minimize
# distance to the flag, and mazimize if the AI wins  (this if for the fitness
# tuple (ai_strength, distance, win))


class Evolution():
	'''
	Evolves AI
	'''

	def __init__(self):
		self.ai2 = AI.AIRule(2,[0.1,1,1,1,1])


	def evaluate_ai(self, ai1):
		'''
		Given an AI, returns the fitness of it
		'''
		
		game = gods.CaptureGame(ai1, self.ai2, True)
		game.run()
		ai_team = ai1.team
		current_state = ai1.state_evaluation
		#print(current_state)
		#print('ai evaluated')
		return(current_state)

	def mutate(self, ai, insert_weights = 0.2, increment_weights = 0.2):
		'''
		change the weights of the AI randomly
		usually mutation involves insertion, deletion, and substitution, but since
		AIRule.wieghts must be fixed length, we only use substitution
		'''
		
		#idk if we need this if statement yet, but i'll leave it
		# commented in case we do
		if random.random() < insert_weights:
			# choose a random index in ai.weights
			i = random.randint(0, len(ai.weights)-1)
			# choose a random number between 0 and 10 to replace
			# the current weight value by
			char = random.randint(0, 100)
			char = float(char/100)
			# insert the new weight at the ith index
			ai.weights[i] = char #.insert(i, char)
			# return ai in a length 1 tuple (required by DEAP)
			#print('no problem')
		if random.random() < increment_weights:
			i = random.randint(0, len(ai.weights)-1)
			if ai.weights[i] <= 0.95:
				ai.weights[i] += 0.05

		return(AI.AIRule(1, ai.weights), )

	def mate(self, ai1, ai2):
		'''
		simulate mating between two individuals
		might be able to use DEAP stuff
		'''
		
		toolbox = base.Toolbox()
		# this seems to do something with mating...
		i = 0
		if len(ai1.weights) == len(ai2.weights):
			while i < len(ai1.weights):
				if random.randint(0,1) == 0:
					new2_weight = ai1.weights[i] 
					new1_weight = ai2.weights[i]
					ai2.weights[i] = new2_weight
					ai1.weights[i] = new1_weight
				i += 1
		ai1.state_evaluation = (0,)
		ai2.state_evaluation = (0,)
		return(ai1, ai2)
		# delete the current fitness values associated with the parents 



	def get_toolbox(self):
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
		toolbox.register("evaluate", self.evaluate_ai)
		# mate using two point crossover
		# TODO: figure out how this works/how we can mate AIRule.weights specifically
		toolbox.register("mate", self.mate)
		
		# mutate function written above (insertion only)
		toolbox.register("mutate", self.mutate)
		
		# selection method, tournsize: number of individuals participlatingin each
		# tournament
		toolbox.register("select", tools.selTournament, tournsize=3)
		return toolbox


	def evolve_ai(self):
		'''
		use evolutionary algorithm to evolve ai object
		mostly going to be DEAP library
		'''
		# set random number generator seed so results are repeatable
		#random.seed(4)

		# configure toolbox using get_toolbox
		toolbox = self.get_toolbox()

		# create a population or random ai objects
		pop = toolbox.population(n=20)

		# Collect statistics as the EA runs
		stats = tools.Statistics(lambda ind: ind.fitness.values)
		stats.register("avg", numpy.mean)
		stats.register("std", numpy.std)
		stats.register("min", numpy.min)
		stats.register("max", numpy.max)
		# run evolutionary algorithm
		pop, log = algorithms.eaSimple(pop,
									   toolbox,
									   cxpb=0.20,  # Prob. of crossover (mating)
									   mutpb=0.20, # Prob of mutation
									   ngen=20,	  # number of generations to run
									   stats=stats)

		#print(stats)
		return pop, log

	def store_ai(self, file_name):
		pop, log = self.evolve_ai()
		if exists(file_name):
			f = open(file_name,'rb+')
			ai_list = [AI.AIRule(1), AI.AIRule(1), AI.AIRule(1)]
			minimum_ai = ai_list[0]
			minimum_index = 0
			for ai in pop:
				for old_ai in ai_list:
					if (old_ai.state_evaluation[0] <= minimum_ai.state_evaluation[0]):
						minimum_index = ai_list.index(minimum_ai)
						minimum_ai = old_ai
				if (ai.state_evaluation[0] > minimum_ai.state_evaluation[0]) and (ai.weights != minimum_ai.weights):
					ai_list[minimum_index] = ai
			dump(ai_list, open(file_name, 'wb'))
			f.close()
		else:
			f = open(file_name, 'wb')
			ai_list = [AI.AIRule(1), AI.AIRule(1), AI.AIRule(1)]
			minimum_ai = ai_list[0]
			minimum_index = 0
			for ai in pop:
				for old_ai in ai_list:
					if (old_ai.state_evaluation[0] <= minimum_ai.state_evaluation[0]):
						minimum_index = ai_list.index(minimum_ai)
						minimum_ai = old_ai
				if (ai.state_evaluation[0] > minimum_ai.state_evaluation[0]) and (ai.weights != minimum_ai.weights):
					ai_list[minimum_index] = ai
			dump(ai_list, f)
			f.close()

			
	def tournament(self, file_name):
		f_new = load(open(file_name, 'rb'))


	def read_ai(self, file_name):
		f_new = load(open(file_name, 'rb'))
		for i in f_new:
			print(i.weights, i.state_evaluation)

evolution = Evolution()
evolution.store_ai('reallynew_ai.txt')
evolution.read_ai('reallynew_ai.txt')



