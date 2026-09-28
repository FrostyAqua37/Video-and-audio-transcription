#!/bin/bash

#Activate .venv and install any dependencies
source .venv/bin/activate
pip install --upgrade pip \
    && -r requirements.txt

#Launching interactive mode after dependency downloads.
/bin/bash "$@"