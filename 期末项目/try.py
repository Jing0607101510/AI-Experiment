​import gym
import tensorflow as tf
import numpy as np
from policy_gradient import util
from policy_gradient.policy import CategoricalPolicy
from policy_gradient.baselines.linear_feature_baseline import LinearFeatureBaseline

np.random.seed(0)
tf.set_random_seed(0)

​tf.reset_default_graph()
sess = tf.Session()
# Construct a neural network to represent policy which maps observed state to action. 
in_dim = util.flatten_space(env.observation_space)
out_dim = util.flatten_space(env.action_space)
hidden_dim = 8

# Initialize your policy
with tf.variable_scope("policy"):
    opt_p = tf.train.AdamOptimizer(learning_rate=0.01)
    policy = CategoricalPolicy(in_dim, out_dim, hidden_dim, opt_p, sess)

class PolicyOptimizer(object):
    def __init__(self, env, policy, baseline, n_iter, n_episode, path_length,
        discount_rate=.99):

        self.policy = policy
        self.baseline = baseline
        self.env = env
        self.n_iter = n_iter
        self.n_episode = n_episode
        self.path_length = path_length
        self.discount_rate = discount_rate

    def sample_path(self):
        obs = []
        actions = []
        rewards = []
        ob = self.env.reset()

        # sample a batch of trajectory
        for _ in range(self.path_length):
            a = self.policy.act(ob.reshape(1, -1
            obs.append(ob)))
            next_ob, r, done, _ = self.env.step(a)
            actions.append(a)
            rewards.append(r)
            ob = next_ob
            if done:
                break

        return dict(
            observations=np.array(obs),
            actions=np.array(actions),
            rewards=np.array(rewards),
        )

    def process_paths(self, paths):
        for p in paths:
            if self.baseline != None:
                b = self.baseline.predict(p)
                b[-1] = 0 # terminal state
            else:
                b = 0
            
            # `p["rewards"]` is a matrix contains the rewards of each timestep in a sample path
            r = util.discount_cumsum(p["rewards"], self.discount_rate)
            
            """
            Problem 3:

            1. Variable `b` is the values predicted by our baseline
            2. Use it to reduce variance and then assign the result to the 
                    variable `a` (baseline reduction)

            Sample solution should be only 1 line.
            """
            # YOUR CODE HERE >>>>>>
            # <<<<<<<<

            p["returns"] = r
            p["baselines"] = b
            p["advantages"] = (a - a.mean()) / (a.std() + 1e-8) # normalize

        obs = np.concatenate([ p["observations"] for p in paths ])
        actions = np.concatenate([ p["actions"] for p in paths ])
        rewards = np.concatenate([ p["rewards"] for p in paths ])
        advantages = np.concatenate([ p["advantages"] for p in paths ])

        return dict(
            observations=obs,
            actions=actions,
            rewards=rewards,
            advantages=advantages,
        )

    
    def train(self):
        loss_list = []
        avg_return_list = []
        for i in range(1, self.n_iter + 1):
            paths = []
            for _ in range(self.n_episode):
                paths.append(self.sample_path())
            data = self.process_paths(paths)
            loss = self.policy.train(data["observations"], data["actions"], data["advantages"])
            avg_return = np.mean([sum(p["rewards"]) for p in paths])
            print("Iteration {}: Average Return = {}".format(i, avg_return))
            loss_list.append(loss)
            avg_return_list.append(avg_return)
            # CartPole-v0 defines "solving" as getting average reward of 195.0 over 100 consecutive trials.
            if avg_return >= 195:
                print("Solve at {} iterations, which equals {} episodes.".format(i, i*100))
                break

            if self.baseline != None:
                self.baseline.fit(paths)
        return loss_list, avg_return_list

    
​sess.run(tf.global_variables_initializer())

n_iter = 200
n_episode = 100
path_length = 200
discount_rate = 0.99
baseline = LinearFeatureBaseline(env.spec)

po = PolicyOptimizer(env, policy, baseline, n_iter, n_episode, path_length,
                     discount_rate)

# Train the policy optimizer
loss_list, avg_return_list = po.train()

LAMBDA = 0.98 # \lambda
class PolicyOptimizer_actor_critic(PolicyOptimizer):
    def __init__(self, env, policy, baseline, n_iter, n_episode, path_length,
        discount_rate=.99):
        PolicyOptimizer.__init__(self, env, policy, baseline, n_iter, n_episode, path_length,
            discount_rate=.99)
    
    def process_paths(self, paths):
        for p in paths:
            if self.baseline != None:
                b = self.baseline.predict(p)
                b[-1] = 0 # terminal state
            else:
                b = 0


sess.run(tf.global_variables_initializer())

n_iter = 200
n_episode = 100
path_length = 200
discount_rate = 0.99
# reinitialize the baseline function
baseline = LinearFeatureBaseline(env.spec) 
sess.run(tf.global_variables_initializer())
po = PolicyOptimizer_actor_critic(env, policy, baseline, n_iter, n_episode, path_length,
                     discount_rate)

# Train the policy optimizer
loss_list, avg_return_list = po.train()