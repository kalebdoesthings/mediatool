#!/usr/bin/env bash

set -e

if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
fi

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Done."
