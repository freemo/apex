#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""APRS Internet Service Class Definitions"""

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import select
import socket

import requests

from apex.aprs import constants as aprs_constants
from apex.aprs import util as aprs_util

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


class IGate(object):

    """APRS Object."""

    logger = logging.getLogger(__name__)
    logger.setLevel(aprs_constants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(aprs_constants.LOG_LEVEL)
    console_handler.setFormatter(aprs_constants.LOG_FORMAT)
    logger.addHandler(console_handler)
    logger.propagate = False

    def __init__(self, user, password='-1', input_url=None):
        self.user = user
        self._url = input_url or aprs_constants.APRSIS_URL
        self._auth = ' '.join(
            ['user', user, 'pass', password, 'vers', 'APRS Python Module'])
        self.aprsis_sock = None
        self.data_buffer = ''
        self.packet_buffer = []

    def __reset_buffer(self):
        self.data_buffer = ''
        self.packet_buffer = []

    def connect(self, server=None, port=None, aprs_filter=None):
        """
        Connects & logs in to APRS-IS.

        :param server: Optional alternative APRS-IS server.
        :param port: Optional APRS-IS port.
        :param filter: Optional filter to use.
        :type server: str
        :type port: int
        :type filte: str
        """
        if not self.aprsis_sock:
            self.__reset_buffer()

            server = server or aprs_constants.APRSIS_SERVER
            port = port or aprs_constants.APRSIS_FILTER_PORT
            aprs_filter = aprs_filter or '/'.join(['p', self.user])

            self.full_auth = ' '.join([self._auth, 'filter', aprs_filter])

            self.server = server
            self.port = port
            self.aprsis_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.aprsis_sock.connect((server, port))
            self.logger.info('Connected to server=%s port=%s', server, port)
            self.logger.debug('Sending full_auth=%s', self.full_auth)
            self.aprsis_sock.sendall((self.full_auth + '\n\r').encode('ascii'))

    def close(self):
        if self.aprsis_sock:
            self.aprsis_sock.close()
            self.__reset_buffer()
            self.aprsis_sock = None

    def write(self, frame_decoded, headers=None, protocol='TCP'):
        """
        Sends message to APRS-IS.

        :param message: Message to send to APRS-IS.
        :param headers: Optional HTTP headers to post.
        :param protocol: Protocol to use: One of TCP, HTTP or UDP.
        :type message: str
        :type headers: dict

        :return: True on success, False otherwise.
        :rtype: bool
        """

        frame = aprs_util.encode_frame(frame_decoded)
        if 'TCP' in protocol:
            self.aprsis_sock.sendall(frame.encode(encoding='UTF-8'))
            return True
        elif 'HTTP' in protocol:
            content = '\n'.join([self._auth, frame])
            headers = headers or aprs_constants.APRSIS_HTTP_HEADERS
            result = requests.post(self._url, data=content, headers=headers)
            return 204 == result.status_code
        elif 'UDP' in protocol:
            content = '\n'.join([self._auth, frame])
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(
                content,
                (aprs_constants.APRSIS_SERVER, aprs_constants.APRSIS_RX_PORT)
            )
            return True

    def read(self, filter_logresp=True):
        """
        Receives from APRS-IS.

        :param callback: Optional callback to deliver data to.
        :type callback: func
        """
        # check if there is any data waiting
        read_more = True
        while read_more:
            selected = select.select([self.aprsis_sock], [], [], 0)
            if len(selected[0]) > 0:
                recvd_data = self.aprsis_sock.recv(aprs_constants.RECV_BUFFER)
                if not recvd_data:
                    self.data_buffer += recvd_data
                else:
                    read_more = False
            else:
                read_more = False

        # check for any complete packets and move them to the packet buffer
        if '\r\n' in self.data_buffer:
            partial = True
            if self.data_buffer.endswith('\r\n'):
                partial = False
            packets = recvd_data.split('\r\n')
            if partial:
                self.data_buffer = str(packets.pop(-1))
            else:
                self.data_buffer = ''
            for packet in packets:
                self.packet_buffer += [str(packet)]

        # return the next packet that matches the filter
        while len(self.packet_buffer):
            packet = self.packet_buffer.pop(0)
            if filter_logresp and packet.startswith('#') and 'logresp' in packet:
                pass
            else:
                return aprs_util.decode_frame(packet)

        return None
