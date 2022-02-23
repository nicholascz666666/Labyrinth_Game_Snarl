# Strategy For Zombie
- We first find players, whoes position is 5 tiles away from the current zombie.
- If there is no other players, the zombie will execute a random move to its surrounding positions. 
- If there are certain players, the zombie will choose the last player and decide the catch that player. 
- We use dijkstra algorithm to find the shortest path to the location of that player.  
- If there is no path to the player (player outside the room), the zombie will also execute a random move to its surrounding positions. 

# Strategy For Ghost
- We first find players, whoes position is 10 tiles away from the current ghost.
- We use 10 tiles for the ghost so that if there is any player within the 10-tile distance, even it is in another room, 
the ghost will go through the hallway to catch that player. 
- If the player is farther than 10-tile distance, the ghost will choose a random move to its surrounding positions. 
- If there are certain players, the ghost will choose the last player and decide the catch that player. 
- We use dijkstra algorithm to find the shortest path to the location of that player, and we let the ghost be able to
pass through the door and walk along the hallway.
