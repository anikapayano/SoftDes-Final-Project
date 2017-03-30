###Background and context: What information about your project does the audience need to participate fully in the technical review? You should share enough to make sure your audience understands the questions you are asking, but without going into unnecessary detail.
Our project is focused on creating a game in pygame with a tuneable AI that can play the game that can be used to create better/different AIs using evolutionary algorithms.
Gameplay/rules - Capture the Flag
  We are basing our game off Capture the Flag. There will be two teams that start out with a base and a flag. The teams will have a chance to place their flags in a section of the field that is visible only to them. From there each team will do their best to grab the other team’s flag and bring it back to their base.
  Each team starts out with limited visibility of the board. There is a section of the field that is unknown to both players. They can discover more about the field by sending units to explore the unknown space. Each unit has a radius of visibility around it that allows it to see. The unknown section of the board could contain enemy units or unknown obstacles. It is the player’s job to remember the layout of the space.
  The base generates units at a set rate of time. Different types of units will have different production times. Ideas for units are:
    Low speed, low strength, low attack, low health -> 5s production time
    Low speed, high strength, low attack, high health -> 10s production time
