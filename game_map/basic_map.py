""" 
    kirmiziy
    tax
    kirmizi
    teleport


    sari
    sari
    chance
    sari
    sari

    jail

    
    yesil
    yesil
    yesil

    purple
    purple
    teleport
    purple
    purple

    turuncu
    turuncu
    teleport
    turuncu
    turuncu

    bue
    bluıe
    blue
    chance

    blue
    goto
    
    pink
    pink
    chance
    pink
    siyah
    chance
    siyah
    tax
    siyah
"""






basic_map = {
    "cells":[
        
        {"type": "start","cell":1},
        
        {"type": "property","name":"Sydney","cell":2,"color": 'brown',
                   'price': 150,"rents":[100,140,200,300,450]},

        {"type": "tax","cell":3},

        {"type": "property","name":"Sihhiye","cell":4,"color": 'brown',
                   'price': 90,"rents":[80,100,160,250,300]},
        
        {"type": "teleport","cell":5},


        
        {"type": "property","name":"Eryaman","cell":6,"color": 'brown',
                   'price': 40,"rents":[30,40,50,90,150]},
        
        {"type": "property","name":"Yesilyurt","cell":7,"color": 'brown',
                   'price': 100,"rents":[40,100,175,275,400]},

        {"type":"chance","cell":8},
                
        {"type": "property","name":"Dogansehir","cell":9,"color": 'brown',
                   'price': 80,"rents":[50,60,70,150,200]},

        {"type": "property","name":"Battalgazi","cell":10,"color": 'brown',
                   'price': 90,"rents":[30,70,150,200,250]},

        {"type": "jail","cell":11},



        
            
        {"type": "property","name":"Kibriscik","cell":12,"color": 'brown',
                   'price': 20,"rents":[30,50,70,100,150]},


        {"type": "tax","cell":13},
        {"type": "property","name":"Seben","cell":14,"color": 'brown',
                   'price': 40,"rents":[50,70,90,110,170]},

        {"type": "property","name":"Merkez","cell":15,"color": 'brown',
                   'price': 150,"rents":[90,130,144,250,500]},
        
        {"type": "property","name":"Besiktas","cell":16,"color": 'brown',
                   'price': 300,"rents":[200,300,350,450,500]},
        {"type": "property","name":"Kadikoy","cell":17,"color": 'brown',
                   'price': 300,"rents":[250,350,400,450,475]},
        {"type": "teleport","cell":18},

        {"type": "property","name":"Sariyer","cell":19,"color": 'brown',
                     'price': 300,"rents":[250,350,400,450,475]},
        {"type": "property","name":"Beykoz","cell":20,"color": 'brown',
                     'price': 300,"rents":[250,350,400,450,475]},   

        {"type": "tax","cell":21},
      
        {"type": "property","name":"Beyoglu","cell":22,"color": 'brown',
                     'price': 500,"rents":[400,475,550,650,775]},
        {"type": "teleport","cell":23},
        {"type": "property","name":"Taksim","cell":24,"color": 'brown',
                        'price': 500,"rents":[400,475,550,650,775]},
        {"type": "property","name":"Karakoy","cell":25,"color": 'brown',
                        'price': 500,"rents":[400,475,550,650,775]},
        
        {"type": "property","name":"Sile","cell":26,"color": 'brown',
                        'price': 600,"rents":[500,600,700,800,900]},

        {"type": "property","name":"Agva","cell":27,"color": 'brown',
                        'price': 600,"rents":[500,600,700,800,900]},
        {"type": "property","name":"Golbasi","cell":28,"color": 'brown',
                        'price': 600,"rents":[500,600,700,800,900]},
        {"type": "chance","cell":29},
        {"type": "property","name":"Kizilay","cell":30,"color": 'brown',
                        'price': 600,"rents":[500,600,700,800,900]},
        {"type": "gotojail","cell":31},
        
        {"type": "property","name":"Altindag","cell":32,"color": 'brown',
                        'price': 700,"rents":[600,700,800,900,1000]},

        {"type": "property","name":"Mamak","cell":33,"color": 'brown',
                        'price': 700,"rents":[600,700,800,900,1000]},
        {"type": "chance","cell":34},


        {"type": "property","name":"Etimesgut","cell":35,"color": 'brown',
                        'price': 700,"rents":[600,700,800,900,1000]},

        

        {"type": "property","name":"Gonya Ovasi","cell":37,"color": 'brown',
                        'price': 800,"rents":[700,800,900,1000,1100]},
        {"type": "chance","cell":38},
        {"type": "property","name":"Mogan Golu","cell":39,"color": 'brown',
                        'price': 800,"rents":[700,800,900,1000,1100]},

        {"type": "tax","cell":40},
        {"type": "property","name":"Vano Glu","cell":41,"color": 'brown',
                        'price': 800,"rents":[700,800,900,1000,1100]},
        
    ],
    "upgrade": 50,
    "teleport": 150,
    "jailbail": 100,
    "tax":45,
    "lottery":600,
    "startup":2500,
    "turn_money":450,
    "chances": [
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
}