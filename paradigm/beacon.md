---
title: Beacon Packet
sidebar: paradigm_sidebar
permalink: /paradigm/beacon/
toc: false
---

APEX Beacons follow the same format as an APRS beacon but with a few additions. First off, the position should always be encoded using mic-e compression. APEX clients can always natively interprit both plain text and mic-e but will transmit as mic-e for packet effiency and backwards-compatability.

APEX beacons should always include the PHG designator even for mobile stations. This is critical for APEX to calculate packet routing so if it is ommited the packet will not be considered APEX compliant. The PHG specification was documented in the original APRS specification as the following.

    POWER-HEIGHT-GAIN:  This optional field replaces the CSE/SPD fields with a
    report of transmitter power, antenna height-above-average-terain and 
    antenna gain.  APRS uses this to plot radio range circles around all 
    stations.  The following details the format to be used in the BText of 
    a TNC dedicated as an APRS digipeater:

    !DDMM.mmN/DDDMM.mmW#PHG5360/WIDE...(identifying comments)...
      |         |      | | ||||  |_____ makes station show up green
      |         |      | | ||||________ Omni (Direction of max gain)
      |         |      | | |||_________ Ant gain in dB
      |         |      | | ||__________ Height = log2(HAAT/10)
     LAT      LONG     | | |___________ Power = SQR(P)
                       | |_____________ Power-Height-Gain identifier *
                       |_______________ # is symbol for digipeater

     As you can see by the integers in the PHG string, there are only 10
     possible values for each of these fields as follows:

     DIGITS   0  1  2   3   4   5   6    7    8    9         Equation
     -------------------------------------------------------------------
     POWER    0, 1, 4,  9, 16, 25, 36,  49,  64,  81  watts  SQR(P)
     HEIGHT  10,20,40, 80,160,320,640,1280,2560,5120  feet   LOG2(H/10)
     GAIN     0, 1, 2,  3,  4,  5,  6,   7,   8,   9  dB
     DIR      0,45,90,135,180,225,270, 315, 360,   .  deg    (D/45)

     The DIRECTIVITY field offsets the PHG circle by one third in the
     indicated direction.  This means a front to back range of 2 to 1.
     Most often this is used to indicate a favored direction or a null
     even though an OMNI antenna is at the site.  Note that 0 means
     OMNI and 8 means 360 or a NORTH offset.

     HEIGHTS are ABOVE-AVERAGE TERRAIN!  Not above ground or sea
     level.  Your antenna may be at 1000 ft above sealevel and be on 
     a 100 foot tower.  But if you go out 10 miles in all directions
     and find that the average elevation is 1200 feet, then your
     height-above-averag-terain is less than ZERO!!!!

Obviously for a mobile station some of the fields, such as height omni, are usually 0. Also for full APEX compliance a few extra dynamic fields are added to the end of the PHG specifier. A tilde acts as a seperator and designator followed by two digits which represent the average number of packets per minute received since the last beacon. This information will be used by the APEX routing system to automatically route packets around high congestion stations.

The resulting beacon format now looks something like this:

    !DDMM.mmN/DDDMM.mmW#PHG5360/WIDE~23...(identifying comments)...
      |         |      | | ||||  |  ||_ avg. packets received per minute
      |         |      | | ||||  |  |__ apex specific seperator
      |         |      | | ||||  |_____ makes station show up green
      |         |      | | ||||________ Omni (Direction of max gain)
      |         |      | | |||_________ Ant gain in dB
      |         |      | | ||__________ Height = log2(HAAT/10)
     LAT      LONG     | | |___________ Power = SQR(P)
                       | |_____________ Power-Height-Gain identifier *
                       |_______________ # is symbol for digipeater

The standard also dictates the content of the identifying comments, which are no longer free form. The current suggestion is
to follow the European standard. The European standard has the following beacon comment format.

    G/D R-I-R 24H
    
The various values are defined in European standard as follows

    Beacon Comment – Service Code
    **features**
    G/D Gate & Digi available
    -/D Digi only
    G/- Gate only

    connectivity
    R-I-R Radio Internet Radio connection
    R-I Radio Internet only
    R Radio only / no internet i.e. Digi/p

    time table
    H24 24 hours operation
    H12 except night hours
    HX variable times / on request
    HN night times 
    
The additions to the european standard defined by APEX includes a connectivity of "I-R" to specify stations which will port internet packets over the radio but will not gate traffic into the internet. Also the addition of a "HD" time table specifier to indicate day time only operation.
