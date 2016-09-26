#!/bin/bash

sudo apt-get --assume-yes --force-yes install python3-serial git
cd $HOME
git clone https://www.github.com/davidlandry93/choir
cd $HOME/choir
git pull
