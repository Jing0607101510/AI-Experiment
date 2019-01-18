#from gui import Puzzle_15_Gui
import copy
import heapq

class Node():
    def __init__(self, puzzle_state, g, h, parent_index=-1):
        self.puzzle_state = puzzle_state
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent_index = parent_index
        
    def find_space_pos(self):
        for i in range(self.puzzle_state):
            for j in range(self.puzzle_state[0]):
                if self.puzzle_state[i][j] == 0:
                    self.space_pos = [i, j]


class Search():
    def __init__(self):
        puzzle1 = [[11, 3, 1, 7], [4, 6, 8, 2], [15, 9, 10, 13], [14, 12, 5, 0]]
        puzzle2 = [[14, 10, 6, 0], [4, 9, 1, 8], [2, 3, 5, 11], [12, 13, 7, 15]]
        puzzle3 = [[0, 5, 15, 14], [7, 9, 6, 13], [1, 2, 12, 10], [8, 11, 4, 3]]
        puzzle4 = [[6, 10, 3, 15], [14, 8, 7, 11], [5, 1, 0, 2], [13, 12, 9, 4]]
        self.target = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        self.puzzles = [puzzle1, puzzle2, puzzle3, puzzle4]
        self.init_dis()

        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        #self.puzzle_15_gui = Puzzle_15_Gui(self.puzzles)
        #self.puzzle_15_gui.main()

    #各个对应的数字在不同位置的曼哈顿距离
    def init_dis(self):
        self.dis = []
        for i in range(16):
            dis = []
            cur_r, cur_c = i / 4, i % 4
            for r in range(4):
                for c in range(4):
                    dis.append(abs(r-cur_r)+abs(cur_c-c))
            self.dis.append(dis)
    
    #1的位置在（0，0）0，2的位置在（0，1）1,0的位置在（3，3）15
    def calc_f(self, puzzle):
        cost = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle[0])):
                target_r = (puzzle[i][j] + 15) / 4
                target_c = (puzzle[i][j] + 15) % 4
                cost += abs(i - target_r) + abs(j - target_c)
        return cost

    def print_road(self):
        pass

    def save_road(self):
        pass

    def check_legel(self, pos, visited):
        if pos[0] < 0 or pos[0] >= 4 or pos[1] < 0 or pos[1] >= 4:
            return False
        elif pos in visited:
            return False
        else:
            return True
            
    def A_star(self, puzzle):
        visited = []
        queue = []

        h = self.calc_f(puzzle)
        node = Node(copy.deepcopy(puzzle), 0, h)
        node.find_space_pos()
        queue.append(node)
        
        while len(queue):
            node = heapq.heappop(queue)
            if node.puzzle_state == self.target:
                self.print_road()
                self.save_road()
                break
            for direction in self.direction:
                next_pos = list(map(lambda x:x[0]+x[1], zip(direction, node.space_pos)))
                next_state = copy.deepcopy(node.puzzle_state)
                next_state[node.space_pos[0]][node.space_pos[1]] = next_node[next_pos[0]][next_pos[1]]
                next_state[next_pos[0]][next_pos[1]] = 0
                if self.check_legel(next_pos, visited):
                    if 
                


    def IDA_star(self):
        pass


if __name__ == "__main__":
    search = Search()
        