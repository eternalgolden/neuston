'''
    helper.py

    has a bunch of helper functions
    that don't belong anywhere particularly

'''
import google_sheets as gs
from enum import *

def init_bulletin():
    bulletin = {}
    data = gs.get("캐릭터", "B2:I53")
    for i in range(0, len(data), 3):
        if len(data[i]) >= 8:
            ch_name = data[i][0]
            bulletin_msg = data[i][7]
            bulletin[ch_name] = bulletin_msg

    return bulletin
            


