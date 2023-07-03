from enum import Enum

class Actions(Enum):
    BUY_PROPERTY = 1
    UPGRADE_PROPERTY = 2
    ROLL_DICE = 3
    PICK_PROPERTY = 4
    BAIL_OUT = 5
    TELEPORT = 6
    RENT = 7
    
class Status(Enum):
    WAITING = 0
    CREATED = 1
    STARTING = 2
    RUNNING = 3
    FINISHED = 4
    CANCELLED = 5
    
class CellTypes(Enum):
    PROPERTY = 1
    TAX = 2
    TELEPORT = 3
    JAIL = 4
    GOTOJAIL = 5
    START = 6
    CHANCE = 7