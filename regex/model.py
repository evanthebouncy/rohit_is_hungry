import tensorflow as tf
from data import L
import numpy as np

num_hidden = 50

class Oracle:

  def make_graph(self):
    self.session = tf.Session()
    print "making graph "
    # input any number of batch, total length up to L, each element is [(true/false),(0,1,pad)]
    # i.e. a tensor of None x L x (2+3)
    self.known_strs = tf.placeholder(tf.float32, [None, L, 5])

    flatten = tf.reshape(self.known_strs, [tf.shape(self.known_strs)[0], L*5])
    hidden_state = tf.layers.dense(flatten, num_hidden, activation=tf.nn.relu)
    average_state = tf.reduce_mean(hidden_state, axis=0)
    print average_state.get_shape()

    # a brand new string w/o any label, just a string of 0 and 1
    self.new_strs = tf.placeholder(tf.float32, [None, L, 3])
    new_flatten = tf.reshape(self.new_strs, [tf.shape(self.new_strs)[0], L*3])
    new_str_embedding = tf.layers.dense(new_flatten, num_hidden, activation=tf.nn.relu)

    average_state = tf.reshape(average_state, [1, -1])

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

  def learn(self, input_strings, new_strings, target_labels):
    loss_train = self.session.run([self.loss, self.train], 
                                   {
                                    self.known_strs: input_strings,
                                    self.new_strs: new_strings,
                                    self.out_labels: target_labels,
                                   }
                                  )
    # print "supervised loss ", loss_train[0]

  def predict(self, input_strings, new_strings):
    print input_strings.shape
    print new_strings.shape
    pred = self.session.run([self.pred_prob], 
                            {
                             self.known_strs: input_strings,
                             self.new_strs: new_strings,
                            }
                           )[0]
    return pred

if __name__ == "__main__":
  import data
  oracle = Oracle()
  train_data = data.gen_train_data()
  truths = train_data[2]

  preds = oracle.predict(train_data[0], train_data[1])
  print "prediction vs truth "
  for xxx in  zip(preds, truths):
    pp,tt = xxx
    print xxx, np.argmax(pp) == np.argmax(tt)


  for i in range(1000):
    oracle.learn(*train_data)

  preds = oracle.predict(train_data[0], train_data[1])
  print "prediction vs truth "
  for xxx in  zip(preds, truths):
    pp,tt = xxx
    print xxx, np.argmax(pp) == np.argmax(tt)



