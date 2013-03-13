#!/bin/sh
virtualenv --no-site-package venv
. venv/bin/activate
pip install -r requirements
