#!/usr/bin/env python3
# coding: utf-8
import argparse
import json
import threading
import math
import sys
sys.path.insert(1, '../src/')
import render
sys.path.insert(1, '../src/Player/')

import localplayer
import localzombie 
sys.path.insert(1, '../src/Observer/')
import localobserver

import gamemanager


import utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=argparse.FileType('r'), default="snarl.levels")
    parser.add_argument("--players", type=int, choices=range(1, 5), default=1)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--observe", action='store_true')
    args = parser.parse_args()

    if args.players > 1:
        print("only support a single player")
        exit()
        
    file_content = args.file.read()
    json_list = utils.decode_json(file_content)
    args.file.close()

    levels = []
    for i in range(json_list[0]):
        level_object = utils.create_level(json_list[i+1])
        levels.append(level_object)

    #print(args.players)
    #print(args.start)
    #print(args.observe)

    manager = gamemanager.GameManager()
    manager.set_levels(levels, args.start)

    for i in range(1):
        print("enter player" + str(i+1) + "'s name")
        player_name = input()

        player = localplayer.LocalPlayer(player_name)
        manager.accept_character(name=player_name, type_="player", client=player)

        if not args.observe:
            t1 = threading.Thread(target=player.render)
            t1.start()
        else:
            observer = localobserver.LocalObserver()
            manager.add_obsever(observer)
            t1 = threading.Thread(target=observer.render)
            t1.start()

    
    


    manager.start_game()




main()
