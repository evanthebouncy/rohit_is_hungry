from model import *
from gen import *
import pickle

VAL_LOC = "./data/data_vallidation.p"

def make_test_data():
  to_store = [gen_train_data(500) for _ in range(1000)]
  pickle.dump( to_store, open( VAL_LOC, "wb" ) )

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
  # make the test data
  # make_test_data()
  # assert 0

  test_data = pickle.load( open( VAL_LOC, "rb" ) )

  from gen import *
  oracle = Oracle("oracle")
  oracle.restore_model("./models/oracle.ckpt")
  best_acc = 0.0

  # for a long ass time
  for i in range(1000000):
    # do some learning 
    oracle.learn(*gen_train_data(n=500))
    if i % 100 == 1:
      acc = compute_accuracy(oracle, test_data)
      if acc > best_acc:
        print "acc improved to : ", acc
        best_acc = acc
        oracle.save()

