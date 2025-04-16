from enum import StrEnum
from xmlrpc.client import ServerProxy
import random

import pygame
from visualizer import Visualizer
import xml.etree.ElementTree as ET

class Agent:

    login: str 
    data: list[str]
    visualizer: Visualizer
    gameserver: ServerProxy

    def __init__(self, filename):
        # TODO 1     - load data from the XML configuration file (filename is in the parameter)
        # TODO 2     - create instance variables (login, data, visualizer, gameserver)
        # login      - load from XML file (tag 'login')
        # data       - an empty list, where data from server will be stored
        # visualizer - instance of the visuzlizer.Visualizer class
        # gameserver - connect to the remote XML-RPC server (url is provided in the XML file, tag 'url')
        # TODO 3     - call method 'add_player' on the server with login as the parameter (use instance variable 'self.login')

        with open(filename) as f:
            xml_input = f.read()

        xml_root = ET.fromstring(xml_input)

        login = xml_root.find("login") 
        if login is None or login.text is None:
            raise Exception("Login not found")

        url = xml_root.find("url")
        if url is None or url.text is None:
            raise Exception("Url not found")

        self.login = login.text
        self.gameserver = ServerProxy(url.text)
        self.visualizer = Visualizer()
        self.data = []

        self.gameserver.add_player(self.login)

        pass

    def action(self):
        # TODO 4 - Call 'make_action' method on the XML-RPC server.
        # The method has 3 parameters (login, action_name, parameters).
        # All three parameters are strings. Call the 'look' method on the server,
        # to take a look around the player, without NY parameter (empty string).

        self.data = self.gameserver.make_action(self.login, "look", "west")

        # Every action returns a list of strings, where each row represents one
        # row from the surrounding area of the player.
        self.visualizer.visualize(self.data)

        # Each string is 11-characters in length and there are 22 rows.

        # First 11 elements of the list represent the agent's environment
        # and other 11 elements of his surroundings
        # (so far, only "p" character is present to represent other agents).
        # The player is in this surrounding at the position [5][5] (5th row, 5th character).

        # Objects on the same position can be sought at the coordinates [5 + 11] [5].

        # "~" water
        # " " grass
        # "*" road
        # "t" tree
        # "o" rock (wall)
        # "f" tiled floor
        # "p" player
        pass
    
    def __repr__(self):
        # return self.data.__repr__()
        # TODO 5 - Returns human readable representation of stored data form 'self.data' variable.
        sep = "---------------------------------------\n"
        x_sep = "**************************************\n"
        return x_sep + "\n".join([line + "\n" for line in self.data[0:12]]) + sep + "\n".join([line + "\n" for line in self.data[0:12]]) + x_sep


    def save_data(self):
        # TODO 6 - Store data into the 'data.txt' filename.
        with open("data.txt") as f:
            f.write(self.data.__repr__())

class AgentRandom(Agent):
    # TODO 7 - This agent will extend from the previous agent and
    # reimplement (override) the 'action' method so that the action will be 'move' and
    # the passed parameter will be one the directions: 'north', 'west', 'south', 'east'.
    # These directions will be randomly selected
    # (find the appropriate method from the random package).
    def action(self):
        dirs = ['north', 'west', 'south', 'east']
        dir = random.randint(0, 3)
        self.data = self.gameserver.make_action(self.login, "move", dirs[dir])

        # Every action returns a list of strings, where each row represents one
        # row from the surrounding area of the player.
        self.visualizer.visualize(self.data)


class Direction(StrEnum):
    W = "west"
    E = "east"
    N = "north"
    S = "south"

class GameObjects(StrEnum):
    GRASS = " " 
    WATER = "~" # water
    ROAD = "*" # road
    TREE = "t" # tree
    ROCK = "o" # rock (wall)
    TILED_FLOOR = "f" # tiled floor
    PLAYER = "p" # player


class AgentLeftRight(Agent):
    # TODO 8 - This agent will be moving just to the left until it hits a barrier.
    # Then it rurn to the right and moves until it hits the barrier again.
    # It repeats such behavior.

    direction: Direction = Direction.W

    def action(self):

        # first get data
        if self.data.count == 0:
            self.data = self.gameserver.make_action(self.login, "look", str(self.direction))

        # check left
        left = self.data[5][4]
        right = self.data[5][6]
        walkable = [GameObjects.GRASS, GameObjects.TILED_FLOOR, GameObjects.ROAD]

        if self.direction == Direction.W and left in walkable:
            self.data = self.gameserver.make_action(self.login, "move", str(self.direction))
        else:
            self.direction = Direction.E

        if self.direction == Direction.E and right in walkable:
            self.data = self.gameserver.make_action(self.login, "move", str(self.direction))
        else:
            self.direction = Direction.W


        # Every action returns a list of strings, where each row represents one
        # row from the surrounding area of the player.
        self.visualizer.visualize(self.data)

class AgentControlled(Agent):
    def action(self):
        dir = None

        if self.visualizer.key_is_pressed(ord("h")):
             dir = Direction.W
        if self.visualizer.key_is_pressed(ord("j")):
             dir = Direction.S
        if self.visualizer.key_is_pressed(ord("k")):
             dir = Direction.N
        if self.visualizer.key_is_pressed(ord("l")):
             dir = Direction.E

        if dir is not None:
            self.data = self.gameserver.make_action(self.login, "move", str(dir))
        else:
            self.data = self.gameserver.make_action(self.login, "look", "")

        self.visualizer.visualize(self.data)

if __name__ == "__main__":
    agent = None
    try:
        # agent = Agent('config.xml')
        # agent = AgentRandom('config.xml')
        # agent = AgentLeftRight('config.xml')
        agent = AgentControlled('config.xml')
        while agent.visualizer.running:
            agent.action()
            print(agent)
        else:
            agent.gameserver.make_action(agent.login, 'exit', '')

        agent.save_data()

    except KeyboardInterrupt:
        if agent:
            agent.gameserver.make_action(agent.login, 'exit', '')


