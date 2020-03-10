import os
import tensorflow.compat.v1 as tf
import numpy as np
import ctypes
from .NeuralNetworks import MultiLayerNN

class QLearningAgent(MultiLayerNN):
    def __init__(self, *args, **kwargs):
        super(QLearningAgent, self).__init__(*args, **kwargs)
        
        self.mem_size = 10 # ?#
        self.mem_cntr = 0
        self.e = 0.1
        self.batch_size = 10 # ?
        self.epsilon_dec = 0.996
        self.epsilon_end = 0.01

        self.state_memory = np.zeros((self.mem_size, self.input_dims))
        self.new_state_memory = np.zeros((self.mem_size, self.input_dims))
        self.action_memory = np.zeros((self.mem_size, self.n_actions), dtype=np.int8)

        self.reward_memory = np.zeros(self.mem_size)
        self.tarminal_memory = np.zeros(self.mem_size, dtype=np.int8)    


    def build_net(self):
        tf.disable_eager_execution()
        self.input = tf.placeholder(tf.float32, shape=[None, self.input_dims], name="input")
        self.actions = tf.placeholder(tf.float32, shape=[None, self.n_actions], name="actions")
        self.old_q_value = tf.placeholder(tf.float32, shape=[None, self.n_actions], name="q_value")

        flatten = tf.layers.flatten(self.input)
        first_dense  = tf.layers.dense(inputs=flatten, units=self.layer1_size, activation=tf.nn.relu)
        second_dense = tf.layers.dense(inputs=first_dense, units=self.layer2_size, activation=tf.nn.relu)

        self.q_values = tf.layers.dense(second_dense, self.n_actions)
        self.loss = tf.reduce_mean(tf.square(self.q_values-self.old_q_value))
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)


    def choose_action(self, observation):
        observation = observation[np.newaxis, :]
        random = np.random.random()
        if random < self.e:
            action = np.random.choice(self.action_space)
        else:
            actions = self.sess.run(self.q_values, feed_dict={self.input: observation})
            action = np.argmax(actions) 
        return action        

    def store_transition(self, observation, action, reward, old_state, terminal):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = observation
        self.new_state_memory[index] = old_state
        self.reward_memory[index] = reward
        actions = np.zeros(self.n_actions)
        actions[action] = 1.0
        self.action_memory[index] = actions
        self.terminal_memory = 1 - terminal
        self.mem_cntr += 1    



    def finish_transition_group(self, reward):
        self.reward_memory[-1] = reward

    def learn(self):
        if self.mem_cntr > self.batch_size:
            max_mem = self.mem_cntr if self.mem_cntr < self.mem_size else self.mem_size
            batch = np.random.choice(max_mem, self.batch_size)

            state_batch = self.state_memory[batch]
            action_batch = self.action_memory[batch]
            action_values = np.array(self.action_space, dtype=np.int8)
            action_indices = np.dot(action_batch, action_values)
            reward_batch = self.reward_memory[batch]
            terminal_batch = self.terminal_memory

            new_state_batch = state_batch.copy()

            q_eval = self.sess.run(self.q_values, feed_dict={self.input: state_batch})
            q_next = self.sess.run(self.q_values, feed_dict={self.input: new_state_batch})
            q_target = q_eval.copy()

            batch_index = np.arange(self.batch_size, dtype=np.int32)
            q_target[:, action_indices] = reward_batch + self.gamma*np.max(q_next, axis=1)*terminal_batch

            _ = self.sess.run(self.train_op, feed_dict={self.input: state_batch,
                                                        self.actions: action_batch,
                                                        self.old_q_value: q_target})

            self.e = self.e*self.epsilon_dec if self.e > self.epsilon_end else self.epsilon_end








