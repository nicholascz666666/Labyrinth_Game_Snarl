
# Rule Checker
Field:
We don't need any fields because the rule checker class does not need to store any infrmation about the game state. 
It only provides static method to check the validity of a given gamestate. 

## Methods:
* check_valid_movement_interaction(game_state, name, position):  check valid game state first. Then based on the name, searching for that character and check validation of that movement and coresponding interaction. (There is a bug when there are characters have the same names). 
* check_input_game_states(game_state): check the given game_state is valid or not. Return a boolean.
* check_status(game_state): check valid game state first and then check the status of the current game state. Return a enum represent it. 



