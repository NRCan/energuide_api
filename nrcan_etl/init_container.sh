#!/bin/bash
service ssh start
gunicorn --pythonpath=src/energuide --bind=0.0.0.0:5010 --worker-class=gevent flask_app:App
