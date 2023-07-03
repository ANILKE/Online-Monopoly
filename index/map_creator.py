
# This file is used to create a map for the game.
def creator(game_name,city_names,city_colors,city_prices,city_level_prices):
    basic_map = {}
    basic_map['cells'] = []
    basic_map['name'] = game_name
    basic_map['cells'].append({"type": "start","cell":1})
    for i in range(len(city_names)):
        basic_map['cells'].append({"type": "property","name":city_names[i],
                                   "cell":i+2,"color": city_colors[i],"price":city_prices[i],
                                   "rents":city_level_prices[i]})

    basic_map['cells'].insert(2,{"type": "tax","cell":3})
    basic_map['cells'].insert(4,{"type": "teleport","cell":5})
    basic_map['cells'].insert(7,{"type":"chance","cell":8})
    basic_map['cells'].insert(10,{"type": "jail","cell":11})
    basic_map['cells'].insert(14,{"type": "tax","cell":13})
    basic_map['cells'].insert(19,{"type": "teleport","cell":18})
    basic_map['cells'].insert(20,{"type": "tax","cell":21})
    basic_map['cells'].insert(24,{"type": "teleport","cell":23})
    basic_map['cells'].insert(28,{"type": "chance","cell":29})
    basic_map['cells'].insert(30,{"type": "gotojail","cell":31})
    basic_map['cells'].insert(33,{"type": "chance","cell":34})
    basic_map['cells'].insert(37,{"type": "chance","cell":38})
    basic_map['cells'].insert(39,{"type": "tax","cell":40})
    
    

    for i in range(len(basic_map['cells'])):
        basic_map['cells'][i]['cell'] = i + 1
    


    basic_map['upgrade'] = 50
    basic_map['teleport'] = 150
    basic_map['jailbail'] = 100
    basic_map['tax'] = 45
    basic_map['lottery'] = 600
    basic_map['startup'] = 2500
    basic_map['turn_money'] = 450

    basic_map['chances'] = [
        {"type":"teleport"},
        {"type":"upgrade"},
        {"type":"downgrade"},
        {"type":"colorupgrade"},
        {"type":"downgrade"},
        {"type":"gotojail"},
        {"type":"jailfree"},
        {"type":"lottery"},
        {"type":"tax"},
        {"type":"colordowngrade"},
        {"type":"downgrade"},
        {"type":"gotojail"},
        {"type":"teleport"},
        {"type":"upgrade"},
        {"type":"downgrade"},
        {"type":"jailfree"},
        {"type":"lottery"},
        {"type":"tax"},
    ]


    return basic_map