#!/bin/bash

sudo -H pip3 install --upgrade pip >/dev/null
yes | sudo apt-get autoremove >/dev/null
sudo -H pip3.6 install -r /home/pi/hawkbot/requirements.txt --upgrade >/dev/null
sudo python3.6 /home/pi/hawkbot/Main.py
