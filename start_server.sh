#!/bin/sh
ARG1=$1
PORT=${ARG1:="9099"}
./venv/bin/uwsgi --http :${PORT} --virtualenv venv --wsgi-file lxcrest.py --callable app
