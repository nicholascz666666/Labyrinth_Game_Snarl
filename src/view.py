#!/usr/bin/env python3
# coding: utf-8

#The view class to render Level object in json format to string
class View:
    #The game map
    #A list of list of String represeting one of door, wall, empty
    game_map = [[]]

    def __init__(self):
        self.game_map = [[]]

    def set_game_state(self, game_state):
        self.set_level(game_state.level.toJSON())
        players = game_state.players
        adversaries = game_state.adversaries
        for character in players + adversaries:
            pos = character.pos
            self.game_map[pos[1]][pos[0]] = character.name

    #Take Level object in json format as input and create the game map
    def set_level(self, level):
        self._create_game_map(level)
        self._modify_game_map(level)

    #Return the level in string format
    def render(self):
        result = ""
        for y in range(len(self.game_map)):
            
            for x in range(len(self.game_map[0])):
                result += self.game_map[y][x] + ", "
            
            result += "\n"

        return result


    def _create_game_map(self, level):
        rooms = level.get("rooms")
        hallways = level.get("hallways")

        posx = []
        posy = []
        for room in rooms:
            posx.append(room.get("position")[0])
            posx.append(room.get("position")[0] + room.get("size")[0])
            posy.append(room.get("position")[1])
            posy.append(room.get("position")[1] + room.get("size")[1])

        for hallway in hallways:
            waypoints = hallway.get("waypoints")
            for waypoint in waypoints:
                posx.append(waypoint[0])
                posy.append(waypoint[1])

        width = max(posx) - min(posx)
        height = max(posy) - min(posy)
        gameMap = [["    " for i in range(20)] for j in range(20)] 
        self.game_map = gameMap

    def _modify_game_map(self, level):
        rooms = level.get("rooms")
        hallways = level.get("hallways")

        for room in rooms:
            self._set_room(room)

        for hallway in hallways:
            self._set_hallway(hallway)

    def _set_room(self, room):
        position = room.get("position")
        size = room.get("size")
        walls =  room.get("walls")
        doors = room.get("doors")
        objects = room.get("objects")

        y = position[1]
        x = position[0]
        for row in range(y, y + size[1]):
            for col in range(x, x + size[0]):
                self.game_map[row][col] = "empt"

        for wall in walls:
            self.game_map[wall[1] + y][wall[0] + x] = "wall"
        for door in doors:
            self.game_map[door[1] + y][door[0] + x] = "door"
        for obj in objects.items():
            name, pos = obj
            self.game_map[pos[1] + y][pos[0] + x] = name

    def _set_hallway(self, hallway):
        posFrom = hallway.get("posFrom")
        posTo = hallway.get("posTo")
        waypoints = hallway.get("waypoints")
        
        allPos = [posFrom] + waypoints + [posTo]
        
        

        for i in range(len(allPos) - 1):
            start = allPos[i]
            to = allPos[i+1]
            self._set_hallway_path(start, to)
            #self._set_wall_around_hallway(start, to)
            
            
    def _set_wall_around_hallway(self, start, to):
        if start[0] - to[0] != 0:
            if start[0] - to[0] < 0:
                startX = start[0]
                toX = to[0]
            else:
                startX = to[0]
                toX = start[0]
                
            if start[0] - to[0] < 0:
                for posx in range(startX, toX + 2):
                    if self.game_map[start[1]-1][posx] == "    " :
                        self.game_map[start[1]-1][posx] = "wall"
                    if self.game_map[start[1]+1][posx] == "    " :
                        self.game_map[start[1]+1][posx] = "wall"
        else:
            if start[1] - to[1] < 0:
                startY = start[1]
                toY = to[1]
            else:
                startY = to[1]
                toY = start[1]

            for posy in range(startY, toY + 2):
                if self.game_map[posy][start[0]-1] == "    ":
                    self.game_map[posy][start[0]-1] = "wall"
                if self.game_map[posy][start[0]+1] == "    ":
                    self.game_map[posy][start[0]+1] = "wall"


    def _set_hallway_path(self, start, to):
        if start[0] - to[0] != 0:
            if start[0] - to[0] < 0:
                startX = start[0]
                toX = to[0]
            else:
                startX = to[0]
                toX = start[0]
                
            for posx in range(startX, toX + 1):
                self.game_map[start[1]][posx] = "hall"
        else:
            if start[1] - to[1] < 0:
                startY = start[1]
                toY = to[1]
            else:
                startY = to[1]
                toY = start[1]

            for posy in range(startY, toY + 1):
                self.game_map[posy][start[0]] = "hall"

