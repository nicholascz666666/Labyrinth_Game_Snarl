# interfaces for the Game Manager 
# Class Game Manager 
Since Rule Checker is part of a Game Manager, we will use the methods in Rule Checker to help us check the validation.

Game Manager should communicate with Player through network TCP socket. 

Player will call accept_command method and input a command in json format.

- Ex. {"command": "start", "level_num": 2}

- or  {"command": "accept_player", "name": "Player1"}

- or  {"command": "move", "pos": (0, 1)} etc...

## Fields:
- Players: a list of player Object for a game.
- GameState: a Gamestate object. It is created after command "start". 


## Methods:
- accept_command(String json_string): accept the command from the player, and based on the command, function differently.

- accept_player(String name): accept a string as the name of the new gamer. Create a Player object based on the name. check the name is valid or not and if there are already 4 players, throw exception.

- start_game()：construct a gamestate object with a randomly generated Level and the list of Player
