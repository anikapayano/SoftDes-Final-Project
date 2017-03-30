### Background and context: What information about your project does the audience need to participate fully in the technical review? You should share enough to make sure your audience understands the questions you are asking, but without going into unnecessary detail.
Our project is focused on creating a game in pygame with a tuneable AI that can play the game that can be used to create better/different AIs using evolutionary algorithms.

Gameplay/rules - Capture the Flag
- We are basing our game off Capture the Flag. There will be two teams that start out with a base and a flag. The teams will  have a chance to place their flags in a section of the field that is visible only to them. From there each team will do their best to grab the other team’s flag and bring it back to their base.
- Each team starts out with limited visibility of the board. There is a section of the field that is unknown to both players. They can discover more about the field by sending units to explore the unknown space. Each unit has a radius of visibility around it that allows it to see. The unknown section of the board could contain enemy units or unknown obstacles. It is the player’s job to remember the layout of the space.
- The base generates units at a set rate of time. Different types of units will have different production times. Ideas for units are:
  - Low speed, low strength, low attack, low health -> 5s production time
  - Low speed, high strength, low attack, high health -> 10s production time
  
AI - Colvin and Connor 
- Part of our goal is to create some form of nonhuman character that makes decisions about player movement using weights to choose different actions. 
- Definition of AI: collection of weights and some basic logic circuits
- Path finding (Connor)
  - Astar 
    - Tiles are weighted based on which unit is being moved & how many opposing units are in other tiles, & obstacles
  - Needs a tile based system 
  - Remembers where the tiles are
- Force AI (Colvin)
  - A fluid system with a specific position for each object (No tiles)
     - To display, positions are rounded to the nearest pixel value
     - Buffers needed for collisions
  - Movement of each unit is defined by a vector for direction, and each unit’s speed ability.
  - Unit direction is defined by combining different “forces” from other objects in the playing field
  - AI is personalized and uses weights that affect force strength, and  decision thresholds.
- Evolving -Sophia
  - The AI will be represented as a set a of values (weights or forces) that determine how the AI plays the games. 
  - We will start with a randomly generated population (each value is a randomly generated value within a specified range)
  - We will then ‘kill off’ AI’s based on a ‘fit function’
    - In the first evolution, we’ll chose AI’s based on how well they play the game
    - In the second evolution(s) we’ll evolve the AI’s to different playing styles (ie. aggressive or defensive)
  - Then we ‘mutate’ and ‘mate’ the AI’s by changing values and crossing them over between AI’s respectively
  
### Key questions: What do you want to learn from the review? What are the most important decisions your team is currently contemplating? Where might an outside perspective be most helpful? As you select key questions to ask during the review, bear in mind both the time limitations and background of your audience.
How do people want to see the game go (2 AIs, players against AI) - Anika
- If there are 2 AIs, the person playing the game will only interact at the beginning, setting up the board. The rest of the game will play out as two AIs.
- If there is continuous input from the player, the AI will only apply to the opposing team and the way units move for the player. 
List out pros and cons
Pose questions
- Path finding (Connor) vs Force system AI (Colvin)
  - Astar would need a tile based system and the program would need to remember where the tiles are
    - In this -> do units fit in one tile or do units take up more than one tile?
    - If they take up more tiles -> more tiles to remember
    - If they take up less tiles -> less dynamics in terms of size differences
  - Force AI
    - A tile-less fluid system where each unit can move in any direction. The AI chooses direction from “force vectors”
      - Is this more compelling for the scenario than pathinding?
  - Is there a way to combine the two?

### Agenda for technical review session: Be specific about how you plan to use your allotted time. What strategies will you use to communicate with your audience?
- What we want out of it: A better idea about which AI to use
- Talk about the background (capture the flag game, AI, evolving algorithm)
- Visual Aid to explain the different types of AI -> Connor
- Throw up list of pros and cons and ask for more thoughts
- Lead discussion to decision about either ones
