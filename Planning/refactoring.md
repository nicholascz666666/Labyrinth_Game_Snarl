# Milestone 6 - Refactoring Report

** Team members: Zhi Cheng, Jiayuan Chen

** Github team/repo: https://github.ccs.neu.edu/CS4500-S21/Gulinde


## Plan

- change the valid_moves() and interact() function for the subclasses of Character. 
- add a boolean in the gamestate for reaching the exit.
- implement a way to render the level graphically using GUI.
- change to use rulecheck in constructor of gamestate.
- make changes to rulechecker check_input_game_states() and check_status() method.

## Changes

- change the valid_moves() base on the rule for Player, Adversary, and Ghost.
- implement interact() base on the rule for Player, Adversary, and Ghost.
- implement the boolean in the gamestate to represent that certain player reach the exit.
- implement level rendering using pygame.
- change to use rulecheck in constructor of gamestate.
- check_status() return win lose or in-progress. 
- check_input_game_states() check unique name for every player and adversary.


## Future Work

- we need specification for rules of whether the adversary can land on the key tile and Ghost can travese void tile.
- we might consider changing the representation of a pos from cartesian based to Row,Col based


## Conclusion
In this week, we have imporved our design as shown in the changes section. We focus on the move and interact fuctions for the subclasses of the Character class since we have more understanding of the rules. However, we think we still need some changes on thoes methods when we are told more specifications about the rules. Also, we add a boolean in the gamestate to represent that certain player reach the exit. In the past design, when a player is catched by an adversary or a gost, the player will disappear; while if someone of the players find the key and a player reach the exit, that player will also disappear. Hence, we add that boolean to distinguish two situations. Another change in the GameState is that we let the rulechecker check the validation of the gamestate sine rulechecker is suppsoed to do that. In addition to some changes to the Character and GameState, we make some changes in the rule checkers since we have changed the gamestate. Last, we create a graphical render for the gamestate using GUI.   
