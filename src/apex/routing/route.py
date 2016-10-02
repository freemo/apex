#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


def has_seen(port_map, frame):
    # Can't digipeat anything when you are the source
    for port in port_map.values():
        if frame['source'] == port['identifier']:
            return True

    # can't digipeat things we already digipeated.
    for hop in frame['path']:
        for port in port_map.values():
            if hop.startswith(port['identifier']) and hop.endswith('*'):
                return True

    return False


def is_hop_consumed(hop):
    if hop.strip()[-1] is '*':
        return True
    else:
        return False
