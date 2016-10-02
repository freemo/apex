#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Util Module."""

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

import apex.kiss
import apex.kiss.constants

from .kiss_mock import KissMock

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

# KG6WTF>S7TSUV,MTOSO-2,WIDE2*,qAR,KF6FIR-10:`17El#X-/kg6wtf@gosselinfamily.com
ENCODED_FRAME = [192, 0, 75, 71, 54, 87, 84, 70, 62, 83, 55, 84, 83, 85, 86, 44, 77, 84, 79, 83, 79, 45, 50, 44, 87, 73,
                 68, 69, 50, 42, 44, 113, 65, 82, 44, 75, 70, 54, 70, 73, 82, 45, 49, 48, 58, 96, 49, 55, 69, 108, 35,
                 88, 45, 47, 107, 103, 54, 119, 116, 102, 64, 103, 111, 115, 115, 101, 108, 105, 110, 102, 97, 109, 105,
                 108, 121, 46, 99, 111, 109, 192]
DECODED_FRAME = [75, 71, 54, 87, 84, 70, 62, 83, 55, 84, 83, 85, 86, 44, 77, 84, 79, 83, 79, 45, 50, 44, 87, 73, 68,
                 69, 50, 42, 44, 113, 65, 82, 44, 75, 70, 54, 70, 73, 82, 45, 49, 48, 58, 96, 49, 55, 69, 108, 35,
                 88, 45, 47, 107, 103, 54, 119, 116, 102, 64, 103, 111, 115, 115, 101, 108, 105, 110, 102, 97, 109,
                 105, 108, 121, 46, 99, 111, 109]

# pylint: disable=R0904,C0103
class KissUtilTestCase(unittest.TestCase):

    """Test class for KISS Python Module."""

    def setUp(self):
        """Setup."""
        self.kiss_mock = KissMock()

    def tearDown(self):
        """Teardown."""
        self.kiss_mock.clear_interface()

    def test_escape_special_codes_fend(self):
        """
        Tests `kiss.util.escape_special_codes` util function.
        """
        # fend = apex.kiss.util.escape_special_codes(apex.kiss.constants.FEND)
        fend = apex.kiss.Kiss._Kiss__escape_special_codes([apex.kiss.constants.FEND])  # pylint: disable=E1101
        self.assertEqual(fend, apex.kiss.constants.FESC_TFEND)

    def test_escape_special_codes_fesc(self):
        """
        Tests `kiss.util.escape_special_codes` util function.
        """
        fesc = apex.kiss.Kiss._Kiss__escape_special_codes([apex.kiss.constants.FESC])  # pylint: disable=E1101
        self.assertEqual(fesc, apex.kiss.constants.FESC_TFESC)

    def test_read(self):
        self.kiss_mock.clear_interface()
        self.kiss_mock.add_read_from_interface(ENCODED_FRAME)
        translated_frame = self.kiss_mock.read()
        self.assertEqual(DECODED_FRAME, translated_frame)

    def test_write(self):
        self.kiss_mock.clear_interface()
        self.kiss_mock.write(DECODED_FRAME)
        all_raw_frames = self.kiss_mock.get_sent_to_interface()
        self.assertEqual(ENCODED_FRAME, all_raw_frames[0])


if __name__ == '__main__':
    unittest.main()
