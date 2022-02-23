# Class of Player
A Player component represents the interests of the human behind the keyboard in the game. 

A Player needs to receive updates from the Game Manager at appropriate moments. 

When it's the Player's turn, it needs to communicate the chosen action to the Game Manager.

A Player should communicate with Game Manager through network TCP socket.

Player will call send(json) method and input a command in json format.

- Ex. {"command": "start", "level_num": 2}

- or {"command": "accept_player", "name": "Player1"}

- or {"command": "move", "pos": (0, 1)} etc...

Then Player will call receive() to get the updated GameState in json format and call render to draw the restriced view.

## Fields:
- GameState: a GameState in json format

## Methods:
- receive():  receive the updated GameState from the Game Manager after the Players' action.  
- send(action): turn the player's action into json format command and sent it to the Game Manager over network.
- render():  draw the restriced view
 
