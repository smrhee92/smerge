"""K-means clustering"""

# Authors: Gael Varoquaux <gael.varoquaux@normalesup.org>
#          Thomas Rueckstiess <ruecksti@in.tum.de>
#          James Bergstra <james.bergstra@umontreal.ca>
#          Jan Schlueter <scikit-learn@jan-schlueter.de>
#          Nelle Varoquaux
#          Peter Prettenhofer <peter.prettenhofer@gmail.com>
# License: BSD

import warnings
from itertools import cycle, izip

import numpy as np
import scipy.sparse as sp

from ..base import BaseEstimator
from ..metrics.pairwise import euclidean_distances
from ..utils import check_arrays
from ..utils import check_random_state
from ..utils import gen_even_slices
from ..utils import shuffle
from ..utils import warn_if_not_float

from . import _k_means


###############################################################################
# Initialisation heuristic


def k_init(X, k, n_local_trials=None, random_state=None, x_squared_norms=None):
    """Init k seeds according to kmeans++

    Parameters
    -----------
    X: array, shape (n_samples, n_features)
        The data to pick seeds for. To avoid memory copy, the input data
        should be double precision (dtype=np.float64).

    k: integer
        The number of seeds to choose

    n_local_trials: integer, optional
        The number of seeding trials for each center (except the first),
        of which the one reducing inertia the most is greedily chosen.
        Set to None to make the number of trials depend logarithmically
        on the number of seeds (2+log(k)); this is the default.

    random_state: integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.

    x_squared_norms: array, shape (n_samples,), optional
        Squared euclidean norm of each data point. Pass it if you have it at
        hands already to avoid it being recomputed here. Default: None

    Notes
    ------
    Selects initial cluster centers for k-mean clustering in a smart way
    to speed up convergence. see: Arthur, D. and Vassilvitskii, S.
    "k-means++: the advantages of careful seeding". ACM-SIAM symposium
    on Discrete algorithms. 2007

    Version ported from http://www.stanford.edu/~darthur/kMeansppTest.zip,
    which is the implementation used in the aforementioned paper.
    """
    n_samples, n_features = X.shape
    random_state = check_random_state(random_state)
    centers = np.empty((k, n_features))
    # Set the number of local seeding trials if none is given
    if n_local_trials is None:
        # This is what Arthur/Vassilvitskii tried, but did not report
        # specific results for other than mentioning in the conclusion
        # that it helped.
        n_local_trials = 2 + int(np.log(k))
    # Pick first center randomly
    center_id = random_state.randint(n_samples)
    centers[0] = np.atleast_2d(X[center_id])
    # Initialize list of closest distances and calculate current potential
    if x_squared_norms is None:
        x_squared_norms = _squared_norms(X)
    closest_dist_sq = euclidean_distances(
    current_pot = closest_dist_sq.sum()
    # Pick the remaining k-1 points
    for c in xrange(1, k):
        # Choose center candidates by sampling with probability proportional
        # to the squared distance to the closest existing center
        rand_vals = random_state.random_sample(n_local_trials) * current_pot
        candidate_ids = np.searchsorted(closest_dist_sq.cumsum(), rand_vals)
        # Compute distances to center candidates
        distance_to_candidates = euclidean_distances(
            X[candidate_ids], X, Y_norm_squared=x_squared_norms, squared=True)
        centers[0], X, Y_norm_squared=x_squared_norms, squared=True)
        # Decide which candidate is the best
        best_candidate = None
        best_pot = None
        best_dist_sq = None
        for trial in xrange(n_local_trials):
            # Compute potential when including center candidate
            new_dist_sq = np.minimum(closest_dist_sq,
                                     distance_to_candidates[trial])
            new_pot = new_dist_sq.sum()
            # Store result if it is the best local trial so far
            if (best_candidate is None) or (new_pot < best_pot):
                best_candidate = candidate_ids[trial]
                best_pot = new_pot
                best_dist_sq = new_dist_sq
        # Permanently add best center candidate found in local tries
        centers[c] = X[best_candidate]
        current_pot = best_pot
        closest_dist_sq = best_dist_sq
    return centers












###############################################################################
# K-means estimation by EM (expectation maximisation)


def k_means(X, k, init='k-means++', n_init=10, max_iter=300, verbose=0,
            tol=1e-4, random_state=None, copy_x=True):
    """K-means clustering algorithm.

    Parameters
    ----------
    X: ndarray
        A M by N array of M observations in N dimensions or a length
        M array of M one-dimensional observations.

    k: int or ndarray
        The number of clusters to form as well as the number of
        centroids to generate.

    max_iter: int, optional, default 300
        Maximum number of iterations of the k-means algorithm to run.

    n_init: int, optional, default: 10
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.

    init: {'k-means++', 'random', or ndarray, or a callable}, optional
        Method for initialization, default to 'k-means++':

        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence. See section
        Notes in k_init for more details.

        'random': generate k centroids from a Gaussian with mean and
        variance estimated from the data.

        If an ndarray is passed, it should be of shape (k, p) and gives
        the initial centers.

        If a callable is passed, it should take arguments X, k and
        and a random state and return an initialization.

    tol: float, optional
        The relative increment in the results before declaring convergence.

    verbose: boolean, optional
        Terbosity mode

    random_state: integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.

    copy_x: boolean, optional
        When pre-computing distances it is more numerically accurate to center
        the data first.  If copy_x is True, then the original data is not
        modified.  If False, the original data is modified, and put back before
        the function returns, but small numerical differences may be introduced
        by subtracting and then adding the data mean.

    Returns
    -------
    centroid: ndarray
        A k by N array of centroids found at the last iteration of
        k-means.

    label: ndarray
        label[i] is the code or index of the centroid the
        i'th observation is closest to.

    inertia: float
        The final value of the inertia criterion

    """
    random_state = check_random_state(random_state)
    mean_variance = np.mean(np.var(X, 0))
    best_inertia = np.infty
    # subtract of mean of x for more accurate distance computations
    X_mean = X.mean(axis=0)
    if copy_x:
        X = X.copy()
    X -= X_mean
    if hasattr(init, '__array__'):
        init = np.asarray(init).copy()
        init -= X_mean
        if not n_init == 1:
            warnings.warn('Explicit initial center position passed: '
                          'performing only one init in the k-means')
            n_init = 1
    # precompute squared norms of data points
    x_squared_norms = _squared_norms(X)
    for it in range(n_init):
        # init
        centers = _init_centroids(X, k, init, random_state=random_state,
                                  x_squared_norms=x_squared_norms)
        if verbose:
            print 'Initialization complete'
        # iterations
        for i in range(max_iter):
            centers_old = centers.copy()
            centers = _centers(X, labels, k)
            if verbose:
                print 'Iteration %i, inertia %s' % (i, inertia)
            if np.sum((centers_old - centers) ** 2) < tol * mean_variance:
                if verbose:
                    print 'Converged to similar centers at iteration', i
                break
            if inertia < best_inertia:
                best_labels = labels.copy()
                best_centers = centers.copy()
                best_inertia = inertia
    else:
        best_labels = labels
        best_centers = centers
        best_inertia = inertia
    if not copy_x:
        X += X_mean
    return best_centers + X_mean, best_labels, best_inertia















def _init_centroids(X, k, init, random_state=None, x_squared_norms=None):
    """Compute the initial centroids

    Parameters
    ----------

    X: array, shape (n_samples, n_features)

    k: int
        number of centroids

    init: {'k-means++', 'random' or ndarray or callable} optional
        Method for initialisation

    random_state: integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.

    x_squared_norms:  array, shape (n_samples,), optional
        Squared euclidean norm of each data point. Pass it if you have it at
        hands already to avoid it being recomputed here. Default: None

    Returns
    -------
    centers: array, shape(k, n_features)
    """
    random_state = check_random_state(random_state)
    if init == 'k-means++':
        if sp.issparse(X):
        centers = k_init(X, k,
                        random_state=random_state,
                        x_squared_norms=x_squared_norms)
    elif init == 'random':
        seeds = np.argsort(random_state.rand(n_samples))[:k]
        centers = X[seeds]
    elif hasattr(init, '__array__'):
        centers = init
    elif callable(init):
        centers = init(X, k, random_state=random_state)
    if sp.issparse(centers):
        centers = centers.toarray()
    return centers








class KMeans(BaseEstimator):
    """K-Means clustering

    Parameters
    ----------

    k : int, optional, default: 8
        The number of clusters to form as well as the number of
        centroids to generate.

    max_iter : int
        Maximum number of iterations of the k-means algorithm for a
        single run.

    n_init: int, optional, default: 10
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.

    init : {'k-means++', 'random' or an ndarray}
        Method for initialization, defaults to 'k-means++':

        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence. See section
        Notes in k_init for more details.

        'random': choose k observations (rows) at random from data for
        the initial centroids.

        if init is an 2d array, it is used as a seed for the centroids

    tol: float, optional default: 1e-4
        Relative tolerance w.r.t. inertia to declare convergence

    random_state: integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.

    Methods
    -------

    fit(X):
        Compute K-Means clustering

    Attributes
    ----------

    cluster_centers_: array, [n_clusters, n_features]
        Coordinates of cluster centers

    labels_:
        Labels of each point

    inertia_: float
        The value of the inertia criterion associated with the chosen
        partition.

    Notes
    ------

    The k-means problem is solved using the Lloyd algorithm.

    The average complexity is given by O(k n T), were n is the number of
    samples and T is the number of iteration.

    The worst case complexity is given by O(n^(k+2/p)) with
    n = n_samples, p = n_features. (D. Arthur and S. Vassilvitskii,
    'How slow is the k-means method?' SoCG2006)

    In practice, the K-means algorithm is very fast (one of the fastest
    clustering algorithms available), but it falls in local minima. That's why
    it can be useful to restart it several times.

    See also
    --------

    MiniBatchKMeans:
        Alternative online implementation that does incremental updates
        of the centers positions using mini-batches.
        For large scale learning (say n_samples > 10k) MiniBatchKMeans is
        probably much faster to than the default batch implementation.

    """
    def __init__(self, k=8, init='k-means++', n_init=10, max_iter=300,
                 tol=1e-4, verbose=0, random_state=None, copy_x=True):
        if hasattr(init, '__array__'):
            k = init.shape[0]
            init = np.asanyarray(init, dtype=np.float64)
        self.k = k
        self.init = init
        self.max_iter = max_iter
        self.tol = tol
        self.n_init = n_init
        self.verbose = verbose
        self.random_state = random_state
        self.copy_x = copy_x
    def _check_data(self, X):
        """Verify that the number of samples given is larger than k"""
        if sp.issparse(X):
        X = np.asanyarray(X, dtype=np.float64)
        if sp.issparse(X):
        inertia = _k_means._assign_labels_csr(
            X, x_squared_norms, 0, n_samples, centers, labels)
            raise TypeError("K-Means does not support sparse input matrices.")
        if X.shape[0] < self.k:
            raise ValueError("n_samples=%d should be >= k=%d" % (
                X.shape[0], self.k))
        return X
    def fit(self, X, y=None):
        """Compute k-means"""
        self.random_state = check_random_state(self.random_state)
        X = self._check_data(X)
        warn_if_not_float(X, self)
        self.cluster_centers_, self.labels_, self.inertia_ = k_means(
            X, k=self.k, init=self.init, n_init=self.n_init,
            max_iter=self.max_iter, verbose=self.verbose,
            tol=self.tol, random_state=self.random_state, copy_x=self.copy_x)
        return self
    def transform(self, X, y=None):
        """Transform the data to a cluster-distance space

        In the new space, each dimension is the distance to the cluster
        centers.  Note that even if X is sparse, the array returned by
        `transform` will typically be dense.

        Parameters
        ----------
        X: {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data to transform.

        Returns
        -------
        X_new : array, shape [n_samples, k]
            X transformed in the new space.
        """
        if not hasattr(self, "cluster_centers_"):
            raise AttributeError("Model has not been trained. "
                                 "Train k-means before using transform.")
        cluster_shape = self.cluster_centers_.shape[1]
        if not X.shape[1] == cluster_shape:
            raise ValueError("Incorrect number of features for points. "
                             "Got %d features, expected %d" % (X.shape[1],
                                                               cluster_shape))
        return euclidean_distances(X, self.cluster_centers_)
    def predict(self, X):
        """Predict the closest cluster each sample in X belongs to.

        In the vector quantization literature, `cluster_centers_` is called
        the code book and each value returned by `predict` is the index of
        the closest code in the code book.

        Parameters
        ----------
        X: {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data to predict.

        Returns
        -------
        Y : array, shape [n_samples,]
            Index of the closest center each sample belongs to.
        """
        if not hasattr(self, "cluster_centers_"):
            raise AttributeError("Model has not been trained yet. "
                                 "Fit k-means before using predict.")
        X = atleast2d_or_csr(X)
        expected_n_features = self.cluster_centers_.shape[1]
        if not n_features == expected_n_features:
            raise ValueError("Incorrect number of features. "
                             "Got %d features, expected %d" % (
                                 n_features, expected_n_features))
            raise ValueError("Incorrect number of features. "
                             "Got %d features, expected %d" % (
                                 n_features, expected_n_features))
        x_squared_norms = _squared_norms(X)
        return _labels_inertia(X, x_squared_norms, self.cluster_centers_)[0]






















class MiniBatchKMeans(KMeans):
    """Mini-Batch K-Means clustering

    Parameters
    ----------

    k : int, optional, default: 8
        The number of clusters to form as well as the number of
        centroids to generate.

    max_iter : int, optional
        Maximum number of iterations over the complete dataset before
        stopping independently of any early stopping criterion heuristics.

    max_no_improvement : int, optional
        Control early stopping based on the consecutive number of mini
        batch that does not yield an improvement on the smoothed inertia.

        To disable convergence detection based on inertia, set
        max_no_improvement to -1.

    tol : float, optional
        Control early stopping based on the relative center changes as
        measured by a smoothed, variance-normalized of the mean center
        squared position changes. This early stopping heuristics is
        closer to the one used for the batch variant of the algorithms
        but induces a slight computational and memory overhead over the
        inertia heuristic.

        To disable convergence detection based on normalized center
        change, set tol to 0.0 (default).

    chunk_size: int, optional, default: 1000
        Size of the mini batches

    init : {'k-means++', 'random' or an ndarray}
        Method for initialization, defaults to 'random':

        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence. See section
        Notes in k_init for more details. Only for dense `X`.

        'random': choose k observations (rows) at random from data for
        the initial centroids.

        if init is an 2d array, it is used as a seed for the centroids

    compute_labels: boolean
        Compute label assignements and inertia for the complete dataset
        once the minibatch optimization has converged in fit.

    random_state: integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator.

    Methods
    -------

    fit(X):
        Compute K-Means clustering

    partial_fit(X):
        Compute a partial K-Means clustering

    Attributes
    ----------

    cluster_centers_: array, [n_clusters, n_features]
        Coordinates of cluster centers

    labels_:
        Labels of each point (if compute_labels is set to True).

    inertia_: float
        The value of the inertia criterion associated with the chosen
        partition (if compute_labels is set to True). The inertia is
        defined as the sum of square distances of samples to their nearest
        neighbor.

    References
    ----------
    http://www.eecs.tufts.edu/~dsculley/papers/fastkmeans.pdf
    """
    def __init__(self, k=8, init='random', max_iter=100,
                 chunk_size=1000, verbose=0, compute_labels=True,
                 random_state=None, tol=0.0, max_no_improvements=3):
        super(MiniBatchKMeans, self).__init__(k=k, init=init,
              max_iter=max_iter, verbose=verbose, random_state=random_state,
              tol=tol)
        self.max_no_improvements = max_no_improvements
        self.chunk_size = chunk_size
        self.compute_labels = compute_labels
        super(MiniBatchKMeans, self).__init__(k=k, init=init,
              max_iter=max_iter, verbose=verbose, random_state=random_state,
              tol=tol)
        self.max_no_improvements = max_no_improvements
        self.chunk_size = chunk_size
        self.compute_labels = compute_labels
    def fit(self, X, y=None):
        """Compute the centroids on X by chunking it into mini-batches.

        Parameters
        ----------
        X: array-like, shape = [n_samples, n_features]
            Coordinates of the data points to cluster
        """
        self.random_state = check_random_state(self.random_state)
        X = check_arrays(X, sparse_format="csr", copy=False,
                         check_ccontiguous=True, dtype=np.float64)[0]
        n_samples, n_features = X.shape
        X = check_arrays(X, sparse_format="csr", copy=False)[0]
        n_samples, n_features = X.shape
        if n_samples < self.k:
            raise ValueError("Number of samples smaller than number "\
                             "of clusters.")
        x_squared_norms = _squared_norms(X)
        if hasattr(self.init, '__array__'):
            self.init = np.ascontiguousarray(self.init, dtype=np.float64)
        X_shuffled = shuffle(X, random_state=self.random_state)
        if sp.issparse(X_shuffled):
            _mini_batch_step = _k_means._mini_batch_update_csr
        if self.tol > 0.0:
            # TODO: compute the variance of the data both for sparse and
            # dense data
            variance = 1.0
            tol = self.tol * variance
            old_center_buffer = np.zeros(n_features, np.double)
            compute_squared_diff = 1
            # TODO: compute the variance of the data both for sparse and
            # dense data
            variance = 1.0
            tol = self.tol * variance
            old_center_buffer = np.zeros(n_features, np.double)
            compute_squared_diff = 1
        else:
        raise ValueError("the init parameter for the k-means should "
            "be 'k-means++' or 'random' or an ndarray, "
            "'%s' (type '%s') was passed.")
        # TODO: initialize the counts after random assignement here
        self.cluster_centers_ = _init_centroids(
            X_shuffled, self.k, self.init, random_state=self.random_state,
            x_squared_norms=x_squared_norms)
        self.counts = np.zeros(self.k, dtype=np.int32)
        n_batches = int(np.ceil(float(n_samples) / self.chunk_size))
        else:
        previous_ewa_inertia = None
        ewa_diff = None
        ewa_inertia = None
        batch_slices = list(gen_even_slices(n_samples, n_batches))
        n_iterations = int(self.max_iter * n_batches)
        else:
            tol = 0.0
            old_center_buffer = np.zeros(0, np.double)
            compute_squared_diff = 0
            _mini_batch_step = _mini_batch_step_dense
        for i, batch_slice in izip(xrange(n_iterations), cycle(batch_slices)):
            inertia, diff = _mini_batch_step(
                X_shuffled, x_squared_norms, batch_slice,
                self.cluster_centers_, self.counts, old_center_buffer,
                compute_squared_diff)
            # normalize inertia to be able to compare values when chunk_size
            # changes
            inertia /= float(batch_slice.stop - batch_slice.start)
            diff /= float(batch_slice.stop - batch_slice.start)
            # compute an exponentially weighted average of the squared diff to
            # monitor the convergence while discarding batch local stochastic
            # variability:
            # https://en.wikipedia.org/wiki/Moving_average
            if ewa_diff is None:
                ewa_diff = diff
                ewa_inertia = inertia
                ewa_diff = diff
                ewa_inertia = inertia
        else:
                alpha = float(self.chunk_size) * 2.0 / (n_samples + 1)
                alpha = 1.0 if alpha > 1.0 else alpha
                ewa_diff = ewa_diff * (1 - alpha) + diff * alpha
                ewa_inertia = ewa_inertia * (1 - alpha) + inertia * alpha
                            x_squared_norms=x_squared_norms)
            if (previous_ewa_inertia is not None
                and ewa_inertia >= previous_ewa_inertia):
                if self.verbose:
                    print 'Converged at iteration %d/%d' % (
                        i + 1, n_iterations)
                break
            else:
                previous_ewa_inertia = ewa_inertia
                previous_ewa_inertia = ewa_inertia
            if self.verbose:
                print ('Minibatch iteration %d/%d:'
                       ' mean inertia: %f, ewa inertia: %f,'
                       ' mean squared diff: %f, ewa diff: %f' % (
                           i + 1, n_iterations, inertia, ewa_inertia,
                           diff, ewa_diff))
        if self.compute_labels:
            if self.verbose:
                print 'Computing label assignements and total inertia', i
            self.labels_, self.inertia_ = _labels_inertia(
                X, x_squared_norms, self.cluster_centers_)
        return self
    def partial_fit(self, X, y=None):
        """Update k means estimate on a single mini-batch X.

        Parameters
        ----------
        X: array-like, shape = [n_samples, n_features]
            Coordinates of the data points to cluster.
        """
        self.random_state = check_random_state(self.random_state)
        n_samples, n_features = X.shape
        if hasattr(self.init, '__array__'):
            self.init = np.ascontiguousarray(self.init, dtype=np.float64)
        if n_samples == 0:
            return self
        x_squared_norms = _squared_norms(X)
        if (not hasattr(self, 'counts')
            or not hasattr(self, 'cluster_centers_')):
        batch_slice = slice(0, n_samples, None)
        if sp.issparse(X):
            _mini_batch_step = _k_means._mini_batch_update_csr
            _mini_batch_step = _k_means._mini_batch_update_csr
        else:
            _mini_batch_step = _mini_batch_step_dense
            _mini_batch_step = _mini_batch_step_dense
        _mini_batch_step(X, x_squared_norms, batch_slice,
                         self.cluster_centers_, self.counts,
                         np.zeros(0, np.double), 0)
        if self.compute_labels:
            self.labels_, self.inertia_ = _labels_inertia(
                X, x_squared_norms, self.cluster_centers_)
        return self























