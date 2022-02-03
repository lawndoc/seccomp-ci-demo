#!/bin/bash

# start api server
gunicorn -b 0.0.0.0:5000 -w 4 -k gevent --worker-tmp-dir /dev/shm server:app &

# run tests
pytest