# Recurrent Neural Network
#-*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import sys

from TraningImg import makeTraningSet

x_data, y_data = makeTraningSet(sys.argv[1], sys.argv[2])
x_data = np.array(x_data ,dtype = 'f')

print y_data

# Configuration
rnn_size = 4 # 1 hot coding (one of 4) output size
time_step_size = 10  # 'hell' -> predict 'ello'
batch_size = x_data.shape[0] / 10  # (x_data.len / 10) sample

rnn_cell = tf.nn.rnn_cell.BasicRNNCell(rnn_size) # RNN cell을 생성 rnn_size는 output 갯수
state = tf.zeros([batch_size, rnn_cell.state_size])
X_split = tf.split(0, time_step_size, x_data)
outputs, state = tf.nn.rnn(rnn_cell, X_split, state)
#rnn_cell을 사용 그것의 입력 백터로 X_split을 사용 rnn은 이전 state를 입력받아 연산
#X_split의 0번 index는 batch_size 1번 인덱스은 글자 4개중 하나 hot encoding한것


logits = tf.reshape(tf.concat(1, outputs), [-1, rnn_size])
targets = tf.reshape(y_data[:], [-1])
weights = tf.ones([time_step_size * batch_size])

print logits
print targets
print weights

loss = tf.nn.seq2seq.sequence_loss_by_example([logits], [targets], [weights])
cost = tf.reduce_sum(loss) / batch_size
train_op = tf.train.RMSPropOptimizer(0.01, 0.9).minimize(cost)

with tf.Session() as sess:
    # you need to initialize all variables
    tf.initialize_all_variables().run()
    for i in range(10000):
        sess.run(train_op)
        print sess.run(cost)
        result = sess.run(tf.arg_max(logits, 1))
