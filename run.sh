#! /bin/bash

FILES="./study-case-one-function/*.c"

# iterates over C files
for f in $FILES
do
    echo "Running simulation in: $f"

    # remove file extension and append .out
    outfile="${f%.*}.out"
    (time -p python run.py $f) > $outfile 2>&1
done

