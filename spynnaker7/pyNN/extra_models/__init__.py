# spynnaker 7 extra models
from spynnaker.pyNN.models.neuron.builds import IFCondExpStoc
from spynnaker.pyNN.models.neuron.builds import IFCurrDelta
from spynnaker.pyNN.models.neuron.builds import IFCurrExpCa2Adaptive
from spynnaker.pyNN.models.neuron.builds import IzkCondExpBase as IZK_cond_exp
from spynnaker.pyNN.models.neuron.builds import IzkCurrExpBase as IZK_curr_exp
from spynnaker.pyNN.models.neuron.builds\
    import IFCurrDualExpBase as IF_curr_dual_exp
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_semd_base \
    import IFCurrExpSEMDBase as IF_curr_exp_sEMD

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
    .weight_dependence_additive_triplet import WeightDependenceAdditiveTriplet

__all__ = [
    # spynnaker 7 models
    'IFCurrDelta', 'IFCurrExpCa2Adaptive', 'IFCondExpStoc',
    'IZK_curr_exp', 'IZK_cond_exp', 'IF_curr_dual_exp', 'IF_curr_exp_sEMD',

    # spynnaker 7 plastic stuff
    'WeightDependenceAdditiveTriplet',
    'PfisterSpikeTriplet',
    'SpikeNearestPair',
    'RecurrentRule', 'Vogels2011Rule']
