---
title: Cross-band Routing
sidebar: protocol_sidebar
keywords: RFC
tags: [rfc]
permalink: /protocol/cross-band/
toc: false
status: RFC
rfclink: https://www.reddit.com/r/ApexProtocol/comments/4byrdm/crossband_repeating_rfc/
---

In order to facilitate cross-band routing the APEX protocol defines several
new designators as well as includes many of the old ones. Obviously WIDEN-n,
GATE, and your own callsign will behave similarly to how they behaved in the
old paradigm. However the new band-specific designators will have a form of
##M### or ###M## where # represents any digit 0 to 9. The first group of
numbers specifies the band ID, while the second group of numbers is the net
ID and is optional. In this way the designator 30M would represent the 30
meter band as a whole (specifically any nets on that band the station is
capable of). When 30M is specified in a path, a station will repeat that
packet out on any port which is tuned to the 30M band. Similarly 30M1 would
specify a frequency (net) that resides within the 30M band. The list of
identifiers for the various nets will be updated periodically as new nets show
up. However right now 30M1 would specify the world wide FSK based APRS network
residing on 10.1476 Mhz USB; similarly 30M2 would specify the world wide Robust
Packet Radio based APRS network which resides on 10.1473 Mhz USB. similarly
other designations would be chosen for other networks throughout the world. A
complete list would have to be compiled.

Using these new designators in a path would be relatively straight forward. If,
for example, you wanted a packet to take one hop, then move over to the 30
meter Robust Packet Radio channel, then move back to ordinary VHF for its last
hop, and you do not care what the specific frequency on that hop, then you would
construct your path as follows:

    WIDE1-1,30M2,2M

Notice the last hop is just 2M with no number suffix. This is because we just
want it to gate into 2M network and don't care which frequency on that band it
is gating into. As a side note the GATE specifier would actually perform the
same function as the 2M specifier.

Finally, when the first digit of alias is a 0 then the numbers in the first group are considered to be in centimeters rather than meters. Therefore while 30M represents the 30 meter band 033M represents the 33 centimeter band.

# Generic Cross-band Aliases

The following generic cross-band aliases allow for cross band operation to specific bands, rather then an explicit frequency within them. This is useful for global operation where the local frequency used may differ from region to region.

Alias   | Frequency Range 
--------|----------
023M    | 1240 Mhz - 1300 Mhz
033M    | 900 Mhz - 930 Mhz
070M    | 420 Mhz - 450 Mhz
1M      | 150 Mhz - 300 Mhz
2M      | 100 Mhz - 150 Mhz
6M      | 50 Mhz - 55 Mhz
10M     | 28 Mhz - 30 Mhz
12M     | 24 Mhz - 25 Mhz
15M     | 21 Mhz - 22 Mhz
17M     | 18 Mhz - 19 Mhz
20M     | 14 Mhz - 15 Mhz
30M     | 10 Mhz - 11 Mhz
40M     | 7 Mhz - 7.3 Mhz
60M     | 5.3 Mhz - 5.5 Mhz
80M     | 3.5 Mhz - 4 Mhz
160M    | 1.5 Mhz - 2 Mhz

# Specific Frequency Cross-band Aliases

The following table gives the current frequency-specific cross-band aliases. This list is constantly growing and will be added to anytime we learn of a new local frequency utilizing APRS or APEX protocols.

Alias   | Frequency          | Modulation 
--------|--------------------|---------------------
2M1     | 144.39 Mhz  (spot) | FM
2M2     | 144.8 Mhz   (spot) | FM
2M3     | 144.525 Mhz (spot) | FM
2M4     | 144.62 Mhz  (spot) | FM
2M5     | 144.54 Mhz  (spot) | FM
2M6     | 144.66 Mhz  (spot) | FM
2M7     | 144.93 Mhz  (spot) | FM
2M8     | 145.01 Mhz  (spot) | FM
2M9     | 145.175 Mhz (spot) | FM
2M10    | 145.525 Mhz (spot) | FM
2M11    | 145.575 Mhz (spot) | FM
20M1    | 14.1033 Mhz (USB)  | Robust Packet Radio
20M2    | 14.0963 Mhz (USB)  | Robust Packet Radio
20M3    | 14.1046 Mhz (spot) | FSK
20M4    | 14.0982 Mhz (spot) | FSK
30M1    | 10.1473 Mhz (USB)  | Robust Packet Radio
30M2    | 10.1492 Mhz (spot) | FSK
40M1    | 7.0473 Mhz  (USB)  | Robust Packet Radio
40M2    | 7.0363 Mhz  (USB)  | Robust Packet Radio
40M3    | 7.0492 Mhz  (spot) | FSK
40M4    | 7.0376 Mhz  (spot) | FSK
80M1    | 3.610 Mhz   (USB)  | Robust Packet Radio
