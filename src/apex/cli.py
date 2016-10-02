#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mapex` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``apex.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``apex.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import signal
import sys
import threading
import time

import click
import six

import apex.aprs
import apex.buffers
from apex.kiss import constants as kissConstants
from apex.plugin_loader import get_plugins
from apex.plugin_loader import load_plugin

from .buffers import NonrepeatingBuffer
from .util import echo_colorized_error
from .util import echo_colorized_warning

configparser = None
if six.PY2:
    import ConfigParser  # noqa: F401
    if configparser is None:
        configparser = ConfigParser
elif six.PY3:
    import configparser

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

config = None
aprsis = None
port_map = {}
running = True
plugin_modules = []
plugin_threads = []


def sigint_handler(signal=None, frame=None):
    global running
    running = False

    click.echo()
    click.echo('SIGINT caught, shutting down..')

    for plugin_module in plugin_modules:
        plugin_module.stop()
    if aprsis:
        aprsis.close()
    # Lets wait until all the plugins successfully end
    for plugin_thread in plugin_threads:
        plugin_thread.join()
    for port in port_map.values():
        port['tnc'].close()

    click.echo('APEX successfully shutdown.')
    sys.exit(0)


def find_config(config_paths, verbose):
    config_file = 'apex.conf'
    rc_file = '.apexrc'
    cur_path = os.path.join(os.curdir, config_file)
    home_path = os.path.join(os.path.expanduser('~'), rc_file)
    etc_path = os.path.sep + os.path.join('etc', config_file)
    if config_paths is None:
        if os.name == 'posix':
            config_paths = [cur_path, home_path, etc_path]
        else:
            config_paths = [cur_path, home_path]
    elif isinstance(config_paths, str):
        config_paths = [config_paths]
    elif not isinstance(config_paths, list):
        raise TypeError('config_paths argument was neither a string nor a list')

    if verbose:
        click.echo('Searching for configuration file in the following locations: %s' % repr(config_paths))

    config = configparser.ConfigParser()
    for config_path in config_paths:
        try:
            if len(config.read(config_path)) > 0:
                return config
        except IOError:
            pass

    return None


def configure(configfile, verbose=False):
    global config
    config = find_config(configfile, verbose)
    if config is None:
        echo_colorized_error('No apex configuration found, can not continue.')
        return False
    for section in config.sections():
        if section.startswith("TNC "):
            tnc_name = section.strip().split(" ")[1].strip()
            if tnc_name is 'IGATE':
                echo_colorized_error('IGATE was used as the name for a TNC in the configuration, this name is reserved')
                return False
            if config.has_option(section, 'com_port') and config.has_option(section, 'baud'):
                com_port = config.get(section, 'com_port')
                baud = config.get(section, 'baud')
                kiss_tnc = apex.buffers.ReconnectingPacketBuffer(apex.aprs.AprsKiss(apex.kiss.KissSerial(com_port=com_port, baud=baud)))
            elif config.has_option(section, 'tcp_host') and config.has_option(section, 'tcp_port'):
                tcp_host = config.get(section, 'tcp_host')
                tcp_port = config.get(section, 'tcp_port')
                kiss_tnc = apex.buffers.ReconnectingPacketBuffer(apex.aprs.AprsKiss(apex.kiss.KissTcp(host=tcp_host, tcp_port=tcp_port)))
            else:
                echo_colorized_error("""Invalid configuration, must have both com_port and baud set or tcp_host and
                           tcp_port set in TNC sections of configuration file""")
                return False

            if not config.has_option(section, 'kiss_init'):
                echo_colorized_error('Invalid configuration, must have kiss_init set in TNC sections of configuration file')
                return False
            kiss_init_string = config.get(section, 'kiss_init')
            if kiss_init_string == 'MODE_INIT_W8DED':
                kiss_tnc.connect(kissConstants.MODE_INIT_W8DED)
            elif kiss_init_string == 'MODE_INIT_KENWOOD_D710':
                kiss_tnc.connect(kissConstants.MODE_INIT_KENWOOD_D710)
            elif kiss_init_string == 'NONE':
                kiss_tnc.connect()
            else:
                echo_colorized_error('Invalid configuration, value assigned to kiss_init was not recognized: %s'
                                     % kiss_init_string)
                return False

            for port in range(1, 1 + int(config.get(section, 'port_count'))):
                port_name = tnc_name + '-' + str(port)
                port_section = 'PORT ' + port_name
                port_identifier = config.get(port_section, 'identifier')
                port_net = config.get(port_section, 'net')
                tnc_port = int(config.get(port_section, 'tnc_port'))
                port_map[port_name] = {'identifier': port_identifier,
                                       'net': port_net,
                                       'tnc': NonrepeatingBuffer(kiss_tnc, port_name, tnc_port),
                                       'tnc_port': tnc_port}

    global aprsis
    aprsis = None
    if config.has_section('IGATE'):
        aprsis_callsign = config.get('IGATE', 'callsign')
        if config.has_option('IGATE', 'password'):
            aprsis_password = config.get('IGATE', 'password')
        else:
            aprsis_password = -1
        aprsis_server = config.get('IGATE', 'server')
        aprsis_server_port = config.get('IGATE', 'server_port')
        aprsis_base = apex.buffers.ReconnectingPacketBuffer(apex.aprs.IGate(aprsis_callsign, aprsis_password))
        aprsis = NonrepeatingBuffer(aprsis_base, 'IGATE')
        aprsis.connect(aprsis_server, int(aprsis_server_port))

    return True


@click.command(context_settings=dict(auto_envvar_prefix='APEX'))
@click.option('-c',
              '--configfile',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
              help='Configuration file for APEX.')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
def main(verbose, configfile):
    # load the configuration, if it fails, exit
    if not configure(configfile, verbose):
        return

    click.echo("Press ctrl + c at any time to exit")

    # start the plugins
    try:
        plugin_loaders = get_plugins()
        if not len(plugin_loaders):
            echo_colorized_warning('No plugins were able to be discovered, will only display incoming messages.')
        for plugin_loader in plugin_loaders:
            if verbose:
                click.echo('Plugin found at the following location: %s' % repr(plugin_loader))
            loaded_plugin = load_plugin(plugin_loader)
            plugin_modules.append(loaded_plugin)
            new_thread = threading.Thread(target=loaded_plugin.start, args=(config, port_map, aprsis))
            new_thread.start()
            plugin_threads.append(new_thread)
    except IOError:
        echo_colorized_warning('plugin directory not found, will only display incoming messages.')

    signal.signal(signal.SIGINT, sigint_handler)

    # process all incoming frames by sending them to each of the plugins.
    if verbose:
        click.echo('Starting packet processing...')
    while running:
        something_read = False
        for port_name in port_map.keys():
            port = port_map[port_name]
            frame = port['tnc'].read()
            if frame:
                for plugin_module in plugin_modules:
                    something_read = True
                    plugin_module.handle_packet(frame, port, port_name)

        if something_read is False:
            time.sleep(1)
