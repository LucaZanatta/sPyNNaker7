import unittest
import os
import shutil

import spinn_utilities.conf_loader as conf_loader
import spynnaker.pyNN
from spynnaker7.pyNN.spinnaker import Spinnaker


class TestCFGs(unittest.TestCase):

    def setUp(self):
        conf = conf_loader.load_config(spynnaker.pyNN, "spynnaker.cfg")

        self._previous_reportsEnabled = conf.get(
            "Reports", "reportsEnabled")
        self.previous_defaultReportFilePath = conf.get(
            "Reports", "defaultReportFilePath")

    def tearDown(self):
        conf = conf_loader.load_config(spynnaker.pyNN, "spynnaker.cfg")
        conf.set("Reports", "defaultReportFilePath",
                 self.previous_defaultReportFilePath)
        conf.set("Reports", "reportsEnabled", self._previous_reportsEnabled)

    @unittest.skip("broken")
    def test_reports_creation_custom_location(self):
        conf = conf_loader.load_config(spynnaker.pyNN, "spynnaker.cfg")
        current_path = os.path.dirname(os.path.abspath(__file__))
        conf.set("Reports", "defaultReportFilePath", current_path)
        conf.set("Reports", "reportsEnabled", "True")
        spinn = Spinnaker(timestep=1, min_delay=1, max_delay=10)

        if 'reports' in os.listdir(current_path):
            shutil.rmtree(os.path.join(current_path, 'reports'))
        spinn._set_up_report_specifics()

        self.assertEqual(spinn._report_default_directory,
                         os.path.join(current_path, 'reports', 'latest'))
        # File reports should be in the new location
        self.assertIn('reports', os.listdir(current_path))


if __name__ == '__main__':
    unittest.main()
