---
title: APEX Paradigm
sidebar: paradigm_sidebar
keywords: news, blog, updates, release notes, announcements
permalink: /paradigm/
toc: false
---
The APEX Protocol relies on some peers, preferably most, run the APEX paradigm.
While the old APRS Paradigm can be used, which in fact is very similar and
backwards compatible with the APEX Paradigm, it will reduce the functionality
provided by the APEX network.

# Why a new Paradigm?

The APRS network relies heavily on internet connectivity. The only way you can
get a packet to its intended destination, without a nearby connection, is to
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
infrastructure as well as standardized across the two as much as possible.
Across europe there is a multi-band Robust Packet Radio and APRS network
in place across 3 HF networks and one or more VHF networks. The european
system also includes a backbone of repeaters with standardized digipeating
configurations.

In the end we hope to provide a standard which supports the current APRS
network and paradigm while still expanding it and improving it to make
the network more resiliant to emergency and more useful during normal
operation as well.
