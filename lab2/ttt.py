import tensorflow as tf


a_gpu = tf.Variable(0, name="a_gpu")
a_cpu = tf.Variable(0, name="a_cpu") 
# 通过allow_soft_placement参数自动将无法放在GPU上的操作放回CPU上。
sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True))
sess.run(tf.initialize_all_variables())

