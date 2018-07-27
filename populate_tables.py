#!/usr/bin/python

"""
Andrew Southard andsouth44@gmail.com.
2018 Packet Consulting Inc.
"""


import mysql.connector
import logging
from jnpr.junos import Device
import private_vars as private
from create_tables_mysql import create_tables
from datetime import datetime
import os
from multiprocessing import Process, Lock


cwd = os.path.dirname(os.path.abspath(__file__))


""" Configure logging """
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s:%(asctime)s:%(name)s:%(process)d')
file_handler = logging.FileHandler('{}/sn_conf.log'.format(cwd), mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


""" Helper functions """


def breakup_hyphen(s):
    """ Function to convert string 110-114 to list [110, 111, 112, 113, 114] """
    numbers = []
    l,h = map(int, s.split('-'))
    numbers += range(l,h+1)
    return numbers


lock = Lock()


def db_do(action):
    """ Function to acquire multiprocessing lock before running 'action' """
    lock.acquire()
    action
    lock.release()


def get_chunks(data, size):
    """ Function to return iterables of items from data of size 'size' """
    return (data[pos:pos + size] for pos in range(0, len(data), size))


""" Main function """


def orchestrator():
    """
    Function to:
    Create new MySQL DB
    Orchestrate setting up multiprocessing processes in groups

    """
    start = datetime.now()
    logger.info('Module starting')

    create_tables()

    procs = []

    hostnames = open(cwd + '/switchlist1.txt').readlines()

    for group in get_chunks(hostnames, 8):
        for hostname in group:
            proc = Process(target=populate_db, args=(hostname,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

    duration = datetime.now() - start
    logger.info('Module took {} to complete'.format(duration))


""" Called function """


def populate_db(hostname):
    """
    Function to:
    Connect to a device
    Grab config in XML format
    Search through the config
    Upload relevant parameters to database

    """

    db = mysql.connector.connect(pool_name="mypool", user=private.mysqluser, password=private.mysqlpw, host=private.mysqlhost, database=private.mysqldb)
    cur = db.cursor()
    try:
        logger.info('Working on: {}'.format(hostname.strip()))
        dev = Device(host=hostname.strip(), user=private.deviceuser, password=private.devicepw, port=22)
        dev.open(auto_probe=5)
        model = dev.facts['model']
        config = dev.rpc.get_config()
        dev.close()
    except Exception as e:
        logger.warning('Error: {}'.format(e))

    if config.findall('interfaces/interface') is not None and model[:2] == 'EX':
        interfaces = config.findall('interfaces/interface')

        for item in interfaces:
            """
            If the interface is an ae bundle member, use the main interface number and
            description and record the bundle number
            """

            if item.find('ether-options/ieee-802.3ad/bundle') is not None:
                interface = item.find('name').text
                interface_details = {'device_int': '{}_{}'.format(hostname.strip(), interface),
                                     'bundle': item.find('ether-options/ieee-802.3ad/bundle').text}

                if item.find('description') is not None:
                    interface_details['description'] = item.find('description').text
                else:
                    interface_details['description'] = None

                logger.debug(interface_details)

                try:
                    db_do(cur.execute(
                        'insert into interfaces (device_int_unit, description, bundle) values (%s, %s, %s)',
                        (interface_details['device_int'], interface_details['description'],
                         interface_details['bundle'])))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

            elif item.find('name').text.split('-')[0][:2] in ('ge', 'xe', 'ae', 'ir', 'lo', 'sp', 'em'):
                # create a variable for the main interface number
                interface = item.find('name').text

                interface_details = {'device_int': '{}_{}'.format(hostname.strip(), interface)}

                if item.find('unit/family/ethernet-switching/port-mode') is not None:
                    interface_details['port_mode'] = item.find('unit/family/ethernet-switching/port-mode').text
                else:
                    interface_details['port_mode'] = None

                if item.find('description') is not None:
                    main_description = item.find('description').text
                    interface_details['description'] = item.find('description').text
                else:
                    interface_details['description'] = None

                logger.debug(interface_details)

                try:
                    db_do(cur.execute(
                        'insert into interfaces (device_int_unit, description, port_mode) values (%s, %s, %s)',
                        (interface_details['device_int'], interface_details['description'],
                         interface_details['port_mode'])))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

                if item.find('unit/family/ethernet-switching/vlan/members') is not None:
                    members = item.findall('unit/family/ethernet-switching/vlan/members')
                    if item.find('unit/family/ethernet-switching/port-mode') is not None:
                        interface_encapsulation = item.find('unit/family/ethernet-switching/port-mode').text
                    else:
                        interface_encapsulation = None

                    for member in members:
                        if '-' in member.text:
                            member_list = breakup_hyphen(member.text)
                            for member in member_list:
                                interface_details = {
                                    'device_int_vlan': '{}_{}.{}'.format(hostname.strip(), interface, member)}
                                interface_details['description'] = main_description
                                interface_details['port_mode'] = interface_encapsulation
                                interface_details['vlan_outer'] = member

                                logger.debug(interface_details)

                                try:
                                    db_do(cur.execute(
                                        'insert into interfaces (device_int_unit, description, port_mode, vlan_outer) values (%s, %s, %s, %s)',
                                        (interface_details['device_int_vlan'], interface_details['description'],
                                         interface_details['port_mode'], interface_details['vlan_outer'])))
                                except Exception as e:
                                    logger.warning('Error: {}'.format(e))

                                db_do(db.commit())

                        else:
                            interface_details = {
                                'device_int_vlan': '{}_{}.{}'.format(hostname.strip(), interface, member.text)}
                            interface_details['port_mode'] = interface_encapsulation
                            interface_details['description'] = main_description
                            interface_details['vlan_outer'] = member.text

                            logger.debug(interface_details)

                            try:
                                db_do(cur.execute(
                                    'insert into interfaces (device_int_unit, description, port_mode, vlan_outer) values (%s, %s, %s, %s)',
                                    (interface_details['device_int_vlan'], interface_details['description'],
                                     interface_details['port_mode'], interface_details['vlan_outer'])))
                            except Exception as e:
                                logger.warning('Error: {}'.format(e))

                            db_do(db.commit())


            elif item.find('name').text in ('vlan',):

                if item.find('unit/name') is not None:
                    interface_details = {
                        'device_int_unit': '{}_vlan.{}'.format(hostname.strip(), item.find('unit/name').text)}

                if item.find('unit/description') is not None:
                    interface_details['description'] = item.find('unit/description').text
                else:
                    interface_details['description'] = None

                if item.find('unit/family/inet/address/name') is not None:
                    interface_details['ip'] = item.find('unit/family/inet/address/name').text
                else:
                    interface_details['ip'] = None

                logger.debug(interface_details)

                try:
                    db_do(cur.execute(
                        'insert into interfaces (device_int_unit, description, ip) values (%s, %s, %s)',
                        (interface_details['device_int_unit'], interface_details['description'],
                         interface_details['ip'])))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

    if config.findall('interfaces/interface') is not None and model[:2] != 'EX':
        interfaces = config.findall('interfaces/interface')

        for item in interfaces:
            """
            If the interface is an ae bundle member, use the main interface number and
            description and record the bundle number
            """
            if item.find('gigether-options/ieee-802.3ad/bundle') is not None:
                interface = item.find('name').text
                interface_details = {'device_int_unit': '{}_{}'.format(hostname.strip(), interface),
                                     'bundle': item.find('gigether-options/ieee-802.3ad/bundle').text}

                if item.find('description') is not None:
                    interface_details['description'] = item.find('description').text
                else:
                    interface_details['description'] = None

                logger.debug(interface_details)

                try:
                    db_do(cur.execute(
                        'insert into interfaces (device_int_unit, description, bundle) values (%s, %s, %s)',
                        (interface_details['device_int_unit'], interface_details['description'],
                         interface_details['bundle'])))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

            elif item.find('ether-options/ieee-802.3ad/bundle') is not None:
                interface = item.find('name').text
                interface_details = {'device_int_unit': '{}_{}'.format(hostname.strip(), interface),
                                     'bundle': item.find('ether-options/ieee-802.3ad/bundle').text}

                if item.find('description') is not None:
                    interface_details['description'] = item.find('description').text
                else:
                    interface_details['description'] = None

                logger.debug(interface_details)

                try:
                    db_do(cur.execute(
                        'insert into interfaces (device_int_unit, description, bundle) values (%s, %s, %s)',
                        (interface_details['device_int_unit'], interface_details['description'],
                         interface_details['bundle'])))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

            elif item.find('name').text.split('-')[0][:2] in ('ge', 'xe', 'ae', 'ir', 'lo', 'sp', 'em'):
                # create a variable for the main interface number
                interface = item.find('name').text
                # create a variable for the main interface description, if present
                if item.find('description') is not None:
                    main_description = item.find('description').text
                else:
                    main_description = None

                for units in item.iter('unit'):
                    interface_details = {'device_int_unit': '{}_{}.{}'.format(hostname.strip(), interface,
                                                                              units.find('name').text)}
                    '''
                    if the unit has no description use the main interface description
                    '''
                    if units.find('description') is None:
                        interface_details['description'] = main_description
                    else:
                        interface_details['description'] = units.find('description').text

                    if units.find('encapsulation') is not None:
                        interface_details['encapsulation'] = units.find('encapsulation').text
                    else:
                        interface_details['encapsulation'] = 'ENET'

                    if units.find('vlan-id') is None and units.find('vlan-tags') is None:
                        interface_details['vlan_outer'] = None
                        interface_details['vlan_inner'] = None

                    if units.find('vlan-id') is not None:
                        interface_details['vlan_outer'] = units.find('vlan-id').text
                        interface_details['vlan_inner'] = None

                    if units.find('vlan-tags') is not None:
                        if units.find('vlan-tags/outer') is not None:
                            interface_details['vlan_outer'] = units.find('vlan-tags/outer').text
                        if units.find('vlan-tags/inner') is not None:
                            interface_details['vlan_inner'] = units.find('vlan-tags/inner').text
                        else:
                            interface_details['vlan_inner'] = None

                    if units.find('family/inet/address/name') is not None:
                        interface_details['ip'] = units.find('family/inet/address/name').text
                    else:
                        interface_details['ip'] = None

                    interface_details['bundle'] = None

                    logger.debug(interface_details)

                    try:
                        db_do(cur.execute(
                            'insert into interfaces (device_int_unit, description, encapsulation, vlan_outer, vlan_inner, bundle, ip) values (%s, %s, %s, %s, %s, %s, %s)',
                            (interface_details['device_int_unit'], interface_details['description'],
                             interface_details['encapsulation'], interface_details['vlan_outer'],
                             interface_details['vlan_inner'], interface_details['bundle'],
                             interface_details['ip'])))
                    except Exception as e:
                        logger.warning('Error: {}'.format(e))

                    db_do(db.commit())

            elif item.find('name').text.split('-')[0][:2] in ('fx', ):
                continue

            elif item.find('name').text in ('vlan',):

                if item.find('unit/name') is not None:
                    interface_details = {
                        'device_int_unit': '{}_vlan.{}'.format(hostname.strip(), item.find('unit/name').text)}

                if item.find('unit/description') is not None:
                    interface_details['description'] = item.find('unit/description').text
                else:
                    interface_details['description'] = None

                if item.find('unit/family/inet/address/name') is not None:
                    interface_details['ip'] = item.find('unit/family/inet/address/name').text
                else:
                    interface_details['ip'] = None

                logger.debug(interface_details)

                try:
                    db_do(cur.execute(
                        'insert into interfaces (device_int_unit, description, ip) values (%s, %s, %s)',
                        (interface_details['device_int_unit'], interface_details['description'],
                         interface_details['ip'])))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

            else:
                logger.warning('Interface type does not match any recognised type: {}'.format(item.find('name').text))

    if config.findall('interfaces/interface-set') is not None:
        interface_sets = config.findall('interfaces/interface-set')

        for set in interface_sets:

            set_name = set.find('name').text
            int_name = set.find('interface/name').text

            for unit in set.iter('unit'):
                unit_name = unit.find('name').text
                interface = '{}_{}.{}'.format(hostname.strip(), int_name, unit_name)
                try:
                    db_do(cur.execute('update interfaces set interface_set = %s where device_int_unit = %s', (set_name, interface)))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                logger.debug('{} {}_{}.{}'.format(set_name, hostname.strip(), int_name, unit_name))

                db_do(db.commit())

    if config.find('routing-instances') is not None:
        conf_ris = config.find('routing-instances')
        for item in conf_ris:

            ri_details = {}

            if item.find('name') is not None:
                ri_details = {'instance_name' : '{}_{}'.format(hostname.strip(), item.find('name').text)}
            else:
                ri_details['instance_name'] = None

            if item.find('instance-type') is not None:
                ri_details['type'] = item.find('instance-type').text
            else:
                ri_details['type'] = None

            if item.find('route-distinguisher/rd-type') is not None:
                ri_details['rd'] = item.find('route-distinguisher/rd-type').text
            else:
                ri_details['rd'] = None

            if item.find('vrf-target/community') is not None:
                ri_details['rt'] = item.find('vrf-target/community').text
            else:
                ri_details['rt'] = None

            if item.find('protocols/bgp') is not None:
                ri_details['protocol'] = 'BGP'
            elif item.find('protocols/rip') is not None:
                ri_details['protocol'] = 'RIP'
            elif item.find('protocols/ospf') is not None:
                ri_details['protocol'] = 'OSPF'
            elif item.find('protocols/vpls') is not None:
                ri_details['protocol'] = 'VPLS'
            elif item.find('protocols/l2vpn') is not None:
                ri_details['protocol'] = 'L2VPN'
            else:
                ri_details['protocol'] = None

            if item.find('forwarding-options/dhcp-relay/server-group/server-group/address') is not None:
                forwarders = item.findall('forwarding-options/dhcp-relay/server-group/server-group/address')
                IPS = []
                for forwarder in forwarders:
                    IPS.append(forwarder.find('name').text)
                if len(IPS) == 1:
                    ri_details['dhcp_forwarder1'] = IPS[0]
                    ri_details['dhcp_forwarder2'] = None
                if len(IPS) > 1:
                    ri_details['dhcp_forwarder1'] = IPS[0]
                    ri_details['dhcp_forwarder2'] = IPS[1]
            else:
                ri_details['dhcp_forwarder1'] = None
                ri_details['dhcp_forwarder2'] = None

            try:
                db_do(cur.execute(
                    'insert into routing_instances (instance_name, type, rd, rt, protocol, dhcp_forwarder1, dhcp_forwarder2) values (%s, %s, %s, %s, %s, %s, %s)',
                    (ri_details['instance_name'], ri_details['type'], ri_details['rd'], ri_details['rt'], ri_details['protocol'], ri_details['dhcp_forwarder1'], ri_details['dhcp_forwarder2'])))

            except Exception as e:
                logger.warning('Error: {}'.format(e))

            logger.debug(ri_details)

            db_do(db.commit())

            for interface in item.findall('interface'):
                int_name = '{}_{}'.format(hostname.strip(), interface.find('name').text)
                try:
                    db_do(cur.execute('update interfaces set routing_instance = %s where device_int_unit = %s', (item.find('name').text, int_name)))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

                logger.debug('{}_{}'.format(item.find('name').text, int_name))

    if config.find('bridge-domains') is not None:
        bridge_domains = config.find('bridge-domains')

        for bridge in bridge_domains:

            if bridge.find('name') is not None:
                bridge_details = {'domain_name' : '{}_{}'.format(hostname.strip(), bridge.find('name').text)}
            else:
                bridge_details = {'domain_name' : None}

            if bridge.find('description') is not None:
                bridge_details['description'] = bridge.find('description').text
            else:
                bridge_details['description'] = None

            if bridge.find('domain-type') is not None:
                bridge_details['type'] = bridge.find('domain-type').text
            else:
                bridge_details['type'] = None

            if bridge.find('vlan-id') is not None:
                bridge_details['vlan_id'] = bridge.find('vlan-id').text
            else:
                bridge_details['vlan_id'] = None

            try:
                db_do(cur.execute(
                    'insert into bridge_domains (domain_name, description, type, vlan_id) values (%s, %s, %s, %s)',
                    (bridge_details['domain_name'], bridge_details['description'], bridge_details['type'],
                     bridge_details['vlan_id'])))
            except Exception as e:
                logger.warning('Error: {}'.format(e))

            logger.debug(bridge_details)

            db_do(db.commit())

            if bridge.find('routing-interface') is not None:
                int_name = '{}_{}'.format(hostname.strip(), bridge.find('routing-interface').text)
                try:
                    cur.execute('update interfaces set bridge_domain = %s where device_int_unit = %s', (bridge.find('name').text, int_name))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

                logger.debug('{}_{}'.format(bridge.find('name').text, int_name))

            for int in bridge.iter('interface'):
                int_name = '{}_{}'.format(hostname.strip(), int.find('name').text)
                try:
                    cur.execute('update interfaces set bridge_domain = %s where device_int_unit = %s', (bridge.find('name').text, int_name))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

                logger.debug('{}_{}'.format(bridge.find('name').text, int_name))

    if config.find('class-of-service/schedulers') is not None:
        schedulers = config.findall('class-of-service/schedulers')

        for scheduler in schedulers:

            scheduler_details = {'name': '{}_{}'.format(hostname.strip(), scheduler.find('name').text)}

            if scheduler.find('shaping-rate/rate') is not None:
                scheduler_details['shaping_rate'] = scheduler.find('shaping-rate/rate').text
            else:
                scheduler_details['shaping_rate'] = None

            if scheduler.find('transmit-rate/percent') is not None:
                scheduler_details['transmit_rate'] = '{}{}'.format(scheduler.find('transmit-rate/percent').text, '%')
            elif scheduler.find('transmit-rate/rate') is not None:
                scheduler_details['transmit_rate'] = scheduler.find('transmit-rate/rate').text
            else:
                scheduler_details['transmit_rate'] = None

            if scheduler.find('priority') is not None:
                scheduler_details['priority'] = scheduler.find('priority').text
            else:
                scheduler_details['priority'] = None

            logger.debug(scheduler_details)

            try:
                db_do(cur.execute(
                    'insert into schedulers (name, shaping_rate, transmit_rate, priority) values (%s, %s, %s, %s)',
                    (scheduler_details['name'], scheduler_details['shaping_rate'],
                     scheduler_details['transmit_rate'], scheduler_details['priority'])))
            except Exception as e:
                logger.warning('Error: {}'.format(e))

            db_do(db.commit())

    if config.find('class-of-service/forwarding-classes') is not None:
        forwarding_classes = config.findall('class-of-service/forwarding-classes/queue')

        for forwarding_class in forwarding_classes:

            forwarding_details = {
                'name': '{}_{}'.format(hostname.strip(), forwarding_class.find('class-name').text)}

            if forwarding_class.find('name') is not None:
                forwarding_details['queue'] = forwarding_class.find('name').text
            else:
                forwarding_details['queue'] = None

            if forwarding_class.find('priority') is not None:
                forwarding_details['priority'] = forwarding_class.find('priority').text
            else:
                forwarding_details['priority'] = None

            logger.debug(forwarding_details)

            try:
                db_do(cur.execute(
                    'insert into forwarding_classes (name, queue, priority) values (%s, %s, %s)',
                    (forwarding_details['name'], forwarding_details['queue'], forwarding_details['priority'])))
            except Exception as e:
                logger.warning('Error: {}'.format(e))

            db_do(db.commit())

    if config.find('class-of-service/scheduler-maps') is not None:
        scheduler_maps = config.findall('class-of-service/scheduler-maps')

        for scheduler_map in scheduler_maps:

            if scheduler_map.find('name') is not None:
                scheduler_map_details = {
                    'name': '{}_{}'.format(hostname.strip(), scheduler_map.find('name').text)}

            try:
                db_do(cur.execute('insert into scheduler_maps (name) values (%s)', (scheduler_map_details['name'],)))
            except Exception as e:
                logger.warning('Error: {}'.format(e))

            db_do(db.commit())

            if scheduler_map.find('forwarding-class') is not None:

                i = 1
                for forwarding_class in scheduler_map.iter('forwarding-class'):
                    scheduler_map_details['forwarding_class' + str(i)] = '{}_{}'.format(hostname.strip(),
                                                                                        forwarding_class.find(
                                                                                            'name').text)
                    scheduler_map_details['scheduler' + str(i)] = '{}_{}'.format(hostname.strip(),
                                                                                 forwarding_class.find(
                                                                                     'scheduler').text)
                    i = i + 1

                    logger.debug(scheduler_map_details)

                    for k in scheduler_map_details:
                        if k[:16] in ('forwarding_class',):
                            try:
                                db_do(cur.execute('update scheduler_maps set {} = %s where name = %s'.format(k, ),
                                            (scheduler_map_details[k], scheduler_map_details['name'])))
                            except Exception as e:
                                logger.warning('Error: {}'.format(e))
                            db_do(db.commit())

                    for k in scheduler_map_details:
                        if k[:9] in ('scheduler',):
                            try:
                                db_do(cur.execute('update scheduler_maps set {} = %s where name = %s'.format(k, ),
                                            (scheduler_map_details[k], scheduler_map_details['name'])))
                            except Exception as e:
                                logger.warning('Error: {}'.format(e))
                            db_do(db.commit())

    if config.find('class-of-service/traffic-control-profiles') is not None:
        traffic_control_profiles = config.findall('class-of-service/traffic-control-profiles')

        for traffic_control_profile in traffic_control_profiles:

            if traffic_control_profile.find('name') is not None:
                tcp_details = {
                    'name': '{}_{}'.format(hostname.strip(), traffic_control_profile.find('name').text)}
            else:
                tcp_details = {'name': None}

            if traffic_control_profile.find('scheduler-map') is not None:
                tcp_details['scheduler_map'] = '{}_{}'.format(hostname.strip(), traffic_control_profile.find('scheduler-map').text)
            else:
                tcp_details['scheduler_map'] = None

            if traffic_control_profile.find('shaping-rate/rate') is not None:
                tcp_details['shaping_rate'] = traffic_control_profile.find('shaping-rate/rate').text
            else:
                tcp_details['shaping_rate'] = None

            logger.debug(tcp_details)

            try:
                db_do(cur.execute(
                    'insert into traffic_control_profiles (name, scheduler_map, shaping_rate) values (%s, %s, %s)',
                    (tcp_details['name'], tcp_details['scheduler_map'], tcp_details['shaping_rate'])))
            except Exception as e:
                logger.warning('Error: {}'.format(e))

            db_do(db.commit())

    if config.find('class-of-service/interfaces/interface-set') is not None:
        cos_interface_sets = config.findall('class-of-service/interfaces/interface-set')

        for cos_interface_set in cos_interface_sets:

            if cos_interface_set.find('name') is not None:
                cos_interface_set_details = {
                    'name': '{}_{}'.format(hostname.strip(), cos_interface_set.find('name').text)}
            else:
                cos_interface_set_details = {'name': None}

            if cos_interface_set.find('output-traffic-control-profile/profile-name') is not None:
                cos_interface_set_details['traffic_control_profile'] = '{}_{}'.format(hostname.strip(), cos_interface_set.find('output-traffic-control-profile/profile-name').text)
            else:
                cos_interface_set_details['output-traffic-control-profile/profile-name'] = None

            logger.debug(cos_interface_set_details)

            try:
                db_do(cur.execute(
                    'insert into cos_interface_sets (name, traffic_control_profile) values (%s, %s)',
                    (cos_interface_set_details['name'], cos_interface_set_details['traffic_control_profile'])))
            except Exception as e:
                logger.warning('Error: {}'.format(e))

            db_do(db.commit())

    if config.findall('class-of-service/interfaces/interface') is not None:
        cos_interfaces = config.findall('class-of-service/interfaces/interface')

        for cos_interface in cos_interfaces:
            # create a variable for the main interface number
            interface = cos_interface.find('name').text

            cos_interface_details = {'device_int_unit': '{}_{}'.format(hostname.strip(), interface)}

            if cos_interface.find('scheduler-map') is not None:
                cos_interface_details['scheduler_map'] = '{}_{}'.format(hostname.strip(), cos_interface.find(
                    'scheduler-map').text)
            else:
                cos_interface_details['scheduler_map'] = None

            if cos_interface.find('output-traffic-control-profile/profile-name') is not None:
                cos_interface_details['traffic_control_profile'] = '{}_{}'.format(hostname.strip(),
                                                                                  cos_interface.find(
                                                                                      'output-traffic-control-profile/profile-name').text)
            else:
                cos_interface_details['traffic_control_profile'] = None

            if cos_interface.find('apply-groups') is not None:
                cos_interface_details['apply_group'] = cos_interface.find('apply-groups').text
            else:
                cos_interface_details['apply_group'] = None

            logger.debug(cos_interface_details)

            try:
                db_do(cur.execute(
                    'insert into cos_interfaces (device_int_unit, apply_group, scheduler_map, traffic_control_profile) values (%s, %s, %s, %s)',
                    (cos_interface_details['device_int_unit'], cos_interface_details['apply_group'],
                     cos_interface_details['scheduler_map'], cos_interface_details['traffic_control_profile'])))
            except Exception as e:
                logger.warning('Error: {}'.format(e))

            db_do(db.commit())

            for units in cos_interface.iter('unit'):
                cos_interface_details = {'device_int_unit': '{}_{}.{}'.format(hostname.strip(), interface, units.find('name').text)}

                if units.find('scheduler-map') is not None:
                    cos_interface_details['scheduler_map'] = '{}_{}'.format(hostname.strip(),
                                                                            units.find('scheduler-map').text)
                else:
                    cos_interface_details['scheduler_map'] = None

                if units.find('output-traffic-control-profile/profile-name') is not None:
                    cos_interface_details['traffic_control_profile'] = '{}_{}'.format(hostname.strip(),
                                                                                      units.find(
                                                                                          'output-traffic-control-profile/profile-name').text)
                else:
                    cos_interface_details['traffic_control_profile'] = None

                if units.find('apply-groups') is not None:
                    cos_interface_details['apply_group'] = units.find('apply-groups').text
                else:
                    cos_interface_details['apply_group'] = None

                if units.find('classifiers/ieee-802.1/classifier-name') is not None:
                    cos_interface_details['802_classifier'] = units.find(
                        'classifiers/ieee-802.1/classifier-name').text
                else:
                    cos_interface_details['802_classifier'] = None

                if units.find('classifiers/exp/classifier-name') is not None:
                    cos_interface_details['exp_classifier'] = units.find('classifiers/exp/classifier-name').text
                else:
                    cos_interface_details['exp_classifier'] = None

                if units.find('classifiers/dscp/name') is not None:
                    cos_interface_details['dscp_classifier'] = units.find('classifiers/dscp/name').text
                else:
                    cos_interface_details['dscp_classifier'] = None

                if units.find('rewrite-rules/ieee-802.1/rewrite-rule-name') is not None:
                    cos_interface_details['802_rewrite'] = units.find(
                        'rewrite-rules/ieee-802.1/rewrite-rule-name').text
                else:
                    cos_interface_details['802_rewrite'] = None

                if units.find('rewrite-rules/exp/name') is not None:
                    cos_interface_details['exp_rewrite'] = units.find('rewrite-rules/exp/name').text
                else:
                    cos_interface_details['exp_rewrite'] = None

                if units.find('rewrite-rules/dscp/name') is not None:
                    cos_interface_details['dscp_rewrite'] = units.find('rewrite-rules/dscp/name').text
                else:
                    cos_interface_details['dscp_rewrite'] = None

                logger.debug(cos_interface_details)

                try:
                    db_do(cur.execute(
                        'insert into cos_interfaces (device_int_unit, apply_group, scheduler_map, traffic_control_profile, exp_classifier, 802_classifier, dscp_classifier, exp_rewrite, 802_rewrite, dscp_rewrite) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (cos_interface_details['device_int_unit'], cos_interface_details['apply_group'],
                         cos_interface_details['scheduler_map'],
                         cos_interface_details['traffic_control_profile'],
                         cos_interface_details['exp_classifier'], cos_interface_details['802_classifier'],
                         cos_interface_details['dscp_classifier'], cos_interface_details['exp_rewrite'],
                         cos_interface_details['802_rewrite'], cos_interface_details['dscp_rewrite'])))
                except Exception as e:
                    logger.warning('Error: {}'.format(e))

                db_do(db.commit())

    db_do(db.close())


if __name__ == "__main__":
    orchestrator()
