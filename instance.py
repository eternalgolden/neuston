'''
    instance.py

    has everything that have to do with instances

'''

class Instance:

    character_list = []
    enemy_list = []
    ID = ""
    search_count = 0

    def __init__(self, ID):
        self.ID = ID
        self.character_list = []
        self.enemy_list = []
        self.search_count = 0

    def __str__(self):
        return "instance ID : " + self.ID + "\ncharacters :" + str([ch.name for ch in self.character_list]) + "enemies : " + str(len(self.enemy_list)) + "\n"

    def move(self, character, place):
        return_string = character.move_places(place)

        if place.acr == "hq":
            self.character_list.remove(character)
            return place.upon_arrival + f"\n*{character.name}(은)는 {place.name}로 돌아갔다.*"


        if len(self.character_list) == 1:
            return return_string

        # ~~~ 은)는 어디에 도착했다.*
        msg = return_string.split("(")
        return_string = place.upon_arrival
        return_string += f"\n*{character.name}"
        # gathering all names
        for ch in self.character_list:
            if ch.name != character.name:
                ch.move_places(place) 
                return_string += f", {ch.name}"
        return_string += "(" + msg[1]
        return return_string


    def search(self, character):
        self.search_count -= 1
        print(self.search_count)
        if self.search_count < 0:
            self.search_count = -1
            for ch in self.character_list:
                ch.state = None
            return "*오늘은 더이상 탐색을 진행할 수 없다.*"

        elif len(self.character_list) == 1:
            return_string = character.search()
            return return_string
        else:
            return_string = character.search_plus(self.character_list, self.search_count)
            for ch in self.character_list:
                if ch.name != character.name:
                    ch.state = character.state
                    if character.state != None:
                        ch.already_seen.append(character.state.ID)

            return return_string

    def choice(self, character, msg):
        returned = character.choice(msg)
        
        for ch in self.character_list:
            if ch.name != character.name:
                ch.state = character.state

        return returned[1]

        




