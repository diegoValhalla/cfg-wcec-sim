#! /bin/bash

if [ -d './study-case-I/results/' ]; then
    rm ./study-case-I/results/*
fi

#(time -p python run.py ./study-case-I/sim.config wfreq 20 ./study-case-I/results)
#(time -p python run.py ./study-case-I/sim.config valentin 20 ./study-case-I/results)
(time -p python run.py ./study-case-I/sim-mine.config mine 20 ./study-case-I/results)
#bash ./study-case-I/gnuplot/run.sh

#(time -p python run.py ./study-case-II-eight-tests/sim.config wfreq 50000)
#(time -p python run.py ./study-case-II-eight-tests/sim.config valentin 50000)
#(time -p python run.py ./study-case-II-eight-tests/sim-mine.config mine 50000)

