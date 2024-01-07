'''
    owner.py

    contains the owner class

'''
import google_sheets as gs
from enums import *

class Owner:

    chacter_list = {}
    discord_name = ""
    name = ""
    main = None # can be None or a character object
    row = -1

    def __init__(self, name, discord_name, main):
        self.name = name
        self.character_list = {}
        self.discord_name = discord_name
        self.main = main
        self.row = -1

    def set_main(self, character_name):
        if not character_name in self.character_list:
            return f"*[ERROR] 당신은 '{character_name}'의 권한이 없다.\n{str(list(self.character_list.keys()))}중 선택할 수 있다.*"
        else:
            self.main = self.character_list[character_name]
            gs.put(Sheet.OWNER.value, "C" + str(self.row), [character_name])
            return f"*[SYS] 메인 캐릭터가 '{character_name}'(으)로 설정되었다.*"

    def find_character(self, character_name):
        if not character_name in self.character_list:
            return None
        else:
            return self.character_list[character_name]

    def __str__(self):
        return_str =  f"Owner name : {self.name}\nCharacter_List : \n"
        for ch in self.character_list:
            return_str += str(ch) + "\n\n"
        return return_str
