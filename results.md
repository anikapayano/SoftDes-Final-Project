---
title: Results
layout: template
filename: results
--- 

### Evolutionary Algorithm
Currently the algorithm can run through a population of 20 AIs for 20 generations to evolve the most fit AIs. Once it has done this once, it stores the 5 most effective AIs in a file. The next iteration will run the algorithm using these 5 AIs as opponents to the ones it is now evolving, each time comparing the fitness values of the outputted AIs to the current most fit. If they find the  By doing this multiple times, we insure that the AIs become more and more fit.

Below is an image of an example run of the algorithm. The average difference in minimum and maximum fitness values increases for each generation because having a high fitness value is advantageous.

<img src="https://raw.githubusercontent.com/anikapayano/SoftDes-Final-Project/gh-pages/EvolutionResults.png" alt="" />

Once the algorithm is done running, it stores the 5 most fit AIs. Below are are the weights and fitness values associated with the AIs that have bee

<img src="https://raw.githubusercontent.com/anikapayano/SoftDes-Final-Project/gh-pages/TournamentResults.png" alt="" />




