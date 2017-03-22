# common front end imports
import logging
import os

from pyNN.random import RandomDistribution

from spinn_front_end_common.utilities.utility_objs.executable_finder \
    import ExecutableFinder
from spynnaker.pyNN import model_binaries
from spynnaker.pyNN.spinnaker_common import SpiNNakerCommon
from spynnaker7.pyNN.models.pynn_population import Population
from spynnaker7.pyNN.models.pynn_projection import Projection
from spynnaker7.pyNN.utilities.conf import config

from spynnaker7.pyNN.utilities.random_stats.random_stats_scipy_impl import \
    RandomStatsScipyImpl
from spynnaker7.pyNN.utilities.random_stats.random_stats_uniform_impl import \
    RandomStatsUniformImpl

# global objects
logger = logging.getLogger(__name__)
executable_finder = ExecutableFinder()


class Spinnaker(SpiNNakerCommon):
    """
    Spinnaker: the main entrance for the spynnaker front end
    """

    def __init__(
            self, host_name=None, timestep=None, min_delay=None,
            max_delay=None, graph_label=None, database_socket_addresses=None,
            n_chips_required=None):
        # Determine default executable folder location
        # and add this default to end of list of search paths
        executable_finder.add_path(os.path.dirname(model_binaries.__file__))

        # population holders
        SpiNNakerCommon.__init__(
            self, config=config,
            database_socket_addresses=database_socket_addresses,
            executable_finder=executable_finder, graph_label=graph_label,
            n_chips_required=n_chips_required, timestep=timestep,
            hostname=host_name, max_delay=max_delay, min_delay=min_delay)

    def create_population(self, size, cellclass, cellparams, structure, label):
        """ creates a pynn 0.75 population

        :param size: the number of atoms in this population
        :param cellclass: the type of neuron model this pop represents
        :param cellparams: the neuron parameters for this population
        :param structure: something to do with space
        :param label: the human readable label of the population
        :return: a population instance
        """
        return Population(
            size=size, cellclass=cellclass, cellparams=cellparams,
            structure=structure, label=label, spinnaker=self)

    def create_projection(
            self, presynaptic_population, postsynaptic_population, connector,
            source, target, synapse_dynamics, label, rng):
        """

        :param presynaptic_population: source pop this projection goes from
        :param postsynaptic_population: dest pop this projection goes to
        :param connector: the definition of which neurons connect to each other
        :param source:
        :param target: type of projection
        :param synapse_dynamics: plasticity object
        :param label: human readable version of the projection
        :param rng: the random number generator to use on this projection
        :return:
        """
        if label is None:
            label = "Projection {}".format(self._edge_count)
            self._edge_count += 1
        return Projection(
            presynaptic_population=presynaptic_population, label=label,
            postsynaptic_population=postsynaptic_population, rng=rng,
            connector=connector, source=source, target=target,
            synapse_dynamics=synapse_dynamics, spinnaker_control=self,
            machine_time_step=self._machine_time_step,
            timescale_factor=self._time_scale_factor,
            user_max_delay=self.max_supported_delay)

    @staticmethod
    def get_distribution_to_stats():
        return {
            'binomial': RandomStatsScipyImpl("binom"),
            'gamma': RandomStatsScipyImpl("gamma"),
            'exponential': RandomStatsScipyImpl("expon"),
            'lognormal': RandomStatsScipyImpl("lognorm"),
            'normal': RandomStatsScipyImpl("norm"),
            'poisson': RandomStatsScipyImpl("poisson"),
            'uniform': RandomStatsUniformImpl(),
            'randint': RandomStatsScipyImpl("randint"),
            'vonmises': RandomStatsScipyImpl("vonmises")}

    @staticmethod
    def get_random_distribution():
        return RandomDistribution
