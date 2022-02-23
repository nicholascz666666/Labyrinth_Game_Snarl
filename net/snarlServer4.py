#!/usr/bin/env python3
# coding: utf-8
import argparse
import sys
import socket
import json
import threading
from json import JSONDecodeError

import math
import sys
sys.path.insert(1, '../src/')
import render
import snarlGen
sys.path.insert(1, '../src/Player/')

from serverplayer import ServerPlayer
import localzombie 

sys.path.insert(1, '../src/Observer/')
import localobserver

import gamemanager


import utils


SERVER_WELCOME = json.dumps({ "type": "welcome",  "info": "Gulinde" })

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", type=int, default=10)
    parser.add_argument("--clients", type=int, choices=range(1, 5), default=4)
    parser.add_argument("--wait", type=int, default=60)
    parser.add_argument("--observe", action='store_true')
    parser.add_argument("--address", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=45678)
    args = parser.parse_args()


    levels = []
    for i in range(args.generate):
        levels.append(snarlGen.generateLevel())

    manager = gamemanager.GameManager()
    manager.set_levels(levels)
    
    #create server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind socket
    try:
        s.bind((args.address, args.port))
    except socket.error:
        print("unable to bind")
        sys.exit()

    s.settimeout(args.wait)

    s.listen()

    for i in range(args.clients):
        try: 
            conn, addr = s.accept()
        
            conn.sendall(SERVER_WELCOME.encode('utf-8'))
            
            client = ServerPlayer(None, conn)
            while True:
                conn.sendall(json.dumps("name").encode('utf-8'))
                name = conn.recv(2048).decode('utf-8')

                #if the name is invalid, prompt again
                name_valid = manager.accept_character(name, client=client)
                if name_valid:
                    print("accepted player:", name)
                    client.set_name(name)
                    break
                print("invalid name " + name)

        except socket.timeout:
            print("timeout")
            break
        
    s.close()
    print("start game")

    if args.observe:
        observer = localobserver.LocalObserver()
        manager.add_obsever(observer)
        t1 = threading.Thread(target=observer.render)
        t1.start()


    manager.start_game()




main()