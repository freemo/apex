---
title: APEX Application
sidebar: software_sidebar
permalink: /software/
toc: false
---

As part of the APEX initiative the project includes an APEX and APRS client that
acts as the APEX reference implementation. It is extensible and anyone with
python experience can write plugins to expand it and hook their own software
into it. This allows for lots of opportunities from the community to get
involved and contribute to the project.

The reference implementation implements all aspects of the APEX protocol. This
includes the transmitting beacon, status, and id packets, and digipeating. So
everything is ready for experimentation. As new features roll out they will be
added to the APEX Reference Implementation as well. It is a command line
Python 3 application and you can [find it on github](https://github.com/Syncleus/apex).
It is very simple to run and you just need to configure a few things in the config file
to get it up and running.

Below is a screenshot showing it digipeating packets as they come in across two
TNCs. 

[![Screen shot of APEX application.](/images/screenshot1.png)](/images/screenshot1.png)
