'''
    character.py

    character files


'''
from state import *
from enums import *
import google_sheets as gs
import formatter as frmat

class Character:

    name = ""
    money = 0
    bag = {}
    bag_index = []
    place = None
    title = ""
    title_list = []
    state = None
    search_count = 0


    def __init__(self, name):
        self.name = name
        self.money = 0
        self.bag = {}
        self.bag_index = ["", ""]
        self.place = None
        self.title = ""
        self.title_list = []
        self.state = None
        self.search_count = 0


    def add_bag(self, item, amount, update):
        if item in self.bag:
            self.bag[item] += amount
        else:
            self.bag[item] = amount

        if update:
            self.put_bag()
        return True

    def subtract_bag(self, item, amount):
        if item in self.bag:
            if self.bag[item] >= amount:
                self.bag[item] -= amount

                delete_keys = []
                for k, v in self.bag.items():
                    if v == 0:
                        delete_keys.append(k)
                for k in delete_keys:
                    self.bag.pop(k)

                self.put_bag()
                return True
            else:
                return False
        return False

    def print_bag(self):
        compiled_string = ""

        for key in self.bag.keys():
            compiled_string += f"{key}({self.bag[key]}), "
        return compiled_string[:len(compiled_string)-2]


    def put_bag(self):
        top = list(self.bag.keys())
        bottom = []
        for k in top:
            bottom.append(self.bag[k])
        top.append("")
        bottom.append("")
        how_many = len(self.bag) + 1

        top_range = gs.range_calc(self.bag_index[0] + str(self.bag_index[1]), how_many, True)
        top_range = top_range[:len(top_range) - len(str(self.bag_index[1]))]
        top_range += str(self.bag_index[1] + 1)

        gs.put_multiple(Sheet.CHARACTER.value, top_range, [top, bottom])

 
    # 이동 
    def move_places(self, new_place):
        if self.state == None:
            self.place = new_place
            row = self.bag_index[1]-1
            gs.put(Sheet.CHARACTER.value, "D" + str(row), [new_place.kor_acr])
            return new_place.upon_arrival + f"\n[{self.name}(은)는 {new_place.name}에 도착했습니다.]"
        else:
            return "[위치를 이동하기 전, 현 위치에서의 탐색을 완료해주세요.]\n" + frmat.content_formatter(self, True)


    def __str__(self):
        c = f"Character : {self.name}----------------\n"
        c += f"money: {self.money} | place: " + str(self.place.acr) + "\n"
        c += f"bag_index : {self.bag_index}\n"
        c += "bag: " + self.print_bag() + "\n"
        if self.state == None:
            c += f"state: {self.state}\n\n"
        else:
            c+=f"state: {self.state.ID}\n\n"
        return c    

    def print_place(self):
        return frmat.place_formatter(self.place)

    def search(self):

        # choose a new state
        if self.state == None:
            next_event = random.choice(self.place.free_search_deck)
            self.state = next_event
            return_string = frmat.content_formatter(self, True)
            if len(self.state.choices) == 0:
                self.state = None
            return return_string

        # haven't picked a choice
        else:
            return_string = "[탐색을 재차례 진행하기 전에 선택지를 골라주세요.]\n"
            return_string += frmat.content_formatter(self, True)
            return return_string

    def choice(self, msg):

        return_string = ""

        try:
            choice_index = self.state.choices.index(msg)
            pool_results = []

            # a percentage thing
            if self.results[choice_index][0].find("%") != -1:
                pool_results = self.state.choose_result(choice_index)
            else:
                pool_results = self.state.results

            # should have [some choices, a no-option choice]




            # find out what no_choice_option is for
            if no_choice_option != "":
                no_choice_index = pool_result.find(no_choice_option)
                init_parsed = no_choice_option.split("| ")   # (word op num)| and text
                parsed = init_parsed[0].split(" ")           # (word and op num)

                # money barrier
                if parsed[0][1:] == "소지금":
                    # money less than something
                    if parsed[1][:1] == "<":
                        # calculate exact barrier
                        how_much = int(parsed[1][1:parsed[1].find(")")])
                        # if character has less than that amount, return that response
                        if character.money < how_much:
                            return [init_parsed[1], pool_next[no_choice_index]]




        except ValueError as e:
            return_string += "[입력하신 선택지는 목록에 없습니다.]\n"
            return_string += frmat.choice_formatter(self.state.choices)


        return return_string




