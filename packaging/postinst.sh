#!/usr/bin/env bash

# Link geolocate executable from /usr/bin.
ln -s /opt/coko/bin/coko /usr/bin/coko

# Link man page from /usr/share/man/man1
ln -s /opt/coko/lib/python3.7/site-packages/coko-1.0.5-py3.7.egg/share/man/man1/coko.1 /usr/share/man/man1/coko.1
