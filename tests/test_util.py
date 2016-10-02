#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Python APRS util methods."""

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import logging.handlers
import unittest

import apex.aprs.util
from apex.aprs import constants as aprs_constants

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '0123456789'
POSITIVE_NUMBERS = NUMBERS[1:]
ALPHANUM = ''.join([ALPHABET, NUMBERS])

VALID_CALLSIGNS = ['W2GMD', 'W2GMD-1', 'KF4MKT', 'KF4MKT-1', 'KF4LZA-15']
INVALID_CALLSIGNS = ['xW2GMDx', 'W2GMD-16', 'W2GMD-A', 'W', 'W2GMD-1-0',
                     'W*GMD', 'W2GMD-123']


class AprsUtilTestCase(unittest.TestCase):  # pylint: disable=R0904
    """Tests for Python APRS Utils."""

    logger = logging.getLogger(__name__)
    logger.setLevel(aprs_constants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(aprs_constants.LOG_LEVEL)
    formatter = logging.Formatter(aprs_constants.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False

    def test_latitude_north(self):
        """Test Decimal to APRS Latitude conversion.

        Spec per ftp://ftp.tapr.org/aprssig/aprsspec/spec/aprs101/APRS101.pdf
        --
        Latitude is expressed as a fixed 8-character field, in degrees and
        decimal minutes (to two decimal places), followed by the letter N for
        north or S for south. Latitude degrees are in the range 00 to 90.
        Latitude minutes are expressed as whole minutes and hundredths of a
        minute, separated by a decimal point.

        For example:

            4903.50N is 49 degrees 3 minutes 30 seconds north.

        In generic format examples, the latitude is shown as the 8-character
        string ddmm.hhN (i.e. degrees, minutes and hundredths of a minute
        north).
        """
        test_lat = 37.7418096
        aprs_lat = apex.aprs.util.dec2dm_lat(test_lat)
        self.logger.debug('aprs_lat=%s', aprs_lat)

        lat_deg = int(aprs_lat.split('.')[0][:1])
        # lat_hsec = aprs_lat.split('.')[1]

        self.assertTrue(len(aprs_lat) == 8)
        self.assertTrue(lat_deg >= 00)
        self.assertTrue(lat_deg <= 90)
        self.assertTrue(aprs_lat.endswith('N'))

    def test_latitude_south(self):
        """Test Decimal to APRS Latitude conversion.

        Spec per ftp://ftp.tapr.org/aprssig/aprsspec/spec/aprs101/APRS101.pdf
        --
        Latitude is expressed as a fixed 8-character field, in degrees and
        decimal minutes (to two decimal places), followed by the letter N for
        north or S for south. Latitude degrees are in the range 00 to 90.
        Latitude minutes are expressed as whole minutes and hundredths of a
        minute, separated by a decimal point.

        For example:

            4903.50N is 49 degrees 3 minutes 30 seconds north.

        In generic format examples, the latitude is shown as the 8-character
        string ddmm.hhN (i.e. degrees, minutes and hundredths of a minute
        north).
        """
        test_lat = -37.7418096
        aprs_lat = apex.aprs.util.dec2dm_lat(test_lat)
        self.logger.debug('aprs_lat=%s', aprs_lat)

        lat_deg = int(aprs_lat.split('.')[0][:1])
        # lat_hsec = aprs_lat.split('.')[1]

        self.assertTrue(len(aprs_lat) == 8)
        self.assertTrue(lat_deg >= 00)
        self.assertTrue(lat_deg <= 90)
        self.assertTrue(aprs_lat.endswith('S'))

    def test_longitude_west(self):
        """Test Decimal to APRS Longitude conversion.

        Spec per ftp://ftp.tapr.org/aprssig/aprsspec/spec/aprs101/APRS101.pdf
        --
        Longitude is expressed as a fixed 9-character field, in degrees and
        decimal minutes (to two decimal places), followed by the letter E for
        east or W for west.

        Longitude degrees are in the range 000 to 180. Longitude minutes are
        expressed as whole minutes and hundredths of a minute, separated by a
        decimal point.

        For example:

            07201.75W is 72 degrees 1 minute 45 seconds west.

        In generic format examples, the longitude is shown as the 9-character
        string dddmm.hhW (i.e. degrees, minutes and hundredths of a minute
        west).
        """
        test_lng = -122.38833
        aprs_lng = apex.aprs.util.dec2dm_lng(test_lng)
        self.logger.debug('aprs_lng=%s', aprs_lng)

        lng_deg = int(aprs_lng.split('.')[0][:2])
        # lng_hsec = aprs_lng.split('.')[1]

        self.assertTrue(len(aprs_lng) == 9)
        self.assertTrue(lng_deg >= 000)
        self.assertTrue(lng_deg <= 180)
        self.assertTrue(aprs_lng.endswith('W'))

    def test_longitude_east(self):
        """Test Decimal to APRS Longitude conversion.

        Spec per ftp://ftp.tapr.org/aprssig/aprsspec/spec/aprs101/APRS101.pdf
        --
        Longitude is expressed as a fixed 9-character field, in degrees and
        decimal minutes (to two decimal places), followed by the letter E for
        east or W for west.

        Longitude degrees are in the range 000 to 180. Longitude minutes are
        expressed as whole minutes and hundredths of a minute, separated by a
        decimal point.

        For example:

            07201.75W is 72 degrees 1 minute 45 seconds west.

        In generic format examples, the longitude is shown as the 9-character
        string dddmm.hhW (i.e. degrees, minutes and hundredths of a minute
        west).
        """
        test_lng = 122.38833
        aprs_lng = apex.aprs.util.dec2dm_lng(test_lng)
        self.logger.debug('aprs_lng=%s', aprs_lng)

        lng_deg = int(aprs_lng.split('.')[0][:2])
        # lng_hsec = aprs_lng.split('.')[1]

        self.assertTrue(len(aprs_lng) == 9)
        self.assertTrue(lng_deg >= 000)
        self.assertTrue(lng_deg <= 180)
        self.assertTrue(aprs_lng.endswith('E'))

    def test_valid_callsign_valid(self):
        """
        Tests valid callsigns using `aprs.util.valid_callsign()`.
        """
        for i in VALID_CALLSIGNS:
            self.assertTrue(apex.aprs.util.valid_callsign(i), '%s is a valid call' % i)

    def test_valid_callsign_invalid(self):
        """
        Tests invalid callsigns using `aprs.util.valid_callsign()`.
        """
        for i in INVALID_CALLSIGNS:
            self.assertFalse(
                apex.aprs.util.valid_callsign(i), '%s is an invalid call' % i)

    def test_decode_aprs_ascii_frame(self):
        """
        Tests creating an APRS frame-as-dict from an APRS frame-as-string
        using `aprs.util.decode_aprs_ascii_frame()`.
        """
        ascii_frame = (
            'W2GMD-9>APOTC1,WIDE1-1,WIDE2-1:!3745.94N/12228.05W>118/010/'
            'A=000269 38C=Temp http://w2gmd.org/ Twitter: @ampledata')
        frame = apex.aprs.util.decode_frame(ascii_frame)
        self.assertEqual(
            {
                'source': 'W2GMD-9',
                'destination': 'APOTC1',
                'path': 'APOTC1,WIDE1-1,WIDE2-1',
                'text': ('!3745.94N/12228.05W>118/010/A=000269 38C=Temp '
                         'http://w2gmd.org/ Twitter: @ampledata'),
            },
            frame
        )

    def test_format_aprs_frame(self):
        """
        Tests formatting an APRS frame-as-string from an APRS frame-as-dict
        using `aprs.util.format_aprs_frame()`.
        """
        frame = {
            'source': 'W2GMD-1',
            'destination': 'OMG',
            'path': ['WIDE1-1'],
            'text': 'test_format_aprs_frame'
        }
        formatted_frame = apex.aprs.util.encode_frame(frame)
        self.assertEqual(
            formatted_frame,
            'W2GMD-1>OMG,WIDE1-1:test_format_aprs_frame'
        )


if __name__ == '__main__':
    unittest.main()
