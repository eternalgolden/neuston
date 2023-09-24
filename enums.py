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

class Stat(Enum):
    TRS = 0
    ETH = 1
    AQU = 2
    KIN = 3
class Dest(Enum):
    DAWN = "새벽녘마을"
    HQ = "본부"

class Channel(Enum):
    HQ = "본부"
    S1 = "조사-1"
    S2 = "조사-2"
    S3 = "조사-3"
    S4 = "개인조사-4"
 
class M_Channel(Enum):
    HQ = "mock-본부"
    S1 = "mock-조사1"
    S2 = "mock-조사2"
    S3 = "mock-조사3"
    S4 = "mock-조사4"
