#!/bin/bash

dir='/Users/marialinechardelin/current/Zabargad/3_4_deformation/4_analysis'
example=$scripts/creeePY/example

cp -r $example/* $dir

# matlab..... command line ? lancer la macro depuis python !

#python3 treatment.py
#python3 stats.py
#python conversion.py

#python3 plot.py
python3 display.py
#python3 tex.py
