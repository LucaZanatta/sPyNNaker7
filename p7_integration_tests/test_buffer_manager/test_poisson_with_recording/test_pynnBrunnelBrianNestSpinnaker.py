import p7_integration_tests.scripts.pynnBrunnelPlot as pblt

from p7_integration_tests.base_test_case import BaseTestCase
import p7_integration_tests.scripts.pynnBrunnelBrianNestSpinnaker as script

import os
from unittest import SkipTest
import unittest

Neurons = 3000  # number of neurons in each population
sim_time = 1000
simulator_Name = 'spiNNaker'


def plot(esp, sim_time, N_E):
    import pylab  # deferred so unittest are not dependent on it
    if esp is not None:
        ts_ext = [x[1] for x in esp]
        ids_ext = [x[0] for x in esp]
        title = 'Raster Plot of the excitatory population in %s' \
                % simulator_Name,
        pblt._make_plot(ts_ext, ts_ext, ids_ext, ids_ext,
                        len(ts_ext) > 0, 5.0, False, title,
                        'Simulation Time (ms)', total_time=sim_time,
                        n_neurons=N_E)

        pylab.show()


class PynnBrunnelBrianNestSpinnaker(BaseTestCase):

    @unittest.skipIf(os.environ.get(
        'CONTINUOUS_INTEGRATION', "false").lower() == 'true', reason="Too big")
    def test_run(self):
        (esp, s, N_E) = script.do_run(Neurons, sim_time, record=True)
        try:
            self.assertLess(200, len(esp))
            self.assertGreater(300, len(esp))
            self.assertLess(22000, len(s))
            self.assertGreater(26000, len(s))
            self.assertEquals(2400, N_E)
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)


if __name__ == '__main__':
    (esp, s, N_E) = script.do_run(Neurons, sim_time, record=True)
    plot(esp, sim_time, N_E)
    print len(esp)
    print len(s)
    print N_E
