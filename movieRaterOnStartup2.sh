#!/bin/bash

# initialize ngrok server
xterm -hold -e bash /home/kyle/Documents/movieRater/runNgrok.sh

python /home/kyle/Documents/movieRater/sendNgrokPortEmail.py