#!/bin/bash

sudo -H pip install --upgrade pip >/dev/null
sudo apt-get install python3-distutils >/dev/null
sudo apt-get install libpq-dev >/dev/null
yes | sudo apt-get autoremove >/dev/null
sudo -H pip3.6 install -r requirements.txt >/dev/null
sudo python3.6 ../Main.py
