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
    stats = []


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
        self.stats = [0, 0, 0, 0]


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
                for k in deleteo_keys:
                    self.bag.pop(k)

                self.put_bag()
                return True
            else:
                return False
        return False

    def add_money(self, m):
        self.money += m
        money_range = 'C' + str(self.bag_index[1]-1)
        gs.put(Sheet.CHARACTER.value, money_range, self.money)
        return f"*{self.name}의 소지금에 {m}C가 추가됐다.*"

    def subtract_money(self, m):
        self.money -= m
        if self.money < 0:
            self.money = 0
        gs.put(Sheet.CHARACTER.value, 'C' + str(self.bag_index[1]-1), self.money)
        return f"*{self.name}의 소지금에서 {m}C가 빠져나갔다...*"


    def print_bag(self):
        compiled_string = ""

        for key in self.bag.keys():
            compiled_string += f"{key}({self.bag[key]}), "
        return compiled_string[:len(compiled_string)-2]

    def roll_stats(self):
        success = []
        for stat in self.stats:
            if random.randint(1,10) < stat:
                success.append(True)
            else:
                success.append(False)
        return success


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
            return new_place.upon_arrival + f"\n*{self.name}(은)는 {new_place.name}에 도착했다.*"
        else:
            return "*위치를 이동하기 전, 현 위치에서의 탐색을 완료하자.*\n" + frmat.content_formatter(self)


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

        if len(self.place.free_search_deck) == 0:
            return "*이 곳에선 탐색을 진행할 수 없다. 다른곳으로 이동 후 시도하자.*"

        # choose a new state
        if self.state == None:
            new_event = random.choice(self.place.free_search_deck)
            self.state = new_event

        return_string = frmat.content_formatter(self)

        if len(self.state.choices) == 0:
            self.state = None

        return return_string

    def possible_result(self, result, stat_rolls):

        if result.barriers[0] < 0 and self.money > (-1*int(result.barriers[0])):
            return False
        elif result.barriers[0] > 0 and self.money <= (int(result.barriers[0])):
            return False

        if result.barriers[1] != -1 and not result.barriers[1] in self.bag:
            return False

        # gotta work on roll possible result and success
        if result.barriers[2] == "TRS":
            if result.barriers[3] != stat_rolls[0]:
                return False

        elif result.barriers[2] == "ETH":
            if result.barriers[3] != stat_rolls[1]:
                return False

        elif result.barriers[2] == "AQU":
            if result.barriers[3] != stat_rolls[2]:
                return False

        elif result.barriers[2] == "KIN":
            if result.barriers[3] != stat_rolls[3]:
                return False
        return True


    def choice(self, msg):

        if self.state == None:
            return

        ret_msg = ""

        try:
            print("1")
            choice_index = self.state.choices.index(msg)
            chosen_result = None
            chosen_result_num = -1
            pool = self.state.results[choice_index]
            
            if len(pool) == 1:
                print("2 " + str(len(pool)))
                chosen_result = pool[0]
                chosen_result_num = 0
            else:
                print("3")
                stat_rolls = self.roll_stats()
                possible_results = []
                possible_num = []
                for r in range(len(pool)):
                    if self.possible_result(pool[r], stat_rolls):
                        possible_results.append(pool[r])
                        possible_num.append(r)

                print("4")
                if len(possible_results) == 1:
                    print("5")
                    chosen_result = possible_results[0]
                    chosen_result_num = possible_num[0]

                elif len(possible_results) == 0:
                    print(f"encountered error in choice for {self.name}\nhere are results in pool:")
                    for b in pool:
                        print(str(r))
                    print(f"\non state {self.state.ID} and possible results pool is 0 somehow\n")
                    print("here is character info\n" + str(self) + "\n")

                    chosen_result = None
                    chosen_result_num = -1

                elif possible_results[0].percent != 100:
                    print("6")
                    rs = State.choose_result(possible_results)
                    chosen_result = rs[0]
                    chosen_result_num = rs[1]

                else:
                    print(f"encountered error in choice for {self.name}\nhere are results in pool:")
                    for b in pool:
                        print(str(r))
                    print(f"\non state {self.state.ID} and possible results pool is {len(possible_results)}\n")
                    for a in possible_results:
                        print(str(a))
                    print("here is character info\n" + str(self) + "\n")

                    chosen_result = possible_results[0]
                    chosen_result_num = possible_num[0]

            if chosen_result == None:
                self.state = None
                return "*에러가 발생했다. 이지비에게 보고하고... 일단은 현 탐색상황을 리셋시켰으니 다른곳으로 가보세요*"
            else:
                self.search_count += chosen_result.search_count
                self.state = self.state.nxt[choice_index][chosen_result_num]

                print("in here")
                print(str(chosen_result))
                print(chosen_result.content)
                # also apply other stuff here
                return chosen_result.content

        except ValueError as e:
            return_string = "*입력한 선택지는 목록에 없다.*\n"
            return_string += frmat.choice_formatter(self.state.choices)
            return return_string




