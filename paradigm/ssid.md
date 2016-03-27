---
title: Callsign SSID Selection
sidebar: paradigm_sidebar
permalink: /paradigm/ssid/
toc: false
---

The callsign specifier is similar in APEX as it is in the APRS specification. That is, it is your ham radio callsign followed by a dash and then a number from 0 to 15 inclusive. An SSID of 0 is equivelant to the callsign with no SSID specified. So the following two callsigns are identical.

    WI2ARD
    WI2ARD-0
  
According to the APEX specification the SSID of 0 is reserved, when assigning a callsign to a TNC port never select an SSID of 0, nor are you allowed to drop the SSID all together. If it is an operating station it must be assigned an ssid of 1 or larger. Furthermore each TNC port, or any radio operating on a specific frequency should have a unique SSID; This ensures that explicit paths can be generated that hot cross-band paths without needing to use an alias that might generated unneceserary repeat transmissions.

The reason the ssid of 0 is reserved int he APEX system is because it is used for store & forward messaging and is the address where all messages should get sent to. These messages will ultimately get forwarded to an active station with an SSID. So in this way the transmitting station doesnt need to be aware of which ssid you are actively using, he can just send it to your main callsign and it will get routed appropriately. Store and forward will also allow you to receive messages when your station is offline, which will be received next time the station comes online.
