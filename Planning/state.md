An implementation of Snarl demands a data representation for game states. <br />
Our game state will include: <br />
A Level object that contains all the information about the game map<br />
A list of Player information, A List of AI position, A int represent player turn <br />
When it's the turn for a certain player, we will collect the movement from the user and update the game state. After the movement of the player, we move the enemy. 

<br />
Method:

* MovePlayerPositon(position): when reaching the turn of the current player, move the player to the position
* CheckIsGameOver(): return boolean whether the game is over or not


We need to create a class of Level which has fields: 
Level has two subclass: Room and Hallway
- **rooms**: a list of Room object in the current level; 
- **hallways** : a list of Hallway object in the current level. 
* To construct a level, we will make sure that there is no overlap for the rooms and hallways. Also, the hallways should be checked to be valid.  We will also have a toJSON method to return a json file of the current Level. 

We need to create a class of Room in the Level class which has fields: 
- **position** : a tuple to represent the upper-left Cartesian position； 
- **size** ：a tuple to represent the boundary dimensions；
- **walls** : a list of tuples to represent the wall tiles; 
- **doors** : a list of tuples to represent the one or more exitsdoors in the room; 
- **objects** : a dictionary of tuples to represent the Objects, like the key and the level exit, may be inside of a room.
* To construct a valid room, we need to make sure that the size is not equal or less than 0 and the positon of the door should at the boundry of the room. We will have a toJSON method to return the a json format of the current room.

We need to create a class of Hallway in the Level class which has fields: 
- **posFrom** : a tuple to represent the start position of the hallway
- **posTo** : a tuple to represent the end position of the hallway；
- **waypoints** : a list of tuples to represent the waypoints of the hallway. 
* We will also have a toJSON method to return a json file of the current hallway. 


