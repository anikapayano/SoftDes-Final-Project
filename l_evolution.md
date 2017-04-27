---
title: Project Evolution
layout: template
filename: l_evolution
--- 

The goal of this project is to engage game design, Artificial Intelligenge design, and evolutionary algorithms to create one user experience. The stretch goal was to evolve AI's not only to win the game but to play it with certain 'personalities.'

# The Game

The game started (and ended) as a capture the flag game. We intitially planned for each team to have one flag, one base, and an amount of units that grew as the game went on. At first, all the units were the same, but as the game developed, we decided to add multipule different types of units with different properties to have some element of strategy and to make the AI more complex and interesting.

# The AI

Our AI makes decisions about individual movement by thinking about effects of the other objects as exerting forces where the unit's direction of movement is the sum of these forces.

Getting the AI to make decisions about multiple units was much more difficult. We extensivly investigated useing Neural Networks where an AI's decision would have an input of all the object positions and an output of a set of unit movements. Neural Networks were not a great fit because we are not trying to solve a classification problem and we would have to create training data ourselves and would not be able to create a large enough sample size.

# The Evolution

The evolution of the AI happened in the fitness function. The mutating and mating functions affect the weights attribute of each AI. The fitness function started out as a function that evaluated to 1 if the AI won and 0 if it lost. We then tried to maximize this value, but the binary fit function meant that evolution did not improve the AI in a small number of generations. Currently, the fitness function takes a ratio of units lost and enemy units lost and subtracts that from a winning coefficient. This coefficient is either 50 (won) or 0 (lost). We are still optimizing the fit function to evaluate other factors such as the average distance away from the flag most units were and how long it took each AI to win. These factors will be important in evolving personalities.
