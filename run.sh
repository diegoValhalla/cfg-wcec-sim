#! /bin/bash

if [ -d './data/' ]; then
    rm data/*
fi

#(time -p python run.py ./study-case-I-three-tests/sim.config wfreq 20)
#(time -p python run.py ./study-case-I-three-tests/sim.config valentin 20)
python run.py ./study-case-I-three-tests/sim-mine.config mine 20

#(time -p python run.py ./study-case-II-eight-tests/sim.config wfreq 50000)
#(time -p python run.py ./study-case-II-eight-tests/sim.config valentin 50000)
#(time -p python run.py ./study-case-II-eight-tests/sim-mine.config mine 50000)

