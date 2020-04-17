import tensorflow.compat.v1 as tf

tensor = tf.constant([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
print(tensor)
t2 = tensor * [1, 2, 3, 4]
print(t2)