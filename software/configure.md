---
title: APEX Configuration
sidebar: software_sidebar
permalink: /software/configure/
toc: false
---

There is only a single configuration file for the application named apex.cfg. There should be a sample configuration file in the APEX repository base directory named apex.cfg.example, rename this to apex.cfg.

The sample configuration should be something like the following.

    [TNC KENWOOD]
    com_port=/dev/ttyUSB1
    baud=9600
    parity=none
    stop_bits=1
    byte_size=8
    port_count=1
    kiss_init=MODE_INIT_KENWOOD_D710
    
    [TNC RPR]
    com_port=/dev/ttyUSB0
    baud=38400
    parity=none
    stop_bits=1
    byte_Size=8
    port_count=1
    kiss_init=MODE_INIT_W8DED
    
    [PORT KENWOOD-1]
    identifier=WI2ARD-1
    net=2M1
    tnc_port=0
    beacon_path=WIDE1-1,WIDE2-2
    status_path=WIDE1-1,WIDE2-2
    beacon_text=!/:=i@;N.G& --PHG5790/G/D R-I-R H24 C30
    status_text=>Listening on 146.52Mhz http://JeffreyFreeman.me
    id_text=WI2ARD/30M1 GATE/2M1 WI2ARD-1/2M1 WIDEN-n IGATE
    id_path=WIDE1-1,WIDE2-2
    
    [PORT RPR-1]
    identifier=WI2ARD
    net=30M1
    tnc_port=0
    beacon_path=WIDE1-1
    status_path=WIDE1-1
    beacon_text=!/:=i@;N.G& --PHG5210/G/D R-I-R H24 C1
    status_text=>Robust Packet Radio http://JeffreyFreeman.me
    id_text=WI2ARD/30M1 GATE/2M1 WI2ARD-1/2M1 WIDEN-n IGATE
    id_path=WIDE1-1
    
    [APRS-IS]
    callsign=WI2ARD
    password=12345
    server=noam.aprs2.net
    server_port=14580

Obviously you will need to edit this file to resemble your own setup. Each section beginning with TNC is associated with a single physical TNC. These sections represent the com port settings and initialization string settings to talk to the TNC.

For a list of acceptable initialization strings check out [the constants file](https://github.com/Syncleus/apex/blob/master/kiss/constants.py). The other property under the TNC section that needs explanation is port_count. This should be a number 1 or greater that indicates the number of ports on the TNC. A TNC port represents a physical connection to the radio; most TNC have either 1 or 2 ports.

For each port associated with a TNC you must also add a PORT section. In the example configuration both TNC are single port TNC so each one has only a single port associated with it. The PORT section should be named such that it uses the same designation as the one in the TNC section but with a dash and a number at the end representing the port id. The port id start counting at 1, not 0, so the first port on the "KENWOOD" TNC in the example configuration is KENWOOD-1.

In the port station the identifier is the station id. In the APEX standard station id with an SSID of 0 are reserved for store and forward messaging so you need to select a non-zero SSID. The net property specifies what port and frequency the port is associated with. For more information on the correct setting for this value view [the page on cross-band routing](/protocol/cross-band/). The tnc_port property may be a bit confusing, this property is the port id according to the TNC itself, it does not need to necessarily agree with the port id int he section heading. The rest of the properties under this section should be straight forward specifying the path and content of various packet types that beacon regularly. For now these are free form but in later versions of APEX these will be constructed automatically.

Finally add a APRS-IS section to add internet gateway capability. Most of the settings in this section should be pretty straight forward.
