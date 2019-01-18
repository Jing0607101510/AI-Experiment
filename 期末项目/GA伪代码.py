initialize P(0);
t = 0;             //t是进化的代数，一代、二代、三代…
while(t <= T) do
    for i = 1 to M  do     //M是初始种群的个体数
        Evaluate fitness of P(t);  //计算P（t）中各个个体的适应度
    for i = 1 to M  do
        Select operation to P(t);  //将选择算子作用于群体
    for i = 1 to M/2  do
        Crossover operation to P(t); //将交叉算子作用于群体
    for i = 1 to M  do
        Mutation operation to P(t);  //将变异算子作用于群体
    for i = 1 to M  do
        P(t+1) = P(t);      //得到下一代群体P（t + 1）
    t = t + 1;      //终止条件判断  t≦T：t← t+1 


policy = build_policy_model()
game.start()
while True:  
    if turn == BLACK:
        state = game.currentState()
        enables = game.enables()
        action, prob = policy.chooseAction(state, enables)
        reward = game.play(action)
        trajectory.append((state, prob, action, reward))
        turn = WHITE
    if turn == WHITE:
        state = game.currentState()
        enables = game.enables()
        action, prob = policy.chooseAction(state, enables)
        reward = game.play(action)
        trajectory.append((state, prob, action, reward))
        turn = BLACK
    if game.terminated():
        policy.backpropagation(trajectories)
        game.restart()

def mutation(self):
    for i in range(self.population_size):
        rand_rate = random.random()
        if rand_rate <= self.mutation_rate:
            random_chrom = self.population[random.randrange(self.population_size-1)]
            random_index = random.randrange(5)
            random_position = random.randrange(8)
            mask = (1 << random_position) & 0xff
            random_chrom[random_index] = (random_chrom[random_index] ^ mask)

for i in range(self.iternum):
    #计算各个染色体的适应度
    self.fitness_degree = self.calc_fitness()
    #选择操作#这个population是n-1大小，还需要加上best_one
    self.population, self.best_one = self.select()            
    self.cross()#交叉操作            
    self.mutation()#变异操作            
    self.population.append(self.best_one)#更新种群

temp_population = []
for i in range(self.population_size-1):
    rand_num = random.random() * sum
    j = 0
    while j < self.population_size and rand_num > accumulate[j]:
        j += 1
    temp_population.append(copy.deepcopy(self.population[j]))

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

def choose_action(self, observation, enables):
    prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.tf_obs:observation[np.newaxis, :]})#newaxis的作用是增加一维。原来的输入是一维的。
    positions = np.arange(prob_weights.shape[1])[enables]
    if np.sum(np.array(prob_weights.ravel())[enables]) != 0:
        p = np.array(prob_weights.ravel())[enables] / np.sum(np.array(prob_weights.ravel())[enables])
    else:
        p = np.ones(np.array(prob_weights.ravel())[enables].shape) / np.sum(np.ones(np.array(prob_weights.ravel())[enables].shape))
    action = np.random.choice(positions, p=p)#返回0-63其中一个数，代表位置
    return action



for i in range(self.population_size): 
    HUMAN, AI, turn = WHITE, BLACK, BLACK
    for j in range(self.population_size):
        if i != j:
            #返回输赢信息#限授赢1，平0，输-1
            res = self.whiteblackChess.start_game(turn, list(map(lambda x:x/MAX, self.population[i])),  list(map(lambda x:x/MAX, self.population[j])))
            self.fitness_degree[i] += res
            self.fitness_degree[j] -= res

with tf.name_scope("loss_"):
    neg_log_prob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=all_act, labels=self.tf_acts)
    self.loss = tf.reduce_mean(neg_log_prob * self.tf_vt)
with tf.name_scope('train_'):
    self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)
self.sess.run([self.train_op, self.loss], feed_dict={
    self.tf_obs:np.vstack(self.ep_obs),
    self.tf_acts:np.array(self.ep_as),
    self.tf_vt:discounted_ep_rs_norm,
    })


observation = whiteblack.board_tolist(BLACK)
enables =  whiteblack.legal_positions_tolist(BLACK)
if any(enables):
    action = RL_BLACK.choose_action(observation, enables)
    reward, done = whiteblack.step(action, BLACK)#在棋盘中走一步
    RL_BLACK.store_transition(observation, action, reward)