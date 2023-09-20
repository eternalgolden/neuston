'''
    state.py

    contains the class state with
    different functions that pertain to
    the states


'''

import random

class Result:
    content = ""
    percent = 100
    barriers = []   # money, item, 판정, success
    effects = []    # money, item
    search_count = 0

    def __init__(self, content, count):
        self.content = ""
        self.percent = 100
                       #    money is <0 for less and >0 for greater
                       #   money   item    roll    success
        self.barriers = [    0,      -1,     -1,     -1]
                       #   money   item
        self.effects = [     0,      -1]
        self.search_count = count

        # parsing starts ---------------------

        current = ""

            # load content
        if content.find("|") != -1:
            current = content.split("| ")
            self.content = current[1]
        else:
            self.content = content
            return

        current = current[0]

            # load percent
        if current.find("%") != -1:
            current = current.split("%")
            self.percent = int(current[0])
            current = current[1]

            # load barriers / effects
        if current.find("(") != -1:
            current = current.split("(")
            for c in current:
                # barriers
                if c.find("아이템소지") != -1:
                    name = c.split(": ")[1]
                    self.barriers[1] = name[:len(name)-1]
                elif c.find("소지금 >") != -1:
                    amount = c.split(">")[1]
                    self.barriers[0] = int(amount[:len(amount)-1])
                elif c.find("소지금 <") != -1:
                    amount = c.split("<")[1]
                    self.barriers[0] = int(amount[:len(amount)-1])*(-1)

                # effects
                elif c.find("아이템소비") != -1 or c.find("아이템:") != -1:
                    name = c.split(": ")[1]
                    self.effects[1] = name[:len(name)-1]
                elif c.find("소지금") != -1: # 소지금 +-
                    amount = c.split(" ")[1]
                    self.effects[0] = int(amount[:len(amount)-1])

                # success/fail
                elif c.find("TRS") != -1 or c.find("ETH") != -1 or c.find("AQU") != -1 or c.find("KIN") != -1:
                    check = c.split(" ")
                    self.barriers[2] = check[0]
                    if check[1].find("성공") != -1:
                        self.barriers[3] = True
                    else:
                        self.barriers[3] = False






    def __str__(self):
        return "Result: \ncontent-> " + self.content + "\npercent-> " + str(self.percent) + "%\nbarriers-> " + str(self.barriers) + "\neffects-> " + str(self.effects) + "\nsearch_count : " + str(self.search_count)


class State:


    content = ""
    choices = []
    results = []
    nxt = []
    ID = 0

    # static variable
    GLOBAL_ID = 0

    
    def __init__(self, content):
        self.content = content
        self.ID = State.GLOBAL_ID

        self.choices = []
        self.results = []
        self.nxt = []

        State.GLOBAL_ID += 1

    # for making a new set of events
    def reset_global_id():
        State.Global_ID = 0

    # the text that gets saved has the percents in the front
    # and may have a > included for percent things
    def add_choice(self, choice):
        self.choices.append(choice)

    # we can't add a legit n yet (just a number) bc we have to go through all the events first
    def add_result(self, choice_id, result, n):
        if not self.results or len(self.results) <= choice_id: # choice has something, results is empty
            self.results.append([result])
            self.nxt.append([n])
        elif self.results[choice_id]: # results is not empty
            self.results[choice_id].append(result)
            self.nxt[choice_id].append(n)

    # calculates which result & returns the next state included too
    # returns one of the omi choices (with a percentage)
    # gets potential results from pool_result -- assumes that all results have % in them
    def choose_result(omikuji):

        draw = random.randint(0, 100)
        omikuji_cuts = []
        counter = 0

        for m in omikuji:
            counter += m.percent
            omikuji_cuts.append(counter)


        for o in range(len(omikuji_cuts)):
            if draw <= omikuji_cuts[o]:
                return [omikuji[o], o]

        return [omikuji[len(omikuji)-1], len(omikuji)-1]

    def make_copy(self):
        global_id = State.GLOBAL_ID
        new = State(self.content)
        State.GLOBAL_ID = global_id
        new.ID = self.ID
        new.choices = self.choices.copy()
        
        new_result = []
        new_nxt = []
        for i in range(len(self.results)):
            new_result.append([])
            new_nxt.append([])
            for j in range(len(self.results[i])):
                new_result[i].append(self.results[i][j])
                new_nxt[i].append(self.nxt[i][j])
        new.results = new_result
        new.nxt = new_nxt
        return new

    def change_nxt(self, choice_id, result_id, change_into):
        self.nxt[choice_id][result_id] = change_into


    def __eq__(self, other):
        if other == None or type(other) != type(self) or self.ID != other.ID: 
            return False
        return self.content == other.content and len(self.results) == len(other.results) and len(self.nxt) == len(other.nxt)
        

    def __str__(self):
        comp_string = f"state {self.ID}----------\n"
        comp_string = comp_string + self.content +"\n"


        for c in range(len(self.choices)):
            comp_string += f"choice {c} : " + self.choices[c] + "\n"

        comp_string += "\n"

        for r in range(len(self.results)):
            comp_string += "result " + str(r) + ":\n"
            for j in range(len(self.results[r])):
                comp_string += "\"" + self.results[r][j].content + "\" -> "
                if(type(self.nxt[r][j]) == type(self)):
                    comp_string += "[state ID : " + str(self.nxt[r][j].ID) +"]"
                else:
                    comp_string += str(self.nxt[r][j])
                comp_string += "\n"

            comp_string += "\n"

        return comp_string













