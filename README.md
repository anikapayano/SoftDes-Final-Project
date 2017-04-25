# Gods of Capture: Evolved AI play Capture the Flag

[Visit our Website](https://anikapayano.github.io/SoftDes-Final-Project/)

## Description:
Gods of Capture is a 2 vs. 2 capture the flag game built to be played by two
algorithms (after called AIs) pitted against one another. The objective of each
AI is to capture the opposing team's flag and return the flag to it's base. The
bases spawn units at certain time intervals and can be set to spawn different
types of units costing more or less time.

The AIs created are basic if-tree algorithms. Their procedures regarding
choosing where each unit goes and which units to generate are hard-coded into
nested if-statements. Each set of nested if-statements determines the direction
of a single force acting on a given unit (e.g. if the enemy flag isn't captured,
a force towards the flag acts on friendly units). These forces are then weighted
using weights taken from a matrix defined when the AI is instantiated. Once all
of the forces have been calculated, they are summed, and the unit moves in the
direction of the final sum. This list of weights serves to define the AI's play
style, and can be modified to make the AI play differently.

To create new and better AIs, evolutionary algorithms are implemented on
randomly generated populations of AIs, breeding the best algorithms,
mutating some, keeping others, removing ineffective algorithms, and repeating
the process many times in a structure similar to evolution, hence the name.
To determine how good any one AI is at the game, a fit function is defined
based on the AI's performance against a "default AI". Winning quickly means a
function is more highly sought after by the evolutionary algorithm.

This project was worked on as a final project in Olin College of Engineering's
spring semester Software Design course.

## Authors:
- Anika Payano [Github](https://github.com/anikapayano)
- Connor Novak [Github](https://github.com/ConnorNovak) | [LinkedIn](https://www.linkedin.com/in/connor-novak-b606a0116)
- Colvin Chapman [Github](https://github.com/Colvchap)
- Emily Lepert [Github](https://github.com/Elepert)
- Sophia Nielsen [Github](https://github.com/snielsen221b)

## Getting Started:
### Downloading Files:
Download the following files from the `release` branch of the repository:
- `gods_of_capture.py`: Main game file, holds CaptureGame class
- `objects.py`: Holds Unit class/subclasses, Flag class, Base class
- `mvc.py`: Holds Model class, View class, Controller class
- `ai_rule.py`: Holds AIRule class

### Installing Packages:
TODO Describe which packages to install and how

## Usage:
TODO: instructions on how to install packages

## License:
