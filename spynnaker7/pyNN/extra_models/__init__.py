# spynnaker 8 extra models
from spynnaker.pyNN.models.neuron.builds import IFCondExpStoc
from spynnaker.pyNN.models.neuron.builds import IFCurrDelta
from spynnaker.pyNN.models.neuron.builds import IFCurrExpCa2Adaptive
from spynnaker.pyNN.models.neuron.builds import IzkCondExpBase as IZK_cond_exp
from spynnaker.pyNN.models.neuron.builds import IzkCurrExpBase as IZK_curr_exp
from spynnaker.pyNN.models.neuron.builds\
    import IFCurrDualExpBase as IF_curr_dual_exp

# additional synapse shaping
from spynnaker.pyNN.models.neuron.builds.if_curr_comb_exp \
    import IFCurrCombExp as IF_curr_comb_exp
from spynnaker.pyNN.models.neuron.builds.if_curr_comb_exp_2E2I \
    import IFCurrCombExp2E2I as IF_curr_comb_exp_2E2I
from spynnaker.pyNN.models.neuron.builds.if_curr_comb_exp_5E5I \
    import IFCurrCombExp5E5I as IF_curr_comb_exp_5E5I
from spynnaker.pyNN.models.neuron.builds.if_curr_comb_exp_4E4I \
    import IFCurrCombExp4E4I as IF_curr_comb_exp_4E4I
from spynnaker.pyNN.models.neuron.builds.if_curr_comb_exp_7E7I \
    import IFCurrCombExp7E7I as IF_curr_comb_exp_7E7I
from spynnaker.pyNN.models.neuron.builds.izk_curr_comb_exp_4E4I \
    import IzkCurrCombExp4E4I as IZK_curr_comb_exp_4E4I

# plastic timing spynnaker 7
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceRecurrent as RecurrentRule
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceSpikeNearestPair as SpikeNearestPair
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceVogels2011 as Vogels2011Rule
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependencePfisterSpikeTriplet as PfisterSpikeTriplet

# plastic weight spynnaker 7
from spynnaker7.pyNN.models.plasticity_components.weight_dependence \
    .weight_dependence_additive_triplet \
    import WeightDependenceAdditiveTriplet as WeightDependenceAdditiveTriplet

__all__ = [
    # spynnaker 7 models
    'IFCurrDelta', 'IFCurrExpCa2Adaptive', 'IFCondExpStoc',
    'IZK_curr_exp', 'IZK_cond_exp', 'IF_curr_dual_exp',

    # additional synapses
    'IF_curr_comb_exp',
    'IF_curr_comb_exp_2E2I',
    'IF_curr_comb_exp_5E5I',
    'IF_curr_comb_exp_4E4I',
    'IF_curr_comb_exp_7E7I',
    'IZK_curr_comb_exp_4E4I',

    # spynnaker 7 plastic stuff
    'WeightDependenceAdditiveTriplet',
    'PfisterSpikeTriplet',
    'SpikeNearestPair',
    'RecurrentRule', 'Vogels2011Rule']
