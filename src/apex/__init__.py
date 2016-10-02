"""
Main module for APEX refernce implementation application.
"""

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .buffers import NonrepeatingBuffer  # noqa: F401
from .buffers import ReconnectingPacketBuffer  # noqa: F401
from .util import echo_colorized_error  # noqa: F401
from .util import echo_colorized_frame  # noqa: F401
from .util import echo_colorized_warning  # noqa: F401

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []
__version__ = '0.0.6'
