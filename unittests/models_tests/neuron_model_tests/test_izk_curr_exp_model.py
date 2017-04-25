import unittest
from spynnaker.pyNN.models.neuron.builds.izk_curr_exp_base import \
    IzkCurrExpBase


class TestIZKCurrExpModel(unittest.TestCase):

    @unittest.skip("unittests\models_tests\neuron_model_tests\test_if_curr_dual_exp_model "
                   "test_new_izk_curr_exp_mode")
    def test_new_izk_curr_exp_model(self):
        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0}
        n_neurons = 10
        izk_curr_exp = IzkCurrExpBase(
            n_neurons, 1000, 1.0)

        self.assertEqual(izk_curr_exp.model_name, "IZK_curr_exp")
        self.assertEqual(len(izk_curr_exp.get_parameters()), 8)
        self.assertEqual(izk_curr_exp._a, 0.02)
        self.assertEqual(izk_curr_exp._b, 0.2)
        self.assertEqual(izk_curr_exp._c, -65.0)
        self.assertEqual(izk_curr_exp._d, 2.0)

        self.assertEqual(izk_curr_exp._i_offset, 0)
        self.assertEqual(izk_curr_exp._tau_syn_E, 5.0)
        self.assertEqual(izk_curr_exp._tau_syn_I, 5.0)


if __name__ == "__main__":
    unittest.main()
