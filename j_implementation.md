---
title: Implementation
layout: template
filename: j_implementation
---

# Class Diagram
<img src="https://raw.githubusercontent.com/anikapayano/SoftDes-Final-Project/gh-pages/UMLGods1.png" alt="" />

# AI Structure
The AI is the part of the game that controls one of the teams that play the game. They are structured using an if-tree style logic using weights to make decisions. The Weights control how each AI reacts to the imformation provided to each team.

For example, the AI checks if it has a unit carrying the enemy flag and directs them to bring it back to the base (the if tree). The unit also wants to avoid opposing units in the process, and uses weights to decide how much of an influence each opposing unit has on the path of the flag carrying unit. This decision is done mathematically by making a hypothetical force for each other object that should effect the path of a unit, whose weights are a factor of the distance to the other object, and the corresponding weight stored by the AI.

The weights contain information for the AI's offense/defense ratio, unit production preferences, and path-finding preferences for each unit_type. The weights are stored in a matrix (or list of lists) that can then be rearranged into a single list of numbers that can be optimized using evolutionary techniques.

# Evolutionary Algorithm
We utilised the DEAP library to implement an evolutionary algorithm on the AIs. Our goal was to play an AI against a base AI, analyze the fitness of the AI, mutate and mate AIs, and restart the process for the next generation. The Evolution class creates an AI population, initiliazes a game, and runs each AI against the base AI. Each AI keeps track of its losses and its opponent's losses. When the game ends (either an AI wins or the game timesout), the AI takes the ratio of its losses to its opponent's losses and subtracts that to a winning coefficient. This coefficient is either 50 if the AI won or 0 if it lost.
This is the current fitness function. The corresponding state_evaluation variable will be large if the AI killed more units than it lost and will be low if it lost more units than it killed. Winning provides a large boost.

The DEAP library then selects which AIs from the population had high fitness values, chooses some to mate and mutate, and then outputs a new generation to run against the AI.

Once it has run the algorithm once, it stores the 5 most effective AIs in a file. The next iteration will run the algorithm 5 separate times using these 5 AIs as opponents to the ones it is now evolving, each time comparing the fitness values of the outputted AIs to the current most fit. If they find that one of the AIs' fitness value is greater than the 5 currently on file, it will replace it with the new one. By doing this multiple times, we insure that the AIs become more and more fit.
