import sys
import math
import random
import numpy
import copy

BLACK = 1
NULL = 0
WHITE = -1

CHESS_SIZE = 8


AI = 1
HUMAN = -1
MAX = 255

position_value = [
    [10, -9, 8, 4, 4, 8, -9, 10],
    [-9, -9, -4, -3, -3, -4, -9, -9],
    [8, -4, 8, 2, 2, 8, -4, 8],
    [4, 3, 2, 1, 1, 2, 3, 4],
    [4, 3, 2, 1, 1, 2, 3, 4],
    [8, -4, 8, 2, 2, 8, -4, 8],
    [-9, -9, -4, -3, -3, -4, -9, -9],
    [10, -9, 8, 4, 4, 8, -9, 10],
]

class GA():
    def __init__(self):
        self.iternum = 5
        self.population_size = 5
        self.chrom_length = 5
        self.cross_rate = 0.6
        self.mutation_rate = 0.08
        self.whiteblackChess = WhiteBlack()
        self.init_population()
        
    
    def init_population(self):
        self.population = [[0] * self.chrom_length for i in range(self.population_size)]         
        for i in range(self.population_size):
            for j in range(self.chrom_length):
                self.population[i][j] = random.randint(0, 255)
            print(self.population[i])
    
    def iteration(self):
        for i in range(self.iternum):
            pass
            #计算各个染色体的适应度
            self.fitness_degree = self.calc_fitness()
            #选择操作#这个population是n-1大小，还需要加上best_one
            self.population, self.best_one = self.select()

            #交叉操作
            self.cross()

            #变异操作
            self.mutation()
            #更新种群
            self.population.append(self.best_one)
            #寻找最优解
            print("最大胜率：", max(self.win)/(2*(self.population_size-1)))
            
            for j in range(self.population_size):
                print(self.population[j])

    # def test(self):
    #     print("初始population")
    #     for i in range(self.population_size-1):
    #         print(self.population[i])
    #     print("交换")
    #     self.cross()
    #     # print("变异")
    #     # self.mutation()


    def mutation(self):
        for i in range(self.population_size):
            rand_rate = random.random()
            if rand_rate <= self.mutation_rate:
                print("mutation!!")
                random_chrom = self.population[random.randrange(self.population_size-1)]
                random_index = random.randrange(5)
                random_position = random.randrange(8)
                print("index,", random_index)
                print("position,", random_position)
                print("前：", random_chrom)
                mask = (1 << random_position) & 0xff
                random_chrom[random_index] = (random_chrom[random_index] ^ mask)
                print("后：", random_chrom)
        print("mutation")
        for i in range(len(self.population)):
            print(self.population[i])
                
    
    
    #使用均匀交叉
    def cross(self):
        for i in range(self.population_size):
            rand_rate = random.random()
            if rand_rate <= self.cross_rate:
                print("cross!!")
                cross_position = int(random.random() * self.chrom_length * 8)
                cross_direction = random.randint(0,1)
                print("cross_position," ,cross_position)
                print("cross_direction", cross_direction)
                #如果cross_direction为0，则前index-1的整数交换，第index个整数从0到shift交换
                #如果cross_direction为1，则后index+1的整数交换，第index个整数从shift到7位交换
                random_index1 = random.randrange(self.population_size-1)
                while True:
                    random_index2 = random.randrange(self.population_size-1)
                    if random_index2 != random_index1:
                        break
                random_chrom1 = self.population[random_index1]
                random_chrom2 = self.population[random_index2]
                print("交换前：", random_chrom1, random_chrom2)

                index = cross_position // 8
                shift = cross_position % 8

                #交换前index-1个整数
                if cross_direction == 0:
                    for j in range(index):
                        random_chrom1[j], random_chrom2[j] = random_chrom2[j], random_chrom1[j]
                    mask1 = (0xff << (7-shift))&0xff
                    mask2 = (0xff >> (shift+1))&0xff
                    tmp1 = random_chrom1[index] & mask1
                    tmp2 = random_chrom2[index] & mask1
                    random_chrom1[index] = (random_chrom1[index] & mask2) | tmp2
                    random_chrom2[index] = (random_chrom2[index] & mask2) | tmp1
                elif cross_direction == 1:
                    for j in range(index+1, self.chrom_length):
                        random_chrom1[j], random_chrom2[j] = random_chrom2[j], random_chrom1[j]
                    mask1 = (0xff >> shift) & 0xff
                    mask2 = (0xff << (8-shift)) & 0xff
                    tmp1 = random_chrom1[index] & mask1
                    tmp2 = random_chrom2[index] & mask1
                    random_chrom1[index] = (random_chrom1[index] & mask2) | tmp2
                    random_chrom2[index] = (random_chrom2[index] & mask2) | tmp1
                print("交换后", random_chrom1, random_chrom2)
                print("populstion中：")
                for i in range(len(self.population)):
                    print(self.population[i])


                
                

    
    def select(self):
        #找到最优个体
        best_fitness = -sys.maxsize
        best_one = [0] * self.chrom_length
        best_index = -1
        
        for i in range(self.population_size):
            if self.fitness_degree[i] > best_fitness:
                best_fitness = self.fitness_degree[i]
                best_index = i
        for i in range(self.chrom_length):
            best_one[i] = self.population[best_index][i]

        #使用论转法选择个体
        accumulate = [0] * self.population_size
        sum = 0
        for i in range(self.population_size):
            accumulate[i] = sum + self.fitness_degree[i]
            sum += self.fitness_degree[i]

        #选择self.population_size-1个个体,使用轮转法
        temp_population = []
        for i in range(self.population_size-1):
            rand_num = random.random() * sum
            j = 0
            while j < self.population_size and rand_num > accumulate[j]:
                j += 1
            temp_population.append(copy.deepcopy(self.population[j]))
        print("select")
        print("best_one", best_one)
        print("temp_population", temp_population)
        
        return temp_population, best_one
            
    

    def calc_fitness(self):
        #未归一化
        self.fitness_degree = [0] * self.population_size
        self.win = [0] * self.population_size
        for i in range(self.population_size): 
            HUMAN = WHITE
            AI = BLACK
            turn = AI
            for j in range(self.population_size):
                if i != j:
                    #返回输赢信息#限授赢1，平0，输-1
                    res = self.whiteblackChess.start_game(turn, list(map(lambda x:x/MAX, self.population[i])),  list(map(lambda x:x/MAX, self.population[j])))
                    self.fitness_degree[i] += res
                    self.fitness_degree[j] -= res
                    if res == 1:
                        self.win[i] += 1
                    elif res == -1:
                        self.win[j] += 1
        self.fitness_degree = numpy.array(self.fitness_degree)
        #映射到正整数范围#加1防止出现全零状态
        self.fitness_degree = (self.fitness_degree - self.fitness_degree.min()+1).tolist()
        print("calc_fitness")
        print("fitness", self.fitness_degree)
        print("win", self.win)
        return self.fitness_degree

            
       

class WhiteBlack():
    def __init__(self):
        self.init_board()
        #8个方向
        self.directions = [[0, -1], [1, 0], [-1, 0], [0, 1], [-1, -1], [1, -1], [-1, 1], [1, 1]]

    



    def init_board(self):
        self.board = [[0] * CHESS_SIZE for i in range(CHESS_SIZE)]
        self.board[CHESS_SIZE//2-1][CHESS_SIZE//2-1] = WHITE
        self.board[CHESS_SIZE//2][CHESS_SIZE//2-1] = BLACK
        self.board[CHESS_SIZE//2-1][CHESS_SIZE//2] = BLACK
        self.board[CHESS_SIZE//2][CHESS_SIZE//2] = WHITE
    
    #只判断位置是否在棋盘范围内
    def is_legal(self, x, y):
        if x >= 0 and x < CHESS_SIZE and y < CHESS_SIZE and y >= 0:
            return True
        else:
            return False

    #找到可以放置棋子的位置
    def find_legal_positions(self, board, player):
        #找到可以反转棋子颜色的所有位置为合法的位置
        positions = []
        for x in range(CHESS_SIZE):
            for y in range(CHESS_SIZE):
                if self.can_reverse(board, x, y, player):
                    positions.append([x, y])
        return positions

    
    #判断某个位置是否可以反转棋子的颜色
    def can_reverse(self, board, x, y, color):
        if (not self.is_legal(x, y)) or board[x][y] != NULL:
            return False
        #位置合法，且位置为空
        for direction in self.directions:
            nx, ny = x+direction[0], y+direction[1]
            if self.is_legal(nx, ny) and board[nx][ny] == -color:#颜色相反
                #print("x",x, "y", y,"board[x][y]:", board[x][y], "nx", nx, "ny", ny, "board[nx][ny]:", board[nx][ny], end=' ')
                nx += direction[0]
                ny += direction[1]
                while self.is_legal(nx, ny):
                    if board[nx][ny] == color:
                        return True
                    elif board[nx][ny] == NULL:
                        break
                    nx += direction[0]
                    ny += direction[1]
        return False
    
    
    #放置棋子
    def place_chess(self, x, y, color):
        self.board[x][y] = color
        #反转颜色
        self.reverse_chess(x, y, color)
    

    #反转颜色
    def reverse_chess(self, x, y, color):#反转被夹住的棋子的颜色
        for direction in self.directions:
            nx = x + direction[0]
            ny = y + direction[1]
            if self.is_legal(nx, ny) and self.board[nx][ny] == -color:
                nnx = nx + direction[0]
                nny = ny + direction[1]
                while self.is_legal(nnx, nny):
                    if self.board[nnx][nny] == NULL:
                        break
                    elif self.board[nnx][nny] == color:
                        nnx -= direction[0]; nny -= direction[1]
                        while nnx != x or nny != y:
                            self.board[nnx][nny] = color
                            nnx -= direction[0]; nny -= direction[1]                            
                        break
                    #查看该方向的下一个位置
                    nnx += direction[0]; nny += direction[1]

    #计算当前黑白棋子的个数
    def calc_chess(self):
        white_cnt = 0
        black_cnt = 0
        for i in range(CHESS_SIZE):
            for j in range(CHESS_SIZE):
                if self.board[i][j] == WHITE:
                    white_cnt += 1
                elif self.board[i][j] == BLACK:
                    black_cnt += 1
        return (white_cnt, black_cnt)#白棋个数，黑棋个数
    
    #通过alphabeta找到最好的位置
    def find_best_place(self, color, chrom):
        depth = 5
        a = -sys.maxsize
        b = sys.maxsize
        _, move = self.alphaBeta(self.board, chrom, color, a, b, color, depth)
        return move

    #是否有合法位置下棋
    def can_move(self, board, color):
        position = self.find_legal_positions(board, color)
        if len(position) != 0:
            return True
        else:
            return False
    
    #对AI 黑色要最大
    def alphaBeta(self, board, chrom, player, a, b, color, depth):
        maximum = -sys.maxsize#初始化为最小
        if color == player:
            sign = 1
        elif color == -player:
            sign = -1

        if depth <= 0:#达到深度阈值，返回这个深度下棋盘的估价值
            return sign * self.evaluate(board, chrom, player), None
        if not self.can_move(board, color):#如果当前一方不能下
            if not self.can_move(board, -color):#双方都不能下
                return sign * self.evaluate(board, chrom, player), None#返回对当前棋盘的估价
            else:#到另一方下棋
                res = self.alphaBeta(board, chrom, player, -b, -a, -color, depth)
                return -res[0], res[1]
        moves = self.find_legal_positions(board, color)
        action = None
        #遍历当前这一方能够下棋的位置
        for move in moves:#move是两个元素的列表
            board[move[0]][move[1]] = color
            #获取在这个位置下棋后的估计值
            val, _ = self.alphaBeta(board, chrom, player, -b, -a, -color, depth-1)
            val = -val
            board[move[0]][move[1]] = NULL#恢复
            if val > a:#更新a的值
                if val >= b:#发生剪枝
                    return val, move
                a = max(val, a)
            if val > maximum:
                maximum = val
                action = move
        return maximum, action

    
    #计算稳定度
    def calc_stable_degree(self, board, x, y):
        directions = [[(0, -1), (0, 1)], 
                    [(-1, 0), (1, 0)],
                    [(-1, -1), (1, 1)],
                    [(-1, 1), (1, -1)]]
        position = [[0] * 2, [0]*2]
        degree = 0
        color = board[x][y]

        for i in range(4):
            position[0][0] = x
            position[0][1] = y
            position[1][0] = x
            position[1][1] = y
            for j in range(2):
                while (self.is_legal(position[j][0] + directions[i][j][0], position[j][1] +directions[i][j][1]) and board[position[j][0] + directions[i][j][0]][position[j][1] +directions[i][j][1]]==color):
                    position[j][0] += directions[i][j][0]
                    position[j][1] += directions[i][j][1]
                position[j][0] += directions[i][j][0]
                position[j][1] += directions[i][j][1]
            if (not self.is_legal(position[0][0], position[0][1])) or (not self.is_legal(position[1][0], position[1][1])):
                degree += 1
            elif (board[position[0][0]][position[0][1]] == -color) and (board[position[1][0]][position[1][1]] == -color):
                degree += 1
        
        return degree
        
 

    def start_game(self, turn, chrom1, chrom2):#HUMAN为人，AI为AI
        self.init_board()
        while self.can_move(self.board, HUMAN) or self.can_move(self.board, AI):
            if turn == AI:
                if self.can_move(self.board, AI):
                    move = self.find_best_place(turn, chrom1)
                    self.draw_chessbox()
                    self.place_chess(move[0], move[1], AI)
                    #重新计算当前得分
                    white_score, black_score = self.calc_chess()
                    print("AI place (%s, %s)"%(move[0], move[1]))
                    print('The Scroe BLACK : WHITE --->', str(black_score), ':', str(white_score)) 
                    turn = HUMAN
                else:
                    turn = HUMAN
                
            if turn == HUMAN:
                if self.can_move(self.board, HUMAN):
                    move = self.find_best_place(turn, chrom2)
                    self.draw_chessbox()
                    self.place_chess(move[0], move[1], HUMAN)
                    #重新计算当前得分
                    white_score, black_score = self.calc_chess()
                    print("HUMAN place (%s, %s)"%(move[0], move[1]))
                    print('The Scroe BLACK : WHITE --->', str(black_score), ':', str(white_score)) 
                    turn = AI
                else:
                    turn = AI
        #双方都不可以移动了，则游戏结束
        print("game over")
        print('The Scroe BLACK : WHITE --->', str(black_score), ':', str(white_score)) 
        if black_score > white_score:
            return 1
        elif black_score == white_score:
            return 0
        else:
            return -1


    def start_game2(self, turn, chrom1, chrom2):#HUMAN为人，AI为AI
        self.init_board()
        while self.can_move(self.board, HUMAN) or self.can_move(self.board, AI):
            if turn == AI:
                if self.can_move(self.board, AI):
                    move = self.find_best_place(turn, chrom1)
                    self.draw_chessbox()
                    self.place_chess(move[0], move[1], AI)
                    #重新计算当前得分
                    white_score, black_score = self.calc_chess()
                    print("AI place (%s, %s)"%(move[0], move[1]))
                    print('The Scroe BLACK : WHITE --->', str(black_score), ':', str(white_score)) 
                    turn = HUMAN
                else:
                    turn = HUMAN
                
            if turn == HUMAN:
                if self.can_move(self.board, HUMAN):
                    legal_positions = self.find_legal_positions(self.board, HUMAN)
                    self.draw_chessbox(legal_positions)
                    #人类输入位置
                    while True:
                        # try:
                        row, col = map(int, input("请输入下棋位置:").strip().split(' '))
                        if [row, col] in legal_positions:
                            break
                        # except:
                        #     continue        
                    self.place_chess(row, col, HUMAN)
                    
                    #重新计算当前得分
                    white_score, black_score = self.calc_chess()
                    print("HUMAN place (%s, %s)"%(row, col))
                    print('The Scroe BLACK : WHITE --->', str(black_score), ':', str(white_score)) 
                    turn = AI
                else:
                    turn = AI
        print("game over")
        print('The Scroe BLACK : WHITE --->', str(black_score), ':', str(white_score)) 


    def evaluate(self, board, c, color):
        #c[0]行动力，c[1]前沿点，c[2]棋子数，c[3]稳定子，c[4]地势表

        #行动力
        black_value = c[0] * len(self.find_legal_positions(board, BLACK))#c[0]为行动力的系数
        white_value = c[0] * len(self.find_legal_positions(board, WHITE))

        for i in range(CHESS_SIZE):
            for j in range(CHESS_SIZE):
                if board[i][j] == BLACK:
                    #前沿点
                    for k in range(4):
                        if self.is_legal(i+self.directions[k][0], j+self.directions[k][1]) and board[i+self.directions[k][0]][j+self.directions[k][1]] == NULL:
                            black_value += c[1]
                            break
                    #棋子数
                    black_value += c[2]
                    #稳定子
                    # if (i == 0 and j == 0) or (i == 0 and j == CHESS_SIZE-1) or (i == CHESS_SIZE-1 and j = 0) or (i == CHESS_SIZE-1 and j == CHESS_SIZE-1):
                    #     black_value += c[3]
                    black_value += self.calc_stable_degree(board, i, j) * c[3]
                    #地势表
                    black_value += position_value[i][j] * c[4]
                if board[i][j] == WHITE:
                    #前沿点
                    for k in range(4):
                        if self.is_legal(i+self.directions[k][0], j+self.directions[k][1]) and board[i+self.directions[k][0]][j+self.directions[k][1]] == NULL:
                            white_value += c[1]
                            break
                    #棋子数
                    white_value += c[2]
                    #稳定子
                    # if (i == 0 and j == 0) or (i == 0 and j == CHESS_SIZE-1) or (i == CHESS_SIZE-1 and j = 0) or (i == CHESS_SIZE-1 and j == CHESS_SIZE-1):
                    #     white_value += c[3]
                    white_value += self.calc_stable_degree(board, i, j) * c[3]
                    #地势表
                    white_value += position_value[i][j] * c[4]
        if color == BLACK:
            return black_value - white_value
        elif color == WHITE:
            return white_value - white_value
                    

    
    def draw_chessbox(self, next_position=None):
        for i in range(CHESS_SIZE+1):
            if i > 0:
                print(i-1, end='')
            else:
                print(" ", end="")
        print()
        if next_position == None:
            for i in range(CHESS_SIZE):
                print(i, end="")
                for j in range(CHESS_SIZE):
                    if self.board[i][j] == BLACK:
                        print("•", end='')
                    elif self.board[i][j] == WHITE:
                        print("o", end="")
                    elif self.board[i][j] == NULL:
                        print("-", end="")
                print()      
        else:
            for  i in range(CHESS_SIZE):
                print(i, end="")
                for j in range(CHESS_SIZE):
                    if self.board[i][j] == BLACK:
                        print("•", end='')
                    elif self.board[i][j] == WHITE:
                        print("o", end='')
                    elif self.board[i][j] == NULL:
                        if [i, j] in next_position:
                            print("+", end="")
                        else:
                            print("-", end="")
                print()




if __name__ == "__main__":
    while True:
        is_train = input("训练：1，验证：0")
        if is_train == '0' or is_train == '1':
            break
    if is_train == '1':
        ga = GA()
        ga.iteration()
    elif is_train == '0':
        w = WhiteBlack()
        while True:
            # try:
            choose = int(input("choose white or black, 0 is white, 1 is black"))
            if choose == 0:
                HUMAN = WHITE
                AI = BLACK
                turn = AI
                break
            elif choose == 1:
                HUMAN = BLACK
                AI = WHITE
                turn = HUMAN
                break
            # except:
                # continue
        best_chrome = [1, 1, 1, 1, 1]
        w.start_game2(turn, best_chrome, best_chrome)











