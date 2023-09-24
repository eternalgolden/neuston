'''
    free_search_loader.py

    gets the events off google sheets and
    loads them into the designated arrays

'''

import google_sheets as gs
from state import *

# adds all the states to the right array
# @param -- content, choices, results (in list form)
def add_states(contents, choices, results, nxt, count):
    master = []

    curr_content = -1
    curr_choice = 0

    for i in range(len(contents)):

        # if content isnt empty
        if contents[i][0] != '-':
            curr_content += 1
            a = State(contents[i][0])
            curr_choice = 0
            # if choice not empty
            if choices[i][0] != '-':
                a.add_choice(choices[i][0])
                if nxt[i][0] != '-':
                    nnxt = nxt[i][0]
                else:
                    nnxt = None

                a.add_result(curr_choice, Result(results[i][0], int(count[i][0])), nnxt)

            master.append(a)
        # if content is empty
        else:
            # if choice not empty
            if choices[i][0] != '-':
                curr_choice += 1
                master[curr_content].add_choice(choices[i][0])

                if nxt[i][0] != '-':
                    nnxt = nxt[i][0]
                else:
                    nnxt = None

                master[curr_content].add_result(curr_choice, Result(results[i][0], int(count[i][0])), nnxt)
            # if choice is empty
            else:
                if nxt[i][0] != '-':
                    nnxt = nxt[i][0]
                else:
                    nnxt = None

                master[curr_content].add_result(curr_choice, Result(results[i][0], int(count[i][0])), nnxt)

    return master

#   edits any entry with a next that's not -1
#   and takes them out of the array
#   google sheet number - 1 ==> master array #
#   @param mater the mater array with all the states
#   @return the array with only the "non-next" states
def manage_next(master):
    bloom_filter = []
    new_master = []

    for e in master:
        nxt = e.nxt;
        for i in range(len(nxt)):
            for j in range(len(nxt[i])):
                if nxt[i][j] != None and (int(nxt[i][j])) != e.ID:
                    bloom_filter.append(int(nxt[i][j]))
                    e.change_nxt(i,j,master[ int(nxt[i][j])]) 
                elif nxt[i][j] != None:
                    e.change_nxt(i,j,e)

    for i in range(len(master)):

        try:
            if bloom_filter.index(i):
                pass
        except ValueError as e:
            new_master.append(master[i])

    return new_master

# make copies of this function later if we have more places
def init_dawn():    

    dawn_sheet = "탐색:새벽녘"

    #              contents    choices    results    next   search_count
    dawn_range = ['D5:D137', 'E5:E137', 'F5:F137', 'G5:G137', 'H5:H137' ]
    
    dawn_content =  gs.get(dawn_sheet, dawn_range[0])
    dawn_choices =  gs.get(dawn_sheet, dawn_range[1])
    dawn_results =  gs.get(dawn_sheet, dawn_range[2])
    dawn_nxt =      gs.get(dawn_sheet, dawn_range[3])
    dawn_count =    gs.get(dawn_sheet, dawn_range[4])

    dawn_events = []

    init_dawn_events = add_states(dawn_content, dawn_choices, dawn_results, dawn_nxt, dawn_count)

    dawn_events = manage_next(init_dawn_events)

    return dawn_events

