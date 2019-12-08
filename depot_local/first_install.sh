#!/bin/bash
set +x
virtualenv -p python2 env
source ./env/bin/activate
pip install -r requirements.txt
deactivate
