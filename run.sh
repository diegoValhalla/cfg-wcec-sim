#! /bin/bash

if [ -d './study-case-I/results/' ]; then
    rm './study-case-I/results/*'
fi

# old results
#(time -p python run.py ./study-case-I/old-results/sim.config wfreq 20 ./study-case-I/results)
#(time -p python run.py ./study-case-I/old-results/sim.config valentin 20 ./study-case-I/results)
#(time -p python run.py ./study-case-I/old-results/sim-mine.config mine 20 ./study-case-I/results)
#bash ./study-case-I/gnuplot/run.sh

if [ -d './study-case-II/results/' ]; then
    rm './study-case-II/results/*'
fi

# old results
#(time -p python run.py ./study-case-II/old-results/sim.config wfreq 50000 ./study-case-II/results)
#(time -p python run.py ./study-case-II/old-results/sim.config valentin 50000 ./study-case-II/results)
#(time -p python run.py ./study-case-II/old-results/sim-mine.config mine 50000 ./study-case-II/results)
#bash ./study-case-II/gnuplot/run.sh

#(time -p python run.py ./study-case-II/sim.config wfreq 50000 ./study-case-II/results)
#(time -p python run.py ./study-case-II/sim.config valentin 50000 ./study-case-II/results)
(time -p python run.py ./study-case-II/sim-mine.config mine 50000 ./study-case-II/results)
#bash ./study-case-II/gnuplot/run.sh

