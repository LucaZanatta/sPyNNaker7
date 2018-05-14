from scipy.stats import uniform
from spynnaker.pyNN.utilities.random_stats import AbstractRandomStats


class RandomStatsUniformImpl(AbstractRandomStats):
    """ An implementation of AbstractRandomStats for uniform distributions\
        (as scipy.stats.uniform takes slightly different parameters to\
        numpy.random.uniform)
    """

    def _get_params(self, dist):
        return [dist.parameters[0], dist.parameters[1] - dist.parameters[0]]

    def cdf(self, dist, v):
        return uniform.cdf(v, *self._get_params(dist))

    def ppf(self, dist, p):
        return uniform.ppf(p, *self._get_params(dist))

    def mean(self, dist):
        return uniform.mean(*self._get_params(dist))

    def std(self, dist):
        return uniform.std(*self._get_params(dist))

    def var(self, dist):
        return uniform.var(*self._get_params(dist))

    def high(self, dist):
        """ Return the variance of the distribution
        """
        if dist.boundaries is None:
            return None
        return max(dist.boundaries)

    def low(self, dist):
        """ Return the variance of the distribution
        """
        if dist.boundaries is None:
            return None
        return min(dist.boundaries)
