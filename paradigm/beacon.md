---
title: Beacon Packet
sidebar: paradigm_sidebar
permalink: /paradigm/beacon/
toc: false
---

APEX Beacons follow the same format as an APRS beacon but with a few additions. First off, the position is prefered to be encoded using mic-e compression, however it may be encoded as plain text as well. APEX clients must always natively interprit both plain text and mic-e but may transmit either.

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

Obviously for a mobile station some of the fields, such as height omni, are usually 0.

The standard also dictates the content of the identifying comments, which are no longer free form. The current suggestion is
to follow the European standard, with some small modifications. The European standard has the following beacon comment format.

    G/D R-I-R 24H
    
The various values are defined in European standard as follows

    Beacon Comment – Service Code
    
    ----features----
    G/D Gate & Digi available
    -/D Digi only
    G/- Gate only

    ----connectivity----
    R-I-R Radio Internet Radio connection
    R-I Radio Internet only
    R Radio only / no internet i.e. Digi/p

    ----time table----
    H24 24 hours operation
    H12 except night hours
    HX variable times / on request
    HN night times 
    
The additions to the european standard defined by APEX includes a connectivity of "I-R" to specify stations which will port internet packets over the radio but will not gate traffic into the internet. It also adds an additional field at the end in the form of C## which specifies the rate at which packets were received since the last beacon was sent out. The rate is in average packets per minute.

The new APEX standard for the beacon comment would, therefore, be the following.

    Beacon Comment – Service Code
    
    ----features----
    G/D Gate & Digi available
    -/D Digipeater only
    G/- Internet Gate only

    ----connectivity----
    R-I-R Bidirection traffic between radio and internet gateway
    R-I Radio traffic reported to internet only.
    I-R Internet traffic emited into radio network only.
    R Radio only / no internet

    ----time table----
    H24 24 hours operation
    H12 except night hours
    HX  variable times / on request
    HN  night time operation only
    
    ----congestion level----
    C## congestion level, ## is aveage packets per minute
    
Therefore the beacon comment on an APEX compliant beacon packet looks like the following

    G/D R-I-R H24 C30
    
The following is an examples of a complete compliant APEX beacon including PHG specifier and coordinates:

    !/:=i@;N.G& --PHG5360/WIDE G/D R-I-R H24 C30
    
**NOTE:** The beacon on every port of a TNC should always be the same.
