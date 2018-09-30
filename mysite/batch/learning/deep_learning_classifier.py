import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle
from . import BaseClassifier
 
sess = tf.Session()

class DeepLearner(BaseClassifier):

    def __init__(self):
        super().__init__()
        self.set_neural_network()

    def set_neural_network(self, input_dim = 0, n_layer1 = 10, n_layer2 = 10, learning_rate = 0.1):
        self.x = tf.placeholder(tf.float32, shape=[None, input_dim])   ### Input
        self.t = tf.placeholder(tf.float32, shape=[None, 1])
        self.keep_prob = tf.placeholder(tf.float32)   ### drop out 연결할 확률 (0~1사이)

        w1 = tf.Variable(tf.truncated_normal([input_dim, n_layer1]))
        b1 = tf.Variable(tf.zeros([n_layer1]))
        z1 = tf.nn.dropout(tf.nn.sigmoid(tf.matmul(self.x, w1)+b1), self.keep_prob)   ### Hidden layer 1

        w2 = tf.Variable(tf.truncated_normal([n_layer1, n_layer2]))
        b2 = tf.Variable(tf.zeros([n_layer2]))
        z2 = tf.nn.dropout(tf.nn.sigmoid(tf.matmul(z1, w2)+b2), self.keep_prob)   ### Hidden layer 2

        w3 = tf.Variable(tf.truncated_normal([n_layer2, 1]))
        b3 = tf.Variable(tf.zeros([1]))
        self.y = tf.nn.sigmoid(tf.matmul(z2, w3)+b3)   ### Output

        self.cross_ent = -tf.reduce_mean(self.t*tf.log(self.y) + (1-self.t)*tf.log(1-self.y))   ### Error function
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        self.train_step = optimizer.minimize(self.cross_ent)   ### Error의 Gradient Descendent 를 최소화

        correct_pred = tf.equal(tf.to_float(tf.greater(self.y, 0.5)), self.t)   ### y와 0.5의 값 비교 ( T, F 반환 )
        self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))   ### 정확도 측정 

        init = tf.global_variables_initializer()   ### tensorflow에서는 계산시 initialize 필요
        sess.run(init)

    def print_process(self, X, Y):
        self.model_accuracy= self.accuracy.eval(session=sess, feed_dict={self.x:X, self.t:Y, self.keep_prob:1.0})
        self.loss = self.cross_ent.eval(session=sess, feed_dict={self.x:X, self.t:Y, self.keep_prob:1.0})
        print("Accuracy :", self.model_accuracy, ",   Loss :", self.loss)

    def teach(self, X_train, Y_train, dropout_prob = 0.7, n_try = 100, batch_size = 16): 
        n_samples = X_train.shape[0]
        bch_size = batch_size   ### 보통 2^n 꼴로 정한다.
        n_batches = n_samples // bch_size

        for epoch in range(n_try):   ### n_try번 반복
            X_, Y_ = shuffle(X_train, Y_train)   ### 순서를 섞어준다.
            for i in range(n_batches):   ### batch마다 n_batches 번 학습
                start = i*bch_size
                end = start + bch_size
                sess.run(self.train_step, feed_dict={self.x:X_[start:end], self.t:Y_[start:end], self.keep_prob:dropout_prob})
            if epoch % 10 == 0:   ### 이건 그냥 잘 돌아가는지 판단하려고...
                self.print_process(X_train, Y_train)
                if np.isnan(self.loss):
                    break
        self.print_process(X_train, Y_train)

    def get_result(self):
        print("Accuracy :", self.model_accuracy, ",   Loss :", self.loss)

    def get_fitted_value(self, X_test):
        self.fitted_value = self.y.eval(session=sess, feed_dict={self.x:X_test, self.keep_prob:1.0})
        return self.fitted_value
