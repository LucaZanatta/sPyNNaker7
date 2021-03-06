import os
import random
import sys
import unittest
from unittest import SkipTest
from spinn_front_end_common.utilities import globals_variables
import spinn_utilities.conf_loader as conf_loader

p7_integration_factor = float(os.environ.get('P7_INTEGRATION_FACTOR', "1"))
random.seed(os.environ.get('P7_INTEGRATION_SEED', None))


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        factor = random.random()
        if factor > p7_integration_factor:
            msg = "Test skipped by random number {} above " \
                  "P7_INTEGRATION_FACTOR {}" \
                  "".format(factor, p7_integration_factor)
            raise SkipTest(msg)
        globals_variables.unset_simulator()
        class_file = sys.modules[self.__module__].__file__
        path = os.path.dirname(os.path.abspath(class_file))
        os.chdir(path)

    def assert_logs_messages(
            self, log_records, sub_message, log_level='ERROR', count=1):
        seen = 0
        for record in log_records:
            if record.levelname == log_level:
                if sub_message in record.msg:
                    seen += 1
        if seen == count:
            return
        msg = "\"{}\" not found in any {} logs {} times, was found {} " \
              "times".format(sub_message, log_level, count, seen)
        raise self.failureException(msg)

    def assert_not_spin_three(self):
        config = conf_loader.load_config(
            filename="spynnaker.cfg", defaults=[])
        if config.has_option("Machine", "version"):
            version = config.get("Machine", "version")
            if version in ["2", "3"]:
                msg = "This test will not run on a spin {} board" \
                      "".format(version)
                raise SkipTest(msg)
