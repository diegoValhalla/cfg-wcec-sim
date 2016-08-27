GNUPLOT_DIR=$(dirname $(readlink -f $0))

echo 'Ploting to end time'
cd $GNUPLOT_DIR/end-time
gnuplot plot.p

echo 'Ploting to acc energy'
cd $GNUPLOT_DIR/energy-acc
gnuplot plot.p

echo 'Ploting to partial energy'
cd $GNUPLOT_DIR/energy-partial
gnuplot plot.p

