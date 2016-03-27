---
title: Roadmap
sidebar: home_sidebar
permalink: /roadmap/
toc: false
---

There are many features that have yet to be implemented and we have some pretty lofty goals in store for APEX. A lot of this is brainstorming from the team so it is subject to change as well. But here are the ideas we have so far on what needs to get implemented into APEX and defined within the protocol.

* Ability to send a signal check packet. These will never get digipeated. Instead you send a packet which contains some diagnostic information about the antenna (HAAT, Power, gain, etc). Next any station which directly heard you will respond immediately with information regarding their own antenna information. Also if possible data will be encoded to indicate received signal strength of the received packet (on most setups this information wont be encoded). The signal test request packet will also specify if they desire the reply packet to be over the air, or through APRS-IS or both. In this way the information can be used for someone to probe band conditions as well as objectively try to configure a new antenna installation.

* When possible encapsulate all existing AX.25 packets in FX.25 packets instead, thereby introducing backwards-compatible Forward Error Correction.

* Provide throttling to prevent congestion. Packets are given priority based on several factors such as the length of the packet, and how frequent the sender sends packets, to determine a packets priority. Higher packets go through while lower priority packets get dropped. Misbehaving nodes, or out of date notes not running APEX would be potential reasons to give a packet a lower priority in addition to traffic statistics.

* Include the ability to send images and other media, potentially across multiple packets.

* Optionally request acks at the packet level. This is particularly useful when using callsign paths. Though for WIDE paths it is still useful to know what paths a packet took for diagnostic reasons and path discovery reasons. In this way an initial packet in a series can use wide but once the paths are discovered then the explicit paths can be used for the subsequent packets. This would reduce network congestion.

* Subscribe-to-callsign: a mechanism whereby a request can be sent to a normally out-of-range station to send me periodic updates to their beacon or other similar packets (comment, id). This is useful for tracking a friend when the station doesnt have internet access of their own.

* Improve or replace the IGATE system so that multiple instances of the same packet can be reported to it (with different paths)

* Rolling beacon ranges. Stations will move over to a store and forward approach. Essentially they will cache as much information about the system as possible. The longer it stays on the net the more information it should receive from distance nodes. This is accomplished with rolling beacons. Basically every station will keep track of how many times they have heard a beacons from the various stations. Any time a beacon is heard more than 'D' times where the receiving station is the last hop, then it will digipeat the beacon, and reset the counter. The value of D is an integer representing decay rate. A higher letter for D and stronger the decay rate. What this will cause is a beacon from a station that has been on a long time will get their beacon across the world hundreds of hops, but very slowly. Because the packets decay with distance this also wont cause a lot of net congestion. For example you might hear a beacon on VHF come from across the continent, but such occurrences would be very rare as well. So it may be exciting to follow rare DX like that. Using this system even if the network went down across the world (not an expected occurrence) it would still be possible for systems to communicate across long distance APRS links, by leveraging the stores cache of beacons every station has they can easily form a path.

* Smart routing for internet capable stations. When considering #8 combined with IGATE access it makes smart routing a possibility. Smart routing would be the process where the route of a packet to reach its destination can be discovered from the fixed stations in a region. The idea is that if the internet goes down these stations still have a cache locally of where the stations are around the world and in their area. This information can be used to create more direct route for message-type packets with a specific destination. This will significantly help congestion since these packets no longer need to try to follow WIDE type paths. Plus a system like this will be more resilient in situations where you have wide spread internet outages.

* Enforcement of certain behavioral rules for stations and to react automatically to a misbehaving station. For example if a beacon rate is too high then all beacons above the accepted rate will be dropped. This will also penalize the priority that station gets when routing its packets.

* Proper standards defined and implemented to encode the protocol version into the packets.

* Geographic routing: We want to add the ability to route packets to approximate geographic coordinates, either in an attempt to send a specific message or to transmit a WIDE message at that location to seek contact with anyone who may be actively listening.

* Better software messages for responding to various types of messaging: CQ, Bulletins, and messages need a nice clean GUI to work with or command line tool

* Delay Tolerant Networks - The general use case is to leverage moving cars for long-distance packets where latency isnt a top concern. It can transport high volumes of data long distance where normal packets could not.

* Retry packets from partial path: When a packet doesnt get to its destination, since stations will be expected to a have a large cache of packets heard, delivery can be retried by the closest node that successfully received the packet. This would make long-distance packets far more feasible.

* Mobile stations can announce stationary "home station". Once geographic packet routing is in place then two mobile stations can stay in touch by simply knowing their route to the home station at anytime. This simplifies discovering routes that would otherwise be impossible between two mobile stations without the use of the internet.

* Formalize the use of ID packets to clearly specify the various path identifiers that can be used with the station and their effects. for example "WI2ARD/30M2 IGATE" might specify I have a station with ID WI2ARD on 30 meter robust packet radio, and it is also igate capable. This, along with position beacons, should make it possible to discover paths dynamically.
