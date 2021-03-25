#!/bin/bash

sudo -H pip3 install --upgrade pip >/dev/null
yes | sudo apt-get autoremove >/dev/null
sudo -H pip3 install -r /mnt/c/Users/larsv/Documents/GitHub/hawkbot/requirements.txt --upgrade >/dev/null
sudo python3 /mnt/c/Users/larsv/Documents/GitHub/hawkbot/Main.py
