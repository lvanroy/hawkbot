#!/bin/bash

sudo -H pip install --upgrade pip >/dev/null
yes | sudo apt-get autoremove >/dev/null
sudo -H pip3.6 install -r requirements.txt >/dev/null
sudo python3.6 ../Main.py
