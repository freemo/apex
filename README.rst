========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/apex/badge/?version=latest
    :target: http://apex.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/Syncleus/apex.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Syncleus/apex

.. |requires| image:: https://requires.io/github/Syncleus/apex/requirements.svg?branch=master
     :alt: Requirements Status
     :target: https://requires.io/github/Syncleus/apex/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/github/Syncleus/apex/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/Syncleus/apex?branch=master

.. |codecov| image:: https://codecov.io/github/Syncleus/apex/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Syncleus/apex

.. |landscape| image:: https://landscape.io/github/Syncleus/apex/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Syncleus/apex/master
    :alt: Code Quality Status

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/4d662dc79744416b950273fb57a64d6e
    :target: https://www.codacy.com/app/freemo/apex?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Syncleus/apex&amp;utm_campaign=Badge_Grade
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/Syncleus/apex/badges/gpa.svg
   :target: https://codeclimate.com/github/Syncleus/apex
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/apex-radio.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/apex-radio

.. |downloads| image:: https://img.shields.io/pypi/dm/apex-radio.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/apex-radio

.. |wheel| image:: https://img.shields.io/pypi/wheel/apex-radio.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/apex-radio

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/apex-radio.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/apex-radio

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/apex-radio.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/apex-radio

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/Syncleus/apex/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/Syncleus/apex/


.. end-badges

APEX is a next generation APRS based protocol. This repository represents the reference implementation and is a full features application for digipeating across multiple AX.25 KISS TNC devices using the full APEX stack.

For more information on the project please check out `the project's home page <http://apexprotocol.com/>`_.

Running the app
===============

Right now the setup.py has a few bugs in it. So you can either try to fix it, wait for us to fix it, or simply install
the prerequsites manually. The following is a list of the preequsites that need to be installed.

    pynmea2 >= 1.4.2
    pyserial >= 2.7
    requests >= 2.7.0
    cachetools >= 1.1.5

The application is written for python 3 specifically, it may not work with python 2. Once installed copy the
apex.cfg.example file over to apex.cfg in the same directory, then edit the file and replace it with your details. Next
just run the application with the following command.

    python ./apex.py

There isn't much to the application right now, so thats all you should need to run it. Digipeating will occur
automatically and respond to the WIDEN-n paradigm as well as your own callsign. Cross-band repeating is enabled right
now but only by specifying the call sign directly. The application is still pre-release so more features and
configuration options should be added soon.

This is Free software: Apache License v2

Installation
============

::

    pip install apex

Documentation
=============

https://apex.readthedocs.io/

Development
===========

Initial setup::

    pip install -U pyenv tox
    pyenv install 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1
    pyenv global 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1

NOTE: The specific versions mentioned above may be different for each platform. use `pyenv install --list` to view the
list of available versions. You will need a version of 2.7.x, 3.3.x, 3.4.x, 3.5.x, and pypy. Try to use the latest
available version for each. Also some flavors of pyenv have different formats for it's arguments. So read the pyenv
documentation on your platform.

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

Releasing
---------

* Ensure you have an account on PyPI, if you do not create one `here <https://pypi.python.org/pypi?%3Aaction=register_form>`_.

* Create or verify your `~/.pypirc` file. It should look like this::

    [distutils]
    index-servers =
      pypi
      pypitest

    [pypi]
    repository=https://pypi.python.org/pypi
    username = <username>
    password = <password>

    [pypitest]
    repository=https://testpypi.python.org/pypi
    username = <username>
    password = <password>


* Update CHANGELOG.rst

* Commit the changes::

    git add CHANGELOG.rst
    git commit -m "Changelog for upcoming release 0.1.1."


* Install the package again for local development, but with the new version number::

    python setup.py develop


* Run the tests::

    tox



* Release on PyPI by uploading both sdist and wheel::

    python setup.py sdist upload -r pypi
    python setup.py sdist upload -r pypitest
    python setup.py bdist_wheel --universal upload -r pypi
    python setup.py bdist_wheel --universal upload -r pypitest

  NOTE: Make sure you have Python Wheel installed for your distribution or else the above commands will not work.

* Update version number (can also be minor or major)::

    bumpversion patch


* Commit the version bump changes::

    git add .
    git commit -m "Bumping version for release cycle"


* Test that it pip installs::

    pip install apex-radio
    <try out my_project>


* Push: `git push`

* Push tags: `git push --tags`

* Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy
  and paste the RestructuredText into `ninjs <http://rst.ninjs.org/>`_ to find out what broke the formatting.

* Edit the release on `GitHub <https://github.com/Syncleus/apex/releases>`_ . Paste the release notes into the
  release's release page, and come up with a title for the release.


.. image:: https://badges.gitter.im/Syncleus/APEX.svg
   :alt: Join the chat at https://gitter.im/Syncleus/APEX
   :target: https://gitter.im/Syncleus/APEX?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge