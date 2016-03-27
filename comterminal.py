#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the entry point for the application, just a sandbox right now."""
import aprs.aprs_kiss

__author__ = 'Jeffrey Phillips Freeman WI2ARD <freemo@gmail.com>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'

import time
import signal
import sys
import kiss.constants
import aprs
import aprs.util
import threading
import configparser
import cachetools
import traceback
import pluginloader

port_map = {}
config = configparser.ConfigParser()
config.read('apex.cfg')
for section in config.sections():
    if section.startswith("TNC "):
        tnc_name = section.split(" ")[1]
        kiss_tnc = aprs.AprsKiss(com_port=config.get(section, 'com_port'), baud=config.get(section, 'baud'))
        kiss_init_string = config.get(section,'kiss_init')
        if kiss_init_string == 'MODE_INIT_W8DED':
            kiss_tnc.start(kiss.constants.MODE_INIT_W8DED)
        elif kiss_init_string == 'MODE_INIT_KENWOOD_D710':
            kiss_tnc.start(kiss.constants.MODE_INIT_KENWOOD_D710)
        elif kiss_init_string == 'NONE':
            kiss_tnc.start()
        else:
            raise Exception("KISS init mode not specified")
        for port in range(1, 1+int(config.get(section, 'port_count'))):
            port_name = tnc_name + '-' + str(port)
            port_section = 'PORT ' + port_name
            port_identifier = config.get(port_section, 'identifier')
            port_net = config.get(port_section, 'net')
            tnc_port = int(config.get(port_section, 'tnc_port'))
            port_map[port_name] = {'identifier':port_identifier, 'net':port_net, 'tnc':kiss_tnc, 'tnc_port':tnc_port}
    elif section == "APRS-IS":
        aprsis_callsign = config.get('APRS-IS', 'callsign')
        aprsis_password = config.get('APRS-IS', 'password')
        aprsis_server = config.get('APRS-IS', 'server')
        aprsis_server_port = config.get('APRS-IS', 'server_port')
        aprsis = aprs.AprsInternetService(aprsis_callsign, aprsis_password)
        aprsis.connect(aprsis_server, int(aprsis_server_port))

packet_cache = cachetools.TTLCache(10000, 5)

def sigint_handler(signal, frame):
    for port in port_map.values():
        port['tnc'].close()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

print("Press ctrl + c at any time to exit")

#start the plugins
plugins = []
plugin_loaders=pluginloader.getPlugins()
for plugin_loader in plugin_loaders:
    loaded_plugin=pluginloader.loadPlugin(plugin_loader)
    plugins.append(loaded_plugin)
    threading.Thread(target=loaded_plugin.start, args=(config, port_map, packet_cache, aprsis)).start()

while 1:
    something_read = False
    try:
        for port_name in port_map.keys():
            port = port_map[port_name]
            frame = port['tnc'].read()
            if frame:
                formatted_aprs = aprs.util.format_aprs_frame(frame)
                print(port_name + " << " + formatted_aprs)
                for plugin in plugins:
                    something_read = True
                    plugin.handle_packet(frame, port, port_name)
    except Exception as ex:
        # We want to keep this thread alive so long as the application runs.
        traceback.print_exc(file=sys.stdout)
        print("caught exception while reading packet: " + str(ex))

    if something_read is False:
        time.sleep(1)
