# Traveller Module
Implement traveller module using Java 8.  
The traveller module has a Network of Towns.   
When this module is instantiated it should have an empty Network of Towns and no Characters.

A Network of Towns is a simple graph.   
Each node in the graph represents a town and each town has a name.

A Character has a name and a location.  
The location is a node within the Network of Towns.  
A Character can only be in one location at once.  
Multiple Characters can be in the same location at once.

#### The required interactions that this module must support are (signatures are provided):
1. A function to add a new town to a network.   
`void addTown(String townName)`
1. A function to place a character in a town. If the town doesn't exist, throw an exception. 
If the character already exists in the Network it should be placed at the new location and removed 
from it's previous location. 
`void placeCharacter(String townName, String characterName)`
1. A function to get the names of characters that are currently in a town. If no characters are in 
the town, return an empty list. If the town doesn't exist, throw an exception.
`List<String> getCharactersInTown(String townName)`
1. A function to query whether a path exists between the character's current town and the given 
town that contains only nodes with no characters.
If a path does exist it returns true. If not, it returns false. If the town or character doesn't
exist, throw an exception.
`boolean characterlessPathExists(String destinationTown, String characterName)`

__This module should not__  
1. Allow the user to remove towns or characters after they have been placed in the Network of Towns.
2. Expose the data structures or classes used within the module. The only way to interact with the 
module should be through the functions above.