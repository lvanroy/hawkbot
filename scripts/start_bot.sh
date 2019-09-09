#!/bin/bash

sudo -H pip install --upgrade pip
sudo apt install python3-distutils
sudo python3.6 -m pip install -r requirements.txt
sudo python3.6 ../Main.py
