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
        DROP DATABASE IF EXISTS configurationdb;
        """,
        """
        CREATE DATABASE configurationdb;
        """,
        """
        USE configurationdb;
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
            ip VARCHAR(50) COLLATE utf8_bin NULL
        )
        """,
        """
        CREATE TABLE interface_sets (
            device_name VARCHAR(50) COLLATE utf8_bin NOT NULL PRIMARY KEY,
            interface1 VARCHAR(50) COLLATE utf8_bin NULL,
            interface2 VARCHAR(50) COLLATE utf8_bin NULL,
            interface3 VARCHAR(50) COLLATE utf8_bin NULL,
            interface4 VARCHAR(50) COLLATE utf8_bin NULL,
            interface5 VARCHAR(50) COLLATE utf8_bin NULL,
            interface6 VARCHAR(50) COLLATE utf8_bin NULL,
            interface7 VARCHAR(50) COLLATE utf8_bin NULL,
            interface8 VARCHAR(50) COLLATE utf8_bin NULL,
            interface9 VARCHAR(50) COLLATE utf8_bin NULL,
            interface10 VARCHAR(50) COLLATE utf8_bin NULL,
            interface11 VARCHAR(50) COLLATE utf8_bin NULL,
            interface12 VARCHAR(50) COLLATE utf8_bin NULL,
            interface13 VARCHAR(50) COLLATE utf8_bin NULL,
            interface14 VARCHAR(50) COLLATE utf8_bin NULL,
            interface15 VARCHAR(50) COLLATE utf8_bin NULL,
            interface16 VARCHAR(50) COLLATE utf8_bin NULL,
            interface17 VARCHAR(50) COLLATE utf8_bin NULL,
            interface18 VARCHAR(50) COLLATE utf8_bin NULL,
            interface19 VARCHAR(50) COLLATE utf8_bin NULL,
            interface20 VARCHAR(50) COLLATE utf8_bin NULL,
            interface21 VARCHAR(50) COLLATE utf8_bin NULL,
            interface22 VARCHAR(50) COLLATE utf8_bin NULL,
            interface23 VARCHAR(50) COLLATE utf8_bin NULL,
            interface24 VARCHAR(50) COLLATE utf8_bin NULL,
            interface25 VARCHAR(50) COLLATE utf8_bin NULL,
            interface26 VARCHAR(50) COLLATE utf8_bin NULL,
            interface27 VARCHAR(50) COLLATE utf8_bin NULL,
            interface28 VARCHAR(50) COLLATE utf8_bin NULL,
            interface29 VARCHAR(50) COLLATE utf8_bin NULL,
            interface30 VARCHAR(50) COLLATE utf8_bin NULL,
            interface31 VARCHAR(50) COLLATE utf8_bin NULL,
            interface32 VARCHAR(50) COLLATE utf8_bin NULL,
            interface33 VARCHAR(50) COLLATE utf8_bin NULL,
            interface34 VARCHAR(50) COLLATE utf8_bin NULL,
            interface35 VARCHAR(50) COLLATE utf8_bin NULL,
            interface36 VARCHAR(50) COLLATE utf8_bin NULL,
            interface37 VARCHAR(50) COLLATE utf8_bin NULL,
            interface38 VARCHAR(50) COLLATE utf8_bin NULL,
            interface39 VARCHAR(50) COLLATE utf8_bin NULL,
            interface40 VARCHAR(50) COLLATE utf8_bin NULL,
            interface41 VARCHAR(50) COLLATE utf8_bin NULL,
            interface42 VARCHAR(50) COLLATE utf8_bin NULL,
            interface43 VARCHAR(50) COLLATE utf8_bin NULL,
            interface44 VARCHAR(50) COLLATE utf8_bin NULL,
            interface45 VARCHAR(50) COLLATE utf8_bin NULL,
            FOREIGN KEY (interface1) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface2) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface3) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface4) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface5) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface6) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface7) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface8) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface9) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface10) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface11) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface12) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface13) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface14) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface15) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface16) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface17) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface18) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface19) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface20) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface21) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface22) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface23) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface24) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface25) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface26) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface27) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface28) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface29) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface30) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface31) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface32) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface33) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface34) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface35) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface36) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface37) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface38) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface39) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface40) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface41) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface42) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface43) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface44) REFERENCES interfaces (device_int_unit),
            FOREIGN KEY (interface45) REFERENCES interfaces (device_int_unit)          
        )
        """,
        """
        CREATE TABLE routing_instances (
            instance_name VARCHAR(50) COLLATE utf8_bin NOT NULL PRIMARY KEY,
            type VARCHAR(50) COLLATE utf8_bin NULL,
            rd VARCHAR(50) COLLATE utf8_bin NULL,
            rt VARCHAR(50) COLLATE utf8_bin NULL,
            protocol VARCHAR(50) COLLATE utf8_bin NULL,
            interface1 VARCHAR(50) COLLATE utf8_bin NULL,
            interface2 VARCHAR(50) COLLATE utf8_bin NULL,
            interface3 VARCHAR(50) COLLATE utf8_bin NULL,
            interface4 VARCHAR(50) COLLATE utf8_bin NULL,
            interface5 VARCHAR(50) COLLATE utf8_bin NULL,
            interface6 VARCHAR(50) COLLATE utf8_bin NULL,
            interface7 VARCHAR(50) COLLATE utf8_bin NULL,
            interface8 VARCHAR(50) COLLATE utf8_bin NULL,
            interface9 VARCHAR(50) COLLATE utf8_bin NULL,
            interface10 VARCHAR(50) COLLATE utf8_bin NULL,
            interface11 VARCHAR(50) COLLATE utf8_bin NULL,
            interface12 VARCHAR(50) COLLATE utf8_bin NULL,
            interface13 VARCHAR(50) COLLATE utf8_bin NULL,
            interface14 VARCHAR(50) COLLATE utf8_bin NULL,
            interface15 VARCHAR(50) COLLATE utf8_bin NULL,
            interface16 VARCHAR(50) COLLATE utf8_bin NULL,
            interface17 VARCHAR(50) COLLATE utf8_bin NULL,
            interface18 VARCHAR(50) COLLATE utf8_bin NULL,
            interface19 VARCHAR(50) COLLATE utf8_bin NULL,
            interface20 VARCHAR(50) COLLATE utf8_bin NULL,
            interface21 VARCHAR(50) COLLATE utf8_bin NULL,
            interface22 VARCHAR(50) COLLATE utf8_bin NULL,
            interface23 VARCHAR(50) COLLATE utf8_bin NULL,
            interface24 VARCHAR(50) COLLATE utf8_bin NULL,
            interface25 VARCHAR(50) COLLATE utf8_bin NULL,
            interface26 VARCHAR(50) COLLATE utf8_bin NULL,
            interface27 VARCHAR(50) COLLATE utf8_bin NULL,
            interface28 VARCHAR(50) COLLATE utf8_bin NULL,
            interface29 VARCHAR(50) COLLATE utf8_bin NULL,
            interface30 VARCHAR(50) COLLATE utf8_bin NULL,
            interface31 VARCHAR(50) COLLATE utf8_bin NULL,
            interface32 VARCHAR(50) COLLATE utf8_bin NULL,
            interface33 VARCHAR(50) COLLATE utf8_bin NULL,
            interface34 VARCHAR(50) COLLATE utf8_bin NULL,
            interface35 VARCHAR(50) COLLATE utf8_bin NULL,
            interface36 VARCHAR(50) COLLATE utf8_bin NULL,
            interface37 VARCHAR(50) COLLATE utf8_bin NULL,
            interface38 VARCHAR(50) COLLATE utf8_bin NULL,
            interface39 VARCHAR(50) COLLATE utf8_bin NULL,
            interface40 VARCHAR(50) COLLATE utf8_bin NULL,
            interface41 VARCHAR(50) COLLATE utf8_bin NULL,
            interface42 VARCHAR(50) COLLATE utf8_bin NULL,
            interface43 VARCHAR(50) COLLATE utf8_bin NULL,
            interface44 VARCHAR(50) COLLATE utf8_bin NULL,
            interface45 VARCHAR(50) COLLATE utf8_bin NULL,
            interface46 VARCHAR(50) COLLATE utf8_bin NULL,
            interface47 VARCHAR(50) COLLATE utf8_bin NULL,
            interface48 VARCHAR(50) COLLATE utf8_bin NULL,
            interface49 VARCHAR(50) COLLATE utf8_bin NULL,
            interface50 VARCHAR(50) COLLATE utf8_bin NULL,
            interface51 VARCHAR(50) COLLATE utf8_bin NULL,
            interface52 VARCHAR(50) COLLATE utf8_bin NULL,
            interface53 VARCHAR(50) COLLATE utf8_bin NULL,
            interface54 VARCHAR(50) COLLATE utf8_bin NULL,
            interface55 VARCHAR(50) COLLATE utf8_bin NULL,
            interface56 VARCHAR(50) COLLATE utf8_bin NULL,
            interface57 VARCHAR(50) COLLATE utf8_bin NULL,
            interface58 VARCHAR(50) COLLATE utf8_bin NULL,
            interface59 VARCHAR(50) COLLATE utf8_bin NULL,
            interface60 VARCHAR(50) COLLATE utf8_bin NULL,
            interface61 VARCHAR(50) COLLATE utf8_bin NULL,
            interface62 VARCHAR(50) COLLATE utf8_bin NULL,
            interface63 VARCHAR(50) COLLATE utf8_bin NULL,
            interface64 VARCHAR(50) COLLATE utf8_bin NULL,
            interface65 VARCHAR(50) COLLATE utf8_bin NULL,
            interface66 VARCHAR(50) COLLATE utf8_bin NULL,
            interface67 VARCHAR(50) COLLATE utf8_bin NULL,
            interface68 VARCHAR(50) COLLATE utf8_bin NULL,
            interface69 VARCHAR(50) COLLATE utf8_bin NULL,
            interface70 VARCHAR(50) COLLATE utf8_bin NULL,
            interface71 VARCHAR(50) COLLATE utf8_bin NULL,
            interface72 VARCHAR(50) COLLATE utf8_bin NULL,
            interface73 VARCHAR(50) COLLATE utf8_bin NULL,
            interface74 VARCHAR(50) COLLATE utf8_bin NULL,
            interface75 VARCHAR(50) COLLATE utf8_bin NULL,
            interface76 VARCHAR(50) COLLATE utf8_bin NULL,
            interface77 VARCHAR(50) COLLATE utf8_bin NULL,
            interface78 VARCHAR(50) COLLATE utf8_bin NULL,
            interface79 VARCHAR(50) COLLATE utf8_bin NULL,
            interface80 VARCHAR(50) COLLATE utf8_bin NULL,
            interface81 VARCHAR(50) COLLATE utf8_bin NULL,
            interface82 VARCHAR(50) COLLATE utf8_bin NULL,
            interface83 VARCHAR(50) COLLATE utf8_bin NULL,
            interface84 VARCHAR(50) COLLATE utf8_bin NULL,
            interface85 VARCHAR(50) COLLATE utf8_bin NULL,
            interface86 VARCHAR(50) COLLATE utf8_bin NULL,
            interface87 VARCHAR(50) COLLATE utf8_bin NULL,
            interface88 VARCHAR(50) COLLATE utf8_bin NULL,
            interface89 VARCHAR(50) COLLATE utf8_bin NULL,
            interface90 VARCHAR(50) COLLATE utf8_bin NULL,
            interface91 VARCHAR(50) COLLATE utf8_bin NULL,
            interface92 VARCHAR(50) COLLATE utf8_bin NULL,
            interface93 VARCHAR(50) COLLATE utf8_bin NULL,
            interface94 VARCHAR(50) COLLATE utf8_bin NULL,
            interface95 VARCHAR(50) COLLATE utf8_bin NULL,
            interface96 VARCHAR(50) COLLATE utf8_bin NULL,
            interface97 VARCHAR(50) COLLATE utf8_bin NULL,
            interface98 VARCHAR(50) COLLATE utf8_bin NULL,
            interface99 VARCHAR(50) COLLATE utf8_bin NULL,
            interface100 VARCHAR(50) COLLATE utf8_bin NULL,
            interface101 VARCHAR(50) COLLATE utf8_bin NULL,
            interface102 VARCHAR(50) COLLATE utf8_bin NULL,
            interface103 VARCHAR(50) COLLATE utf8_bin NULL,
            interface104 VARCHAR(50) COLLATE utf8_bin NULL,
            interface105 VARCHAR(50) COLLATE utf8_bin NULL,
            interface106 VARCHAR(50) COLLATE utf8_bin NULL,
            interface107 VARCHAR(50) COLLATE utf8_bin NULL,
            interface108 VARCHAR(50) COLLATE utf8_bin NULL,
            interface109 VARCHAR(50) COLLATE utf8_bin NULL,
            interface110 VARCHAR(50) COLLATE utf8_bin NULL,
            interface111 VARCHAR(50) COLLATE utf8_bin NULL,
            interface112 VARCHAR(50) COLLATE utf8_bin NULL,
            interface113 VARCHAR(50) COLLATE utf8_bin NULL,
            interface114 VARCHAR(50) COLLATE utf8_bin NULL,
            interface115 VARCHAR(50) COLLATE utf8_bin NULL,
            interface116 VARCHAR(50) COLLATE utf8_bin NULL,
            interface117 VARCHAR(50) COLLATE utf8_bin NULL,
            interface118 VARCHAR(50) COLLATE utf8_bin NULL,
            interface119 VARCHAR(50) COLLATE utf8_bin NULL,
            interface120 VARCHAR(50) COLLATE utf8_bin NULL,
            interface121 VARCHAR(50) COLLATE utf8_bin NULL,
            interface122 VARCHAR(50) COLLATE utf8_bin NULL,
            interface123 VARCHAR(50) COLLATE utf8_bin NULL,
            interface124 VARCHAR(50) COLLATE utf8_bin NULL,
            interface125 VARCHAR(50) COLLATE utf8_bin NULL,
            interface126 VARCHAR(50) COLLATE utf8_bin NULL,
            interface127 VARCHAR(50) COLLATE utf8_bin NULL,
            interface128 VARCHAR(50) COLLATE utf8_bin NULL,
            interface129 VARCHAR(50) COLLATE utf8_bin NULL,
            interface130 VARCHAR(50) COLLATE utf8_bin NULL,
            interface131 VARCHAR(50) COLLATE utf8_bin NULL,
            interface132 VARCHAR(50) COLLATE utf8_bin NULL,
            interface133 VARCHAR(50) COLLATE utf8_bin NULL,
            interface134 VARCHAR(50) COLLATE utf8_bin NULL,
            interface135 VARCHAR(50) COLLATE utf8_bin NULL,
            interface136 VARCHAR(50) COLLATE utf8_bin NULL,
            interface137 VARCHAR(50) COLLATE utf8_bin NULL,
            interface138 VARCHAR(50) COLLATE utf8_bin NULL,
            interface139 VARCHAR(50) COLLATE utf8_bin NULL,
            interface140 VARCHAR(50) COLLATE utf8_bin NULL,
            interface141 VARCHAR(50) COLLATE utf8_bin NULL,
            interface142 VARCHAR(50) COLLATE utf8_bin NULL,
            interface143 VARCHAR(50) COLLATE utf8_bin NULL,
            interface144 VARCHAR(50) COLLATE utf8_bin NULL,
            interface145 VARCHAR(50) COLLATE utf8_bin NULL,
            interface146 VARCHAR(50) COLLATE utf8_bin NULL,
            interface147 VARCHAR(50) COLLATE utf8_bin NULL,
            interface148 VARCHAR(50) COLLATE utf8_bin NULL,
            interface149 VARCHAR(50) COLLATE utf8_bin NULL,
            interface150 VARCHAR(50) COLLATE utf8_bin NULL,
            interface151 VARCHAR(50) COLLATE utf8_bin NULL,
            interface152 VARCHAR(50) COLLATE utf8_bin NULL,
            interface153 VARCHAR(50) COLLATE utf8_bin NULL,
            interface154 VARCHAR(50) COLLATE utf8_bin NULL,
            interface155 VARCHAR(50) COLLATE utf8_bin NULL,
            interface156 VARCHAR(50) COLLATE utf8_bin NULL,
            interface157 VARCHAR(50) COLLATE utf8_bin NULL,
            interface158 VARCHAR(50) COLLATE utf8_bin NULL,
            interface159 VARCHAR(50) COLLATE utf8_bin NULL,
            interface160 VARCHAR(50) COLLATE utf8_bin NULL,
            interface161 VARCHAR(50) COLLATE utf8_bin NULL,
            interface162 VARCHAR(50) COLLATE utf8_bin NULL,
            interface163 VARCHAR(50) COLLATE utf8_bin NULL,
            interface164 VARCHAR(50) COLLATE utf8_bin NULL,
            interface165 VARCHAR(50) COLLATE utf8_bin NULL,
            interface166 VARCHAR(50) COLLATE utf8_bin NULL,
            interface167 VARCHAR(50) COLLATE utf8_bin NULL,
            interface168 VARCHAR(50) COLLATE utf8_bin NULL,
            interface169 VARCHAR(50) COLLATE utf8_bin NULL,
            interface170 VARCHAR(50) COLLATE utf8_bin NULL,
            interface171 VARCHAR(50) COLLATE utf8_bin NULL
        )
        """,
        """
         CREATE TABLE bridge_domains (
             domain_name VARCHAR(50) COLLATE utf8_bin NOT NULL PRIMARY KEY,
             description VARCHAR(100) COLLATE utf8_bin NULL,
             type VARCHAR(50) COLLATE utf8_bin NULL,
             vlan_id VARCHAR(50) COLLATE utf8_bin NULL,
             interface1 VARCHAR(50) COLLATE utf8_bin NULL,
             interface2 VARCHAR(50) COLLATE utf8_bin NULL,
             interface3 VARCHAR(50) COLLATE utf8_bin NULL,
             interface4 VARCHAR(50) COLLATE utf8_bin NULL,
             interface5 VARCHAR(50) COLLATE utf8_bin NULL,
             interface6 VARCHAR(50) COLLATE utf8_bin NULL,
             interface7 VARCHAR(50) COLLATE utf8_bin NULL,
             interface8 VARCHAR(50) COLLATE utf8_bin NULL,
             interface9 VARCHAR(50) COLLATE utf8_bin NULL,
             interface10 VARCHAR(50) COLLATE utf8_bin NULL,
             interface11 VARCHAR(50) COLLATE utf8_bin NULL,
             interface12 VARCHAR(50) COLLATE utf8_bin NULL,
             interface13 VARCHAR(50) COLLATE utf8_bin NULL,
             interface14 VARCHAR(50) COLLATE utf8_bin NULL,
             interface15 VARCHAR(50) COLLATE utf8_bin NULL,
             interface16 VARCHAR(50) COLLATE utf8_bin NULL,
             interface17 VARCHAR(50) COLLATE utf8_bin NULL,
             interface18 VARCHAR(50) COLLATE utf8_bin NULL,
             interface19 VARCHAR(50) COLLATE utf8_bin NULL,
             interface20 VARCHAR(50) COLLATE utf8_bin NULL,
             interface21 VARCHAR(50) COLLATE utf8_bin NULL,
             interface22 VARCHAR(50) COLLATE utf8_bin NULL,
             interface23 VARCHAR(50) COLLATE utf8_bin NULL,
             interface24 VARCHAR(50) COLLATE utf8_bin NULL,
             interface25 VARCHAR(50) COLLATE utf8_bin NULL,
             interface26 VARCHAR(50) COLLATE utf8_bin NULL,
             interface27 VARCHAR(50) COLLATE utf8_bin NULL,
             interface28 VARCHAR(50) COLLATE utf8_bin NULL,
             interface29 VARCHAR(50) COLLATE utf8_bin NULL,
             interface30 VARCHAR(50) COLLATE utf8_bin NULL,
             interface31 VARCHAR(50) COLLATE utf8_bin NULL,
             interface32 VARCHAR(50) COLLATE utf8_bin NULL,
             interface33 VARCHAR(50) COLLATE utf8_bin NULL,
             interface34 VARCHAR(50) COLLATE utf8_bin NULL,
             interface35 VARCHAR(50) COLLATE utf8_bin NULL,
             interface36 VARCHAR(50) COLLATE utf8_bin NULL,
             interface37 VARCHAR(50) COLLATE utf8_bin NULL,
             interface38 VARCHAR(50) COLLATE utf8_bin NULL,
             interface39 VARCHAR(50) COLLATE utf8_bin NULL,
             interface40 VARCHAR(50) COLLATE utf8_bin NULL,
             interface41 VARCHAR(50) COLLATE utf8_bin NULL,
             interface42 VARCHAR(50) COLLATE utf8_bin NULL,
             interface43 VARCHAR(50) COLLATE utf8_bin NULL,
             interface44 VARCHAR(50) COLLATE utf8_bin NULL,
             interface45 VARCHAR(50) COLLATE utf8_bin NULL,
             interface46 VARCHAR(50) COLLATE utf8_bin NULL,
             interface47 VARCHAR(50) COLLATE utf8_bin NULL,
             interface48 VARCHAR(50) COLLATE utf8_bin NULL,
             interface49 VARCHAR(50) COLLATE utf8_bin NULL,
             interface50 VARCHAR(50) COLLATE utf8_bin NULL,
             interface51 VARCHAR(50) COLLATE utf8_bin NULL,
             interface52 VARCHAR(50) COLLATE utf8_bin NULL,
             interface53 VARCHAR(50) COLLATE utf8_bin NULL,
             interface54 VARCHAR(50) COLLATE utf8_bin NULL,
             interface55 VARCHAR(50) COLLATE utf8_bin NULL,
             interface56 VARCHAR(50) COLLATE utf8_bin NULL,
             interface57 VARCHAR(50) COLLATE utf8_bin NULL,
             interface58 VARCHAR(50) COLLATE utf8_bin NULL,
             interface59 VARCHAR(50) COLLATE utf8_bin NULL,
             interface60 VARCHAR(50) COLLATE utf8_bin NULL,
             interface61 VARCHAR(50) COLLATE utf8_bin NULL,
             interface62 VARCHAR(50) COLLATE utf8_bin NULL,
             interface63 VARCHAR(50) COLLATE utf8_bin NULL,
             interface64 VARCHAR(50) COLLATE utf8_bin NULL,
             interface65 VARCHAR(50) COLLATE utf8_bin NULL,
             interface66 VARCHAR(50) COLLATE utf8_bin NULL,
             interface67 VARCHAR(50) COLLATE utf8_bin NULL,
             interface68 VARCHAR(50) COLLATE utf8_bin NULL,
             interface69 VARCHAR(50) COLLATE utf8_bin NULL,
             interface70 VARCHAR(50) COLLATE utf8_bin NULL,
             interface71 VARCHAR(50) COLLATE utf8_bin NULL,
             interface72 VARCHAR(50) COLLATE utf8_bin NULL,
             interface73 VARCHAR(50) COLLATE utf8_bin NULL,
             interface74 VARCHAR(50) COLLATE utf8_bin NULL,
             interface75 VARCHAR(50) COLLATE utf8_bin NULL,
             interface76 VARCHAR(50) COLLATE utf8_bin NULL,
             interface77 VARCHAR(50) COLLATE utf8_bin NULL,
             interface78 VARCHAR(50) COLLATE utf8_bin NULL,
             interface79 VARCHAR(50) COLLATE utf8_bin NULL,
             interface80 VARCHAR(50) COLLATE utf8_bin NULL,
             interface81 VARCHAR(50) COLLATE utf8_bin NULL,
             interface82 VARCHAR(50) COLLATE utf8_bin NULL,
             interface83 VARCHAR(50) COLLATE utf8_bin NULL,
             interface84 VARCHAR(50) COLLATE utf8_bin NULL,
             interface85 VARCHAR(50) COLLATE utf8_bin NULL,
             interface86 VARCHAR(50) COLLATE utf8_bin NULL,
             interface87 VARCHAR(50) COLLATE utf8_bin NULL,
             interface88 VARCHAR(50) COLLATE utf8_bin NULL,
             interface89 VARCHAR(50) COLLATE utf8_bin NULL,
             interface90 VARCHAR(50) COLLATE utf8_bin NULL,
             interface91 VARCHAR(50) COLLATE utf8_bin NULL,
             interface92 VARCHAR(50) COLLATE utf8_bin NULL,
             interface93 VARCHAR(50) COLLATE utf8_bin NULL,
             interface94 VARCHAR(50) COLLATE utf8_bin NULL,
             interface95 VARCHAR(50) COLLATE utf8_bin NULL,
             interface96 VARCHAR(50) COLLATE utf8_bin NULL,
             interface97 VARCHAR(50) COLLATE utf8_bin NULL,
             interface98 VARCHAR(50) COLLATE utf8_bin NULL,
             interface99 VARCHAR(50) COLLATE utf8_bin NULL,
             interface100 VARCHAR(50) COLLATE utf8_bin NULL,
             interface101 VARCHAR(50) COLLATE utf8_bin NULL,
             interface102 VARCHAR(50) COLLATE utf8_bin NULL,
             interface103 VARCHAR(50) COLLATE utf8_bin NULL,
             interface104 VARCHAR(50) COLLATE utf8_bin NULL,
             interface105 VARCHAR(50) COLLATE utf8_bin NULL,
             interface106 VARCHAR(50) COLLATE utf8_bin NULL,
             interface107 VARCHAR(50) COLLATE utf8_bin NULL,
             interface108 VARCHAR(50) COLLATE utf8_bin NULL,
             interface109 VARCHAR(50) COLLATE utf8_bin NULL,
             interface110 VARCHAR(50) COLLATE utf8_bin NULL,
             interface111 VARCHAR(50) COLLATE utf8_bin NULL,
             interface112 VARCHAR(50) COLLATE utf8_bin NULL,
             interface113 VARCHAR(50) COLLATE utf8_bin NULL,
             interface114 VARCHAR(50) COLLATE utf8_bin NULL,
             interface115 VARCHAR(50) COLLATE utf8_bin NULL,
             interface116 VARCHAR(50) COLLATE utf8_bin NULL,
             interface117 VARCHAR(50) COLLATE utf8_bin NULL,
             interface118 VARCHAR(50) COLLATE utf8_bin NULL,
             interface119 VARCHAR(50) COLLATE utf8_bin NULL,
             interface120 VARCHAR(50) COLLATE utf8_bin NULL,
             interface121 VARCHAR(50) COLLATE utf8_bin NULL,
             interface122 VARCHAR(50) COLLATE utf8_bin NULL,
             interface123 VARCHAR(50) COLLATE utf8_bin NULL,
             interface124 VARCHAR(50) COLLATE utf8_bin NULL,
             interface125 VARCHAR(50) COLLATE utf8_bin NULL,
             interface126 VARCHAR(50) COLLATE utf8_bin NULL,
             interface127 VARCHAR(50) COLLATE utf8_bin NULL,
             interface128 VARCHAR(50) COLLATE utf8_bin NULL,
             interface129 VARCHAR(50) COLLATE utf8_bin NULL
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
        DROP PROCEDURE IF EXISTS find_set;
        """,
        """
        CREATE PROCEDURE find_set (a VARCHAR(50)) BEGIN
        SELECT device_name from interface_sets where
            interface1 LIKE a OR
            interface2 LIKE a OR
            interface3 LIKE a OR
            interface4 LIKE a OR
            interface5 LIKE a OR
            interface6 LIKE a OR
            interface7 LIKE a OR
            interface8 LIKE a OR
            interface9 LIKE a OR
            interface10 LIKE a OR
            interface11 LIKE a OR
            interface12 LIKE a OR
            interface13 LIKE a OR
            interface14 LIKE a OR
            interface15 LIKE a OR
            interface16 LIKE a OR
            interface17 LIKE a OR
            interface18 LIKE a OR
            interface19 LIKE a OR
            interface20 LIKE a OR
            interface21 LIKE a OR
            interface22 LIKE a OR
            interface23 LIKE a OR
            interface24 LIKE a OR
            interface25 LIKE a OR
            interface26 LIKE a OR
            interface27 LIKE a OR
            interface28 LIKE a OR
            interface29 LIKE a OR
            interface30 LIKE a OR
            interface31 LIKE a OR
            interface32 LIKE a OR
            interface33 LIKE a OR
            interface34 LIKE a OR
            interface35 LIKE a OR
            interface36 LIKE a OR
            interface37 LIKE a OR
            interface38 LIKE a OR
            interface39 LIKE a OR
            interface40 LIKE a OR
            interface41 LIKE a OR
            interface42 LIKE a OR
            interface43 LIKE a OR
            interface44 LIKE a OR
            interface45 LIKE a;
        END
        """,
        """
        CREATE PROCEDURE find_ri (a VARCHAR(50)) BEGIN
        SELECT instance_name from routing_instances where
            interface1 LIKE a OR
            interface2 LIKE a OR
            interface3 LIKE a OR
            interface4 LIKE a OR
            interface5 LIKE a OR
            interface6 LIKE a OR
            interface7 LIKE a OR
            interface8 LIKE a OR
            interface9 LIKE a OR
            interface10 LIKE a OR
            interface11 LIKE a OR
            interface12 LIKE a OR
            interface13 LIKE a OR
            interface14 LIKE a OR
            interface15 LIKE a OR
            interface16 LIKE a OR
            interface17 LIKE a OR
            interface18 LIKE a OR
            interface19 LIKE a OR
            interface20 LIKE a OR
            interface21 LIKE a OR
            interface22 LIKE a OR
            interface23 LIKE a OR
            interface24 LIKE a OR
            interface25 LIKE a OR
            interface26 LIKE a OR
            interface27 LIKE a OR
            interface28 LIKE a OR
            interface29 LIKE a OR
            interface30 LIKE a OR
            interface31 LIKE a OR
            interface32 LIKE a OR
            interface33 LIKE a OR
            interface34 LIKE a OR
            interface35 LIKE a OR
            interface36 LIKE a OR
            interface37 LIKE a OR
            interface38 LIKE a OR
            interface39 LIKE a OR
            interface40 LIKE a OR
            interface41 LIKE a OR
            interface42 LIKE a OR
            interface43 LIKE a OR
            interface44 LIKE a OR
            interface45 LIKE a OR
            interface46 LIKE a OR
            interface47 LIKE a OR
            interface48 LIKE a OR
            interface49 LIKE a OR
            interface50 LIKE a OR
            interface51 LIKE a OR
            interface52 LIKE a OR
            interface53 LIKE a OR
            interface54 LIKE a OR
            interface55 LIKE a OR
            interface56 LIKE a OR
            interface57 LIKE a OR
            interface58 LIKE a OR
            interface59 LIKE a OR
            interface60 LIKE a OR
            interface61 LIKE a OR
            interface62 LIKE a OR
            interface63 LIKE a OR
            interface64 LIKE a OR
            interface65 LIKE a OR
            interface66 LIKE a OR
            interface67 LIKE a OR
            interface68 LIKE a OR
            interface69 LIKE a OR
            interface70 LIKE a OR
            interface71 LIKE a OR
            interface72 LIKE a OR
            interface73 LIKE a OR
            interface74 LIKE a OR
            interface75 LIKE a OR
            interface76 LIKE a OR
            interface77 LIKE a OR
            interface78 LIKE a OR
            interface79 LIKE a OR
            interface80 LIKE a OR
            interface81 LIKE a OR
            interface82 LIKE a OR
            interface83 LIKE a OR
            interface84 LIKE a OR
            interface85 LIKE a OR
            interface86 LIKE a OR
            interface87 LIKE a OR
            interface88 LIKE a OR
            interface89 LIKE a OR
            interface90 LIKE a OR
            interface91 LIKE a OR
            interface92 LIKE a OR
            interface93 LIKE a OR
            interface94 LIKE a OR
            interface95 LIKE a OR
            interface96 LIKE a OR
            interface97 LIKE a OR
            interface98 LIKE a OR
            interface99 LIKE a OR
            interface100 LIKE a OR
            interface101 LIKE a OR
            interface102 LIKE a OR
            interface103 LIKE a OR
            interface104 LIKE a OR
            interface105 LIKE a OR
            interface106 LIKE a OR
            interface107 LIKE a OR
            interface108 LIKE a OR
            interface109 LIKE a OR
            interface110 LIKE a OR
            interface111 LIKE a OR
            interface112 LIKE a OR
            interface113 LIKE a OR
            interface114 LIKE a OR
            interface115 LIKE a OR
            interface116 LIKE a OR
            interface117 LIKE a OR
            interface118 LIKE a OR
            interface119 LIKE a OR
            interface120 LIKE a OR
            interface121 LIKE a OR
            interface122 LIKE a OR
            interface123 LIKE a OR
            interface124 LIKE a OR
            interface125 LIKE a OR
            interface126 LIKE a OR
            interface127 LIKE a OR
            interface128 LIKE a OR
            interface129 LIKE a OR
            interface130 LIKE a OR
            interface131 LIKE a OR
            interface132 LIKE a OR
            interface133 LIKE a OR
            interface134 LIKE a OR
            interface135 LIKE a OR
            interface136 LIKE a OR
            interface137 LIKE a OR
            interface138 LIKE a OR
            interface139 LIKE a OR
            interface140 LIKE a OR
            interface141 LIKE a OR
            interface142 LIKE a OR
            interface143 LIKE a OR
            interface144 LIKE a OR
            interface145 LIKE a OR
            interface146 LIKE a OR
            interface147 LIKE a OR
            interface148 LIKE a OR
            interface149 LIKE a OR
            interface150 LIKE a OR
            interface151 LIKE a OR
            interface152 LIKE a OR
            interface153 LIKE a OR
            interface154 LIKE a OR
            interface155 LIKE a OR
            interface156 LIKE a OR
            interface157 LIKE a OR
            interface158 LIKE a OR
            interface159 LIKE a OR
            interface160 LIKE a OR
            interface161 LIKE a OR
            interface162 LIKE a OR
            interface163 LIKE a OR
            interface164 LIKE a OR
            interface165 LIKE a OR
            interface166 LIKE a OR
            interface167 LIKE a OR
            interface168 LIKE a OR
            interface169 LIKE a OR
            interface170 LIKE a OR
            interface171 LIKE a;
        END      
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
