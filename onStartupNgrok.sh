#!/bin/bash

# initialize ngrok server
xterm -e bash /home/kyle/Documents/movieRater/runNgrok.sh

python3 /home/kyle/Documents/movieRater/sendNgrokPortEmail.py

