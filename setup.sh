#!/bin/bash
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install --upgrade pip
pip3 install --upgrade virtualenv
virtualenv -p python3 venv
find . -name "*.sh" -execdir chmod u+x {} +
source venv/bin/activate && pip3 install -r requirements.txt
