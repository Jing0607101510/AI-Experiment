import sys
import math

BLACK = 1
NULL = 0
WHITE = -1

WIDTH = 1000
HEIGHT = 720
FPS = 30
GRID_WIDTH = HEIGHT // 8

AI = 1#对应黑色
PEOPLE = -1#对应白色
import time

class WhiteBlack():
    def __init__(self, game_gui):
    #def __init__(self):
        self.init_board()
        self.directions = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        self.game_gui = game_gui

    

    def init_board(self):
        self.board = [[0] * 6, [0] * 6, [0] * 6, [0] * 6, [0] * 6, [0] * 6]
        self.board[2][2] = WHITE
        self.board[3][2] = BLACK
        self.board[2][3] = BLACK
        self.board[3][3] = WHITE
    
    def is_legal(self, x, y):
        #只判断位置是否在棋盘范围内
        if x >= 0 and x <= 5 and y <= 5 and y >= 0:
            return True
        else:
            return False

    def find_legal_positions(self, board, player):
        #找到可以反转棋子颜色的所有位置为合法的位置
        positions = []
        for x in range(6):
            for y in range(6):
                if self.can_reverse(board, x, y, player):
                    positions.append([x, y])
        return positions

    # def test(self):
    #     self.board = [[0] * 6, [0] * 6, [0] * 6, [0] * 6, [0] * 6, [0] * 6,]
    #     self.board[2][2] = -1
    #     self.board[2][3] = 1
    #     self.board[3][2] = 1
    #     self.board[3][3] = -1
    #     self.place_chess(3, 1, WHITE)
    #     print(self.find_legal_positions(self.board, WHITE))
    #     print()
    #     for i in range(6):
    #         print(self.board[i])
    #     print()
    #     self.place_chess(4, 1, BLACK)
    #     print(self.find_legal_positions(self.board, BLACK))
    #     print()
    #     for i in range(6):
    #         print(self.board[i])
    
    #判断某个位置是否可以反转棋子的颜色
    def can_reverse(self, board, x, y, color):
        if (not self.is_legal(x, y)) or board[x][y] != NULL:
            return False
        #位置合法，且位置为空
        for direction in self.directions:
            nx, ny = x+direction[0], y+direction[1]
            if self.is_legal(nx, ny) and board[nx][ny] == -color:
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
        chess_reverse = self.reverse_chess(x, y, color)
        for r in chess_reverse:
            self.game_gui.draw_chess([r[1], r[0]], color)
    
    #反转颜色
    def reverse_chess(self, x, y, color):#反转被夹住的棋子的颜色
        chess_reverse = []
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
                            chess_reverse.append([nnx, nny])
                            nnx -= direction[0]; nny -= direction[1]                            
                        break
                    nnx += direction[0]; nny += direction[1]
        return chess_reverse

    #计算当前黑白棋子的个数
    def calc_chess(self):
        people = 0
        AI = 0
        for i in range(6):
            for j in range(6):
                if self.board[i][j] == WHITE:
                    people += 1
                elif self.board[i][j] == BLACK:
                    AI += 1
        return (people, AI)
    
    #通过alphabeta找到最好的位置
    def find_best_place(self, color):
        depth = 5
        a = -sys.maxsize
        b = sys.maxsize
        _, move = self.alphaBeta(self.board, a, b, color, depth)
        return move

    def can_move(self, board, color):
        position = self.find_legal_positions(board, color)
        if len(position) != 0:
            return True
        else:
            return False
    
    #对AI 黑色要最大
    def alphaBeta(self, board, a, b, color, depth):
        maximum = -sys.maxsize#初始化为最小
        if depth <= 0:#达到深度阈值，返回这个深度下棋盘的估价值
            return color * self.evaluate(board), None
        if not self.can_move(board, color):#如果当前一方不能下
            if not self.can_move(board, -color):#双方都不能下
                return color * self.evaluate(board), None#返回对当前棋盘的估价
            else:#到另一方下棋
                res = self.alphaBeta(board, -b, -a, -color, depth)
                return -res[0], res[1]
        moves = self.find_legal_positions(board, color)
        action = None
        #遍历当前这一方能够下棋的位置
        for move in moves:#move是两个元素的列表
            board[move[0]][move[1]] = color
            #获取在这个位置下棋后的估计值
            val, _ = self.alphaBeta(board, -b, -a, -color, depth-1)
            val = -val
            board[move[0]][move[1]] = NULL#恢复
            if val > a:#更新a的值
                if val > b:#发生剪枝
                    return val, move
                a = max(val, a)
            if val > maximum:
                maximum = val
                action = move
        return maximum, action

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
        

    #1.角：+5
    #2.边：+2
    #3.其他位置：+1
    #4.行动力
    #5.稳定度

    #稳定子
    #行动力
    def evaluate(self, board):
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
        return black_value - white_value

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

    
    def start_game(self, turn, event):#-1为人，1为AI#只走一步
        if self.can_move(self.board, AI) or self.can_move(self.board, PEOPLE):
            if turn == AI:
                time.sleep(2)
                if self.can_move(self.board, AI):
                    move = self.find_best_place(turn)
                    #更改画面
                    self.game_gui.draw_chess([move[1], move[0]], AI)
                    self.place_chess(move[0], move[1], BLACK)
                    #重新计算当前得分
                    people_score, AI_score = self.calc_chess()
                    self.game_gui.score = [people_score, AI_score]
                    self.game_gui.AI_step.append(move)
                    turn = PEOPLE
                else:
                    turn = PEOPLE
                

            elif turn == PEOPLE:
                if self.can_move(self.board, PEOPLE):
                    legal_positions = self.find_legal_positions(self.board, PEOPLE)

                    #可以点击画面选择位置
                    mouse_pos = event.pos 
                    grid = int(math.floor(mouse_pos[0] / GRID_WIDTH))-1, int(math.floor(mouse_pos[1] / GRID_WIDTH))-1#注意行和列对换
                    #判断位置是否在合法的位置上 
                    if [grid[1], grid[0]] in legal_positions:#grid[0]是水平的距离，grid[1]是竖直的距离
                        self.game_gui.draw_chess(grid, PEOPLE)
                        self.place_chess(grid[1], grid[0], WHITE)
                    #重新计算当前得分
                        people_score, AI_score = self.calc_chess()
                        self.game_gui.score = [people_score, AI_score]
                        self.game_gui.people_step.append([grid[1], grid[0]])
                        turn = AI
                else:
                    turn = AI
            return turn #返回下一个下子的人
        #双方都不可以移动了，则游戏结束
        else:
            return NULL
        

if __name__ == "__main__":
    w = WhiteBlack()
    w.test()











