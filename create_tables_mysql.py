#!/usr/bin/python

"""
Andrew Southard andsouth44@gmail.com.
2018 Packet Consulting Inc.
"""

import mysql.connector
import private_vars as private
import logging
import os

cwd = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s:%(asctime)s:%(name)s')
file_handler = logging.FileHandler('{}/conf_db.log'.format(cwd), mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def create_tables():
    """ create tables in the mySQL database"""
    commands = (
        """
        DROP DATABASE IF EXISTS configuration;
        """,
        """
        CREATE DATABASE configuration;
        """,
        """
        USE configuration;
        """,
        """
        CREATE TABLE interfaces (
            device_int_unit VARCHAR(50) COLLATE utf8_bin NOT NULL PRIMARY KEY,
            description VARCHAR(130) COLLATE utf8_bin NULL,
            encapsulation VARCHAR(50) COLLATE utf8_bin NULL,
            port_mode VARCHAR(50) COLLATE utf8_bin NULL,
            vlan_outer VARCHAR(50) COLLATE utf8_bin NULL,
            vlan_inner VARCHAR(50) COLLATE utf8_bin NULL,
            bundle VARCHAR(50) COLLATE utf8_bin NULL,
            ip VARCHAR(50) COLLATE utf8_bin NULL,
            interface_set VARCHAR(50) COLLATE utf8_bin NULL,
            routing_instance VARCHAR(50) COLLATE utf8_bin NULL,
            bridge_domain VARCHAR(50) COLLATE utf8_bin NULL
        )
        """,
        """
        CREATE TABLE routing_instances (
            instance_name VARCHAR(50) COLLATE utf8_bin NOT NULL PRIMARY KEY,
            type VARCHAR(50) COLLATE utf8_bin NULL,
            rd VARCHAR(50) COLLATE utf8_bin NULL,
            rt VARCHAR(50) COLLATE utf8_bin NULL,
            protocol VARCHAR(50) COLLATE utf8_bin NULL
        )
        """,
        """
         CREATE TABLE bridge_domains (
             domain_name VARCHAR(50) COLLATE utf8_bin NOT NULL PRIMARY KEY,
             description VARCHAR(100) COLLATE utf8_bin NULL,
             type VARCHAR(50) COLLATE utf8_bin NULL,
             vlan_id VARCHAR(50) COLLATE utf8_bin NULL
         )
        """,
        """
        CREATE TABLE schedulers (
            name VARCHAR(50) COLLATE utf8_bin PRIMARY KEY NOT NULL,
            shaping_rate VARCHAR(50) COLLATE utf8_bin NULL,
            transmit_rate VARCHAR(50) COLLATE utf8_bin NULL,
            priority VARCHAR(50) COLLATE utf8_bin NULL
        )
        """,
        """
        CREATE TABLE forwarding_classes (
            name VARCHAR(50) COLLATE utf8_bin PRIMARY KEY NOT NULL,
            queue VARCHAR(50) COLLATE utf8_bin NULL,
            priority VARCHAR(50) COLLATE utf8_bin NULL
        )
        """,
        """
        CREATE TABLE scheduler_maps (
            name VARCHAR(50) COLLATE utf8_bin PRIMARY KEY NOT NULL,
            forwarding_class1 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler1 VARCHAR(50) COLLATE utf8_bin NULL,
            forwarding_class2 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler2 VARCHAR(50) COLLATE utf8_bin NULL,
            forwarding_class3 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler3 VARCHAR(50) COLLATE utf8_bin NULL,
            forwarding_class4 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler4 VARCHAR(50) COLLATE utf8_bin NULL,
            forwarding_class5 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler5 VARCHAR(50) COLLATE utf8_bin NULL,
            forwarding_class6 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler6 VARCHAR(50) COLLATE utf8_bin NULL,
            forwarding_class7 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler7 VARCHAR(50) COLLATE utf8_bin NULL,
            forwarding_class8 VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler8 VARCHAR(50) COLLATE utf8_bin NULL,
            FOREIGN KEY (forwarding_class1) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler1) REFERENCES schedulers (name),
            FOREIGN KEY (forwarding_class2) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler2) REFERENCES schedulers (name),
            FOREIGN KEY (forwarding_class3) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler3) REFERENCES schedulers (name),
            FOREIGN KEY (forwarding_class4) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler4) REFERENCES schedulers (name),
            FOREIGN KEY (forwarding_class5) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler5) REFERENCES schedulers (name),
            FOREIGN KEY (forwarding_class6) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler6) REFERENCES schedulers (name),
            FOREIGN KEY (forwarding_class7) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler7) REFERENCES schedulers (name),
            FOREIGN KEY (forwarding_class8) REFERENCES forwarding_classes (name),
            FOREIGN KEY (scheduler8) REFERENCES schedulers (name)
        )
        """,
        """
        CREATE TABLE traffic_control_profiles (
            name VARCHAR(100) COLLATE utf8_bin PRIMARY KEY NOT NULL,
            scheduler_map VARCHAR(50) COLLATE utf8_bin NULL,
            shaping_rate VARCHAR(50) COLLATE utf8_bin NULL,
            FOREIGN KEY (scheduler_map) REFERENCES scheduler_maps (name)
        )
        """,
        """
        CREATE TABLE cos_interface_sets (
            name VARCHAR(100) COLLATE utf8_bin PRIMARY KEY NOT NULL,
            traffic_control_profile VARCHAR(50) COLLATE utf8_bin NULL,
            FOREIGN KEY (traffic_control_profile) REFERENCES traffic_control_profiles (name)
        )
        """,
        """
        CREATE TABLE cos_interfaces (
            device_int_unit VARCHAR(100) COLLATE utf8_bin PRIMARY KEY NOT NULL,
            apply_group VARCHAR(50) COLLATE utf8_bin NULL,
            scheduler_map VARCHAR(50) COLLATE utf8_bin NULL,
            traffic_control_profile VARCHAR(50) COLLATE utf8_bin NULL,
            exp_classifier VARCHAR(50) COLLATE utf8_bin NULL,
            802_classifier VARCHAR(50) COLLATE utf8_bin NULL,
            dscp_classifier VARCHAR(50) COLLATE utf8_bin NULL,
            exp_rewrite VARCHAR(50) COLLATE utf8_bin NULL,
            802_rewrite VARCHAR(50) COLLATE utf8_bin NULL,
            dscp_rewrite VARCHAR(50) COLLATE utf8_bin NULL,
            FOREIGN KEY (scheduler_map) REFERENCES scheduler_maps (name),
            FOREIGN KEY (traffic_control_profile) REFERENCES traffic_control_profiles (name)
        )
        """,
        """
        CREATE PROCEDURE getsize() BEGIN
        SELECT table_schema AS "Database", ROUND(SUM(data_length + index_length) / 1024 /1024, 2) AS "Size (MB)" FROM information_schema.TABLES GROUP BY table_schema;
        END
        """
    )

    try:
        # connect to the mySQL server
        db = mysql.connector.connect(user=private.mysqluser, password=private.mysqlpw, host=private.mysqlhost, database=private.mysqldb)
        cur = db.cursor()

        # run SQL commands to set up DB and tables
        for command in commands:
            cur.execute(command)

        # commit the changes
        db.commit()

        # close communication with the mySQL database server
        db.close()

    except Exception as e:
        logger.warning('Error: {}'.format(e))

if __name__ == '__main__':
    create_tables()
