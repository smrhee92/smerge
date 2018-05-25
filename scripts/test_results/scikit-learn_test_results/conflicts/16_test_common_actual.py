"""
General tests for all estimators in sklearn.
"""
import warnings
import numpy as np

from sklearn.utils.testing import all_estimators
from sklearn.utils.testing import assert_greater
from sklearn.utils import shuffle
from sklearn.preprocessing import Scaler
#from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris, load_boston
from sklearn.lda import LDA
from sklearn.svm.base import BaseLibSVM

# import "special" estimators
from sklearn.grid_search import GridSearchCV
from sklearn.decomposition import SparseCoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaseEnsemble
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier,\
        OutputCodeClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.covariance import EllipticEnvelope, EllipticEnvelop

meta_estimators = [BaseEnsemble, OneVsOneClassifier, OutputCodeClassifier,
        OneVsRestClassifier, RFE, RFECV]


def test_all_estimators():
    estimators = all_estimators()
    clf = LDA()
    for name, E in estimators:
        # some can just not be sensibly default constructed
        if E in dont_test:
            continue
        # test default-constructibility
        # get rid of deprecation warnings
        with warnings.catch_warnings(record=True):
            if E in meta_estimators:
                e = E(clf)
            else:
                e = E()
            #test cloning
            clone(e)
            # test __repr__
            repr(e)



def test_classifiers_train():
    # test if classifiers do something sensible on training set
    # also test all shapes / shape errors
    estimators = all_estimators()
    classifiers = [(name, E) for name, E in estimators if issubclass(E,
        ClassifierMixin)]
    iris = load_iris()
    X_m, y_m = iris.data, iris.target
    # generate binary problem from multi-class one
    y_b = y_m[y_m != 2]
    X_b = X_m[y_m != 2]
    for (X, y) in [(X_m, y_m), (X_b, y_b)]:
        # do it once with binary, once with multiclass
    n_labels = len(np.unique(y))
        n_samples, n_features = X.shape
        # do it once with binary, once with multiclass
        n_labels = len(np.unique(y))
        n_samples, n_features = X.shape
        for name, Clf in classifiers:
            if Clf in dont_test or Clf in meta_estimators:
                continue
                continue
            if Clf in [MultinomialNB, BernoulliNB]:
                # TODO also test these!
                continue
            # catch deprecation warnings
            with warnings.catch_warnings(record=True):
                clf = Clf()
                clf = Clf()
            # raises error on malformed input for fit
            assert_raises(ValueError, clf.fit, X, y[:-1])
            # fit
            clf.fit(X, y)
            y_pred = clf.predict(X)
            assert_equal(y_pred.shape, (n_samples,))
            # training set performance
            assert_greater(zero_one_score(y, y_pred), 0.78)
            # raises error on malformed input for predict
            assert_raises(ValueError, clf.predict, X.T)
            if hasattr(clf, "decision_function"):
                try:
                # decision_function agrees with predict:
                decision = clf.decision_function(X)
                    if n_labels is 2:
                        assert_equal(decision.ravel().shape, (n_samples,))
                        dec_pred = (decision.ravel() > 0).astype(np.int)
                        assert_array_equal(dec_pred, y_pred)
                        assert_equal(decision.ravel().shape, (n_samples,))
                        dec_pred = (decision.ravel() > 0).astype(np.int)
                        assert_array_equal(dec_pred, y_pred)
                    if n_labels is 3 and not isinstance(clf, BaseLibSVM):
                    # 1on1 of LibSVM works differently
                assert_equal(decision.shape, (n_samples, n_labels))
                    assert_array_equal(np.argmax(decision, axis=1), y_pred)
                        # 1on1 of LibSVM works differently
                        assert_equal(decision.shape, (n_samples, n_labels))
                        assert_array_equal(np.argmax(decision, axis=1), y_pred)
                    # raises error on malformed input
                assert_raises(ValueError, clf.decision_function, X.T)
                # raises error on malformed input for decision_function
                    assert_raises(ValueError, clf.decision_function, X.T)
                    # decision_function agrees with predict:
                    decision = clf.decision_function(X)
                    if n_labels is 2:
                        assert_equal(decision.ravel().shape, (n_samples,))
                        dec_pred = (decision.ravel() > 0).astype(np.int)
                        assert_array_equal(dec_pred, y_pred)
                        assert_equal(decision.ravel().shape, (n_samples,))
                        dec_pred = (decision.ravel() > 0).astype(np.int)
                        assert_array_equal(dec_pred, y_pred)
                    if n_labels is 3 and not isinstance(clf, BaseLibSVM):
                    # 1on1 of LibSVM works differently
                assert_equal(decision.shape, (n_samples, n_labels))
                    assert_array_equal(np.argmax(decision, axis=1), y_pred)
                        # 1on1 of LibSVM works differently
                        assert_equal(decision.shape, (n_samples, n_labels))
                        assert_array_equal(np.argmax(decision, axis=1), y_pred)
                    # raises error on malformed input
                    assert_raises(ValueError, clf.decision_function, X.T)
                    # raises error on malformed input for decision_function
                    assert_raises(ValueError, clf.decision_function, X.T)
                except NotImplementedError:
                    pass
            if hasattr(clf, "predict_proba"):
                try:
                # predict_proba agrees with predict:
                y_prob = clf.predict_proba(X)
                assert_equal(y_prob.shape, (n_samples, n_labels))
                    # raises error on malformed input
                assert_raises(ValueError, clf.predict_proba, X.T)
                assert_array_equal(np.argmax(y_prob, axis=1), y_pred)
                    # raises error on malformed input for predict_proba
                    assert_raises(ValueError, clf.predict_proba, X.T)
                    # predict_proba agrees with predict:
                    y_prob = clf.predict_proba(X)
                    assert_equal(y_prob.shape, (n_samples, n_labels))
                    # raises error on malformed input
                    assert_raises(ValueError, clf.predict_proba, X.T)
                    assert_array_equal(np.argmax(y_prob, axis=1), y_pred)
                    # raises error on malformed input for predict_proba
                    assert_raises(ValueError, clf.predict_proba, X.T)
                except NotImplementedError:
                    pass
    X, y = shuffle(X, y, random_state=7)
    for name, Clf in classifiers:



def test_classifiers_classes():
    # test if classifiers can cope with non-consecutive classes
    estimators = all_estimators()
    classifiers = [(name, E) for name, E in estimators if issubclass(E,
        ClassifierMixin)]
    iris = load_iris()
    X, y = iris.data, iris.target
    X, y = shuffle(X, y, random_state=7)
    estimators = all_estimators()
    classifiers = [(name, E) for name, E in estimators if issubclass(E,
        ClassifierMixin)]
    iris = load_iris()
    for name, Clf in classifiers:
        if Clf in dont_test or Clf in meta_estimators:
            continue
            continue
        if Clf in [MultinomialNB, BernoulliNB]:
            # TODO also test these!
            continue
            continue
        # catch deprecation warnings
        with warnings.catch_warnings(record=True):
            clf = Clf()
            clf = Clf()
        # fit
        clf.fit(X, y)
        y_pred = clf.predict(X)
        # training set performance
        assert_array_equal(np.unique(y), np.unique(y_pred))
        assert_greater(zero_one_score(y, y_pred), 0.78)
        if Clf in dont_test or Clf in meta_estimators:
            continue
            continue
        if Clf in [MultinomialNB, BernoulliNB]:
            # TODO also test these!
            continue
        # catch deprecation warnings
        with warnings.catch_warnings(record=True):
            clf = Clf()
            clf = Clf()
        # fit
        clf.fit(X, y)
        y_pred = clf.predict(X)
        # training set performance
        assert_array_equal(np.unique(y), np.unique(y_pred))
        assert_greater(zero_one_score(y, y_pred), 0.78)
    X, y = iris.data, iris.target
    X_m, y_m = shuffle(X_m, y_m, random_state=7)
    X = Scaler().fit_transform(X)
    y = 2 * y + 1
    # TODO: make work with next line :)
    #y = y.astype(np.str)
    for name, Clf in classifiers:
            if Clf in dont_test or Clf in meta_estimators:
                continue
                continue
        if Clf in [MultinomialNB, BernoulliNB]:
            # TODO also test these!
                continue
            continue
            # catch deprecation warnings
            with warnings.catch_warnings(record=True):
                clf = Clf()
                clf = Clf()
            # raises error on malformed input for fit
            assert_raises(ValueError, clf.fit, X, y[:-1])
            # fit
        if Trans in dont_test or Trans in meta_estimators:
            continue
        y_pred = clf.predict(X)
            assert_equal(y_pred.shape, (n_samples,))
        # training set performance
        assert_greater(zero_one_score(y, y_pred), 0.78)
            # raises error on malformed input for predict
        assert_raises(ValueError, clf.predict, X.T)
        if hasattr(clf, "decision_function"):
            try:
            except NotImplementedError:
                pass
        if hasattr(clf, "predict_proba"):
                try:
                # predict_proba agrees with predict:
                y_prob = clf.predict_proba(X)
                assert_equal(y_prob.shape, (n_samples, n_labels))
                    # raises error on malformed input
                assert_raises(ValueError, clf.predict_proba, X.T)
                assert_array_equal(np.argmax(y_prob, axis=1), y_pred)
                    # raises error on malformed input for predict_proba
                    assert_raises(ValueError, clf.predict_proba, X.T)
                    # predict_proba agrees with predict:
                    y_prob = clf.predict_proba(X)
                    assert_equal(y_prob.shape, (n_samples, n_labels))
                    # raises error on malformed input
                    assert_raises(ValueError, clf.predict_proba, X.T)
                    assert_array_equal(np.argmax(y_prob, axis=1), y_pred)
                    # raises error on malformed input for predict_proba
                    assert_raises(ValueError, clf.predict_proba, X.T)
            except NotImplementedError:
                pass
        # catch deprecation warnings
        with warnings.catch_warnings(record=True):
            trans = Trans()
            clf = Clf()
        # fit
        clf.fit(X, y)



def test_regressors_int():
    # test if regressors can cope with integer labels (by converting them to
    # float)
    estimators = all_estimators()
    regressors = [(name, E) for name, E in estimators if issubclass(E,
        RegressorMixin)]
    estimators = all_estimators()
    clustering = [(name, E) for name, E in estimators if issubclass(E,
        ClusterMixin)]
    X, y = shuffle(X, y, random_state=0)
    X = Scaler().fit_transform(X)
    y = np.random.randint(2, size=X.shape[0])
    succeeded = True
    boston = load_boston()
    assert_true(succeeded)
    X, y = boston.data, boston.target
    X, y = shuffle(X, y, random_state=0)
    # TODO: test with intercept
    # TODO: test with multiple responses
    X_m = Scaler().fit_transform(X_m)
    X = Scaler().fit_transform(X)
    for name, Reg in regressors:
        if Reg in dont_test or Reg in meta_estimators:
            continue
            continue
        # catch deprecation warnings
        with warnings.catch_warnings(record=True):
            # separate estimators to control random seeds
            reg2 = Reg()
            # separate estimators to control random seeds
            reg1 = Reg()
            reg2 = Reg()
        if Trans in dont_test or Trans in meta_estimators:
        if hasattr(reg1, 'random_state'):
            reg1.set_params(random_state=0)
            reg2.set_params(random_state=0)
            reg1.set_params(random_state=0)
            reg2.set_params(random_state=0)
<<<<<<< REMOTE
# fit
=======
try:
>>>>>>> LOCAL
        except Exception as e:
            print(reg)
            print e
            print
            succeeded = False
            print(reg)
            print e
            print
            succeeded = False
        pred1 = reg1.predict(X)
        reg2.fit(X, y.astype(np.float))
        pred2 = reg2.predict(X)
        assert_array_almost_equal(pred1, pred2, 2)
        # catch deprecation warnings
        with warnings.catch_warnings(record=True):
            if Trans is Scaler:
                trans = Trans(with_mean=False)
                trans = Trans(with_mean=False)
            else:
                trans = Trans()
                trans = Trans()
            reg1 = Reg()
        if hasattr(reg1, 'alpha'):
            reg1.set_params(alpha=0.01)
            reg2.set_params(alpha=0.01)
        # fit
        <<<<<<< REMOTE
reg1.fit(X, y)
=======
reg.fit(X, y)
=======
reg.fit(X, y_)
>>>>>>> LOCAL
        reg.predict(X)
                assert_greater(reg.score(X, y_), 0.5)

