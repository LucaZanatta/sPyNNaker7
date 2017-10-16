import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase
import pylab


def do_run(plot):
    p.setup(timestep=1.0)

    cell_params_lif = {'cm': 0.25,
                       'i_offset': 0.0,
                       'tau_m': 20.0,
                       'tau_refrac': 2.0,
                       'tau_syn_E': 5.0,
                       'tau_syn_I': 5.0,
                       'v_reset': -70.0,
                       'v_rest': -65.0,
                       'v_thresh': -40.0
                       }

    def create_grid(n, label, dx=1.0, dy=1.0):
        grid_structure = p.Grid2D(dx=dx, dy=dy, x0=0.0, y0=0.0)
        return p.Population(n*n, p.IF_curr_exp, cell_params_lif,
                            structure=grid_structure, label=label)

    # Parameters
    n = 10
    weight_to_spike = 5.0
    delay = 5
    runtime = 200

    # Network population
    grid = create_grid(n, 'grid')

    # SpikeInjector
    injectionConnection = [(0, 0, weight_to_spike, delay)]
    spikeArray = {'spike_times': [[0]]}
    inj_pop = p.Population(1, p.SpikeSourceArray, spikeArray,
                           label='inputSpikes_1')

    # Injector projection
    p.Projection(inj_pop, grid, p.FromListConnector(injectionConnection))

    # Connectors
    dist_dep_exc = "d<2.5"
    dist_dep_inh = "d<1.5"
    # dist_dep_exc = "exp(-d)/{tau_exc}".format(tau_exc=tau_exc)
    # dist_dep_inh = 'exp(-0.5*d)/{tau_inh}'.format(tau_inh=tau_inh)

    exc_connector = p.DistanceDependentProbabilityConnector(
        dist_dep_exc, weights=2.0, delays=5, allow_self_connections=False)

    inh_connector = p.DistanceDependentProbabilityConnector(
        dist_dep_inh, weights=1.5, delays=10, allow_self_connections=False)

    # Wire projections for grid
    p.Projection(grid, grid, exc_connector)
    p.Projection(grid, grid, inh_connector)

    grid.record()
    grid.record_v()

    p.run(runtime)

    v = grid.get_v()
    spikes = grid.getSpikes()

    if plot:
        # Make some graphs
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

        if v is not None:
            print (len(v))
            ticks = len(v) / (n*n)
            pylab.figure()
            pylab.xlabel('Time/ms')
            pylab.ylabel('v')
            pylab.title('v')
            for pos in range(0, n):
                v_for_neuron = v[pos * ticks: (pos + 1) * ticks]
                pylab.plot([i[2] for i in v_for_neuron])
            pylab.show()

    p.end()

    return v, spikes


class DistanceDependentProbabilityConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes = do_run(plot=False)
        # any checks go here
        self.assertEquals(6101, len(spikes))


if __name__ == '__main__':
    v, spikes = do_run(plot=True)
