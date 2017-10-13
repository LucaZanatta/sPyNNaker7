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
                       'v_thresh': -50.0
                       }

    def create_grid(n, label, dx=1.0, dy=1.0):
        grid_structure = p.Grid2D(dx=dx, dy=dy, x0=0.0, y0=0.0)
        return p.Population(n*n, p.IF_curr_exp, cell_params_lif,
                            structure=grid_structure, label=label)


    # Parameters
    n = 5
    weight_to_spike = 5.0
    delay = 2
    runtime=1000

    # Network
    small_world = create_grid(n, 'small_world')

    # SpikeInjector
    injectionConnection = [(0, 0, weight_to_spike, delay)]
    spikeArray = {'spike_times': [[0]]}
    inj_pop = p.Population(1, p.SpikeSourceArray, spikeArray, label='inputSpikes_1')

    # Injector projection
    p.Projection(inj_pop, small_world, p.FromListConnector(injectionConnection))

    # Connectors
    degree = 2
    rewiring = 0.4
    small_world_connector = p.SmallWorldConnector(degree, rewiring,
                                                  weights=2.0, delays=5)

    # Projection
    p.Projection(small_world, small_world, small_world_connector)

    small_world.record()
    small_world.record_v()

    p.run(runtime)

    v = small_world.get_v()
    spikes = small_world.getSpikes()

    # Make some graphs
    if plot:
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
            ticks = len(v) / (n*n)
            pylab.figure()
            pylab.xlabel('Time/ms')
            pylab.ylabel('v')
            pylab.title('v')
            for pos in range(0, n, 2):
                v_for_neuron = v[pos * ticks: (pos + 1) * ticks]
                pylab.plot([i[2] for i in v_for_neuron])
            pylab.show()

    p.end()

    return v, spikes


class SmallWorldConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes = do_run(plot=False)
        # any checks go here

if __name__ == '__main__':
    v, spikes = do_run(plot=True)