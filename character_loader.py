'''
    character_loader.py

    loads character sheets using character and google sheets

'''
import google_sheets as gs
from character import *
from enums import *

def get_characters():

    # get sheet
    
    characters_info = gs.get(Sheet.CHARACTER.value, "A2:ZZ58")

    characters = {}
    current = None

    for r in range(0, len(characters_info), 3):

        row  = characters_info[r] # name, money, place

        current = Character(row[1])
        current.money = int(row[2])
        current.stats = {'TRS': int(row[4]), 'ETH': int(row[5]), 'AQU': int(row[6]), 'KIN':int(row[7])}
        current.search_count = current.stats['AQU']
        current.stamina = int(current.stats['AQU'] * 1.5)
        current.cost = int(current.stats['AQU'] * 0.2)
        current.hp = {'head': current.stats['TRS'], 'body': current.stats['TRS'] + 2, 'arm': int(current.stats['TRS'] * 1.6), 'leg': int(current.stats['TRS']*1.6),\
                        'san': current.stats['ETH'] * 5 }

        current.place = row[3] # later replace with place obj
        current.bag_index[0] = "B"
        current.bag_index[1] = r+1+2

        item_names = characters_info[r+1]
        item_nums = characters_info[r+2]

        for i in range(1, len(item_names)):
            current.add_bag(item_names[i], item_nums[i], False)

        characters[current.name] = current

    return characters





