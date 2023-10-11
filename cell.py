'''
    cell.py

    used for fights/dungeons
'''

class Cell:
    
    isWall = False
    row = 0
    col = 0

    def __init__(self, wall, row, col):
        self.isWall = wall
        self.row = row
        self.col = col

    def __str__(self):
        if self.isWall:
            return "[ w ]"
        else:
            return "[   ]"
