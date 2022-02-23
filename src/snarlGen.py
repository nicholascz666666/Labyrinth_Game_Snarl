#!/usr/bin/env python3
# coding: utf-8
import math
import random
from scipy.spatial import Delaunay
import numpy as np

from level import Level
import heapq

import argparse

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def normalize(self):
        mag = self.length()
        if mag == 0:
            self.x = 0
            self.y = 0
        else:
            self.x /= mag
            self.y /= mag

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def dist(self, other):
        p = Point(self.x - other.x, self.y - other.y)
        return p.length()

class Room(Point):
    def __init__(self, x, y, size):
        super().__init__(x, y)
        self.size = size
        self.doors = []
        self.walls = []

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

    def addDoor(self, doorPos):
        doorPos = (doorPos[0] - self.x, doorPos[1] - self.y)
        self.doors.append(doorPos)
        if doorPos in self.walls: 
            self.walls.remove(doorPos)

    def potentialDoorPos(self):
        result = []
        for wall in self.walls:
            if wall[0] == 0 and (wall[1] == 0 or wall[1] == self.size[1] - 1):
                continue
            if wall[0] == self.size[0] - 1 and (wall[1] == 0 or wall[1] == self.size[1] - 1):
                continue
            result.append((wall[0] + self.x, wall[1] + self.y))
        return result

def getRandomPointInCircle(radius):
    t = 2 * math.pi * random.random()
    u = random.random() + random.random()
    if u > 1:
        r = 2 - u 
    else:
        r = u
    return math.floor(radius*r*math.cos(t)), math.floor(radius*r*math.sin(t))

def computeSeparation(myAgent, agentArray, t):
    v = Point()
    neighborCount = 0

    for agent in agentArray:
        if agent != myAgent:
            if myAgent.dist(agent) < t * 1.3:
                v.x += agent.x - myAgent.x;
                v.y += agent.y - myAgent.y
                neighborCount += 1
    if neighborCount == 0:
        return v
    v.x /= neighborCount
    v.y /= neighborCount
    v.x *= -1;
    v.y *= -1;
    v.normalize()
    return v

def generateRooms(room_num, min_dim, max_dim):
    agentArray = []
    for _ in range(room_num):
        point = getRandomPointInCircle(1)
        x = random.randint(min_dim[0], max_dim[0])
        y = random.randint(min_dim[1], max_dim[1])
        agent = Room(point[0], point[1], [x, y])
        agentArray.append(agent)
    return agentArray

def seperateRooms(agentArray, t):
    while True:
        stop = True
        for agent in agentArray:
            separation = computeSeparation(agent, agentArray, t)
            agent.x += separation.x
            agent.y += separation.y

            if separation.x != 0 or separation.y != 0:
                stop = False
        if stop:
            break
    for room in agentArray:
        room.x = math.floor(room.x)
        room.y = math.floor(room.y)

    return agentArray

def generateConnectedGraph(agentArray):
    neighbor = {}
    if len(agentArray) == 1:
        neighbor[agentArray[0]] = []
        return neighbor

    elif len(agentArray) == 2:
        neighbor[agentArray[0]] = [agentArray[1]]
        neighbor[agentArray[1]] = []
        return neighbor

    points = np.array([[agent.x, agent.y] for agent in agentArray])
    simplices = Delaunay(points).simplices

    for tri in simplices:
        for i in range(len(tri)):
            agent = agentArray[tri[i]]
            if agent not in neighbor:
                neighbor[agent] = []

            n1 = agentArray[tri[i-1]]
            n2 = agentArray[tri[(i+1)%len(tri)]]
            if n1 not in neighbor[agent]:
                neighbor[agent].append(n1)
            if n2 not in neighbor[agent]:
                neighbor[agent].append(n2)

    return neighbor


def reduceNumberOfConnection(graph, visited=[], queue=[]):

    visited.append(list(graph.keys())[0])
    queue.append(list(graph.keys())[0])

    new_graph = {}
    while queue:
        room = queue.pop(0)
        for neighbor in graph[room]:
            if room not in new_graph:
                new_graph[room] = []

            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)                
                new_graph[room].append(neighbor)
            else:
                rand = random.random()
                if rand < 0.1 and room not in new_graph.get(neighbor, []):
                    new_graph[room].append(neighbor)

    return new_graph

def generateHallways(graph):
    space_occupied = set()
    for room in graph.keys():
        for x in range(room.size[0]):
            for y in range(room.size[1]):
                space_occupied.add((room.x + x, room.y + y))
    

    hallways = []
    for room, neighbor in graph.items():
        for n in neighbor:
            
            dist_pos = {}
            for w1 in room.potentialDoorPos():
                for w2 in n.potentialDoorPos():
                    dist = abs(w1[0] - w2[0]) + abs(w1[1] - w2[1])
                    if dist not in dist_pos:
                        dist_pos[dist] = []
                    dist_pos[dist].append((w1, w2))
            
            
            shortest_path_dist = float('inf') 
            shortest_path = None

            for i in sorted(dist_pos.keys())[: min(3, len(dist_pos.keys()))]:
                for wallPair in dist_pos[i]:
                    wall1 = wallPair[0]
                    wall2 = wallPair[1]
                    
                    path = astar(wall1, wall2, space_occupied)

                    if path:
                        if len(path) < shortest_path_dist:
                            shortest_path_dist = len(path)
                            shortest_path = path

            if shortest_path:

                for p in shortest_path:
                    space_occupied.add(p)

                room.addDoor(shortest_path[-1])
                n.addDoor(shortest_path[0])
                
                hallway = path2hallway(shortest_path)
                hallways.append(hallway)

            else:
                raise RuntimeError('no path')

    return hallways

def add_walls(roomArray):
    for room in roomArray:
        walls = set()
        for x in range(room.size[0]):
            walls.add((x, 0))
            walls.add((x, room.size[1] - 1))
        for y in range(room.size[1]):
            walls.add((0, y))
            walls.add((room.size[0] - 1, y))
        room.walls = list(walls)
        
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, target, space_occupied):
    d = {start: 0}
    parent = {start: None}
    pq = [(heuristic(start, target), start)]
    visited = set()

    while pq:
        cost, pos = heapq.heappop(pq)
        if pos in visited: 
            continue
        if pos == target:
            path = []
            curr = pos
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path

        visited.add(pos)

        adj = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adj = [(pos[0] + a[0], pos[1] + a[1]) for a in adj]
        for p in adj:
            
            if p[0] < 0 or p[1] < 0 or p[0] > maxx or p[1] > maxy:
                continue
            if p in space_occupied and p != target:
                continue
            g = d[pos] + 1
            if p not in d or d[p] > g:
                d[p] = g
                f = g + heuristic(p, target)
                parent[p] = pos
                heapq.heappush(pq, (g + f, p))

    return None

def path2hallway(path):
    posFrom = path[0]
    posTo = path[-1]

    waypoints = []

    direction = None
    for i in range(len(path) - 1):
        p0 = path[i]
        p1 = path[i+1]

        new_direction = (p0[0] - p1[0], p0[1] - p1[1])

        if direction == None:
            direction = new_direction

        if new_direction != direction:
            #change of direction, add waypoint
            waypoints.append((p0[0], p0[1]))
            direction = new_direction

    hallway = {"posFrom" : posFrom, "posTo": posTo, "waypoints": waypoints}
    return hallway


def generateLevel(room_num=5, min_dim=[4,4], max_dim=[15,15]):
    while True:
        try:
            roomArray = generateRooms(room_num, min_dim, max_dim)
            roomArray = seperateRooms(roomArray, max(max_dim))
            
            add_walls(roomArray)
            graph = generateConnectedGraph(roomArray)
            graph = reduceNumberOfConnection(graph)
            


            minx = min([room.x for room in roomArray])
            miny = min([room.y for room in roomArray])
            if minx < 0:
                for room in roomArray:
                    room.x -= minx
            if miny < 0:
                for room in roomArray:
                    room.y -= miny

            global maxx, maxy
            maxx = max([room.x for room in roomArray]) + max_dim[0]
            maxy = max([room.y for room in roomArray]) + max_dim[1]

            hallways = generateHallways(graph)

            l = {"rooms": [], "hallways": hallways}
            for room in roomArray:
                r = {}
                r["position"] = (room.x, room.y)
                r["size"] = (room.size[0], room.size[1])
                r["walls"] = room.walls
                r["doors"] = room.doors
                r["objects"] = {}
                l["rooms"].append(r)

            key_room = l["rooms"][-1]
            key_room["objects"]["key"] = (random.randint(1, key_room["size"][0] - 2), random.randint(1, key_room["size"][1] - 2))
            exit_room = l["rooms"][0]
            exit_room["objects"]["exit"] = ((random.randint(1, exit_room["size"][0] - 2), random.randint(1, exit_room["size"][1] - 2)))
            level = Level(l)

            return level
        except:
            continue



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rooms", type=int, default=5)
    parser.add_argument("--min", nargs="+", type=int, default=[4, 4])
    parser.add_argument("--max", nargs="+", type=int, default=[15, 15])
    parser.add_argument("--json", action='store_true')
    parser.add_argument("--render", action='store_true')
    args = parser.parse_args()

    if args.rooms <= 0:
        print("room number should be > 0")
        exit()

    level = generateLevel(args.rooms, args.min, args.max)

    if args.json:
        print(str(level))
    
    if args.render or (not args.json and not args.render):
        import pygame
        import render

        pygame.init()
        screen = pygame.display.set_mode([900, 900])

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((50, 50, 50))

            render.draw_level_object(screen, level)

            pygame.display.flip()

        pygame.quit()

