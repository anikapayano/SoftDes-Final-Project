'''
This file is where the evolving of the AIs happen
'''

# make an individual
# from ai_rule import AIRule
import mvc
import random
import ai_rule as AI
import numpy
from deap import algorithms, base, tools, creator
import gods_of_capture as gods
from os.path import exists
import sys
from pickle import dump, load


class Evolution():
	""" DOCSTRING:
	Evolves AI
		"""

	def __init__(self):
		#self.ai2 is the ai that the ai we're evolving runs against and become better
		# at beating. At the start this is simply a base AI
		self.ai2 = AI.AIRule(2,[-.5, -0.8, -.5, -.5, -.5, -.5, -0.8, -.5, -.5, .5,
                                .5, 0.8, .5, .5, .5, .5, 0.8, .5, .5, .5, .5, 0.8,
								.5, .5, .15, .07])


	def evaluate_ai(self, ai1):
		""" DOCSTRING:
			Given an AI, returns the fitness of it by accessing the Ai_Rule's state_evaluation
			attribute. This attribute is updated throughout the game as well as the end of the game
			"""
		# runs a game with the ai1 running against self.ai2
		game = gods.CaptureGame(ai1, self.ai2, True)
		game.run()
		current_state = ai1.state_evaluation
		return(current_state)

	def mutate(self, ai, insert_weights = 0.2, increment_weights = 0.2):
		""" DOCSTRING:
			change the weights of the AI randomly
			usually mutation involves insertion, deletion, and substitution, but since
			AIRule.wieghts must be fixed length, we only use substitution and incrementing
			of weight
			"""
		i = 0
		while i <len(ai.weights):
			if random.random() < insert_weights:
				# choose a random number between -1 and 1 to replace
				# the current weight value by it
				char = random.randint(-100, 100)
				char = float(char/100)
				# insert the new weight at the ith index
				ai.weights[i] = char


			if random.random() < increment_weights:
				# if the weight is smaller than 0.95, then add 0.05 to i
				# cannot be bigger than 0.95 bc it will be above 1 which is larger
				# than any other weight
				if ai.weights[i] <= 0.95:
					ai.weights[i] += 0.05
			i += 1

		# return ai in a length 1 tuple (required by DEAP)
		return(AI.AIRule(1, ai.weights), )

	def mate(self, ai1, ai2, mating_weights = 0.3):
		""" DOCSTRING:
			simulates mating between two individuals by crossing weights over
			from two ais
			"""

		i = 0
		#check that the weights length are equivalent
		if len(ai1.weights) == len(ai2.weights):
			# cycle through all the weights
			while i < len(ai1.weights):
				# there's a 30% chance that crossover happens
				if random.random()< mating_weights:
					#switch weights
					new2_weight = ai1.weights[i]
					new1_weight = ai2.weights[i]
					ai2.weights[i] = new2_weight
					ai1.weights[i] = new1_weight
				i += 1

		# reset state_evaluations of babies
		ai1.state_evaluation = (0, 0, 0)
		ai2.state_evaluation = (0, 0, 0)
		return(ai1, ai2)


	def get_toolbox(self, personality):
		""" DOCSTRING:
			Return DEAP Toolbox configured given AI
			personality is a string, either "offensive", "defensive", or nothing
			"""
		toolbox = base.Toolbox()

		# CREATE POLULATION TO BE EVOLVED

		# create individual (using the AIRule object for an individual we created outselves)
		if personality == "offensive":
			toolbox.register("individual", AI.AIOffensive)
		elif personality == "defensive":
			toolbox.register("individual", AI.AIDefensive)
		else:
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


	def evolve_ai(self, personality):
		""" DOSCTRING:
			use evolutionary algorithm to evolve ai object
			mostly going to be DEAP library
			"""

		# configure toolbox using get_toolbox
		toolbox = self.get_toolbox(personality=personality)

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

		return pop, log

	def store_ai(self, file_name):
		""" DOCSTRING:
			Stores the 5 most fit AIs in a file
			"""
		pop, log = self.evolve_ai(personality="offensive")

		if exists(file_name):
			f = open(file_name,'rb+')

			# load previous list of fit AIs to compare these new AIs against
			ai_list = load(f)

			# ai_list = [AI.AIRule(1), AI.AIRule(1), AI.AIRule(1), AI.AIRule(1), AI.AIRule(1)]
			# take the first AI in the list to be the minimum (will be updated later)
			minimum_ai = ai_list[0]
			minimum_index = 0

			# for each new AI
			for ai in pop:

				# update which AI in the list has the minimum fitness value
				for old_ai in ai_list:

					# if the old_ai's fitness is smaller than the minimum's update the old_ai
					# to be the minimum. update the index to reflect this change
					if (old_ai.state_evaluation[0] <= minimum_ai.state_evaluation[0]):
						minimum_index = ai_list.index(minimum_ai)
						minimum_ai = old_ai

				# if the new AI we're evaluation has a larger fitness value than the smallest fitness value on the list
				# replace the minimum with this new AI. don't replace if the weights are identical
				if (ai.state_evaluation[0] > minimum_ai.state_evaluation[0]) and (ai.weights != minimum_ai.weights):
					ai_list[minimum_index] = ai

			dump(ai_list, open(file_name, 'wb'))
			f.close()
		else:
			f = open(file_name, 'wb')
			# create a list of AIs whose fitnesses are 0. these are just placeholders
			ai_list = [AI.AIRule(1), AI.AIRule(1), AI.AIRule(1), AI.AIRule(1), AI.AIRule(1)]

			# take the first AI in the list to be the minimum (will be updated later)
			minimum_ai = ai_list[0]
			minimum_index = 0

			# for each new AI
			for ai in pop:

				# update which AI in the list has the minimum fitness value
				for old_ai in ai_list:

					# if the old_ai's fitness is smaller than the minimum's update the old_ai
					# to be the minimum. update the index to reflect this change
					if (old_ai.state_evaluation[0] <= minimum_ai.state_evaluation[0]):
						minimum_index = ai_list.index(minimum_ai)
						minimum_ai = old_ai

				# if the new AI we're evaluation has a larger fitness value than the smallest fitness value on the list
				# replace the minimum with this new AI. don't replace if the weights are identical
				if (ai.state_evaluation[0] > minimum_ai.state_evaluation[0]) and (ai.weights != minimum_ai.weights):
					ai_list[minimum_index] = ai

			dump(ai_list, f)
			f.close()


	def tournament(self, file_name):
		""" DOCSTRING:
			takes AIs from previous iterations and uses those as the base AIs to evolve
			new AIs from
			"""
		f = open(file_name, 'rb')
		# load the list of previous 5 most fit AIs
		f_new = load(f)

		for ai in f_new:
			# let self.ai2 be the saved AIs
			self.ai2 = ai
			print(self.ai2.weights)
			print('--------')
			# run store_ai using these new base AIs
			self.store_ai('reallynew_ai.txt')
		f.close()


	def read_ai(self, file_name):
		""" DOCSTRING:
			read the file with the AIs
			"""
		f_new = load(open(file_name, 'rb'))
		for i in f_new:
			# print all of the weights and fitnesses of the stored AIs
			print(i.weights, i.state_evaluation)

evolution = Evolution()
evolution.store_ai('reallnew_ai.txt')
evolution.read_ai('reallnew_ai.txt')

# run store_ai for a new file name first and then run tournament
