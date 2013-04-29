=======================
Rbit: Email that learns
=======================

This is a machine-learning based email local email client that learns from your
past behaviour.

This is rudimentary, but I am doing it mostly to *scratch an itch*: I want a
decent email client on Linux and did not find one.

This is **pre-alpha** software. It might work.

Dependencies
------------

Just copy and paste the commands below to install all dependencies (you must
have ``pip`` installed, but you already did that, right?)::

    sudo apt-get install python-pyside
    sudo apt-get install python-sqlalchemy
    sudo apt-get install python-gevent

    pip install sqlalchemy
    pip install imapclient
    pip install gevent
    pip install whoosh
    pip install pyzmail
    pip install six


Vowpal wabbit
~~~~~~~~~~~~~

Vowpal wabbit must be installed and callable as ``vw`` for the learning to work.

License
-------

GPLv3.

