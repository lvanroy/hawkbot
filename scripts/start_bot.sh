#!/bin/bash

sudo -H pip install --upgrade pip
sudo apt install python3-distutils
sudo apt-get install libpq-dev
sudo apt autoremove
sudo -H pip3.6 install -r requirements.txt
sudo python3.6 ../Main.py
