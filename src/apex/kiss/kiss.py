#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KISS Core Classes."""

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import threading
from abc import ABCMeta
from abc import abstractmethod
from six import with_metaclass

from apex.kiss import constants as kiss_constants

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


class Kiss(with_metaclass(ABCMeta, object)):

    """Abstract KISS Object Class."""

    logger = logging.getLogger(__name__)
    logger.setLevel(kiss_constants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(kiss_constants.LOG_LEVEL)
    formatter = logging.Formatter(kiss_constants.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False

    frame_buffer = []

    def __init__(self, strip_df_start=True):
        self.strip_df_start = strip_df_start
        self.exit_kiss = False
        self.lock = threading.Lock()

    @staticmethod
    def __strip_df_start(frame):
        """
        Strips KISS DATA_FRAME start (0x00) and newline from frame.

        :param frame: APRS/AX.25 frame.
        :type frame: str
        :returns: APRS/AX.25 frame sans DATA_FRAME start (0x00).
        :rtype: str
        """
        while frame[0] is kiss_constants.DATA_FRAME:
            del frame[0]
        while chr(frame[0]).isspace():
            del frame[0]
        while chr(frame[-1]).isspace():
            del frame[-1]
        return frame

    @staticmethod
    def __escape_special_codes(raw_code_bytes):
        """
        Escape special codes, per KISS spec.

        "If the FEND or FESC codes appear in the data to be transferred, they
        need to be escaped. The FEND code is then sent as FESC, TFEND and the
        FESC is then sent as FESC, TFESC."
        - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
        """
        encoded_bytes = []
        for raw_code_byte in raw_code_bytes:
            if raw_code_byte is kiss_constants.FESC:
                encoded_bytes += kiss_constants.FESC_TFESC
            elif raw_code_byte is kiss_constants.FEND:
                encoded_bytes += kiss_constants.FESC_TFEND
            else:
                encoded_bytes += [raw_code_byte]
        return encoded_bytes

    @staticmethod
    def __command_byte_combine(port, command_code):
        """
        Constructs the command byte for the tnc which includes the tnc port and command code.
        :param port: integer from 0 to 127 indicating the TNC port
        :type port: int
        :param command_code: A command code constant, a value from 0 to 127
        :type command_code: int
        :return: An integer combining the two values into a single byte
        """
        if port > 127 or port < 0:
            raise Exception('port out of range')
        elif command_code > 127 or command_code < 0:
            raise Exception('command_Code out of range')
        return (port << 4) & command_code

    @abstractmethod
    def _read_interface(self):
        pass

    @abstractmethod
    def _write_interface(self, data):
        pass

    def connect(self, mode_init=None, **kwargs):
        """
        Initializes the KISS device and commits configuration.

        This method is abstract and must be implemented by a concrete class.

        See http://en.wikipedia.org/wiki/KISS_(TNC)#Command_codes
        for configuration names.

        :param **kwargs: name/value pairs to use as initial config values.
        """
        pass

    def close(self):
        if self.exit_kiss is True:
            self._write_interface(kiss_constants.MODE_END)

    def _write_setting(self, name, value):
        """
        Writes KISS Command Codes to attached device.

        http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes

        :param name: KISS Command Code Name as a string.
        :param value: KISS Command Code Value to write.
        """
        self.logger.debug('Configuring %s = %s', name, repr(value))

        # Do the reasonable thing if a user passes an int
        if isinstance(value, int):
            value = chr(value)

        return self._write_interface(
            [kiss_constants.FEND] +
            [getattr(kiss_constants, name.upper())] +
            [Kiss.__escape_special_codes(value)] +
            [kiss_constants.FEND]
        )

    def __fill_buffer(self):
        """
        Reads any pending data in the interface and stores it in the frame_buffer
        """

        new_frames = []
        read_buffer = []
        read_data = self._read_interface()
        while read_data is not None and len(read_data):
            split_data = [[]]
            for read_byte in read_data:
                if read_byte is kiss_constants.FEND:
                    split_data.append([])
                else:
                    split_data[-1].append(read_byte)
            len_fend = len(split_data)

            # No FEND in frame
            if len_fend == 1:
                read_buffer += split_data[0]
            # Single FEND in frame
            elif len_fend == 2:
                # Closing FEND found
                if split_data[0]:
                    # Partial frame continued, otherwise drop
                    new_frames.append(read_buffer + split_data[0])
                    read_buffer = []
                # Opening FEND found
                else:
                    new_frames.append(read_buffer)
                    read_buffer = split_data[1]
            # At least one complete frame received
            elif len_fend >= 3:
                for i in range(0, len_fend - 1):
                    read_buffer_tmp = read_buffer + split_data[i]
                    if len(read_buffer_tmp) is not 0:
                        new_frames.append(read_buffer_tmp)
                        read_buffer = []
                if split_data[len_fend - 1]:
                    read_buffer = split_data[len_fend - 1]
            # Get anymore data that is waiting
            read_data = self._read_interface()

        for new_frame in new_frames:
            if len(new_frame) and new_frame[0] == 0:
                if self.strip_df_start:
                    new_frame = Kiss.__strip_df_start(new_frame)
                self.frame_buffer.append(new_frame)

    def read(self):
        with self.lock:
            if not len(self.frame_buffer):
                self.__fill_buffer()

            if len(self.frame_buffer):
                return_frame = self.frame_buffer[0]
                del self.frame_buffer[0]
                return return_frame
            else:
                return None

    def write(self, frame_bytes, port=0):
        """
        Writes frame to KISS interface.

        :param frame: Frame to write.
        """
        with self.lock:
            kiss_packet = [kiss_constants.FEND] + [Kiss.__command_byte_combine(port, kiss_constants.DATA_FRAME)] + \
                Kiss.__escape_special_codes(frame_bytes) + [kiss_constants.FEND]

            return self._write_interface(kiss_packet)
