
from state import *
import google_sheets as gs
from character import *
import free_search_loader as ld
import owner_loader as ol
from enum import *
from place import *

ol.get_owners()


'''
CONFIRMING THAT STATE 44 (SHOP) HAS REFERENCE TO ITSELF

dawn_events = ld.init_dawn()
for d in dawn_events:
    if d.ID == 44:
        print(str(d.nxt[0][1]))
'''

'''
RANGE CALC TESTING
data = []
for i in range(50):
    data.append(i)

gs.put("debug", (gs.range_calc("A1", 50, True)), data)
'''

'''

RESULT TESTING

results = gs.flatten(gs.get("탐색:새벽녘", "F5:F136"))

for r in results:
    if r != '-':
        res = Result(r)
        print(str(res))
'''

'''
#bag testing

a = Character("romeo")
pl = Place("a", "b", "c", "d")
a.place = pl
a.bag_index[0] = "B"
a.bag_index[1] = 3
a.add_bag("chipotle", 1, False)
print(str(a))
a.add_bag("chipotle", 1, False)
a.add_bag("chipotle", 2, False)
a.add_bag("yisang", 4, False)
a.add_bag("baked beans", 6, False)
a.add_bag("cat????", 1, True)
a.subtract_bag("cat????", 1)
print(str(a))

'''

#gs.put_single('Sheet2', 'C2', 'mlem')


'''

STATE TESTING

a = State("testing content1")
print(str(a))
a.add_choice("choice 1")
a.add_result(0, "result 1", 1)
a.add_choice("choice 2")
a.add_result(1, "20%> result 2", 2)
a.add_result(1, "20%> result 2-1", 3)
a.add_result(1, "20%> result 2-2", 4)
a.add_result(1, "20%> result 2-3", 5)
a.add_result(1, "20%> result 2-4", 6)

print(str(a))

for i in range(20):
    print(a.choose_result(1))
'''
