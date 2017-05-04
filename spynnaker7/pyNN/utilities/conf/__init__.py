"""
Import Config Files
-------------------
We look for config files in a variety of locations starting with the package
directory, followed by the user's home directory and ending with the current
working directory.

All config is made accessible through the global object `config`.
"""
import ConfigParser
import logging
import os
import shutil
import string
import sys

import spynnaker7 as spynnaker
from spynnaker7.pyNN.utilities.conf import log

from spinn_front_end_common.utilities import exceptions


def _install_cfg(filename):
    template_cfg = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "{}.template".format(filename))
    home_cfg = os.path.expanduser("~/.{}".format(filename))
    shutil.copyfile(template_cfg, home_cfg)
    print "************************************"
    print("{} has been created.  Please edit this file and change \"None\""
          " after \"machineName\" to the hostname or IP address of your"
          " SpiNNaker board, and change \"None\" after \"version\" to the"
          " version of SpiNNaker hardware you are running on:".format(
              home_cfg))
    print "[Machine]"
    print "machineName = None"
    print "version = None"
    print "************************************"


def create_directory(directory):
    """creates a directory if needed, or deletes it and rebuilds it

    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        shutil.rmtree(directory)
        os.makedirs(directory)


def _load_config(filename, config_parsers=[]):
    config = ConfigParser.RawConfigParser()
    default = os.path.join(os.path.dirname(spynnaker.__file__), filename)
    spynnaker_user = os.path.expanduser("~/.{}".format(filename))
    spynnaker_others = (spynnaker_user, filename)
    located_spynnaker = list()

    found_spynnakers = False
    for possible_spynnaker_file in spynnaker_others:
        if os.path.isfile(possible_spynnaker_file):
            found_spynnakers = True
            located_spynnaker.append(os.path.abspath(possible_spynnaker_file))

    if len(located_spynnaker) == 0:
        raise exceptions.ConfigurationException(
            "You need to have at least one spynnaker.cfg file located in one "
            "of the following locations: {}".format(spynnaker_others))

    with open(default) as f:
        config.readfp(f)
    if found_spynnakers:
        read = config.read(spynnaker_others)
        read.append(default)
    else:
        # Create a default spynnaker.cfg in the user home directory and get
        # them to update it.
        _install_cfg(filename)
        sys.exit(2)

    for (section, parser) in config_parsers:
        if config.has_section(section):
            result = parser(config)
            if result is not None:
                read.append(result)

    # Log which config files we read
    logger = logging.getLogger(__name__)
    logger.info("Read config files: %s" % string.join(read, ", "))

    return config


def _machine_spec_parser(config):
    if not config.has_option("Machine", "machine_spec_file"):
        return None
    machine_spec_file_path = config.get("Machine", "machine_spec_file")
    config.read(machine_spec_file_path)
    return machine_spec_file_path


def _logging_parser(config):
    """Create the root logger with the given level.
    Create filters based on logging levels"""
    try:
        if config.getboolean("Logging", "instantiate"):
            logging.basicConfig(level=0)

        for handler in logging.root.handlers:
            handler.addFilter(log.ConfiguredFilter(config))
            handler.setFormatter(log.ConfiguredFormatter(config))
    except ConfigParser.NoOptionError:
        pass
    return None


def load_config():
    """
    Reloads the config.

    Warning until a global config exists this will not affect the config of
    already imported modules

    Will read in the config based on the current path.

    Warning: Should only be used for testing as which configs will and
    will not be effected is uncertain.

    :return:
    :rytpe RawConfigParser
    """
    return _load_config("spynnaker.cfg", [("Machine", _machine_spec_parser),
                                          ("Logging", _logging_parser)])


# Create a config, read global defaults and then read in additional files
config = _load_config("spynnaker.cfg", [
    ("Machine", _machine_spec_parser), ("Logging", _logging_parser)])

__all__ = ['config']
