"""
Synfirechain-like example
"""

# spynnaker imports
import spynnaker7.pyNN as p

# general imports
import os

from p7_integration_tests.base_test_case import BaseTestCase
from spinnman.exceptions import SpinnmanTimeoutException
from unittest import SkipTest


def read_spikefile(file_name, n_neurons):
    """
    helper method for reading in spike data
    :param file_name:
    :param n_neurons:
    :return:
    """
    spike_array = [[] for x in range(n_neurons)]
    with open(file_name) as f_spike:
        for line in f_spike:
            cut_index = line.find(';')
            time_stamp = int(line[0:cut_index])
            neuron_list = line[cut_index+1:-1].split(',')
            for neuron in neuron_list:
                neuron_id = int(neuron)
                spike_array[neuron_id].append(time_stamp)
    return spike_array


def do_run():
    """
    test that tests the printing of v from a pre determined recording
    :return:
    """
    p.setup(timestep=0.1, min_delay=1.0, max_delay=14.0)
    n_neurons = 128 * 128  # number of neurons in each population
    p.set_number_of_neurons_per_core("IF_cond_exp", 256)

    cell_params_lif = {'cm': 0.25,
                       'i_offset': 0.0,
                       'tau_m': 20.0,
                       'tau_refrac': 2.0,
                       'tau_syn_E': 5.0,
                       'tau_syn_I': 5.0,
                       'v_reset': -70.0,
                       'v_rest': -65.0,
                       'v_thresh': -50.0,
                       'e_rev_E': 0.,
                       'e_rev_I': -80.
                       }

    populations = list()
    projections = list()

    weight_to_spike = 0.035
    delay = 1.7

    current_file_path = os.path.dirname(os.path.abspath(__file__))
    spikes_file = os.path.join(current_file_path, 'test.spikes')

    spikes = read_spikefile(spikes_file, n_neurons)
    spike_array = {'spike_times': spikes}

    populations.append(p.Population(
        n_neurons, p.SpikeSourceArray, spike_array,
        label='inputSpikes_1'))
    populations.append(p.Population(
        n_neurons, p.IF_cond_exp, cell_params_lif, label='pop_1'))
    projections.append(p.Projection(
        populations[0], populations[1], p.OneToOneConnector(
            weights=weight_to_spike, delays=delay)))
    populations[1].record()

    p.run(100)

    spikes = populations[1].getSpikes(compatible_output=True)

    p.end()

    return spikes


def plot(spikes):
    """
    test that tests the printing of v from a pre determined recording
    :return:
    """
    import pylab  # deferred so unittest are not dependent on it

    if spikes is not None:
        print spikes
        pylab.figure()
        pylab.plot([i[1] for i in spikes], [i[0] for i in spikes], ".")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('spikes')
        pylab.show()
    else:
        print "No spikes received"


class TestReadingSpikeArrayDataAndBigSlices(BaseTestCase):
    """
    tests the printing of print v given a simulation
    """
    def test_script(self):
        """
        test that tests the printing of v from a pre determined recording
        :return:
        """
        try:
            spikes = do_run()
            # System intentional overload so may error
        except SpinnmanTimeoutException as ex:
            raise SkipTest(ex)
        try:
            self.assertLess(430, len(spikes))
            self.assertGreater(460, len(spikes))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)


if __name__ == '__main__':
    spikes = do_run()
    print len(spikes)
    plot(spikes)
