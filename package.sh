#!/usr/bin/env bash
echo "Cleaning build environment..."
python setup.py clean --all
echo " "
echo "Creating sdist package..."
python setup.py sdist
echo " "
echo "Creating wheel package..."
python setup.py bdist_wheel