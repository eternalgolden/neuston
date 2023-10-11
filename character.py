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
    stats = {}
    # name this different things later for each search event
    already_seen = []
    hp = {}
    stamina = 0
    cost = 0



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
        self.stamina = 0
        self.cost = 0
                    #TRS ETH AQU KIN
        self.stats = {'TRS': 0, 'ETH': 0, 'AQU': 0, 'KIN': 0}
        self.hp = {'head': 0, 'body': 0, 'arm': 0, 'leg': 0, 'san':0 }

        self.already_seen = []


    def head_hp(self):
        return self.stats['TRS']
    def body_hp(self):
        return self.stats['TRS'] + 2
    def arm_hp(self):
        return int(self.stats['TRS'] * 1.6)
    def leg_hp(self):
        return int(self.stats['TRS'] * 1.6)
    def san(self):
        return self.stats['TRS'] * 5
    def full_hp(self):
        return self.head_hp() + self.body_hp() + self.arm_hp() + self.leg_hp()

    def add_bag(self, item, amount, update):
        amount = int(amount)

        if not item in self.bag:
            self.bag[item] = []
        for i in range(int(amount/99)):
            self.bag[item].insert(0, 99) 

        if amount%99 != 0:
            if len(self.bag[item]) > 0:
                self.bag[item][len(self.bag[item])-1] += amount%99
            else:
                self.bag[item].append(amount%99)

            if self.bag[item][len(self.bag[item])-1] > 99:
                self.bag[item].insert(0, 99)
                self.bag[item][len(self.bag[item])-1] -= 99

        if update:
            self.put_bag()

    def subtract_bag(self, item, amount):
        amount = int(amount)

        if item in self.bag:
            for i in range(int(amount/99)):
                if len(self.bag[item]) != 0:
                    self.bag[item].pop(0)

            last_ind = len(self.bag[item])-1
            self.bag[item][last_ind] -= amount%99
            #print(item, last_ind, self.bag[item][last_ind], len(self.bag[item]))
            if self.bag[item][last_ind] <= 0 and len(self.bag[item]) > 1:
                self.bag[item][last_ind-1] += self.bag[item][last_ind]
                self.bag[item].pop()
            elif self.bag[item][last_ind] <= 0:
                del self.bag[item]
            self.put_bag()


    def add_money(self, m):
        ret_string = ""
        self.money += m

        if m > 0:
            ret_string = f"*{self.name}의 소지금에 {m}C가 추가됐다.*"
        else:
            if self.money < 0:
                self.money = 0
            ret_string = f"*{self.name}의 소지금에 {m}C가 추가됐다.*"


        gs.put(Sheet.CHARACTER.value, 'C' + str(self.bag_index[1]-1), [self.money])
        return ret_string

    def print_bag(self):
        compiled_string = ""

        for key in self.bag.keys():
            compiled_string += f"{key}({self.bag[key]}), "
        return compiled_string[:len(compiled_string)-2]

    def put_bag(self):
        top = list(self.bag.keys())
        bottom = []
        for k in top:
            bottom.append(sum(self.bag[k]))
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

    def search(self):

        if len(self.place.free_search_deck) == 0:
            return "*이 곳에선 탐색을 진행할 수 없다. 다른곳으로 이동 후 시도하자.*"

        # choose a new state
        if self.state == None:
            new_event = random.choice(self.place.free_search_deck)
            while new_event.ID in self.already_seen:
                new_event = random.choice(self.place.free_search_deck)
            self.state = new_event
            self.already_seen.append(new_event.ID)


        return_string = frmat.content_formatter(self)

        if len(self.state.choices) == 0:
            self.state = None

        return return_string

    def search_plus(self, others, search_count):

        if len(self.place.free_search_deck) == 0:
            return "*이 곳에선 탐색을 진행할 수 없다. 다른곳으로 이동 후 시도하자.*"

        # choose a new state
        if self.state == None:
            new_event = random.choice(self.place.free_search_deck)
            while new_event.ID in self.already_seen:
                new_event = random.choice(self.place.free_search_deck)
            self.state = new_event
            self.already_seen.append(new_event.ID)


        return_string = frmat.content_formatter_plus(self, others, search_count)

        if len(self.state.choices) == 0:
            self.state = None

        return return_string

    def possible_result(self, result, roll_20):

        # [ money, roll, min success, filter, success, (items/amount) x n ]
        # money calculation
        if result.barriers[0] < 0 and self.money > (-1*int(result.barriers[0])):
            return False
        elif result.barriers[0] > 0 and self.money <= (int(result.barriers[0])):
            return False

        # stat calculation
        self_stat = 0
        if result.barriers[1] != -1:
            # get self stat by TRS, ETH, AQU OR KIN
            self_stat = self.stats[result.barriers[1]]
            if self_stat < int(result.barriers[2]):
                #               result filter       roll 20     self stat filter
                re_calc = int(result.barriers[3]) + roll_20 + int(self_stat/5)
                if (re_calc >= int(result.barriers[2])) != result.barriers[4]:
                    return False

        for i in range(5, len(result.barriers)-1, 2):
            if not result.barriers[i] in self.bag or self.bag[result.barriers[i]] < int(result.barriers[i+1]):
                return False

        return True


    def choice(self, msg):

        if self.state == None:
            return

        ret_msg = ""
        roll_20 = random.randint(1,20)

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
                possible_results = []
                possible_num = []
                for r in range(len(pool)):
                    if self.possible_result(pool[r], roll_20):
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
                return [None, "*에러가 발생했다. 이지비에게 보고하고... 일단은 현 탐색상황을 리셋시켰으니 탐색 한번더~*"]
            else:
                # apply search count, go to next
                self.search_count += chosen_result.search_count
                self.state = self.state.nxt[choice_index][chosen_result_num]
                # add/sub money
                self.add_money(int(chosen_result.effects[0]))
                # add/sub items
                for i in range(1, len(chosen_result.effects)-1, 2):
                    if chosen_result.effects[i] in chosen_result.barriers:
                        self.subtract_bag(chosen_result.effects[i], chosen_result.effects[i+1])
                    else:
                        self.add_bag(chosen_result.effects[i], chosen_result.effects[i+1], True)

                ret = chosen_result.content

                if chosen_result.barriers[1] != -1:
                    bar =       chosen_result.barriers[1]
                    min_suc =   int(chosen_result.barriers[2])
                    filt =      int(chosen_result.barriers[3])
                    succ =      chosen_result.barriers[4]

                    ret = frmat.roll_formatter(bar, self.stats[bar], filt, int(self.stats[bar]/5), roll_20, min_suc, succ) + ret

                # debug
                print(str(chosen_result))

                return [chosen_result, ret]

        except ValueError as e:
            return_string = f"*'{msg}'는 목록에 없다.*\n"
            return_string += frmat.choice_formatter(self.state.choices)
            return [None, return_string]




