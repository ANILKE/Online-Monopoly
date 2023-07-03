"""

Board class for the monopoly game.
It is a basically circular doubly linked list of cells.

"""
from .Cells import *
from queue import Queue
from phase1.ChanceCards import *

class Grid:
    def __init__(self, values,upgrade_cost,teleport_cost,jailbailcost,tax,lottery,startup_money,chanceCards,turn_money):

        self.property_cells = []
        self.chanceCards = Queue()
        self.head = None
        self.tail = None
        self.jail = None
        
        self.turn_money = turn_money 
        self.upgrade_cost = upgrade_cost
        self.teleport_cost = teleport_cost
        self.jailbailcost = jailbailcost
        self.tax = tax
        self.lottery = lottery
        self.startup_money = startup_money
        self.color_types = set()
        
        if values is not None:
            self.add_cells(values)
            self.create_cards(chanceCards)

    
    def filter_property_by_color(self,key):

        curr_ptr = self.head.next

        ans = []
        while curr_ptr is not self.head:
            if isinstance(curr_ptr,PropertyCell) and curr_ptr.color == key:
                ans.push_back(curr_ptr)
            curr_ptr = curr_ptr.next

        return ans
    def add_cell_at_end(self, cell: AbstractCell):
        if self.head == None:
            self.head = cell
            self.tail = cell
            return

        cell.prev = self.tail
        self.tail.next = cell
        self.tail = cell
        cell.next = self.head
        self.head.prev = self.tail

    
    
    def filter_property_by_color(self,key):
        
        curr_ptr = self.head.next
        
        ans = []
        while curr_ptr is not self.head:
            if isinstance(curr_ptr,PropertyCell) and curr_ptr.color == key:
                ans.append(curr_ptr)
            curr_ptr = curr_ptr.next
            
        return ans
    def add_cells(self, cells):

        for cell in cells:
            new_cell = self.cell_creator(cell)
            self.add_cell_at_end(new_cell)
    def create_cards(self, chanceCards):
        for card in chanceCards:
            if (card["type"] == "lottery"):
                new_card = LotteryCard("Lottery Card")
            elif (card["type"] == "tax"):
                new_card = TaxCard("Tax Card")
            elif (card["type"] == "teleport"):
                new_card = TeleportCard("Teleport Card")
            elif (card["type"] == "upgrade"):
                new_card = UpgradePropertyCard("Upgrade Card")
            elif (card["type"] == "downgrade"):
                new_card = DowngradePropertyCard("Downgrade Card")
            elif (card["type"] == "colorupgrade"):
                new_card = ColorUpgradeCard("Color Upgrade Card")
            elif (card["type"] == "colordowngrade"):
                new_card = ColorDowngradeCard("Color Downgrade Card")
            elif (card["type"] == "gotojail"):
                new_card = GotoJailCard("Go To Jail Card")
            elif (card["type"] == "jailfree"):
                new_card = JailFreeCard("Jail Free Card")
            self.chanceCards.put(new_card)
            

    def cell_creator(self, cell):
        """
            Cell is a dictinary for example:
            {"type": "property","name":"Cankaya","cell":20,"color": 'brown',
                   'price': 150,"rents":[100,140,200,300,450]},
        """
        key = 'type'

        if cell[key] == 'property':
            new_node = PropertyCell(None, None,cell["cell"] ,cell['name'], cell['price'], cell['color'], cell['rents'])
            self.property_cells.append(new_node)
            self.color_types.add(cell['color'])

        elif cell[key] == 'start':
            new_node = StartCell(None, None,cell["cell"])

        elif cell[key] == 'chance':
            new_node = ChanceCell(None, None,cell["cell"])

        elif cell[key] == 'tax':
            new_node = TaxCell(None, None,cell["cell"])
        elif cell[key] == 'teleport':
            new_node = TeleportCell(None, None,cell["cell"])
        elif cell[key] == 'jail':
            new_node = JailCell(None, None,cell["cell"])
            self.jail = new_node
        elif cell[key] == 'gotojail':
            new_node = GoToJailCell(None, None,cell["cell"])

        return new_node
    
    def teleporting_cells(self,user):
        res = []
        
        for prop_cell in self.property_cells:
            if prop_cell.owner == user or prop_cell.owner == None:
                res.append(prop_cell)
                
        return res