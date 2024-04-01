import re
import time
import copy
import os
import random
board = [["  " for n in range(0, 300)] for item in range(0, 300)]


def print_board():
    print("\n"*100)
    for row in board:
        out = ""
        for col in row:
            out += col
        print(" "*400 + out)


class Cell:
    to_evolve = []
    all = []
    all_pos = []
    all_dead_neighbours = []

    def __init__(self, pos, neighbours=None, dead_neighbours=None):
        if dead_neighbours is None:
            dead_neighbours = []
        if neighbours is None:
            neighbours = []
        self.pos = pos
        self.neighbours = neighbours
        self.dead_neighbours = dead_neighbours
        Cell.all.append(self)
        Cell.all_pos.append(self.pos)

    @classmethod
    def calc_neighbours(cls):
        cls.all_dead_neighbours = []
        for item in cls.all:
            item.neighbours = []
            item.dead_neighbours = []
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if [item.pos[0] + y, item.pos[1] + x] in cls.all_pos and [item.pos[0] + y, item.pos[1] + x] != item.pos:
                        item.neighbours.append([item.pos[0] + y, item.pos[1] + x])
                    elif [item.pos[0] + y, item.pos[1] + x] != item.pos:
                        item.dead_neighbours.append([item.pos[0] + y, item.pos[1] + x])
                        cls.all_dead_neighbours.append([item.pos[0] + y, item.pos[1] + x])


    @classmethod
    def play(cls):
        cls.calc_neighbours()
        cls.create()
        cls.evolve()
        cls.calc_neighbours()
        cls.draw()

    @classmethod
    def create(cls):
        cls.to_evolve = []
        seen = {}
        seen_list = []
        for item in cls.all_dead_neighbours:
            if item not in seen_list:
                seen_list.append(item)
            seen[str(item)] = 0
        for item in cls.all_dead_neighbours:
            seen[str(item)] = seen[str(item)] + 1
        for item in seen_list:
            if seen.get(str(item)) == 3:
                cls.to_evolve.append(item)




    @classmethod
    def evolve(cls):
        for items in copy.copy(cls.all):
            if len(items.neighbours) == 2 or len(items.neighbours) == 3:
                pass
            elif len(items.neighbours) < 2:
                cls.all.remove(items)
                cls.all_pos.remove(items.pos)
                del items
            elif len(items.neighbours) > 3:
                cls.all.remove(items)
                cls.all_pos.remove(items.pos)
                del items
        for item in cls.to_evolve:
            Cell(item)
        cls.to_evolve = []

    @classmethod
    def draw(cls):
        global board
        board = [["` " for n in range(0, 300)] for item in range(0, 300)]
        for item in cls.all_pos:
            board[item[0]][item[1]] = "# "

    @classmethod
    def debug(cls):
        print(cls.all_pos)
        print(f"all dead neighbours{cls.all_dead_neighbours}")
        for item in cls.all:
            print(f"pos {item.pos}             neighbours{item.neighbours}      dead_neighbours{item.dead_neighbours}")


for e in range(0, 500):
    Cell([(random.randint(120, 180)), (random.randint(120, 180))])
Cell.draw()

while True:
    Cell.play()
    os.system("clear")
    print_board()
    time.sleep(0.05)

