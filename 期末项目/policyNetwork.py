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
    
    def legal_positions_tolist(self, player):
        positions = []
        for x in range(CHESS_SIZE):
            for y in range(CHESS_SIZE):
                if self.can_reverse(self.board, x, y, player):
                    positions.append(True)
                else:
                    positions.append(False)
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

    def step(self, index, color):
        x = index // 8
        y = index % 8
        self.place_chess(x, y, color)
        print("place (%s, %s)"%(x, y), end="\n")
        print()
        self.draw_chessbox()
        if self.can_move(self.board, HUMAN) or self.can_move(self.board, AI):
            done = False
            reward = 0
            
        else:
            done = True
            white_score, black_score = self.calc_chess()
            if color * (black_score - white_score) > 0:
                reward = 100.0
            elif color * (black_score - white_score) == 0:
                reward = 10.0
            else:
                reward = 1.0
        return reward, done
    
    def board_tolist(self, color):
        res = []
        for i in range(CHESS_SIZE):
            for j in range(CHESS_SIZE):
                res.append(color * self.board[i][j])
        return np.array(res)


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
        
 

    def start_game(self, turn, RL_BLACK, RL_WHITE):#HUMAN为人，AI为AI
        self.init_board()
        if AI == BLACK:
            while self.can_move(self.board, HUMAN) or self.can_move(self.board, AI):
                if turn == AI:
                    if self.can_move(self.board, BLACK):
                        observation = whiteblack.board_tolist(BLACK)

                        enables =  whiteblack.legal_positions_tolist(BLACK)

                        action = RL_BLACK.choose_action(observation, enables)
                        
                        whiteblack.step(action, BLACK)

                        self.draw_chessbox()
                        #重新计算当前得分
                        move = [action//8, action%8]
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
        
        elif AI == WHITE:
            while self.can_move(self.board, HUMAN) or self.can_move(self.board, AI):
                if turn == AI:
                    if self.can_move(self.board, WHITE):
                        observation = whiteblack.board_tolist(WHITE)

                        enables =  whiteblack.legal_positions_tolist(WHITE)

                        action = RL_WHITE.choose_action(observation, enables)
                        
                        whiteblack.step(action, WHITE)

                        self.draw_chessbox()
                        #重新计算当前得分
                        move = [action//8, action%8]
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



import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

class PolicyGradient():
    def __init__(self, n_actions, n_features, learning_rate=0.01, reward_decay=0.95, color="BLACK", sess=tf.Session(), output_graph=False):
        self.train = train
        self.color = color
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay#reward递减率
        #存储回合信息
        self.ep_obs = []
        self.ep_as = []
        self.ep_rs = []

        self._build_net()

        #self.sess = tf.Session()
        self.sess = sess

        if output_graph:
            # $ tensorboard --logdir=logs
            # http://0.0.0.0:6006
            # tf.train.SummaryWriter soon be deprecated, use followding
            tf.summary.FileWriter("logs/", self.sess.graph)
        
        self.sess.run(tf.global_variables_initializer())

    
    def _build_net(self):
        with tf.name_scope("inputs_"+self.color):
            #接收observation
            self.tf_obs = tf.placeholder(tf.float32, [None, self.n_features], name="observations_"+self.color)
            #接收在这个回合中选过的actions
            self.tf_acts = tf.placeholder(tf.int32, [None,], name="actions_num_"+self.color)
            #接收每个state-action所对应的value（通过reward计算）
            self.tf_vt = tf.placeholder(tf.float32, [None,], name="actions_value_"+self.color)

        #fc1
        layer = tf.layers.dense(
                inputs = self.tf_obs,
                units = 10,#输出个数
                activation = tf.nn.tanh,#激励函数
                kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),#初始的w
                bias_initializer=tf.constant_initializer(0.1),#初始的b
                name = 'fc1_'+self.color
        )
            #fc2
        all_act = tf.layers.dense(
                inputs = layer,
                units = self.n_actions,
                activation = None,
                kernel_initializer = tf.random_normal_initializer(mean=0, stddev=0.3),
                bias_initializer=tf.constant_initializer(0.1),
                name = 'fc2_'+self.color
        )

        #激励函数softmax输出概率
        self.all_act_prob = tf.nn.softmax(all_act, name="act_prob_"+self.color)

        
        with tf.name_scope("loss_"+self.color):
            #最大化总体reward（log_p*R）就是最小化-（log_p * R），而tf的功能里只有最小化loss
            self.neg_log_prob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=all_act, labels=self.tf_acts)
            self.loss = tf.reduce_mean(self.neg_log_prob * self.tf_vt)#(vt=本reward+衰减的未来reward)引导参数的梯度下降‘
        
        with tf.name_scope('train_'+self.color):
            self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

    
    def choose_action(self, observation, enables):
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.tf_obs:observation[np.newaxis, :]})#newaxis的作用是增加一维。原来的输入是一维的。
        positions = np.arange(prob_weights.shape[1])[enables]
        if np.sum(np.array(prob_weights.ravel())[enables]) != 0:
            p = np.array(prob_weights.ravel())[enables] / np.sum(np.array(prob_weights.ravel())[enables])
        else:
            p = np.ones(np.array(prob_weights.ravel())[enables].shape) / np.sum(np.ones(np.array(prob_weights.ravel())[enables].shape))
        action = np.random.choice(positions, p=p)#返回0-63其中一个数，代表位置
        return action

    def store_transition(self, s, a, r):
        self.ep_obs.append(s)
        self.ep_as.append(a)
        self.ep_rs.append(r)

    def learn(self):
        #衰减并标准化这回合的reward
        discounted_ep_rs_norm = self._discount_and_norm_rewards()

        #train on episode
        _, loss, prob = self.sess.run([self.train_op, self.loss, self.neg_log_prob], feed_dict={
            self.tf_obs:np.vstack(self.ep_obs),
            self.tf_acts:np.array(self.ep_as),
            self.tf_vt:discounted_ep_rs_norm,
        })

        #print(self.color, "误差：", loss, "prob:", prob, 'vt', discounted_ep_rs_norm)
        #print(self.color, "误差：", loss)


        self.ep_obs, self.ep_as, self.ep_rs = [], [], []
        return discounted_ep_rs_norm

    def _discount_and_norm_rewards(self):
        #discount episode rewards
        discounted_ep_rs = np.zeros_like(self.ep_rs, dtype="float64")
        running_add = 0
        for t in reversed(range(0, len(self.ep_rs))):
            running_add = running_add * self.gamma + self.ep_rs[t]
            discounted_ep_rs[t] = running_add
        
        #normalize episode rewards
        # discounted_ep_rs -= np.mean(discounted_ep_rs)
        # discounted_ep_rs /= np.std(discounted_ep_rs)
        return discounted_ep_rs
    
    def save_para(self):
        saver = tf.train.Saver()
        save_path = saver.save(self.sess, 'save/save_%s.ckpt'%(self.color))
        print("保存到：", save_path)
    




if __name__ == '__main__':
    while True:
        train = input("训练还是验证：1为训练，0为验证")
        if train == '1' or train == '0':
            break
    sess_white = tf.Session()
    sess_black = tf.Session()
    RL_BLACK = PolicyGradient(
            n_actions=64,#64个位置
            n_features=64,#64个位置
            learning_rate = 0.02,
            reward_decay=0.99,
            color="BLACK",
            sess=sess_black
    )
    RL_WHITE = PolicyGradient(
            n_actions=64,#64个位置
            n_features=64,#64个位置
            learning_rate = 0.02,
            reward_decay=0.99,
            color="WHITE",
            sess=sess_white
    )
    saver_white = tf.train.Saver() 
    saver_black = tf.train.Saver()
    saver_white.restore(sess_white, 'save/save_WHITE.ckpt')
    saver_black.restore(sess_black, 'save/save_BLACK.ckpt')
    whiteblack = WhiteBlack()
    if train == '1':
        # RL_BLACK = PolicyGradient(
        #     n_actions=64,#64个位置
        #     n_features=64,#64个位置
        #     learning_rate = 0.02,
        #     reward_decay=0.99,
        #     color="BLACK"
        # )
        # RL_WHITE = PolicyGradient(
        #     n_actions=64,#64个位置
        #     n_features=64,#64个位置
        #     learning_rate = 0.02,
        #     reward_decay=0.99,
        #     color="WHITE"
        # )
        
        
        white_total = 0
        black_total = 0
        for i_episode in range(10000):
            whiteblack.init_board()#初始化棋盘    
            while True:
                observation = whiteblack.board_tolist(BLACK)

                enables =  whiteblack.legal_positions_tolist(BLACK)

                if any(enables):
                    action = RL_BLACK.choose_action(observation, enables)

                    reward, done = whiteblack.step(action, BLACK)#在棋盘中走一步

                    RL_BLACK.store_transition(observation, action, reward)


                observation = whiteblack.board_tolist(WHITE)

                enables = whiteblack.legal_positions_tolist(WHITE)

                if any(enables):
                    action = RL_WHITE.choose_action(observation, enables)

                    reward, done = whiteblack.step(action, WHITE)#在棋盘中走一步

                    RL_WHITE.store_transition(observation, action, reward)



                if done:
                    white_score, black_score = whiteblack.calc_chess()
                    if white_score > black_score:
                        white_total += 1
                        RL_BLACK.ep_rs[-1] = -10
                        RL_WHITE.ep_rs[-1] = 10
                    elif white_score < black_score:
                        black_total += 1
                        RL_BLACK.ep_rs[-1] = 10
                        RL_WHITE.ep_rs[-1] = -10
                    else:
                        RL_BLACK.ep_rs[-1] = 2
                        RL_WHITE.ep_rs[-1] = 2

                    black_ep_rs_sum = sum(RL_BLACK.ep_rs)
                    white_ep_rs_sum = sum(RL_WHITE.ep_rs)

                    

                    if 'black_running_reward' not in globals():
                        black_running_reward = black_ep_rs_sum
                    else:
                        black_running_reward = black_running_reward * 0.99 + black_ep_rs_sum * 0.01
                    if 'white_running_reward' not in globals():
                        white_running_reward = white_ep_rs_sum
                    else:
                        white_running_reward = white_running_reward * 0.99 + white_ep_rs_sum * 0.01
                    
                    print("episode:", i_episode, "black_reward:", black_running_reward, "white_reward:", white_running_reward)
                    print("black:white  ", black_total, ":", white_total)

                    black_vt = RL_BLACK.learn()
                    white_vt = RL_WHITE.learn()


                    # if i_episode == 0:
                    #     plt.plot(black_vt)
                    #     plt.plot(white_vt)
                    #     plt.xlabel('episode steps')
                    #     plt.ylabel('normalized state-action value')
                    #     plt.show()
                    break

        RL_BLACK.save_para()
        RL_WHITE.save_para()

    elif train == '0':
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
        
        whiteblack.start_game(turn, RL_BLACK, RL_WHITE)
    
            


