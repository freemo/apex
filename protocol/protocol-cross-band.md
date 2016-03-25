---
title: Cross-band Routing
sidebar: protocol_sidebar
keywords: news, blog, updates, release notes, announcements
permalink: /protocol/cross-band/
toc: false
---

In order to facilitate cross-band routing the APEX protocol defines several
new designators as well as includes many of the old ones. Obviously WIDEN-n,
GATE, and your own callsign will behave similarly to how they behaved in the
old paradigm. However the new band-specific designators will have a form of
##M### or ###M## where # represents any digit 0 to 9. The first group of
numbers specifies the band ID, while the second group of numbers is the net
ID and is optional. In this way the designator 30M would represent the 30
meter band as a whole (specifically any nets on that band the station is
capable of). When 30M is specified in a path, a station will digipeat that
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
hop, and you dont care what the specific frequency on that hop, then you would
construct your path as follows:

    WIDE1-1,30M2,2M

Notice the last hop is just 2M with no number suffix. This is because we just
want it to gate into 2M network and don't care which frequency on that band it
is gating into. As a side note the GATE specifier would actually perform the
same function as the 2M specifier.

