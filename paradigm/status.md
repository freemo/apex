---
title: Status Packet
sidebar: paradigm_sidebar
permalink: /paradigm/status/
toc: false
---

The status packet in the APEX specification follows essentially the same specification as with the older APRS protocol. That is the TO field, like a beacon packet, is "APRS". However a status packet is differentiated from a beacon packet as the first character in the payload is always ">". Any text which follows this identifier is the status text. This can be any free form text the station operator would like to report to the network. This is where you might specify the stations your listening on or a URL to further station information.

The following is an example status packet payload.

    >Robust Packet Radio http://JeffreyFreeman.me
