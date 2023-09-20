'''
    owner_loader.py

    loads owner information
    calls character loader from here

'''

from character import *
from owner import *
from enums import *
import character_loader as cl
import google_sheets as gs

def get_owners():

    # call character loader
    character_list = cl.get_characters()

    # read necessary information
    owner_info = gs.get(Sheet.OWNER.value, "A2:D7")
    owners = {}
    index = 2

    for info in owner_info:
        if info[2] == "-":
            info[2] = None
        owner = Owner(info[0], info[1], info[2])
        owner.row = index

        # get character list
        read_range = gs.range_calc("E" + str(index), int(info[3]), True)
        ch_names = gs.flatten(gs.get(Sheet.OWNER.value, read_range))
        for ch in ch_names:
            owner.character_list[ch] = character_list[ch]

        # add owner to owner list
        owners[owner.discord_name] = owner
        print("discord name " + owner.discord_name)
        index += 1

    return [character_list, owners]




