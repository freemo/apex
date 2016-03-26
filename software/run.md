---
title: Running APEX
sidebar: software_sidebar
permalink: /software/run/
toc: false
---

If you followed all the steps up until now it should be pretty easy to get the application running. If you installed the application your dependencies should be taken care of for you and all you have to do is run the command apex.

However right now since a proper release has not been made yet everyone will run the application directly from the repository. For that first you need to make sure you have the necceseray dependencies installed, those are:

    pynmea2 >= 1.4.2
    pyserial >= 2.7
    requests >= 2.7.0
    cachetools >= 1.1.5

With the dependencies in place and configuration file ready you can start the application with the following command, remember, you need Python 3.

    python ./comterminal.py
