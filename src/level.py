#!/usr/bin/env python3
# coding: utf-8

import json

"""

A room has an upper-left Cartesian position, boundary dimensions (or size), a layout of non-wall tiles, and one or more exitsdoors. Objects, like the key and the level exit, may be inside of a room.

A exitroom door is valid if it is at the boundary dimensions of the room.

A hallway has 2 rooms to connect (via their doors) and a (possibly empty) list of waypoints. The waypoints allow for corners in the hallway. A hallway is valid if a line comprised of the waypoints connects the two rooms. A hallway is valid only if:

it connects two rooms at its endpoints; and
each segment (as delimited by subsequent points1) is either horizontal or vertical (i.e., perpendicular with the x or y axis).
A level is comprised of a series of rooms connected by hallways. A level is valid if no two rooms overlap, no two hallways overlap, and no hallways overlap with any rooms.

"""
class Level:
    #A list of Room object
    rooms = []

    #A list of Hallway object
    hallways = []

    #A dictionary. Key is tuple represents the position. Value is String represent one of door, wall, room, hallway, key, exit
    all_tiles_pos = {}

    #Constructor
    def __init__(self, level):
        self.rooms = []
        self.hallways = []
        self.all_tiles_pos = {}
        rooms = level.get("rooms")
        hallways = level.get("hallways")
        
        self._check_overlap(rooms, hallways)

        for room in rooms:
            position = room.get("position")
            size = room.get("size")
            walls =  room.get("walls")
            doors = room.get("doors")
            objects = room.get("objects")
            room_object = self.Room(position, size, walls, doors, objects)
            self.rooms.append(room_object)
        
        self._check_hallway_perpendicular(hallways)
        self._check_hallway_connects_two_rooms(hallways)
        
        for hallway in hallways:
            posFrom = hallway.get("posFrom")
            posTo = hallway.get("posTo")
            waypoints = hallway.get("waypoints")
            hallway_object = self.Hallway(posFrom, posTo, waypoints)

            self.hallways.append(hallway_object)

    def __str__(self):

        room_list = [json.loads(str(room)) for room in self.rooms]
        hall_list = [json.loads(str(hallway)) for hallway in self.hallways]

        object_list = []
        for pos, value in self.all_tiles_pos.items():
            if value == "key":
                key_pos = [pos[1], pos[0]]
                object_list.append({ "type": "key", "position": key_pos })
            if value == "exit":
                exit_pos = [pos[1], pos[0]]
                object_list.append({ "type": "exit", "position": exit_pos })

        s = {"type": "level",  "rooms": room_list, "hallways": hall_list,  "objects": object_list}

        return json.dumps(s)

    def player_view(self, pos):
        layout = [[1 for i in range(5)] for j in range(5)]

        object_list = []
        for row in range(-2, 3, 1):
            for col in range(-2, 3, 1):
                p = (pos[0] + col, pos[1] + row)
                
                if p not in self.all_tiles_pos or self.all_tiles_pos[p] == "wall":
                    layout[row+2][col+2] = 0
                elif self.all_tiles_pos[p] == "door":
                    layout[row+2][col+2] = 2
                elif self.all_tiles_pos[p] == "key":
                    object_list.append({ "type": "key", "position": [p[1], p[0]] })
                elif self.all_tiles_pos[p] == "exit":
                    object_list.append({ "type": "exit", "position": [p[1], p[0]] })
        
        result = {"layout": layout, "objects": object_list}
        return result

    #Return the Level in json format
    def toJSON(self):
        json_ = {"rooms": [i.toJSON() for i in self.rooms], "hallways": [i.toJSON() for i in self.hallways]}
        return json_

    #check whether the given pos is traversable
    def traversable(self, pos):
        if pos not in self.all_tiles_pos or self.all_tiles_pos[pos] == "wall":
            return False
        return True

    #return string 
    def object_type(self, pos):
        if pos in self.all_tiles_pos and (self.all_tiles_pos[pos] == "key" or self.all_tiles_pos[pos] == "exit"):
            return self.all_tiles_pos[pos]
        return None

    #return string
    def room_or_hallway_or_void(self, pos):
        if pos not in self.all_tiles_pos:
            return "void"
        if self.all_tiles_pos[pos] == "hallway":
            return "hallway"
        return "room"

    #return a list of point
    def reachable(self, pos):
        type_ = self.room_or_hallway_or_void(pos)
        result = []
        if type_ == "void":
            return []
        elif type_ == "hallway":
            hallway = self._get_hallway(pos)
            return [self._get_room(hallway.posFrom).position, self._get_room(hallway.posTo).position]
        else:
            result = []
            room = self._get_room(pos)
            
            for door in room.doors:
                door_pos = (door[0] + room.position[0], door[1] + room.position[1])
                for hallway in self.hallways:
                    if door_pos == hallway.posFrom:
                        room_to = self._get_room(hallway.posTo)
                        result.append(room_to.position)
                    elif door_pos == hallway.posTo:
                        room_to = self._get_room(hallway.posFrom)
                        result.append(room_to.position)
            return result
                            
    def _get_room(self, pos):
        for room in self.rooms:
            if room.position[0] <= pos[0] < room.position[0] + room.size[0] and room.position[1] <= pos[1] < room.position[1] + room.size[1]:
                return room
        return None

    def _get_hallway(self, pos):
        for hallway in self.hallways:
            posFrom = hallway.posFrom
            posTo = hallway.posTo
            waypoints = hallway.waypoints
            all_pos_for_one_hallway = [posFrom] + waypoints + [posTo]
            for i in range(len(all_pos_for_one_hallway) - 1):
                start = all_pos_for_one_hallway[i]
                to = all_pos_for_one_hallway[i + 1]
                if start[0] - to[0] != 0:
                    for posx in range(start[0], to[0]):
                        hallway_pos = (posx, start[1])
                        if pos == hallway_pos:
                            return hallway
                else:
                    for posy in range(start[1], to[1]):
                        hallway_pos = (start[0], posy)
                        if pos == hallway_pos:
                            return hallway

    def _check_hallway_perpendicular(self, hallways):
        for hallway in hallways:
            posFrom = hallway.get("posFrom")
            posTo = hallway.get("posTo")
            waypoints = hallway.get("waypoints")

            #check horizontonal and vertical 
            allPos = [posFrom] + waypoints + [posTo]
            for i in range(len(allPos) - 1):
                start = allPos[i]
                to = allPos[i+1]
                if (start[0] - to[0] != 0):
                    if (start[1] - to[1] != 0):
                        raise Exception('invalid halways')

    def _check_hallway_connects_two_rooms(self, hallways):
        for hallway in hallways:
            posFrom = hallway.get("posFrom")
            posTo = hallway.get("posTo")
            waypoints = hallway.get("waypoints")
            
            if self.all_tiles_pos[posFrom] != "door":
                raise Exception("not connect to door")
            if self.all_tiles_pos[posTo] != "door":
                raise Exception("not connect to door")
        
    def _check_overlap(self, rooms, hallways):
        #check overlap
        all_tiles_pos = {}
        for room in rooms:
            position = room.get("position")
            size = room.get("size")
            walls =  room.get("walls")
            doors = room.get("doors")
            objects = room.get("objects")

            x = position[0]
            y = position[1]
            
            for pos_x in range(x, x + size[0]):
                for pos_y in range(y, y + size[1]):
                    if (pos_x, pos_y) not in all_tiles_pos:
                        all_tiles_pos[(pos_x, pos_y)] = "room"
                    else:
                        raise Exception("overlap")

            for wall in walls:
                all_tiles_pos[(wall[0] + x, wall[1] + y)] = "wall"
            for door in doors:
                all_tiles_pos[(door[0] + x, door[1] + y)] = "door"
            for obj in objects.items():
                name, pos = obj
                all_tiles_pos[(pos[0] + x, pos[1] + y)] = name

        
        for hallway in hallways:
            posFrom = hallway.get("posFrom")
            posTo = hallway.get("posTo")
            waypoints = hallway.get("waypoints")
            all_pos_for_one_hallway = [posFrom] + waypoints + [posTo]

            for i in range(len(all_pos_for_one_hallway) - 1):
                start = all_pos_for_one_hallway[i]
                to = all_pos_for_one_hallway[i + 1]
                if start[0] - to[0] != 0:
                    if start[0] - to[0] < 0:
                        inc = 1
                    else:
                        inc = -1

                    for posx in range(start[0], to[0], inc):
                        hallway_pos = (posx, start[1])
                        if hallway_pos not in all_tiles_pos:
                            all_tiles_pos[hallway_pos] = "hallway"
                        else:
                            if hallway_pos != posFrom and hallway_pos != posTo:
                                raise Exception("overlap")
                else:
                    if start[1] - to[1] < 0:
                        inc = 1
                    else:
                        inc = -1

                    for posy in range(start[1], to[1], inc):
                        hallway_pos = (start[0], posy)
                        if hallway_pos not in all_tiles_pos:
                            all_tiles_pos[hallway_pos] = "hallway"
                        else:
                            if hallway_pos != posFrom and hallway_pos != posTo:
                                raise Exception("overlap")

        self.all_tiles_pos = all_tiles_pos

    class Room:
        #an upper-left Cartesian position
        position = ()

        #boundary dimensions
        size = ()

        #non-wall tiles
        walls = []

        #one or more exitsdoors
        doors = []

        #Objects, like the key and the level exit, may be inside of a room.
        objects = []

        #constructor
        def __init__(self, position, size, walls, doors, objects):
            
            self.position = position

            if size[0] < 0 or size[1] < 0:
                raise Exception("size have to be greater than 0")
            self.size = size

            self.walls = walls

            for door_pos in doors:
                x = door_pos[0]
                y = door_pos[1]
                if (y != 0 and  y != size[1] -1) and (x != 0 and  x != size[0] -1):
                    raise Exception("not in x y boundary")
            self.doors = doors
            self.objects = objects

        def __str__(self):
            
            layout = [[1 for i in range(self.size[0])] for j in range(self.size[1])]

            for p in self.doors:
                layout[p[1]][p[0]] = 2
            for p in self.walls:
                layout[p[1]][p[0]] = 0
                    

            s = { "type" : "room",  "origin" : [self.position[1], self.position[0]], "bounds" : { "rows" : self.size[1], "columns" : self.size[0]}, "layout" : layout}

            return json.dumps(s)


            

        #Return the Room in json format
        def toJSON(self):
            json_ = {"position": self.position, "size": self.size, "walls": self.walls, "doors": self.doors, "objects": self.objects}
            return json_

        

        

    #A hallway has 2 rooms to connect (via their doors) and a (possibly empty) list of waypoints. 
    #The waypoints allow for corners in the hallway. A hallway is valid if a line comprised of the waypoints connects the two rooms. A hallway is valid only if:
    class Hallway:
        
        def __init__(self, posFrom, posTo, waypoints):
            self.posFrom = posFrom
            self.posTo = posTo
            self.waypoints = waypoints

        def __str__(self):
            point_list = [[p[1], p[0]] for p in self.waypoints]
            s = { "type": "hallway", "from": [self.posFrom[1], self.posFrom[0]], "to": [self.posTo[1], self.posTo[0]], "waypoints": point_list}

            return json.dumps(s)


        #Return the Hallway in json format
        def toJSON(self):
            json_ = {"posFrom": self.posFrom, "posTo": self.posTo, "waypoints": self.waypoints}
            return json_






"""

room1 = {}
room1["position"] = (0, 0)
room1["size"] = (4, 4)
room1["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
room1["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
room1["objects"] = {"person": (1, 1), "key": (2, 1)}

hallway = {}
hallway = {"posFrom": (1, 4), "posTo": (2, 6), "waypoints" : [(1, 5), (2, 5)]}

room2 = {}
room2["position"] = (0, 7)
room2["size"] = (4, 4)
room2["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
room2["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
room2["objects"] = {"person": (1, 1), "key": (2, 1)}

l = {"rooms": [room1, room2], "hallways" : [hallway]}
level = Level(l)

import view
v = view.View()
v.set_level(level.toJSON())
print(v.render())

"""