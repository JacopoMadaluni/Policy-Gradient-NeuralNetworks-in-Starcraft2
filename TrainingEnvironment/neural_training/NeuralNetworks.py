import os
import tensorflow.compat.v1 as tf
import numpy as np
import ctypes

class MultiLayerNN():
    """
    To be inherited, general two layer nn layout
    """
    def __init__(self, ALPHA, GAMMA=0.95, n_actions=4,
                 layer1_size=16, layer2_size=16, input_dims=128,
                 chkpt_dir='tmp/checkpoints', action_namespace=None, 
                 network_name=None):
        
        self.network_name = "" if network_name is None else network_name

        self.lr = ALPHA
        self.gamma = GAMMA
        self.n_actions = n_actions
        self.action_space = [i for i in range(n_actions)]
        self.layer1_size = layer1_size
        self.layer2_size = layer2_size
        self.input_dims = input_dims
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []
        self.sess = tf.Session()
        self.build_net()
        self.sess.run(tf.global_variables_initializer())

        self.saver = tf.train.Saver()
        #self.saver = tf.train.Saver([[v for v in tf.all_variables() if self.network_name in v.name]])

        self.checkpoints_dir = chkpt_dir
        self.checkpoint_file = os.path.join(chkpt_dir,'policy_network.ckpt')
        self.action_namespace = action_namespace # serialized to string
        #file_writer = tf.summary.FileWriter(self.checkpoints_dir, self.sess.graph)

    def set_network_name(self, name):
        self.name = name

    def __repr__(self):
        return "ALPHA: {}\nGAMMA: {}\nn_actions: {}\nL1: {}\nL2: {}\ninput_dims: {}\nnamespace: {}".format(self.lr,
                            self.gamma, self.n_actions, self.layer1_size, self.layer2_size, self.input_dims, self.action_namespace)

    def build_net(self):
        pass

    def load_checkpoint(self):
        self.saver.restore(self.sess, self.checkpoint_file)

    def save_checkpoint(self):
        self.saver.save(self.sess, self.checkpoint_file)
