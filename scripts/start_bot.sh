#!/bin/bash

sudo -H pip3 install --upgrade pip >/dev/null
yes | sudo apt-get autoremove >/dev/null
sudo -H pip3 install -r requirements.txt --upgrade >/dev/null
sudo python3 Main.py
