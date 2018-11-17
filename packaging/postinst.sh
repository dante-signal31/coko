#!/usr/bin/env bash

 # Link geolocate executable from /usr/bin.
ln -s /opt/coko/bin/coko /usr/bin/coko

# Copy man page to /usr/share/man/man1
cp /opt/coko/lib/python3.7/site-packages/coko-1.0.9-py3.7.egg/share/man/man1/coko.1 /usr/share/man/man1/.
