# Module: Traveller
## Implementation:
### Language: Python, Version: 3.6
### Module : 
* Traveller: 
Provide the services of a route planner through a network of towns for a role-playing game.

### Class In Traveller: 
* Town: Represent a single town, which would be the single element of the network.
### Field In Town:	
* String name: Represent the name of the town.
* String char: Represent the name of the character. It could be null, and if it is null, it represents no character in the town.
### Constructor In Town:
* town(String name): Construct the Town Class and name the town with the given string name.
### Methods In Module:
* createNetWork(Dictionary of Town): Function as creating a network of copies of towns with given towns. It should be used after creating some towns and the dictionary will indicate the relationship betweem a town with its abjacent towns. 
* setCharacter(String char,String town)：Function as set a character to the given town with the given name of character; if the given town has a character, replace it with new character. It should be used after using createNetwork method, it will loop all the towns and find whether there is one, whoes name is the given string town and place a character called the given string char in that town.
* arrive(String town, String character): Function as check whether a specified character can reach a designated town without running into any other characters for the current network. It should be used after using createNetwork method.
* modifyNetWork(Dictionary of Town): Function as modified a network. It should be used after using createNetwork.The input dictionary of town will indicate the new replationship among towns.


