from phase2 import * 
from phase1 import *
from game_map import * 
import sys


def run():
    #port_num = int(sys.argv[2])
    server = MonopolyServer(1447,3)
    server.start_server()


run()

