#!/usr/bin/python3

import random

def main():
    grid = init()
    while True:
        print(grid)
        user_input = input("Enter choice (x, y), n for new game, or q to quit\n>> ")
        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'n':
            grid = init()
            continue
        elif "," not in user_input: 
            continue

        y, x = user_input.split(",")
        x, y = int(x) - 1, int(y) - 1

        if (grid.grid[x][y].revealed):
            continue
        elif (grid.grid[x][y].mine):
            for row in grid.grid:
                for col in row:
                    col.revealed = True
            print(grid)
            user_input = input("GAME OVER!\nn for new game or q to quit.\n>> ")
            if user_input.lower() == 'q':
                break
            elif user_input.lower() == 'n':
                grid = init()
                continue

        grid.reveal(x, y)


def init():
    grid = Grid()
    grid.place_mines()
    return grid


class Grid(object):
    def __init__(self, x=10, y=10):
        self.grid = [[Node(x, y) for y in range(y)] for x in range(x)]
        self.max_x = x
        self.max_y = y

    def place_mines(self, mine_count=10):
        self.mine_count = mine_count
        while (mine_count):
            x = random.randint(0, self.max_x-1)
            y = random.randint(0, self.max_y-1)
            if self.add_mine(x, y):
                mine_count -= 1

    def add_mine(self, x, y):
        if self.grid[x][y].mine:
            return False
        self.grid[x][y].mine = True
        self.increment_mine_counts(x, y)
        return True

    def increment_mine_counts(self, x, y):
        for node in self.get_adjacent_nodes(x, y):
            node.mine_count += 1

    def reveal(self, x, y):
        self.grid[x][y].revealed = True
        if self.grid[x][y].mine_count:
            return

        ## if empty node, bfs to to reveal all connected numberless nodes and
        ## one row of numbered nodes
        seen_nodes = set([])
        nodes_to_search = set([self.grid[x][y]])
        while nodes_to_search:
            current_node = nodes_to_search.pop()
            adjacent_nodes = self.get_adjacent_nodes(current_node.x, current_node.y)
            for n in adjacent_nodes:
                if n.mine_count:
                    n.revealed = True
            adjacent_nodes = [n for n in adjacent_nodes if n not in seen_nodes and not n.revealed and not n.mine_count and not n.mine]
            for n in adjacent_nodes: nodes_to_search.add(n)
            current_node.revealed = True
            seen_nodes.add(current_node)

    def get_adjacent_nodes(self, x, y):
        adjacent_nodes = []
        for i in range(max(0, x-1), min(self.max_x, x+2)):
            for j in range(max(0, y-1), min(self.max_y, y+2)):
                if i == x and j == y: continue
                adjacent_nodes.append(self.grid[i][j])
        return adjacent_nodes

    def __repr__(self):
        outstring = ""
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                if x == 0: 
                    outstring += str(y)
                elif y == 0: 
                    outstring += str(x)
                else:
                    outstring += str(self.grid[x-1][y-1])
                outstring += " "
            outstring += "\n"
        return outstring


class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mine = False
        self.revealed = False
        self.flagged = False
        self.mine_count = 0

    def __repr__(self):
        if self.flagged:
            return "<"
        elif not self.revealed:
            return "."
        elif self.mine:
            return "*"
        elif self.mine_count:
            return str(self.mine_count)
        return "_"


if __name__ == '__main__':
    main()
