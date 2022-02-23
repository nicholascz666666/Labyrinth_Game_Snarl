# Memorandum
## Date: 01/31/2021

## Memo To: the editors of specifications

## From: Zhi Cheng and Jiayuan Chen

## Subject: Problems of the Specification

We are writing to inform you that the specification you have written would not lead to a result you want.

If we follow your specifications of the Module Traveller, we do not know the relationship between towns. To be more specification, as the specifications, the towns will be represented as strings and the character will be be represented as strings as well. It would work. However, for the addTown method, the instruction need us to add a new town to a network. We are confused about the how the town will be added to a network. More specifically, we want to know the relationship between the town, which need to be added, and other towns existing in the current network. 

In addition to the under-specification of the method addTown, the method  characterlessPathExists doesn’t specify the relationship among towns in the current network. We need the relationship like what the Figure 1 shows. The relationship among towns is very important so that we could know whether there is a path between two towns. 

![alt text](https://drive.google.com/file/d/1XxqC-2EEneQhRYuITIS5s4h_TWahObdv/view?usp=sharing)
Figure 1: The example of relationship.

In order to solving this under-specification, we suggest to let town become a class and, in additition to a field called name, have a filed called adjacentTowns, which is a list of towns that could be reached from the current town. This could solve the issue of the relationship pf towns, and after solving the problem, we suggest to change the type of the input of method addTown from String to the class town.

If you have question or concern about our suggestion, do not hesitate to ask us.
