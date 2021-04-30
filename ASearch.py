"""
Johnlouis Dahhan
CS 4613
Project 1: 15-Puzzle A* Search
Replace global variables with desired values and run code
"""
import heapq
from copy import deepcopy


def readfile(input_filepath):
    """
    Reads input file and returns initial and goal states
    :param input_filepath: filepath of input file
    :return initial, goal: nested lists representing initial and goal states
    """
    infile = open(input_filepath, 'r')
    initial = []
    goal = []
    for i in range(2):  # need to read 2 states
        for j in range(4):  # 4 lines per state
            currlist = infile.readline().strip().split(" ")
            for ind in range(len(currlist)):  # convert all state values to ints
                currlist[ind] = int(currlist[ind])
            if i % 2 == 0:
                initial.append(currlist)
            else:
                goal.append(currlist)
        if i == 0:
            infile.readline()
    infile.close()
    return initial, goal


def writefile(initial, result, output_filepath):
    """
    writes output file given results of A* search
    :param initial: initial state in nested list form
    :param result: goal node and num of generated nodes returned from A* search
    :param output_filepath: filepath of file to write to
    """
    goal = result[0]
    n = result[1]
    outfile = open(output_filepath, 'w')
    for i in range(2):
        for j in range(4):
            if i == 0:
                outfile.write(" ".join(str(x) for x in initial[j]) + '\n')
            else:
                outfile.write(" ".join(str(x) for x in goal.state[j]) + '\n')
        outfile.write("\n")
    outfile.write(str(goal.gx) + '\n' + str(n) + '\n' + " ".join(str(x) for x in goal.path) + '\n' + " ".join(
        str(x) for x in goal.fxlist))
    outfile.close()


INFILE_PATH = "Sample_Input.txt"  # input filepath
OUTFILE_PATH = "Sample_Output.txt"  # output filepath
INITIAL, GOAL = readfile(INFILE_PATH)  # initial and goal nested lists, as read from input file
MOVES = {1: (0, -1), 2: (-1, -1), 3: (-1, 0), 4: (-1, 1), 5: (0, 1), 6: (1, 1), 7: (1, 0),
         8: (1, -1)}  # dict representing possible moves
SEEN = []


def findnum(state, i):
    """
    finds the location of a number in a nested list
    :param state: current state in nested list form
    :param i: number to find
    :return y, x: coordinates of i in state
    """
    for y in range(len(state)):
        for x in range(len(state[y])):
            if state[y][x] == i:
                return y, x


def calculate_h(state):
    """
    calculates sum of chessboard distances for all numbers in some state
    :param state: state represented as nested list
    :return h: sum of chessboard distances
    """
    h = 0
    if state == GOAL:
        return h
    for i in range(16):
        goalcoord = findnum(GOAL, i)
        statecoord = findnum(state, i)
        h += max((abs(goalcoord[0] - statecoord[0]), abs(goalcoord[1] - statecoord[1])))
    return h


class Node:
    # class definition for one node in problem
    def __init__(self, state, gx, path, fxlist):
        """
        Node constructor
        :param state: nested list representing current state of node
        :param gx: cost of reaching current node from root, equivalent to depth in this problem
        :param path: list of moves taken from root to this node
        :param fxlist: list of fx values of nodes on path from root to this node
        """
        self.hx = calculate_h(state)
        self.gx = gx
        self.state = state
        self.path = path
        self.fx = self.gx + self.hx
        self.fxlist = fxlist
        self.fxlist.append(self.fx)

    # overloading comparison operators for use with heapq library
    def __lt__(self, other):
        return self.fx < other.fx

    def __le__(self, other):
        return self.fx <= other.fx

    def __eq__(self, other):
        return self.fx == other.fx

    def __gt__(self, other):
        return self.fx > other.fx

    def __ge__(self, other):
        return self.fx >= other.fx

    def expand(self):
        """
        :return children: list of all nodes that generated from this node
        """
        children = []
        indexy, indexx = findnum(self.state, 0)  # find location of blank space
        currgx = self.gx + 1
        for key in MOVES:
            currstate = deepcopy(self.state)
            currpath = deepcopy(self.path)
            currpath.append(key)
            try:  # try every move if it is possible
                temp = currstate[indexy + MOVES[key][0]][indexx + MOVES[key][1]]
                currstate[indexy + MOVES[key][0]][indexx + MOVES[key][1]] = 0
                currstate[indexy][indexx] = temp
                children.append(Node(currstate, currgx, currpath, deepcopy(self.fxlist)))
            except IndexError:
                pass
        return children


def asearch(initial, goal):
    """
    Conducts graph-like A* search for this problem given an initial and goal state
    :param initial: initial state, nested list
    :param goal: goal state, nested list
    :return: shallowest generated goal node
    """
    seen = [initial]  # don't want to repeat states
    root = Node(initial, 0, [], [])  # create a node for initial state
    frontier = [root]
    while len(frontier) != 0:  # keep running as long as nodes can be generated
        currnode = heapq.heappop(frontier)  # pop node with lowest f(x) value
        if currnode.state == goal:
            return currnode, len(frontier) + len(seen)  # return goal node
        children = currnode.expand()
        for child in children:  # otherwise we expand best node and check its children
            if child.state not in seen:  # don't bother with repeat nodes
                seen.append(child.state)
                heapq.heappush(frontier, child)


def main():
    """
    conducts A* search using globally declared states read from input file, writes them to globally declared output filepath
    """
    writefile(INITIAL, asearch(INITIAL, GOAL), OUTFILE_PATH)


main()
