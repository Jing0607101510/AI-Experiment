import sys
import math

BLACK = 1
NULL = 0
WHITE = -1

CHESS_SIZE = 8


AI = 1
HUMAN = -1


import time

class WhiteBlack():
    def __init__(self):
        self.init_board()
        #8个方向
        self.directions = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]

    

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
    def find_best_place(self, color):#color是指谁使用了博弈树
        depth = 5
        a = -sys.maxsize
        b = sys.maxsize
        _, move = self.alphaBeta(self.board, color, a, b, color, depth)
        return move

    #是否有合法位置下棋
    def can_move(self, board, color):
        position = self.find_legal_positions(board, color)
        if len(position) != 0:
            return True
        else:
            return False
    
    #对AI 黑色要最大#evaluate是对用博弈树一方的一个得益估值
    def alphaBeta(self, board, player, a, b, color, depth):
        maximum = -sys.maxsize#初始化为最小
        if color == player:
            sign = 1
        elif color == -player:
            sign = -1

        if depth <= 0:#达到深度阈值，返回这个深度下棋盘的估价值
            return sign * self.evaluate(board, player), None
        if not self.can_move(board, color):#如果当前一方不能下
            if not self.can_move(board, -color):#双方都不能下
                return sign * self.evaluate(board, player), None#返回对当前棋盘的估价
            else:#到另一方下棋
                res = self.alphaBeta(board, player, -b, -a, -color, depth)
                return -res[0], res[1]
        moves = self.find_legal_positions(board, color)
        action = None
        #遍历当前这一方能够下棋的位置
        for move in moves:#move是两个元素的列表
            board[move[0]][move[1]] = color
            #获取在这个位置下棋后的估计值
            val, _ = self.alphaBeta(board, player, -b, -a, -color, depth-1)
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
        
    #1.角：+5#2.边：+2#3.其他位置：+1#4.行动力#5.稳定度

    #稳定子
    #行动力#需要修改，返回AI的颜色的估价
    def evaluate(self, board, color):
        black_value = 0
        white_value = 0
        weight = [2, 4, 6, 10, 15]
        for i in range(6):
            for j in range(6):
                #对不同位置上棋子的稳定度
                if board[i][j] == WHITE:
                    white_value += weight[self.calc_stable_degree(board, i, j)]
                elif board[i][j] == BLACK:
                    black_value += weight[self.calc_stable_degree(board, i, j)]
        white_value += len(self.find_legal_positions(board, WHITE))#加上黑白棋各自的行动力
        black_value += len(self.find_legal_positions(board, BLACK))
        if color == BLACK:
            return black_value - white_value
        elif color == WHITE:
            return white_value - black_value

    #棋盘上黑白棋的个数
    def evaluate_1(self, board):
        black_value = 0
        white_value = 0
        #统计棋盘上黑棋和白棋的数量
        for i in range(6):
            for j in range(6):
                if board[i][j] == WHITE:
                    white_value += 1
                elif board[i][j] == BLACK:
                    black_value += 1
        #黑棋和白棋的数量差作为估价值
        return black_value - white_value
        
    #关注特殊位置的棋子（边角）
    def evaluate_2(self, board):
        black_value = 0
        white_value = 0
        #角上的棋子的权重为5
        #边上的棋子的权值为2
        #其他位置为1
        for i in range(6):
            for j in range(6):
                if (i == 0 or i == 5) and (j == 0 or j == 5):
                    if board[i][j] == WHITE:
                        white_value += 5
                    elif board[i][j] == BLACK:
                        black_value += 5
                elif i == 0 or i == 5 or j == 0 or j == 5:
                    if board[i][j] == WHITE:
                        white_value += 2
                    elif board[i][j] == BLACK:
                        black_value += 2
                else:
                    if board[i][j] == WHITE:
                        white_value += 1
                    else:
                        black_value += 1
        return black_value - white_value

    #关注边角位置，还有行动力
    def evaluate_3(self, board):
        black_value = 0
        white_value = 0
        for i in range(6):
            for j in range(6):
                if (i == 0 or i == 5) and (j == 0 or j == 5):
                    if board[i][j] == WHITE:
                        white_value += 5
                    elif board[i][j] == BLACK:
                        black_value += 5
                elif i == 0 or i == 5 or j == 0 or j == 5:
                    if board[i][j] == WHITE:
                        white_value += 2
                    elif board[i][j] == BLACK:
                        black_value += 2
                else:
                    if board[i][j] == WHITE:
                        white_value += 1
                    else:
                        black_value += 1
        black_value = 2 * black_value + len(self.find_legal_positions(board, BLACK))
        white_value = 2 * white_value + len(self.find_legal_positions(board, WHITE))
        return black_value - white_value        

    
    def start_game(self, turn):#HUMAN为人，AI为AI
        while self.can_move(self.board, HUMAN) or self.can_move(self.board, AI):
            if turn == AI:
                if self.can_move(self.board, AI):
                    move = self.find_best_place(turn)
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
        #双方都不可以移动了，则游戏结束
        print("game over")
        print('The Scroe BLACK : WHITE --->', str(black_score), ':', str(white_score)) 


        
    
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
    w.start_game(turn)











