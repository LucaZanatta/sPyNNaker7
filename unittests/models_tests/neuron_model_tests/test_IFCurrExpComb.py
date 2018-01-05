import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(0.1)

pop_ex = p.Population(1, p.extra_models.IF_curr_comb_exp, {}, label="test")
pop_src1 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[3, 5, 7]]}, label="src1")



# define the projections
exc_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=0.1), target="inhibitory")

inh_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=0.2), target="excitatory")

#pop_ex.record()
pop_ex.record_gsyn()
#pop_ex.record_v()


#v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
#spikes = pop_ex.getSpikes()

#plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"
import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(0.1)

pop_ex = p.Population(1, p.extra_models.IF_curr_comb_exp, {}, label="test")
pop_src1 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]}, label="src1")
p.set_number_of_neurons_per_core("IF_curr_comb_exp", 27)

# 1.235
# 1.3585

# pop_ex.set('exc_a_tau', 37045.5 )
# pop_ex.set('exc_b_tau',  40750.1)
pop_ex.set('exc_a_tau', 1.235)
pop_ex.set('exc_b_tau', 1.3585)
pop_ex.set('inh_a_tau', 1.235)
pop_ex.set('inh_b_tau', 1.3585)

# define the projections
exc_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=2.2), target="excitatory")

inh_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=5.5), target="inhibitory")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
# p.run(225000)
p.run(15)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"