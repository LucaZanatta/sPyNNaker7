from spynnaker.pyNN.models.neural_projections.connectors \
    import FromListConnector as CommonFromListConnector
from spynnaker.pyNN.exceptions import InvalidParameterType
import logging

logger = logging.getLogger(__name__)


class FromListConnector(CommonFromListConnector):
    """ Make connections according to a list.

    :param: conn_list:\
        a list of tuples, one tuple for each connection. Each\
        tuple should contain::

            (pre_idx, post_idx, weight, delay)

        where pre_idx is the index (i.e. order in the Population,\
        not the ID) of the presynaptic neuron, and post_idx is\
        the index of the postsynaptic neuron.
    """

    def __init__(self, conn_list, safe=True, verbose=False):
        """
        Creates a new FromListConnector.
        """
        # pylint: disable=len-as-condition
        # Disabled the warning because we might have a numpy array
        if conn_list is None or len(conn_list) == 0:
            raise InvalidParameterType(
                "The connection list for the FromListConnector must contain"
                " at least a list of tuples, each of which should contain:"
                " (pre_idx, post_idx, weight, delay)")

        conns, weights, delays, self._extra_conn_data = self._split_conn_list(
            conn_list, ['pre', 'post', 'weight', 'delay'])

        super(FromListConnector, self).__init__(conns, safe, verbose)
        self.set_weights_and_delays(weights, delays)
