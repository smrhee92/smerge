"""
Machine Learning module in python
=================================

scikits.learn is a Python module integrating classique machine
learning algorithms in the tightly-nit world of scientific Python
packages (numpy, scipy, matplotlib).

It aims to provide simple and efficient solutions to learning problems
that are accessible to everybody and reusable in various contexts:
machine-learning as a versatile tool for science and engineering.

See http://scikit-learn.sourceforge.net for complete documentation.
"""

from .base import clone
from . import cross_val
from . import ball_tree
from . import cluster
from . import covariance
from . import datasets
from . import feature_selection
from . import gaussian_process
from . import sgd
from . import glm
from . import lda
from . import metrics
from . import svm

try:
    from numpy.testing import nosetester
    class NoseTester(nosetester.NoseTester):
        """ Subclass numpy's NoseTester to add doctests by default
        """
        def test(self, label='fast', verbose=1, extra_argv=['--exe'],
                        doctests=True, coverage=False):
            return super(NoseTester, self).test(label=label, verbose=verbose,
                                    extra_argv=extra_argv,
                                    doctests=doctests, coverage=coverage)
        
    test = NoseTester().test
    del nosetester
except:
    pass

<<<<<<< REMOTE
__all__ = ['cross_val', 'ball_tree', 'cluster', 'covariance', 'datasets', 'gmm', 'glm',
           'logistic', 'lda', 'metrics', 'svm', 'features', 'clone',
           'test', 'sgd']
=======
__all__ = ['cross_val', 'ball_tree', 'cluster', 'covariance', 'gmm', 'glm',
           'logistic', 'lda', 'metrics', 'svm', 'features', 'clone', 
           'test']
=======
__all__ = ['cross_val', 'ball_tree', 'cluster', 'covariance', 'gmm', 'glm',
           'logistic', 'lda', 'metrics', 'svm', 'gaussian_process', 'features',
           'clone', 'test']
>>>>>>> LOCAL

__version__ = '0.6.git'


