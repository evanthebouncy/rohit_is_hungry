from model import *
from gen import *
import pickle

def make_test_data():
  to_store = [gen_train_data() for _ in range(100)]
  pickle.dump( to_store, open( "./data/data_test_model.p", "wb" ) )

def compute_accuracy(oracle, test_data):
  acc = 0.0
  for t_data in test_data:
    train_ob_in, train_ob_out, unob_in, unob_out = t_data
    preds = oracle.predict(train_ob_in, train_ob_out, unob_in)
    n_correct = 0
    for xxx in  zip(preds, unob_out):
      pp,tt = xxx
      if np.argmax(pp) == np.argmax(tt): n_correct += 1
    acc += float(n_correct) / len(unob_out)
  return acc / len(test_data)

if __name__ == "__main__":
  # make_test_data()
  test_data = pickle.load( open( "./data/data_test_model.p", "rb" ) )
  oracle = Oracle()

  for i in range(10000):
    if i % 100 == 1:
      acc = compute_accuracy(oracle, test_data)
      print acc

    oracle.learn(*gen_train_data())
