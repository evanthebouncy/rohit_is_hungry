import tensorflow as tf
from gen import L, N_CHAR, N_STATES 
import numpy as np

num_hidden = 1000

class Oracle:

  def make_graph(self):
    self.session = tf.Session()
    print "making graph "
    self.observed_strs = tf.placeholder(tf.float32, [None, L, N_CHAR])
    self.observed_TFs  = tf.placeholder(tf.float32, [None, 2])

    flatten_strs = tf.reshape(self.observed_strs, [tf.shape(self.observed_strs)[0], L*N_CHAR])
    print flatten_strs.get_shape()
    flatten_TFs  = self.observed_TFs
    print flatten_TFs.get_shape()

    flatten = tf.concat([flatten_strs, flatten_TFs], 1)
    print flatten.get_shape()

    hidden_states = tf.layers.dense(flatten, num_hidden, activation=tf.nn.relu)

    # a brand new string w/o any label
    self.new_strs = tf.placeholder(tf.float32, [None, L, N_CHAR])
    new_flatten = tf.reshape(self.new_strs, [tf.shape(self.new_strs)[0], L * N_CHAR])
    new_str_embedding = tf.layers.dense(new_flatten, num_hidden, activation=tf.nn.relu)

    print "some book keepings here"
    print new_str_embedding.get_shape()
    print hidden_states.get_shape()
    assert 0

    # a soft attention weight
    soft_attn_weight_matrix = tf.Variable(tf.random_normal([num_hidden*2, 1], mean=0.1, stddev=0.035))

    # do attention here 
    attn_weights = "ho"

    average_state = tf.reduce_mean(hidden_state, axis=0)
    print average_state.get_shape()


    average_state = tf.reshape(average_state, [1, -1])
    print average_state.get_shape()

    # tiled_average = tf.tile(average_state, (10,1)) 
    tiled_average = tf.tile(average_state, (tf.shape(new_str_embedding)[0],1)) 
    
    together = tf.concat([tiled_average, new_str_embedding], 1)
    # together = tf.reshape(together, [1, num_hidden * 2])
    together = tf.layers.dense(together, num_hidden * 2, activation=tf.nn.relu)
    print together.get_shape()

    self.prediction = tf.layers.dense(together, 2)
    self.pred_prob = tf.nn.softmax(self.prediction)
    print self.pred_prob.get_shape()

    # the labeled truth
    self.out_labels = tf.placeholder(tf.float32, [None, 2])

    # add a small number so it doesn't blow up (logp or in action selection)
    self.pred_prob = self.pred_prob + 1e-8

    # set up the cost function for training
    self.log_pred_prob = tf.log(self.pred_prob)
    self.objective = tf.reduce_mean(self.log_pred_prob * self.out_labels)

    self.loss = -self.objective

    self.optimizer = tf.train.AdamOptimizer(0.001)
    self.train = self.optimizer.minimize(self.loss)

    initializer = tf.global_variables_initializer()
    self.session.run(initializer)

    self.saver = tf.train.Saver()

  def __init__(self):
    print "hello "
    self.make_graph()

  def restore_model(self, path):
    self.saver.restore(self.session, path)
    print "model restored  from ", path

  def learn(self, observed_strs, observed_TFs, new_strs, new_TFs):
    loss_train = self.session.run([self.loss, self.train], 
                                   {
                                    self.observed_strs: observed_strs,
                                    self.observed_TFs: observed_TFs,
                                    self.new_strs: new_strs,
                                    self.out_labels: new_TFs,
                                   }
                                  )
    # print "supervised loss OB_SIZE:", len(observed_TFs), " LOSS: ", loss_train[0]

  def predict(self, observed_strs, observed_TFs, new_strs):
    pred = self.session.run([self.pred_prob], 
                            {
                              self.observed_strs: observed_strs,
                              self.observed_TFs: observed_TFs,
                              self.new_strs: new_strs,
                            }
                           )[0]
    return pred

if __name__ == "__main__":
  from gen import *
  oracle = Oracle()
  train_ob_in, train_ob_out, unob_in, unob_out = gen_train_data()

  preds = oracle.predict(train_ob_in, train_ob_out, unob_in)
  print "prediction vs truth "
  n_correct = 0
  for xxx in  zip(preds, unob_out):
    pp,tt = xxx
    print xxx, np.argmax(pp) == np.argmax(tt)
    if np.argmax(pp) == np.argmax(tt): n_correct += 1
  print n_correct, len(unob_out)

  for i in range(10000):
    if i % 100 == 1:
      preds = oracle.predict(train_ob_in, train_ob_out, unob_in)
      n_correct = 0
      for xxx in  zip(preds, unob_out):
        pp,tt = xxx
        if np.argmax(pp) == np.argmax(tt): n_correct += 1
      print n_correct, len(unob_out)

    oracle.learn(*gen_train_data())
    # oracle.learn(train_ob_in, train_ob_out, unob_in, unob_out)

  preds = oracle.predict(train_ob_in, train_ob_out, unob_in)
  n_correct = 0
  for xxx in  zip(preds, unob_out):
    pp,tt = xxx
    print xxx, np.argmax(pp) == np.argmax(tt)
    if np.argmax(pp) == np.argmax(tt): n_correct += 1
  print n_correct, len(unob_out)



