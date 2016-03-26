---
title: Path Selection
sidebar: paradigm_sidebar
permalink: /paradigm/path/
toc: false
---

For the time being path recomendations are the same as the most prevelant paradigms in Europe and the USA. The paradigm depends somewhat on the station's characteristics, and intended use.

Typically digipeaters will repeat their own callsign and ssid combination, if they are cross-band digipeaters then it will respond also to the callsign and ssid of the ports with which it can cross-band repeat to. It is prefered, when possible, to choose a path that prefers station identifiers specifically (explicit pathing) rather than wide area aliases like WIDEN-n.

# VHF and above

VHF and UHF APRS networks tend to have much shorter propagation distances per hop. As such wider paths need to be deployed, especially if it is to be resiliant during an emergency. Digipeaters should respond to the WIDEN-n paradigm, as well as regional aliases, for any number of hops. However APEX ensures smart rate limiting such that long hops are more likely to be dropped. With APEX clients WIDEN-n does not need to be explicitly specified, it is baked in and the number of hops are all determined by the underlieing algorithms.

For outgoing wide area packets packets for general purpose use a path of WIDE3-3, specifically beacon, id, and status packets, as well as outgoing messages where an explicit pathis unknown. For special purposes outgoing messages the regional aliases can also be used, but never for routine messages.

When possible it is allowed to limit the number of hopes of a WIDEN-n message at the digipeater, but few digipeaters offer this functionality. APEX clients will use smart rate limiting to ensure during times of congestion packets are dropped to ensure the integrity of the network.

It is important to note that WIDE3-3 is recomended as opposed to WIDE1-1,WIDE2-2 in some APRS circles. The reason for this is that most digipeaters now tend to support the new paradigm such that this is no longer neccesary. The old approach was to ensure the first hop, could not eat the entire WIDE3-3 alias in a single hop (if it doesnt recognize the ssid as a hop indicator, as older APRS TNC tend to do). If you are in a particularly remote location where older TNC are still in operation and APRS station density is low it may still make sense to use the older WIDE1-1,WIDE2-2 path. However APEX clients will still detect this scenario automatically by listening to incoming packets and determining local digipeating capabilities.

# HF

HF digipeaters should always be configured to digipeat and respond to WIDEN-n and regional path aliases. On older non-APEX systems the digipeater should be configured on HF to only respond to WIDE1-1 and the equivelant regional alias. The new APEX protcol however will use smart rate limiting to allow the digipeater to dynically determine how many hops should be allowed over the bands. So for APEX systems this setting is usually handled for you behind the scenes.

As for the outgoing path to set, when explicit pathing is unknown, on HF this should be WIDE1-1 for older APRS stations, APEX clients will dynamically determine this value in future versions, but for now should be set to WIDE1-1 as well. This path should also be used for beacon, id, and status packets on HF. The reason for this is for messaging to be effective on HF both station must be able to hear the beacon of the other station, or else be dependent on the internet as a conduit (APRS-IS). In times of disaster the radio network needs to be ressiliant enough to continue to be able to pass messages long distance. This is only possible if your beacon can be heard by distant stations.

# Cross-band

[Cross-band digipeating](/protocol/cross-band/) should be enabled where possible and are enabled by default in APEX clients. However cross-band paths should very rarely be used going from VHF to HF (or from a higher baud rate network to a lower in general). Never should it be the default path for beacon, id, and status broadcast packets, nor should it be the first attempted path for outgoing messages. However during times of emergency where VHF packets are no longer viable long distances due to a lack of a local path to an internet gateway it may becomes necceserary to temporarily include cross-band aliases in the route. This can acheive a path to the outside world to relay emergency messages. Ideally if possible an explicit path using a cross-band station should be used rather than the cross-band aliases, which will ensure the outgoing packets do not get transmitted by more than one local HF station.

For APEX clients the path will be determined automatically, allowing for local HF stations to be detected and used in explicit pathing. However by allowing for cross-band aliases it gives operators of older APRS stations to have a mechnism with which to get emergency communications out during a disaster.
