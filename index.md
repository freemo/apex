---
title: APEX
tags: [basics]
sidebar: home_sidebar
---

APEX stands for "**AP**rs **EX**tended"; It will be a new protocol which
expands on and fixes most of the issues in the older APRS protocol while
still remaining backwards compatible.

APEX defines both a new protocol and a new paradigm. Since much of the new
protocol will not run on existing hardware APEX also includes a Python
reference implementation that will provide a full APEX application out of
the box. Since APEX is backwards compatible with APRS it can fully utilize
existing APRS hardware to route APEX packets across the network. Though only
APEX capable stations would be able to make full use of the information in an
APEX packet.

The software for the project can currently be found at the
[APEX GitHub page](https://github.com/Syncleus/apex).

# Why something new?

The APRS network relies heavily on internet connectivity. The only way you can
get a packet to a distant destination, whwn local internet is down, is to
get the packet to a station with an internet gateway. This opens the APRS
network up to all sorts of vulnerability in a disaster scenario where area
wide internet access may be lost.

One way APEX addresses this is by providing path aliases that are capable
of cross-band repeating, combined with a mechanism for identifying which
ports a digipeater provides. The VHF-to-HF cross-band path aliases would never
be used for routine traffic, due to congestion concerns, but during an
emergency even legacy APRS devices can benefit from the APEX paradigm by
being able to get emergency messages out across HF channels efficiently.

Part of the effort is to bring the United States up to date with Europe's
infrastructure as well as produce an internation standards for global
radio networks. Across europe there is a multi-band Robust Packet Radio
and APRS network in place across 4 HF networks and one or more VHF networks.
The european system also includes a backbone of repeaters with standardized
digipeating configurations.

APEX allows for multiple HF networks, and paths that can cross between the
bands; APEX will prioritize HF traffic between short-distance bands such as
160m or 80m, or long distance traffic on 30m dynamically.

In the end we hope to provide a standard which supports the current APRS
network and paradigm while still expanding it and improving it to make
the network more resiliant to emergency and more useful during normal
operation as well.

# Goals

It is important that we build APEX from the lessons we learned from APRS.
This means where possible we will use existing standards, or try to
resolve any differences between regional standards. Any standards
introduced mest be considerate of, and backwards compatible to the
existing networks.

The final network envisioned, once APEX reaches pervasive coverage,
would be an efficient, self-reflective network. Stations would announce
its cross-port capabilities and wide path packets will be rate limited
to reduce congestion on a particular network. Of course most of this will
require adoption of the APEX Protocol, not just the paradigm. The APEX
reference implementation can be used as a full stack reference
implementation; it is a python application, fully configuration, and
ready to be run on a digipeater station capable of interfacing with any
number of TNC across any number of bands.

