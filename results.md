---
title: Results
layout: template
filename: results
--- 

# Evolutionary Algorithm
Currently the algorithm can run through a population of 20 AIs for 20 generations to evolve the most fit AIs. By storing the five most fit, we allow the evolutionary algorithm to use them in future iterations. We use them to play new AIs against, thus increasing the specialisation of each AI.

Below is an image of an example run of the algorithm. The average difference in minimum and maximum fitness values increases for each generation because having a high fitness value is advantageous.

<img src="https://raw.githubusercontent.com/anikapayano/SoftDes-Final-Project/gh-pages/EvolutionResults.png" alt="" />

Once the algorithm is done running, it stores the 5 most fit AIs. We then run the algorithm again using these 5 AIs as base AIs. Below are are the weights and fitness values associated with the resulting AIs from this second iteration.

<img src="https://raw.githubusercontent.com/anikapayano/SoftDes-Final-Project/gh-pages/TournamentResults.png" alt="" />




