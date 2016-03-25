---
title: Preemptive Routing
sidebar: protocol_sidebar
keywords: news, blog, updates, release notes, announcements
permalink: /protocol/preemptive/
toc: false
status: RFC
rfclink: https://www.reddit.com/r/ApexProtocol/comments/4byxl3/preemptive_routing_rfc/
---

Preemptive routing is unique to APEX and also made it into the initial release
of the APEX reference implementation. With preemptive routing a digipeater can
respond to certain specifiers in the path even when they are not the next hop
in the path. With the cross-band path specifier mentioned above, ###M##, an
optional ssid can be added to the end. If the ssid is not 0 then it specifies
that the path should be treated preemptively. Essentially what that means is if
it is the next hop then treat it normally however if it is a future hop you can
skip all the hops in between and go straight to the hop, assuming the station
is capable of operating that band (otherwise it is ignored).

For example say we wanted to create a path where I get a packet out over HF and
thats all I want to do. Consider the following path:

    WIDE1-1,WIDE2-2,30M-1

In this case since 30M-1 is preemptive then the packet will hop across the WIDE
path but every station that hears it along the way that is capable of 30M band
transmission will emit the packet on that port as well. Contrast this without
preemptive paths where it would look like:

    WIDE1-1,WIDE2-2,30M

In this case the packet would follow the WIDE path and even if they are capable
at digipeating on 30M it will not do so. Only the very last stations that hear
the packet after the WIDE portion of the path is spent will actually be the ones
to digipeat over to 30M. This would cause far fewer emissions on the 30M band
while still ensuring the transmitting stations are geographically spread out.
In an emergency this might be a good way to send an emergency packet out.

When a path specifier has a non-zero ssid it is preemptive. The value of the
ssid indicates its priority. So when there is a long path with several
preemptive routes specified it is always the one that is the highest priority
and when there is a tie it is always the right-most (last in the path)
specifier that gets triggered. For example say we had the following path:

    ECHO*,80M-2,WIDE1,30M-2,80M-1

In this case if the packet is received from a all-band capable station then it
would emit the path for 30M-2 when digipeating the packet. The reason is that 2
is a higher priority than 1 and of those of equal priority the 30M-2 was the
later one in the path.

Also important to note is that when preemptive pathing is executed all the
intermediary paths that were skipped get dropped from the path entirely. So the
above path, once digipeated, would be transformed to the following path:

    ECHO*,WI2ARD-1*,30M-2*,80M-1

Another interesting twist is how preemptive routing handles the other types of
path specifiers. Basically the WIDEN-n type specifiers are never treated
preemptively. However specifiers which reflect the stations own callsign are
always treated preemptively. callsigns, unlike cross-band specifiers do not
have their priority reflected by the presence of an ssid; they are also still
treated as preemptive even when they have an ssid of 0.

When there is a mix of callsign and cross-band preemptive specifiers in the same
path then first the cross-band preemptive specifier is determined as before,
second the right most occurrence of the station's callsign is determined. Which
ever of the two occur right most in the path is the one that wins. For example:

    WIDE2-2,WI2ARD-1,30M-1

In this case the preemptive path would jump to 30M1. However if instead we had
the following:

    WIDE2-2,30M-1,WI2ARD-1

In this case the preemptive pathing would jump right to the WI2ARD-1 path.
