# Implementation details of snarlGen:

* 1. Generate randomly sized rooms at random points within a circle of 1 radius.
* 2. Separate rooms by moving them apart until they don’t overlap. 
Followed by Seperation from:
https://gamedevelopment.tutsplus.com/tutorials/3-simple-rules-of-flocking-behaviors-alignment-cohesion-and-separation--gamedev-3444
* 3. Generate a connected graph out of rooms, taking the topology into consideration. With the python scipy library of Delaunay https://docs.scipy.org/doc/scipy/reference/tutorial/spatial.html.
* 4. Reduce the number of connections in the graph by using BFS and add the extra relation among rooms 10% chance.
* 5. Generate hallways between connected rooms. Using a-star algo to find a shortest way to connect two rooms.

We could let the program function smoothly for a small number of rooms to generate. However, when reaching 100 or over,
there will be overlap or no path, which we need to come up with a possible solution. 
