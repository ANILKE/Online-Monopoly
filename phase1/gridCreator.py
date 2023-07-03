from phase1.Grid import Grid

#Basic grid creator helper functions.

def grid_creator(map):
    grid = Grid(map["cells"],
                map["upgrade"],
                map["teleport"],
                map["jailbail"],
                map["tax"],map["lottery"],
                map["startup"],
                map["chances"],
                map["turn_money"]
                )
    return grid