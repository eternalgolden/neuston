'''
    enums.py

    contains useful enums like sheet names

'''

from enum import Enum

pfx = "-"

class SystemMessage(Enum):
    CONFIRM = "[SYS] 해당 행동 확인."
    DENY = "[SYS] 해당 행동 불가능."
    NONEXISTENT = "[ERROR] 해당 행동 불가능 -- 명령어의 부분이 잘못되거나 존재하지 않는다."
    WRONGFORM = "[ERROR] 해당 행동 불가능 -- 양식에 맞지않다."
    INFO =f'''
[SYS] 커맨드 정보.

| `{pfx}게시판 캐릭터이름 메세지`
게시판에 해당 메세지를 익명으로 띄운다. 익명으로 띄우지만 한 캐릭터당 하나기때문에
캐릭터이름으로 분류한다. 다시쓰면 덮어씌워진다.

| `{pfx}메인 캐릭터이름`
메인 캐릭터를 해당 캐릭터로 세운다. 무슨 행동이든 메인 캐릭터를 선언하고 난 다음에
행동이 가능하다. 하지만 조사를 시작하기 전 한번이라도 선언했으면 OK.
행동할 캐릭터가 바뀔때 마다 다시 선언해야한다.

| `{pfx}이동 장소약칭`
조건이 맞다면 해당하는 장소로 이동시켜준다.

| `{pfx}위치`
메인 캐릭터의 현 위치를 보여준다.'''
    WRONGCHANNEL = "[ERROR] 채널이 올바르지 않다. 올바른 채널로 이동 요망."


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
    S4 = "mock-개인조사4"
