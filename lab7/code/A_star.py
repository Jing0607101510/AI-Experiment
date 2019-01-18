#启发式函数的选择：
#1.不再目标位置的个数，不包括空格
#2.街区距离，不包括空格
#3.欧式距离，不包括空格


import copy 
import heapq
import time
import psutil
import os
import math

class Node():
    def __init__(self, state, h, zero_pos = (0, 0), g=0, shift_num=0, move=-1):
        self.state = state
        self.costH = h
        self.costG = g
        self.costF = self.costH + self.costG
        self.parent = None
        #self.zero_pos = self.find_zero(self.state)
        self.zero_pos = zero_pos
        self.shift_num = shift_num#当前状态是从前一个状态移动了哪一个数
        self.move = move#上一个状态到当前状态向那个方向移动了0
    
    def find_zero(self):
        for i in range(len(self.state)):
            if 0 in self.state[i]:
                self.zero_pos = [i, self.state[i].index(0)]
                return
    
    def __lt__(self, other):
        return self.costF < other.costF
    
    def __eq__(self, other):
        if self.state == other.state:
            return True
        else:
            return False

class Search():
    def __init__(self):
        puzzle1 = [ [2,   6,   3,   4],
                    [1,   0,   7,   8],
                    [5,  10,  15,  11],
                    [9,  13,  14,  12]]
        puzzle2 = [ [5,   1,   3,   4],
                    [9,   6,   7,   2],
                    [10,  14,   0,   8],
                    [13,  15,  11,  12]]
        puzzle3 = [[2,   3,   7,   4],
                    [6,  10,   8,  15],
                    [1,  13,  14,   0],
                    [5,   9,  12,  11]]
        puzzle4 = [  [2,   5,   4,   8],
                    [1,  10,   6,   3],
                    [13,   0,   7,  12],
                    [14,   9,  11,  15]]
        self.target = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        self.puzzles = [puzzle1, puzzle2, puzzle3, puzzle4]

        self.moves = [[0,1], [1, 0], [-1, 0], [0,-1]]
        
        #用于IDA*
        self.path = []
        self.directions = []

    
    def solvable(self, puzzle):
        ni = 0
        puzzle_line = []
        for p in puzzle:
            hp = hpy()
            puzzle_line.extend(p)
        for i in range(len(puzzle_line)):
            if puzzle_line[i] == 0:
                continue
            for j in range(i+1, len(puzzle_line)):
                if puzzle_line[j] != 0 and puzzle_line[j] < puzzle_line[i]:
                    ni += 1
        start_puzzle_zero_pos = puzzle_line.index(0) // 4
        target_puzzle_zero_pos = 15 // 4
        dif = abs(target_puzzle_zero_pos - start_puzzle_zero_pos)
        if dif % 2 == 1 and ni % 2 == 1:
            return True
        elif dif % 2 == 0 and ni % 2 == 0:
            return True
        else:
            return False

    def check_target(self, node):
        if node.state == self.target:
            return True
        else:
            return False
    


    def calc_h(self, puzzle):
        h = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle[0])):
                if puzzle[i][j] != 0:
                    target_row = (puzzle[i][j] + 15) // 4 % 4
                    target_col = (puzzle[i][j] + 15) % 4
                    h += abs(i - target_row) + abs(j - target_col)
        return h
    
    def calc_h_greatest(self, puzzle):
        h = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle[0])):
                if puzzle[i][j] != 0:
                    target_row = (puzzle[i][j] + 15) // 4 % 4
                    target_col = (puzzle[i][j] + 15) % 4
                    h += max(abs(i - target_row), abs(j - target_col))
        return h
    
    def calc_h_not_inside(self, puzzle):
        h = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle[0])):
                if puzzle[i][j] != 0 and puzzle[i][j] != i*4+j+1:
                    h += 1                    
        return h
    
    def calc_h_euclidean(self, puzzle):
        h = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle[0])):
                if puzzle[i][j] != 0:
                    target_row = (puzzle[i][j] + 15) // 4 % 4
                    target_col = (puzzle[i][j] + 15) % 4
                    h += math.sqrt((i - target_row)**2 + (j - target_col)**2)
        return h
    
    def check_legel(self, pos):
        if pos[0] < 0 or pos[0] > 3 or pos[1] < 0 or pos[1] > 3:
            return False
        else:
            return True

    
    def A_star(self, puzzle):
        close = [] #只保存puzzle的状态不保存对象
        open = [] #保存的是对象
        start_node = Node(puzzle, self.calc_h(puzzle))
        start_node.find_zero()
        open.append(start_node)

        while len(open):
            current_node = heapq.heappop(open)
            #print("current_node", current_node.state)
            if self.check_target(current_node): 
                return current_node
            else:
                close.append(current_node.state)
                for move in self.moves:
                    #新的零的位置
                    zero_pos = [move[0]+current_node.zero_pos[0], move[1]+current_node.zero_pos[1]]
                    if self.check_legel(zero_pos):
                        #保存的新的puzzle状态
                        state = copy.deepcopy(current_node.state)
                        shift_num = state[zero_pos[0]][zero_pos[1]]
                        state[current_node.zero_pos[0]][current_node.zero_pos[1]] = shift_num
                        state[zero_pos[0]][zero_pos[1]] = 0

                        if state in close:
                            continue
                        #h值
                        h = self.calc_h(state)
                        next_node = Node(state, h, zero_pos, current_node.costG+1, shift_num, self.moves.index(move))
                        #1.是否在open中，2.是否在close中 
                        if next_node in open:
                            index = open.index(next_node)
                            if open[index].costF > next_node.costF:
                                open[index].costG = next_node.costG
                                open[index].costH = next_node.costH
                                open[index].costF = next_node.costF
                                open[index].parent = current_node
                                open[index].shift_num = next_node.shift_num
                                open[index].move = next_node.move
                        else:
                            next_node.parent = current_node
                            heapq.heappush(open, next_node)
        return None
        


    def run_A_star(self):
        for i in range(4):
            start = time.time()
            last = self.A_star(self.puzzles[i])
            end = time.time()
            if last is None:
                print("can't solvable!")
            else:
                step = []
                move = []
                while last is not None:
                    step.append(last.shift_num)
                    move.append(last.move)
                    last = last.parent
                step.pop()
                move.pop()
                step.reverse()
                move.reverse()
                print(step)
                print(move)
                print("time used:", (end-start), "s")
                print("memory used:", psutil.Process(os.getpid()).memory_info().rss)
                print()
    



if __name__ == "__main__":
    search = Search()
    search.run_A_star()

        

        

