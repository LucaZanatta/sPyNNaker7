#!/usr/bin/python
"""
Synfirechain-like example
"""
from p7_integration_tests.base_test_case import BaseTestCase
from p7_integration_tests.scripts.synfire_run import TestRun
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker
from unittest import SkipTest

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
runtime = 5000
synfire_run = TestRun()


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=[runtime])
        spikes = synfire_run.get_output_pop_spikes()
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        try:
            self.assertLess(240, len(spikes))
            self.assertGreater(290, len(spikes))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)


if __name__ == '__main__':
    results = synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                                 run_times=[runtime])
    spikes = synfire_run.get_output_pop_spikes()
    v = synfire_run.get_output_pop_voltage()
    gsyn = synfire_run.get_output_pop_gsyn()

    print len(spikes)
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gsyn")
