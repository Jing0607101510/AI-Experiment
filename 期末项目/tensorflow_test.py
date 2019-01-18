import tensorflow as tf 
import numpy as np 

x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.1 + 0.3

Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
biases = tf.Variable(tf.zeros([1]))

y = Weights * x_data + biases

#计算误差
loss = tf.reduce_mean(tf.square(y-y_data))

#反向传播
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

#训练
#初始化定义的variable
init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

for step in range(201):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))


mat1 = tf.constant([[3,3]])
mat2 = tf.constant([[2],[2]])
product = tf.matmul(mat1, mat2)
with tf.Session() as sess:
    res = sess.run(product)
    print(res)
