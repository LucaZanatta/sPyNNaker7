# general imports
import logging

# fec imports
from spinn_front_end_common.abstract_models \
    import AbstractSendMeMulticastCommandsVertex
from spinn_front_end_common.utilities import globals_variables
from spinn_front_end_common.utilities.notification_protocol \
    import SocketAddress
from spinn_front_end_common.utility_models import LivePacketGather

# spinnman imports
from spinnman.messages.eieio.eieio_type import EIEIOType

# main
from spynnaker.pyNN.connections \
    import EthernetCommandConnection, EthernetControlConnection, \
    SpynnakerLiveSpikesConnection, SpynnakerPoissonControlConnection

from spynnaker.pyNN.external_devices_models \
    import AbstractEthernetController, AbstractEthernetSensor
from spynnaker.pyNN.external_devices_models \
    import ArbitraryFPGADevice, ExternalCochleaDevice, ExternalFPGARetinaDevice
from spynnaker.pyNN.external_devices_models \
    import MunichMotorDevice, MunichRetinaDevice

# PushBot
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_control_modules\
    import PushBotLifEthernet, PushBotLifSpinnakerLink
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_ethernet \
    import PushBotEthernetLaserDevice, PushBotEthernetLEDDevice, \
    PushBotEthernetMotorDevice, PushBotEthernetRetinaDevice, \
    PushBotEthernetSpeakerDevice
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_spinnaker_link \
    import PushBotSpiNNakerLinkLaserDevice, PushBotSpiNNakerLinkLEDDevice, \
    PushBotSpiNNakerLinkMotorDevice, PushBotSpiNNakerLinkRetinaDevice, \
    PushBotSpiNNakerLinkSpeakerDevice
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_parameters \
    import PushBotLED, PushBotMotor, PushBotRetinaResolution, PushBotLaser, \
    PushBotSpeaker, PushBotRetinaViewer

# other plugins
from spynnaker.pyNN.protocols \
    import MunichIoSpiNNakerLinkProtocol
from spynnaker.pyNN.spynnaker_external_device_plugin_manager \
    import SpynnakerExternalDevicePluginManager
from spynnaker.pyNN.external_devices_models import ExternalDeviceLifControl

# injector
from spynnaker.pyNN.models.utility_models \
    import SpikeInjector as ExternalDeviceSpikeInjector

# useful functions
add_database_socket_address = \
    SpynnakerExternalDevicePluginManager.add_database_socket_address
activate_live_output_to = \
    SpynnakerExternalDevicePluginManager.activate_live_output_to
activate_live_output_for = \
    SpynnakerExternalDevicePluginManager.activate_live_output_for
add_poisson_live_rate_control = \
    SpynnakerExternalDevicePluginManager.add_poisson_live_rate_control

logger = logging.getLogger(__name__)

spynnaker_external_devices = SpynnakerExternalDevicePluginManager()

__all__ = [
    "EIEIOType",

    # General Devices
    "ExternalCochleaDevice", "ExternalFPGARetinaDevice",
    "MunichRetinaDevice", "MunichMotorDevice",
    "ArbitraryFPGADevice", "PushBotRetinaViewer",
    "ExternalDeviceLifControl",

    # Pushbot Parameters
    "MunichIoSpiNNakerLinkProtocol",
    "PushBotLaser", "PushBotLED", "PushBotMotor", "PushBotSpeaker",
    "PushBotRetinaResolution",

    # Pushbot Ethernet Parts
    "PushBotLifEthernet", "PushBotEthernetLaserDevice",
    "PushBotEthernetLEDDevice", "PushBotEthernetMotorDevice",
    "PushBotEthernetSpeakerDevice", "PushBotEthernetRetinaDevice",

    # Pushbot SpiNNaker Link Parts
    "PushBotLifSpinnakerLink", "PushBotSpiNNakerLinkLaserDevice",
    "PushBotSpiNNakerLinkLEDDevice", "PushBotSpiNNakerLinkMotorDevice",
    "PushBotSpiNNakerLinkSpeakerDevice", "PushBotSpiNNakerLinkRetinaDevice",

    # Connections
    "SpynnakerLiveSpikesConnection",
    "SpynnakerPoissonControlConnection",

    # Provided functions
    "activate_live_output_for",
    "activate_live_output_to",
    "SpikeInjector",
    "register_database_notification_request",
    "add_poisson_live_rate_control"]


def register_database_notification_request(hostname, notify_port, ack_port):
    """ Adds a socket system which is registered with the notification protocol

    :param hostname: ip address of host
    :param notify_port: port for listeing for when database is set up
    :param ack_port: the port for sending back the ack
    :rtype: None
    """
    spynnaker_external_devices.add_socket_address(SocketAddress(
        hostname, notify_port, ack_port))


def EthernetControl(
        n_neurons, params, label=None, local_host=None, local_port=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Create a PyNN population that can be included in a network to\
        control an external device which is connected to the host

    :param n_neurons: The number of neurons in the control population
    :param model: Class of a model that implements AbstractEthernetController
    :param params: The parameters of the model
    :param label: An optional label for the population
    :param local_host:\
        The optional local host IP address to listen on for commands
    :param lost_port: The optional local port to listen on for commands
    :param database_ack_port_num:\
        The optional port to which responses to the database notification\
        protocol are to be sent
    :param database_notify_port_num:\
        The optional port to which notifications from the database\
        notification protocol are to be sent
    :return:\
        A pyNN Population which can be used as the target of a Projection.\
        Note that the Population can also be used as the source of a\
        Projection, but it might not send spikes.
    """
    if not issubclass(params['model'], AbstractEthernetController):
        raise Exception(
            "Model must be a subclass of AbstractEthernetController")
    vertex = params['model']
    translator = vertex.get_message_translator()
    ethernet_control_connection = EthernetControlConnection(
        translator, local_host, local_port)
    devices_with_commands = [
        device for device in vertex.get_external_devices()
        if isinstance(device, AbstractSendMeMulticastCommandsVertex)]
    if devices_with_commands:
        ethernet_command_connection = EthernetCommandConnection(
            translator, devices_with_commands, local_host,
            database_notify_port_num)
        add_database_socket_address(
            ethernet_command_connection.local_ip_address,
            ethernet_command_connection.local_port, database_ack_port_num)
    live_packet_gather = LivePacketGather(
        ethernet_control_connection.local_ip_address,
        ethernet_control_connection.local_port,
        message_type=EIEIOType.KEY_PAYLOAD_32_BIT,
        payload_as_time_stamps=False, use_payload_prefix=False)
    spynnaker_external_devices.add_application_vertex(live_packet_gather)
    for partition_id in vertex.get_outgoing_partition_ids():
        spynnaker_external_devices.add_edge(
            vertex, live_packet_gather, partition_id)
    return vertex


def EthernetSensorPopulation(
        model, params, local_host=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Create a pyNN population which can be included in a network to\
        receive spikes from a device connected to the host

    :param model: Class of a model that implements AbstractEthernetController
    :param params: The parameters of the model
    :param local_host:\
        The optional local host IP address to listen on for database\
        notification
    :param database_ack_port_num:\
        The optional port to which responses to the database notification\
        protocol are to be sent
    :param database_notify_port_num:\
        The optional port to which notifications from the database\
        notification protocol are to be sent
    :return:\
        A pyNN Population which can be used as the source of a Projection.\
        Note that the Population cannot be used as the target of a Projection.
    """
    if not issubclass(model, AbstractEthernetSensor):
        raise Exception("Model must be a subclass of AbstractEthernetSensor")
    device = model(**params)
    injector_params = dict(device.get_injector_parameters())
    injector_params['notify'] = False

    spike_injector_params = dict(injector_params)
    spike_injector_params['n_neurons'] = device.get_n_neurons()
    spike_injector_params['label'] = device.get_injector_label()

    vertex = SpikeInjector(**injector_params)
    if isinstance(device, AbstractSendMeMulticastCommandsVertex):
        ethernet_command_connection = EthernetCommandConnection(
            device.get_translator(), [device], local_host,
            database_notify_port_num)
        add_database_socket_address(
            ethernet_command_connection.local_ip_address,
            ethernet_command_connection.local_port, database_ack_port_num)
    database_connection = device.get_database_connection()
    if database_connection is not None:
        add_database_socket_address(
            database_connection.local_ip_address,
            database_connection.local_port, database_ack_port_num)
    return vertex


def SpikeInjector(
        n_neurons, label, port=None, notify=True,
        virtual_key=None, database_notify_host=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Supports adding a spike injector to the application graph.

    :param n_neurons: the number of neurons the spike injector will emulate
    :type n_neurons: int
    :param notify: allows us to not bother with the database system
    :type notify: bool
    :param label: the label given to the population
    :type label: str
    :param port: the port number used to listen for injections of spikes
    :type port: int
    :param virtual_key: the virtual key used in the routing system
    :type virtual_key: int
    :param database_notify_host: the hostname for the device which is\
        listening to the database notification.
    :type database_notify_host: str
    :param database_ack_port_num: the port number to which a external device\
        will acknowledge that they have finished reading the database and\
        are ready for it to start execution
    :type database_ack_port_num: int
    :param database_notify_port_num: The port number to which a external\
        device will receive the database is ready command
    :type database_notify_port_num: int
    """
    if notify:
        _process_database_socket(
            database_notify_port_num, database_notify_host,
            database_ack_port_num)
    return ExternalDeviceSpikeInjector(
        n_neurons=n_neurons, label=label, port=port, virtual_key=virtual_key)


def _process_database_socket(
        database_notify_port_num, database_notify_host, database_ack_port_num):
    """ Build a database socket address as needed

    :param database_notify_port_num: \
        the port num where to send the DB-is-written packet.
    :param database_notify_host: \
        the hostname or IP address of where to send the DB-is-written packet.
    :param database_ack_port_num: the port number to listen on for ack of \
        having read and set them selves up on.
    :rtype: None
    """
    config = globals_variables.get_simulator().config
    if database_notify_port_num is None:
        database_notify_port_num = config.getint("Database", "notify_port")
    if database_notify_host is None:
        database_notify_host = config.get("Database", "notify_hostname")
    if database_ack_port_num is None:
        database_ack_port_num = config.get("Database", "listen_port")
        if database_ack_port_num == "None":
            database_ack_port_num = None

    # build the database socket address used by the notification interface
    database_socket = SocketAddress(
        listen_port=database_ack_port_num,
        notify_host_name=database_notify_host,
        notify_port_no=database_notify_port_num)

    # update socket interface with new demands.
    spynnaker_external_devices.add_socket_address(database_socket)
