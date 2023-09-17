'''
    enums.py

    contains useful enums like sheet names

'''

from enum import Enum

# used like Sheet.OWNER.value
class Sheet(Enum):

    # basic info
    OWNER = "오너" 
    CHARACTER = "캐릭터"

    # place sheets
    DAWN = "탐색:새벽녘"
    HQ = "탐색:본부"
    

    # item types
    ITEM_ALCH = "아이템:연금"
    ITEM_MEAT = "아이템:고기"
    ITEM_VEG = "아이템:채소"
    ITEM_FOOD = "아이템:음식"

class Dest(Enum):
    DAWN = "새벽녘"
    HQ = "본부"
