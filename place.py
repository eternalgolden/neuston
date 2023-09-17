'''
    place.py

    contains the class place

'''

import free_search_loader as free_search

class Place:

    acr = ""
    name = ""
    desc = ""
    upon_arrival = ""
    free_search_deck = []
    kor_acr = ""


    def __init__(self, acr, name, desc, arrival):
        self.acr = acr
        self.name = name
        self.desc = desc
        self.upon_arrival = arrival
        self.free_search_deck = []
        self.kor_acr = ""

        if acr == "dawn":
            self.free_search_deck = free_search.init_dawn()

    def __str__(self):
        return f"{self.name} -- acr: {self.acr}\ndesc: {self.desc}\nupon_arrival: {self.upon_arrival}\ndeck size: " + str(len(self.free_search_deck)) +"\n"

        
