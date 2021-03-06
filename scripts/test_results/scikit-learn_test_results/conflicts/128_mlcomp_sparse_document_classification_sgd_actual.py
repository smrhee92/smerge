"""
======================================================
Classification of text documents using sparse features
======================================================

This is an example showing how the scikit-learn can be used to classify
documents by topics using a bag-of-words approach. This example uses
a scipy.sparse matrix to store the features instead of standard numpy arrays.

The dataset used in this example is the 20 newsgroups dataset and should be
downloaded from the http://mlcomp.org (free registration required):

  http://mlcomp.org/datasets/379

Once downloaded unzip the arhive somewhere on your filesystem. For instance in::

  % mkdir -p ~/data/mlcomp
  % cd  ~/data/mlcomp
  % unzip /path/to/dataset-379-20news-18828_XXXXX.zip

You should get a folder ``~/data/mlcomp/379`` with a file named ``metadata`` and
subfolders ``raw``, ``train`` and ``test`` holding the text documents organized by
newsgroups.

Then set the ``MLCOMP_DATASETS_HOME`` environment variable pointing to
the root folder holding the uncompressed archive::

  % export MLCOMP_DATASETS_HOME="~/data/mlcomp"

Then you are ready to run this example using your favorite python shell::

  % ipython examples/mlcomp_sparse_document_classification.py

"""
# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

from time import time
from time import time
import sys
import sys
import os
import os
import numpy as np
import numpy as np
# import pylab as pl

from scikits.learn.datasets import load_mlcomp
from scikits.learn.datasets import load_mlcomp
from scikits.learn.metrics import confusion_matrix
from scikits.learn.metrics import confusion_matrix

# from scikits.learn.svm.sparse import LinearSVC
from scikits.learn.sgd.sparse import SGD
from scikits.learn.sgd.sparse import SGD


if 'MLCOMP_DATASETS_HOME' not in os.environ:
# Load the training set
print "Loading 20 newsgroups training set... "
t0 = time()
news_train = load_mlcomp('20news-18828', 'train', sparse=True)
print "done in %fs" % (time() - t0)

print "Creating binary classification task\n"\
      "alt.atheism vs. comp.graphics"
target = news_train.target
pos = 0 # alt.atheism
neg = 1 # comp.graphics
pos_idx = np.where(target == pos)[0]
neg_idx = np.where(target == neg)[0]
idx = np.concatenate((pos_idx, neg_idx))
np.random.seed(13)
np.random.shuffle(idx)
data = news_train.data[idx]
target = news_train.target[idx]

print "num train docs: ", data.shape[0]
print ""
<<<<<<< REMOTE
print "Training a linear SVM (hinge loss and L2 regularizer) using SGD:"
=======
print "Training a linear SVM (hinge loss and L2 regularizer) using SGD.\n"\
      "SGD(n_iter=50, alpha=0.00001, fit_intercept=True)"
>>>>>>> LOCAL
<<<<<<< REMOTE

=======
t0 = time()
>>>>>>> LOCAL
clf = SGD(n_iter=50, alpha=0.00001, fit_intercept=True)
<<<<<<< REMOTE
print clf
=======
#clf = LinearSVC(**parameters)
>>>>>>> LOCAL
<<<<<<< REMOTE

=======
clf.fit(data, target)
>>>>>>> LOCAL
<<<<<<< REMOTE
clf.fit(data, target)
=======
print "done in %fs" % (time() - t0)
>>>>>>> LOCAL
<<<<<<< REMOTE
print "done in %fs" % (time() - t0)
=======
print "Percentage of non zeros coef: %f" % (np.mean(clf.coef_ != 0) * 100)
>>>>>>> LOCAL
<<<<<<< REMOTE
print "Percentage of non zeros coef: %f" % (np.mean(clf.coef_ != 0) * 100)
=======

>>>>>>> LOCAL
<<<<<<< REMOTE

=======
print "Loading 20 newsgroups test set... "
>>>>>>> LOCAL
<<<<<<< REMOTE
print "Loading 20 newsgroups test set... "
=======
t0 = time()
>>>>>>> LOCAL
<<<<<<< REMOTE
t0 = time()
=======
news_test = load_mlcomp('20news-18828', 'test', sparse=True)
>>>>>>> LOCAL
<<<<<<< REMOTE
news_test = load_mlcomp('20news-18828', 'test', sparse=True)
=======
print "done in %fs" % (time() - t0)
>>>>>>> LOCAL
<<<<<<< REMOTE
print "done in %fs" % (time() - t0)
=======

>>>>>>> LOCAL
<<<<<<< REMOTE

=======
target = news_test.target
>>>>>>> LOCAL
<<<<<<< REMOTE
target = news_test.target
=======
pos_idx = np.where(target == pos)[0]
>>>>>>> LOCAL
<<<<<<< REMOTE
pos_idx = np.where(target == pos)[0]
=======
neg_idx = np.where(target == neg)[0]
>>>>>>> LOCAL
<<<<<<< REMOTE
neg_idx = np.where(target == neg)[0]
=======
idx = np.concatenate((pos_idx, neg_idx))
>>>>>>> LOCAL
<<<<<<< REMOTE
idx = np.concatenate((pos_idx, neg_idx))
=======
data = news_test.data[idx]
>>>>>>> LOCAL
<<<<<<< REMOTE
data = news_test.data[idx]
=======
target = news_test.target[idx]
>>>>>>> LOCAL
<<<<<<< REMOTE
target = news_test.target[idx]
=======

>>>>>>> LOCAL
<<<<<<< REMOTE

=======
print "Predicting the labels of the test set..."
>>>>>>> LOCAL
<<<<<<< REMOTE
print "Predicting the labels of the test set..."
=======
t0 = time()
>>>>>>> LOCAL
<<<<<<< REMOTE
t0 = time()
=======
pred = clf.predict(data)
>>>>>>> LOCAL
<<<<<<< REMOTE
pred = clf.predict(data)
=======
print "done in %fs" % (time() - t0)
>>>>>>> LOCAL
<<<<<<< REMOTE
print "done in %fs" % (time() - t0)
=======
print "Classification accuracy: %f" % (np.mean(pred == target) * 100)
>>>>>>> LOCAL
<<<<<<< REMOTE
print "Classification accuracy: %f" % (np.mean(pred == target) * 100)
=======

>>>>>>> LOCAL
<<<<<<< REMOTE

=======
cm = confusion_matrix(target, pred)
>>>>>>> LOCAL
<<<<<<< REMOTE
cm = confusion_matrix(target, pred)
=======
print "Confusion matrix:"
>>>>>>> LOCAL
<<<<<<< REMOTE
print "Confusion matrix:"
=======
print cm
>>>>>>> LOCAL
<<<<<<< REMOTE
print cm
=======

>>>>>>> LOCAL
<<<<<<< REMOTE

=======
## # Show confusion matrix
>>>>>>> LOCAL
<<<<<<< REMOTE
## # Show confusion matrix
=======
## pl.matshow(cm)
>>>>>>> LOCAL
<<<<<<< REMOTE
## pl.matshow(cm)
=======
## pl.title('Confusion matrix')
>>>>>>> LOCAL
<<<<<<< REMOTE
## pl.title('Confusion matrix')
=======
## pl.colorbar()
>>>>>>> LOCAL
<<<<<<< REMOTE
## pl.colorbar()
=======
## pl.show()
>>>>>>> LOCAL
## pl.show()

