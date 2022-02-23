#!/usr/bin/env python3
# coding: utf-8
import pygame

import json
from json import JSONDecodeError
import sys
import level
import character
import gamestate
import gamemanager
import os
import math

if getattr(sys, 'frozen', False):
    Path = sys._MEIPASS
else:
    Path = os.path.dirname(__file__)

ZOMBIE_PIC = pygame.image.load(os.path.join(Path, 'zombie.jpg'))
GHOST_PIC = pygame.image.load(os.path.join(Path,'ghost.jpg'))
PLAYER_PIC = pygame.image.load(os.path.join(Path, 'player.jpg'))
CURRENT_PLAYER_PIC = pygame.image.load(os.path.join(Path, 'curplayer.jpg'))


PLAYER_COLOR = (255, 192, 203)
ADV_COLOR = (255, 132, 203)
def create_level(level_data):
    rooms = level_data.get("rooms")
    hallways = level_data.get("hallways")
    objects = level_data.get("objects")

    key_pos = None
    exit_pos = None
    for obj in objects:
        t = obj["type"]
        p = obj["position"]

        if t == "exit":
            exit_pos = p
        elif t == "key":
            key_pos = p
    

    l = {"rooms" : [], "hallways" : []}
    for room_data in rooms:
        origin = room_data.get("origin")
        bounds = room_data.get("bounds")
        layout = room_data.get("layout")

        room = {}
        room["position"] = (origin[1], origin[0])
        room["size"] = (bounds["columns"], bounds["rows"])
        room["walls"] = [(col, row) for row in range(bounds["rows"]) for col in range(bounds["columns"]) if layout[row][col] == 0]
        room["doors"] = [(col, row) for row in range(bounds["rows"]) for col in range(bounds["columns"]) if layout[row][col] == 2]
        room["objects"] = {}

        if key_pos:
            if origin[0] <= key_pos[0] < origin[0] + bounds["rows"] and origin[1] <= key_pos[1] < origin[1] + bounds["columns"]:
                room["objects"]["key"] = (key_pos[1] - origin[1], key_pos[0] - origin[0])
        if exit_pos:
            if origin[0] <= exit_pos[0] < origin[0] + bounds["rows"] and origin[1] <= exit_pos[1] < origin[1] + bounds["columns"]:
                room["objects"]["exit"] = (exit_pos[1] - origin[1], exit_pos[0] - origin[0])

        l["rooms"].append(room)

    for hallway_data in hallways:
        from_ = hallway_data.get("from")
        to = hallway_data.get("to")
        waypoints = hallway_data.get("waypoints")

        hallway = {}
        hallway["posFrom"] = (from_[1], from_[0])
        hallway["posTo"] = (to[1], to[0])
        hallway["waypoints"] = [(wp[1], wp[0]) for wp in waypoints]


        
        l["hallways"].append(hallway)

    return level.Level(l)

# actor_data_list is An (actor-position-list) is a list of (actor-position)
#An (actor-position) is the following object:
# {
# "type": (actor-type),
# "name": (string),
# "position": (point)
# }
def create_actor_list(actor_data_list):
    actor_object_list = []
    for actor_data in actor_data_list:
        type_ = actor_data.get("type")
        name = actor_data.get("name")
        position = actor_data.get("position")
        position = (position[1], position[0])

        if type_ == "player":
            actor = character.Player(position, name)
        elif type_ == "zombie":
            actor = character.Adversary(position, name)
        elif type_ == "ghost":
            actor = character.Ghost(position, name)
        actor_object_list.append(actor)
    return actor_object_list


def create_state(game_state_data):
    level_data = game_state_data.get("level")
    players_data = game_state_data.get("players")
    adversaries_data = game_state_data.get("adversaries")
    exit_lock_data = game_state_data.get("exit-locked")

    level_object = create_level(level_data)
    players = create_actor_list(players_data)
    adversaries = create_actor_list(adversaries_data)

    game_state = gamestate.GameState(level_object, players, adversaries, key_found=not exit_lock_data)

    return game_state
    


#TODO: instead of taking in a game manager, input should be a json sting for game movel.
def draw_level(screen, game_state):
    all_tiles_pos = game_state.level.all_tiles_pos

    max_x = sorted(all_tiles_pos.keys(), key = lambda i: i[0], reverse = True)[0][0]
    max_y = sorted(all_tiles_pos.keys(), key = lambda i: i[1], reverse = True)[0][1]

    game_map = [[0 for i in range(max_x + 1)] for j in range(max_y + 1)]

    for k, v in all_tiles_pos.items():
        game_map[k[1]][k[0]] = v
    
    global size
    size = math.floor(min((900 / (max_x + 1)), 900 / (max_y + 1)))
    

    for j in range(len(game_map)):
        for i in range(len(game_map[j])):
            type_ = game_map[j][i]
            if type_ == 0:
                pygame.draw.rect(screen, (50, 50, 50), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "room":
                pygame.draw.rect(screen, (255, 255, 255), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "door":
                pygame.draw.rect(screen, (255, 0, 0), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "wall":
                pygame.draw.rect(screen, (0, 0, 0), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "hallway":
                pygame.draw.rect(screen, (200, 200, 200), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "key":
                pygame.draw.rect(screen, (255, 255, 255), (i * size, j * size, size - 1, size - 1), 0)
                pygame.draw.circle(screen, (0, 255, 0), (i * size + size/2, j * size + size/2), size/2)

            if type_ == "exit":
                pygame.draw.rect(screen, (255, 255, 255), (i * size, j * size, size - 1, size - 1), 0)
                pygame.draw.circle(screen, (0, 255, 255), (i * size + size/2, j * size + size/2), size/2)

def draw_level_object(screen, level):
    all_tiles_pos = level.all_tiles_pos

    max_x = sorted(all_tiles_pos.keys(), key = lambda i: i[0], reverse = True)[0][0]
    max_y = sorted(all_tiles_pos.keys(), key = lambda i: i[1], reverse = True)[0][1]
    
    game_map = [[0 for i in range(max_x + 1)] for j in range(max_y + 1)]

    for k, v in all_tiles_pos.items():
        game_map[k[1]][k[0]] = v
    
    global size
    size = math.floor(min((900 / (max_x + 1)), 900 / (max_y + 1)))
    

    for j in range(len(game_map)):
        for i in range(len(game_map[j])):
            type_ = game_map[j][i]
            if type_ == 0:
                pygame.draw.rect(screen, (50, 50, 50), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "room":
                pygame.draw.rect(screen, (255, 255, 255), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "door":
                pygame.draw.rect(screen, (255, 0, 0), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "wall":
                pygame.draw.rect(screen, (0, 0, 0), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "hallway":
                pygame.draw.rect(screen, (200, 200, 200), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == "key":
                pygame.draw.rect(screen, (255, 255, 255), (i * size, j * size, size - 1, size - 1), 0)
                pygame.draw.circle(screen, (0, 255, 0), (i * size + size/2, j * size + size/2), size/2)

            if type_ == "exit":
                pygame.draw.rect(screen, (255, 255, 255), (i * size, j * size, size - 1, size - 1), 0)
                pygame.draw.circle(screen, (0, 255, 255), (i * size + size/2, j * size + size/2), size/2)
    
def draw_character(screen, state):
    state = json.loads(state)
    players = state.get("players")
    adversaries = state.get("adversaries")
    
    global ZOMBIE_PIC, GHOST_PIC, PLAYER_PIC, CURRENT_PLAYER_PIC
    ZOMBIE_PIC = pygame.transform.scale(ZOMBIE_PIC, (size, size))
    GHOST_PIC = pygame.transform.scale(GHOST_PIC, (size, size))
    PLAYER_PIC = pygame.transform.scale(PLAYER_PIC, (size, size))
    CURRENT_PLAYER_PIC = pygame.transform.scale(CURRENT_PLAYER_PIC, (size, size))
    

    for player in players:
        position = player["position"]
        screen.blit(PLAYER_PIC, (position[1] * size, position[0] * size))
        
        font = pygame.font.SysFont('Arial', 25)
        screen.blit(font.render(player["name"], True, (255,0,0)), (position[1] * size + size/4, position[0] * size + size/4*3))

    for adversaries in adversaries:
        position = adversaries["position"]
        if adversaries["type"] == "ghost":
            screen.blit(GHOST_PIC, (position[1] * size, position[0] * size))
        elif adversaries["type"] == "zombie":
            screen.blit(ZOMBIE_PIC, (position[1] * size, position[0] * size))

        screen.blit(font.render(adversaries["name"], True, (255,0,0)), (position[1] * size + size/4, position[0] * size + size/4*3))


def draw_restricted_level(screen, restricted_view):
    layout = restricted_view["layout"]
    player_pos = restricted_view["position"]
    actors = restricted_view["actors"]
    objects = restricted_view["objects"]
    size = math.floor(900/5)
    
    global ZOMBIE_PIC, GHOST_PIC, PLAYER_PIC, CURRENT_PLAYER_PIC
    ZOMBIE_PIC = pygame.transform.scale(ZOMBIE_PIC, (size, size))
    GHOST_PIC = pygame.transform.scale(GHOST_PIC, (size, size))
    PLAYER_PIC = pygame.transform.scale(PLAYER_PIC, (size, size))
    CURRENT_PLAYER_PIC = pygame.transform.scale(CURRENT_PLAYER_PIC, (size, size))

    for j in range(len(layout)):
        for i in range(len(layout[0])):
            type_ = layout[j][i]
            if type_ == 0:
                pygame.draw.rect(screen, (50, 50, 50), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == 1:
                pygame.draw.rect(screen, (255, 255, 255), (i * size, j * size, size - 1, size - 1), 0)
            if type_ == 2:
                pygame.draw.rect(screen, (255, 0, 0), (i * size, j * size, size - 1, size - 1), 0)

    for obj in objects:
        type_ = obj["type"]
        position =  [obj["position"][0] - player_pos[0]+2, obj["position"][1] - player_pos[1]+2]

        if type_ == "key":
            pygame.draw.circle(screen, (0, 255, 0), (position[1] * size + size/2, position[0] * size + size/2), size/2)
        if type_ == "exit":
            pygame.draw.circle(screen, (0, 255, 255), (position[1] * size + size/2, position[0] * size + size/2), size/2)

    for actor in actors:
        position = [actor["position"][0] - player_pos[0]+2, actor["position"][1] - player_pos[1]+2]

        type_ = actor["type"]
        if type_ == "player":
            screen.blit(PLAYER_PIC, (position[1] * size, position[0] * size))
        elif type_ == "zombie":
            screen.blit(ZOMBIE_PIC, (position[1] * size, position[0] * size))
        elif type_ == "ghost":
            screen.blit(GHOST_PIC, (position[1] * size, position[0] * size))

        font = pygame.font.SysFont('Arial', 25)
        screen.blit(font.render(actor["name"], True, (255,0,0)), (position[1] * size + size/4, position[0] * size + size/4*3))

    screen.blit(CURRENT_PLAYER_PIC, (2 * size , 2 * size))


def draw_board(screen, text):
    pygame.draw.line(screen,  (255,255,0), (900, 0), (900, 900))
    offset = 20
    for t in text:
        t = str(t)
        font = pygame.font.SysFont('Arial', 35)
        screen.blit(font.render(t, True, (255,255,0)), (920,  offset))
        offset += 35

def render(game_manager):
    pygame.init()
    screen = pygame.display.set_mode([900, 900])

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player = game_manager.state.players[0]
                game_manager.move_character_pos_by_name((player.pos[0], player.pos[1] - 1), player.name)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                player = game_manager.state.players[0]
                game_manager.move_character_pos_by_name((player.pos[0], player.pos[1] + 1), player.name)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                player = game_manager.state.players[0]
                game_manager.move_character_pos_by_name((player.pos[0] - 1 , player.pos[1]), player.name)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                player = game_manager.state.players[0]
                game_manager.move_character_pos_by_name((player.pos[0] + 1, player.pos[1]), player.name)

        screen.fill((50, 50, 50))
    
        draw_level(screen, game_manager.state)
        draw_character(screen, str(game_manager.state))

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    with open('../tests/State/1-in.json') as f:
        data = json.load(f)
    

    game_state_data = data[0]
    game_state_object = create_state(game_state_data)
    game_manager = gamemanager.GameManager(game_state_object)


    render(game_manager)
