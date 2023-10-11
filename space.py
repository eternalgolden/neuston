'''
    space.py

    fightable/interactable space
    
'''
from cell import *
from character import *

class Space:
    matrix = []
    character_list = []
    character_cell = []
    entity_list = []

    def __init__(self, l, w):
        for row in range(l):
            self.matrix.append([])
            for col in range(w):
                a = Cell(False, row, col)
                self.matrix[row].append(a)

        self.character_list = []
        self.character_cell = []
        self.entity_list = []

    def __str__(self):
        return_string = "Space --\ncharacter list: " + str([ch.name for ch in self.character_list]) \
                        + "\ncharacter_cell : " + str([str([cell.row, cell.col]) for cell in self.character_cell]) + "\n"
        # printing matrix
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                # place character if not empty
                if len(self.character_cell) != 0 and self.matrix[row][col] in self.character_cell:
                    for i in range(len(self.character_cell)):
                        if self.character_cell[i] == self.matrix[row][col]:
                            return_string += f"[{self.character_list[i].name[:1]}]"
                else:
                    return_string += str(self.matrix[row][col])
            return_string += "\n"

        return return_string


