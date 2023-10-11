'''
    entity.py

    class for entities

'''

def distance_calc(matrix, current, target):
    pass


def chase(matrix, current, target):
    pass

def run(matrix, current, target):
    pass

method = {'chase': chase, 'run': run }

class Entity:
    
    name = ""
    ID = -1
    hostile = False # attacks if true
    attackable = False
    target = None


    def __init__(self, name, ID, hostile, attackable):
        self.name = name
        self.ID = ID
        self.hostile = hostile
        self.attackable = attackable
