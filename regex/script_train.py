from data import *
from model import *

oracle = Oracle()

for i in range(10000):
  train_data = gen_train_data()
  oracle.learn(*train_data)

  if i % 20 == 0:
    truths = train_data[2]

    preds = oracle.predict(train_data[0], train_data[1])
    print "prediction vs truth "
    for xxx in  zip(preds, truths):
      pp,tt = xxx
      print xxx, np.argmax(pp) == np.argmax(tt)

