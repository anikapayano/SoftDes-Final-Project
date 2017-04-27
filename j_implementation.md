---
title: Implementation
layout: template
filename: j_implementation
--- 

Implementation information Code doesn’t tell a story by itself. Use more effective methods such as flowcharts and architectural, class, or sequence diagrams to explain how your code works. You could consider including or linking to snippets of code to highlight a particularly crucial segment.

### Class Diagram
<img src="https://raw.githubusercontent.com/anikapayano/SoftDes-Final-Project/gh-pages/UMLGods1.png" alt="" />

### Evolutionary Algorithm
We utilised the DEAP library to implement an evolutionary algorithm on the AIs. Our goal was to play an AI against a base AI, analyze the fitness of the AI, mutate and mate AIs, and restart the process for the next generation. The Evolution class creates an AI population, initiliazes a game, and runs each AI against the base AI. Each AI keeps track of its losses and its opponent's losses. When the game ends (either an AI wins or the game timesout), the AI takes the ratio of its losses to its opponent's losses and subtracts that to a winning coefficient. This coefficient is either 50 if the AI won or 0 if it lost.
This is the current fitness function. The corresponding state_evaluation variable will be large if the AI killed more units than it lost and will be low if it lost more units than it killed. Winning provides a large boost.
The DEAP library then selects which AIs from the population had high fitness values, chooses some to mate and mutate, and then outputs a new generation to run against the AI.

