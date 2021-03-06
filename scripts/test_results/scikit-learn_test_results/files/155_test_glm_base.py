import numpy as np
from numpy.testing import *
from nose.tools import *

from scikits.learn import glm

def test_toy():
    """Very simple test on a small dataset"""
    X = [[1, 0, -1.],
         [0, 0, 0],
         [0, 1, 1.]]
    Y = [1, 0, -1]

    clf = glm.LeastAngleRegression().fit(X, Y)
    assert_array_almost_equal(clf.coef_, [0, 0, -1.4142], decimal=4)
    assert_array_almost_equal(clf.alphas_.shape, clf.coef_path_.shape[1])
    assert_array_almost_equal(clf.predict(X), np.array(Y))

    # check that Lasso with coordinate descent finds the same coefficients
    clf2 = glm.Lasso().fit(X, Y)
    assert_array_almost_equal(clf.coef_, [0, 0, -1.4142], decimal=4)
    assert_array_almost_equal(clf.predict(X), np.array(Y))


def test_feature_selection():
    n_samples, n_features = 442, 100

    # deterministic test
    np.random.seed(0)

    # generate random input set
    X = np.random.randn(n_samples, n_features)

    # generate a ground truth model with only the first 10 features being non
    # zeros (the other features are not correlated to Y and should be ignored by
    # the L1 regularizer)
    coef_ = np.random.randn(n_features)
    coef_[10:] = 0.0

    # generate the grand truth Y from the model and Y
    Y = np.dot(X, coef_)
    Y += np.random.normal(Y.shape) # make some (label) noise!

    # fit the model assuming that will allready know that only 10 out of
    # n_features are contributing to Y
    clf = glm.LeastAngleRegression().fit(X, Y, n_features=10)

    # ensure that only the first 10 coefs are non zeros and the remaining set to
    # null, as in the ground thrutg model
    assert_equal((clf.coef_[:10] == 0.0).sum(), 0)
    assert_equal((clf.coef_[10:] != 0.0).sum(), 0)

    # train again, but this time without knowing in advance how many features
    # are useful:
    clf = glm.LeastAngleRegression().fit(X, Y, n_features=None)
    assert_equal((clf.coef_[:10] == 0.0).sum(), 0)
    assert_equal((clf.coef_[10:] != 0.0).sum(), 89)

    # explicitly set to zero parameters really close to zero (manual
    # thresholding)
    sparse_coef = np.where(abs(clf.coef_) < 1e-13,
                           np.zeros(clf.coef_.shape),
                           clf.coef_)

    # we find again that only the first 10 features are useful
    assert_equal((sparse_coef[:10] == 0.0).sum(), 0)
    assert_equal((sparse_coef[10:] != 0.0).sum(), 0)


