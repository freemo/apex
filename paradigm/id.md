---
title: ID Packet
sidebar: paradigm_sidebar
permalink: /paradigm/id/
toc: false
---

ID type packets arent well defined in the APRS standard, though many TNC and APRS software use the ID packet similarly, to identify the callsigns assigned various ports on the TNC. An ID packet can be differentiated from a beacon packet from the AX.25 "TO" field of the packet, which should be set to "ID".

Lacking a pre-existing standard APEX borrowed and expanded on the formats currently in yes. The content of the ID packet consists of a space seperated list of all the callsign and path aliases with which the station can respond to, except cross-band aliases which are associated with the aliases associated with them directly. This is best explained with a real world example.

    WI2ARD-1/30M1 WI2ARD-2/2M1 GATE/2M1 WIDEN-n

In the above example WI2ARD-1 is the callsign identifier used on the port associated with HF frequency 30M1 (see [cross-band digipeating](/protocol/cross-band)), WI2ARD-2 is associated with VHF frequency 2M1, the GATE alias is supported and will cross-band repeat into the VHF frequency 2M1. The station is also reporting that it supports the WIDEN-n paradigm.

The ultimate purpose of the ID packet is to allow other stations to discover the cross-band capabilities of a station in an automatic, machine readable, way.
