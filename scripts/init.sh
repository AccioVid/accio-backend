#!/bin/bash
if [ ! -d "venv" ]; then
    echo "creating virtual environement..."
    virtualenv venv
fi
source venv/bin/activate
source .env