#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import apex.kiss.constants

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


class KissMock(apex.kiss.Kiss):

    def __init__(self,
                 strip_df_start=True):
        super(KissMock, self).__init__(strip_df_start)
        self.read_from_interface = []
        self.sent_to_interface = []

    def _read_interface(self):
        if not len(self.read_from_interface):
            return None
        raw_frame = self.read_from_interface[0]
        del self.read_from_interface[0]
        return raw_frame

    def _write_interface(self, data):
        self.sent_to_interface.append(data)

    def clear_interface(self):
        self.read_from_interface = []
        self.sent_to_interface = []

    def add_read_from_interface(self, raw_frame):
        self.read_from_interface.append(raw_frame)

    def get_sent_to_interface(self):
        return self.sent_to_interface
