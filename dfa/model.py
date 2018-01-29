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

    hidden_state = tf.layers.dense(flatten, num_hidden, activation=tf.nn.relu)
    average_state = tf.reduce_mean(hidden_state, axis=0)
    print average_state.get_shape()

    # a brand new string w/o any label, just a string of 0 and 1
    self.new_strs = tf.placeholder(tf.float32, [None, L, N_CHAR])
    new_flatten = tf.reshape(self.new_strs, [tf.shape(self.new_strs)[0], L * N_CHAR])
    new_str_embedding = tf.layers.dense(new_flatten, num_hidden, activation=tf.nn.relu)

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

    self.optimizer = tf.train.AdamOptimizer(0.0001)
    self.train = self.optimizer.minimize(self.loss)

    initializer = tf.global_variables_initializer()
    self.session.run(initializer)

    self.saver = tf.train.Saver()

  def __init__(self, name):
    print "hello "
    self.name = name
    self.make_graph()

  def restore_model(self, path):
    self.saver.restore(self.session, path)
    print "model restored  from ", path

  # save the model
  def save(self):
    model_loc = "./models/" + self.name+".ckpt"
    sess = self.session
    save_path = self.saver.save(sess, model_loc)
    print("Model saved in file: %s" % save_path)

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

  def get_most_unlikely(self, observed, unobserved):
    observed_strs, observed_TFs = [x[0] for x in observed], [x[1] for x in observed]
    unobserved_strs, unobserved_TFs = [x[0] for x in unobserved], [x[1] for x in unobserved]
    all_preds = self.predict(observed_strs, observed_TFs, unobserved_strs)
    all_probs = [np.dot(x[0],x[1]) + random.random()*1e-5 for x in zip(all_preds, unobserved_TFs)]
    abc = zip(all_probs, unobserved)
    return sorted(abc)

  def get_until_confident(self, all_observations, increment=10, confidence=0.9):
    in_np, out_np = examples_to_numpy(all_observations)

    together =   zip(in_np, out_np) 
    observed =   [together[0]]
    unobserved = together[1:]

    unlikely = self.get_most_unlikely(observed, unobserved)

    def avg_confidence(unlikelies):
      return np.mean([x[0] for x in unlikelies])

    conf = []

    while avg_confidence(unlikely) < confidence:
      # print len(observed), len(unobserved), avg_confidence(unlikely)
      observed += [x[1] for x in unlikely[:increment]]
      unobserved = [x[1] for x in unlikely[increment:]]
      if len(unobserved) == 0: break
      unlikely = self.get_most_unlikely(observed, unobserved)
      conf.append(avg_confidence(unlikely))

    print conf
    return observed
    

if __name__ == "__main__":
  from gen import *
  oracle = Oracle("oracle")
  train_ob_in, train_ob_out, unob_in, unob_out = gen_train_data()

  oracle.restore_model("./models/oracle.ckpt")

  mmm = sample_matrix()
  eee = generate_examples(mmm, 1000)

  for i in range(1000000):
    if i % 100 == 1:
      preds = oracle.predict(train_ob_in, train_ob_out, unob_in)
      n_correct = 0
      for xxx in  zip(preds, unob_out):
        pp,tt = xxx
        if np.argmax(pp) == np.argmax(tt): n_correct += 1
      print n_correct, len(unob_out)

      confident_set = oracle.get_until_confident(eee)

      print "confident subset size ", len(confident_set)
      oracle.save()

    oracle.learn(*gen_train_data(n=1000))


