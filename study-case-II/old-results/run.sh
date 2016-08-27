echo 'Ploting to end time'
cd ./end-time
gnuplot plot.p

echo 'Ploting to acc energy'
cd ../energy-acc
gnuplot plot.p

echo 'Ploting to partial energy'
cd ../energy-partial
gnuplot plot.p
