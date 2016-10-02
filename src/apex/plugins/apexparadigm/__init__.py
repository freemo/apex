#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import re

import apex.routing

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []
__version__ = '0.0.6'

plugin = None


def start(config, port_map, aprsis):
    global plugin
    plugin = ApexParadigmPlugin(config, port_map, aprsis)
    plugin.run()


def handle_packet(frame, recv_port, recv_port_name):
    plugin.handle_packet(frame, recv_port, recv_port_name)


def stop():
    plugin.stop()


class ApexParadigmPlugin(object):

    BAND_PATH_REGEX = re.compile(r'(\d{1,4})M(\d{0,3})')

    def __init__(self, config, port_map, aprsis):
        self.port_map = port_map
        self.aprsis = aprsis

    def __passive_digipeat(self, frame, recv_port, recv_port_name):
        # can't digipeat packets if we are in the expended path
        if apex.routing.has_seen(self.port_map, frame):
            return

        for hop_index in range(0, len(frame['path'])):
            hop = frame['path'][hop_index]
            if not apex.routing.is_hop_consumed(hop):
                split_hop = hop.split('-')
                node = split_hop[0].upper()
                if len(split_hop) >= 2 and split_hop[1]:
                    ssid = int(split_hop[1])
                else:
                    ssid = 0

                band_path = None
                band_path_net = None
                band_match = self.BAND_PATH_REGEX.match(node)
                if band_match is not None:
                    band_path = band_match.group(1)
                    band_path_net = band_match.group(2)

                for port_name in self.port_map.keys():
                    port = self.port_map[port_name]
                    split_port_identifier = port['identifier'].split('-')
                    port_callsign = split_port_identifier[0].upper()
                    if len(split_port_identifier) >= 2 and split_port_identifier[1]:
                        port_ssid = int(split_port_identifier[1])
                    else:
                        port_ssid = 0

                    if band_path:
                        if band_path_net:
                            if node == port['net']:
                                frame['path'] = frame['path'][:hop_index] + [recv_port['identifier'] + '*'] +\
                                                [hop + '*'] + frame['path'][hop_index+1:]
                                port['tnc'].write(frame, port['tnc_port'])
                                self.aprsis.write(frame)
                                return
                        else:
                            if port['net'].startswith(node):
                                frame['path'] = frame['path'][:hop_index] + [recv_port['identifier'] + '*'] +\
                                                [hop + '*'] + frame['path'][hop_index+1:]
                                port['tnc'].write(frame, port['tnc_port'])
                                self.aprsis.write(frame)
                                return
                    if node == port_callsign and ssid == port_ssid:
                        if ssid is 0:
                            frame['path'][hop_index] = port_callsign + '*'
                        else:
                            frame['path'][hop_index] = port['identifier'] + '*'
                        port['tnc'].write(frame, port['tnc_port'])
                        self.aprsis.write(frame)
                        return
                    elif node == 'GATE' and port['net'].startswith('2M'):
                        frame['path'] = frame['path'][:hop_index] + [recv_port['identifier'] + '*'] + [node + '*'] +\
                                        frame['path'][hop_index+1:]
                        port['tnc'].write(frame, port['tnc_port'])
                        self.aprsis.write(frame)
                        return
                if node.startswith('WIDE') and ssid > 1:
                    frame['path'] = frame['path'][:hop_index] + [recv_port['identifier'] + '*'] +\
                        [node + '-' + str(ssid-1)] + frame['path'][hop_index+1:]
                    port['tnc'].write(frame, port['tnc_port'])
                    self.aprsis.write(frame)
                    return
                elif node.startswith('WIDE') and ssid is 1:
                    frame['path'] = frame['path'][:hop_index] + [recv_port['identifier'] + '*'] + [node + '*'] + frame['path'][hop_index+1:]
                    port['tnc'].write(frame, port['tnc_port'])
                    self.aprsis.write(frame)
                    return
                elif node.startswith('WIDE') and ssid is 0:
                    frame['path'][hop_index] = node + '*'
                    # no return
                else:
                    # If we didnt digipeat it then we didn't modify the frame, send it to aprsis as-is
                    self.aprsis.write(frame)
                    return

    def __preemptive_digipeat(self, frame, recv_port, recv_port_name):
        # can't digipeat packets if we are in the expended path
        if apex.routing.has_seen(self.port_map, frame):
            return

        selected_hop = {}
        node = None
        ssid = 0
        for hop_index in reversed(range(0, len(frame['path']))):
            hop = frame['path'][hop_index]
            # If this is the last node before a spent node, or a spent node itself, we are done
            if apex.routing.is_hop_consumed(hop) or apex.routing.is_hop_consumed(frame['path'][hop_index-1]):
                break
            split_hop = hop.split('-')
            node = split_hop[0].upper()
            if len(split_hop) >= 2 and split_hop[1]:
                ssid = int(split_hop[1])
            else:
                continue

            band_path = None
            band_path_net = None
            band_match = self.BAND_PATH_REGEX.match(node)
            if band_match is not None:
                band_path = band_match.group(1)
                band_path_net = band_match.group(2)

            if not band_path:
                continue

            for port_name in self.port_map.keys():
                port = self.port_map[port_name]
                if band_path_net and node == port['net']:
                    # only when a ssid is present should it be treated preemptively if it is a band path
                    if not selected_hop:
                        selected_hop['index'] = hop_index
                        selected_hop['hop'] = hop
                        selected_hop['node'] = node
                        selected_hop['ssid'] = ssid
                        selected_hop['port_name'] = port_name
                        selected_hop['port'] = port
                        selected_hop['band_path'] = band_path
                        selected_hop['band_path_net'] = band_path_net
                    elif ssid > selected_hop['ssid']:
                        selected_hop['index'] = hop_index
                        selected_hop['hop'] = hop
                        selected_hop['node'] = node
                        selected_hop['ssid'] = ssid
                        selected_hop['port_name'] = port_name
                        selected_hop['port'] = port
                        selected_hop['band_path'] = band_path
                        selected_hop['band_path_net'] = band_path_net
                elif not band_path_net and port['net'].startswith(band_path):
                    # only when a ssid is present should it be treated preemptively if it is a band path
                    if not selected_hop:
                        selected_hop['index'] = hop_index
                        selected_hop['hop'] = hop
                        selected_hop['node'] = node
                        selected_hop['ssid'] = ssid
                        selected_hop['port_name'] = port_name
                        selected_hop['port'] = port
                        selected_hop['band_path'] = band_path
                        selected_hop['band_path_net'] = band_path_net
                    elif ssid > selected_hop['ssid']:
                        selected_hop['index'] = hop_index
                        selected_hop['hop'] = hop
                        selected_hop['node'] = node
                        selected_hop['ssid'] = ssid
                        selected_hop['port_name'] = port_name
                        selected_hop['port'] = port
                        selected_hop['band_path'] = band_path
                        selected_hop['band_path_net'] = band_path_net
        for hop_index in reversed(range(0, len(frame['path']))):
            hop = frame['path'][hop_index]
            # If this is the last node before a spent node, or a spent node itself, we are done
            if apex.routing.is_hop_consumed(hop) or apex.routing.is_hop_consumed(frame['path'][hop_index-1]):
                break
            elif selected_hop and selected_hop['index'] <= hop_index:
                break

            for port_name in self.port_map.keys():
                port = self.port_map[port_name]

                # since the callsign specifically was specified in the path after the band-path the callsign takes
                # precedence
                if port['identifier'] == hop:
                    selected_hop['index'] = hop_index
                    selected_hop['hop'] = hop
                    selected_hop['node'] = node
                    selected_hop['ssid'] = ssid
                    selected_hop['port_name'] = port_name
                    selected_hop['port'] = port
                    selected_hop['band_path'] = None
                    selected_hop['band_path_net'] = None

        if not selected_hop:
            return

        # now lets digipeat this packet
        new_path = []
        for hop_index in range(0, len(frame['path'])):
            hop = frame['path'][hop_index]
            if not apex.routing.is_hop_consumed(hop):
                if hop_index == selected_hop['index']:
                    if selected_hop['band_path'] is None:
                        new_path += [hop + '*']
                    else:
                        new_path += [selected_hop['port']['identifier'] + '*'] + [hop + '*']
                elif hop_index > selected_hop['index']:
                    new_path += [hop]
            else:
                new_path += [hop]
        frame['path'] = new_path
        port['tnc'].write(frame, port['tnc_port'])
        self.aprsis.write(frame)
        return

    def stop(self):
        return

    def run(self):
        return

    def handle_packet(self, frame, recv_port, recv_port_name):
        self.__preemptive_digipeat(copy.deepcopy(frame), recv_port, recv_port_name)
        self.__passive_digipeat(copy.deepcopy(frame), recv_port, recv_port_name)
