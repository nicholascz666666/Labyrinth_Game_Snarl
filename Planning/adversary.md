# Class of Adversary
An adversary gets the full level information (comprised of rooms, hallways and objects) at the beginning of a level

An adversary gets an update on all player locations, but only when it’s about to make a turn

An Adversary needs to receive updates from the Game Manager at appropriate moments. 

When it's the Adversary's turn, it needs to communicate the chosen action to the Game Manager.

## Fields:
- GameState: a GameState object in json format

## Methods:
- receive():  receive the full level information GameState from the Game Manager when at the beginning of a level or it’s about to make a turn
- send(name,pos): turn the Adversary's action into json format command and sent it to the Game Manager over network.


 
