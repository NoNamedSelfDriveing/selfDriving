import tensorflow as tf
import os

class Model:
    def __init__(self):
        self.X = tf.placeholder("float", [None, 28, 28, 3])
        self.Y = tf.placeholder("float", [None, 4])

        self.w = self.init_weights([3, 3, 3, 64])
        self.w2 = self.init_weights([3, 3, 64, 128])
        self.w3 = self.init_weights([3, 3, 128, 800])
        self.w4 = self.init_weights([800 * 4 * 4, 625])
        self.w_o = self.init_weights([625, 4])

        self.p_keep_conv = tf.placeholder("float")
        self.p_keep_hidden = tf.placeholder("float")
        self.py_x = self.getModel(self.X, self.w, self.w2, self.w3, self.w4, self.w_o, self.p_keep_conv, self.p_keep_hidden)

        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.py_x, self.Y))
        self.train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(self.cost)
        self.predict_op = tf.argmax(self.py_x, 1)

        self.checkpoint_dir = "/home/potato/selfDriving/com/src/data/cps/"

        if not os.path.isdir(self.checkpoint_dir):
            os.mkdir(self.checkpoint_dir)

        self.saver = tf.train.Saver()

    def init_weights(self, shape):
        return tf.Variable(tf.random_normal(shape, stddev=0.01))

    def getModel(self, X, w, w2, w3, w4, w_o, p_keep_conv, p_keep_hidden):
        l1a = tf.nn.relu(tf.nn.conv2d(X, w,                       # l1a shape=(?, 28, 28, 32)
                            strides=[1, 1, 1, 1], padding='SAME'))
        l1 = tf.nn.max_pool(l1a, ksize=[1, 2, 2, 1],              # l1 shape=(?, 14, 14, 32)
                            strides=[1, 2, 2, 1], padding='SAME')

        l1 = tf.nn.dropout(l1, p_keep_conv)
        l2a = tf.nn.relu(tf.nn.conv2d(l1, w2,                     # l2a shape=(?, 14, 14, 64)
                            strides=[1, 1, 1, 1], padding='SAME'))
        l2 = tf.nn.max_pool(l2a, ksize=[1, 2, 2, 1],              # l2 shape=(?, 7, 7, 64)
                            strides=[1, 2, 2, 1], padding='SAME')
        l2 = tf.nn.dropout(l2, p_keep_conv)

        l3a = tf.nn.relu(tf.nn.conv2d(l2, w3,                     # l3a shape=(?, 7, 7, 128)
                            strides=[1, 1, 1, 1], padding='SAME'))
        l3 = tf.nn.max_pool(l3a, ksize=[1, 2, 2, 1],              # l3 shape=(?, 4, 4, 128)
                            strides=[1, 2, 2, 1], padding='SAME')
        l3 = tf.reshape(l3, [-1, w4.get_shape().as_list()[0]])    # reshape to (?, 2048)
        l3 = tf.nn.dropout(l3, p_keep_conv)

        l4 = tf.nn.relu(tf.matmul(l3, w4))
        l4 = tf.nn.dropout(l4, p_keep_hidden)

        pyx = tf.matmul(l4, w_o)
        return pyx

    def loadLearning(self, sess):
        ckpt = tf.train.get_checkpoint_state(self.checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            print ('load learning')
            self.saver.restore(sess, ckpt.model_checkpoint_path)

    def saveLearning(self, sess):
        self.saver.save(sess, self.checkpoint_dir + 'model.ckpt')
