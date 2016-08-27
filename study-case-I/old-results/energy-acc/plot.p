# refer: http://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# refer: http://www.gnuplotting.org/tag/linespoints/
# refer: http://gnuplot.sourceforge.net/docs_4.2/node184.html
clear
reset

set term epslatex font ",10" color colortext

# x-axes settings
set xtics nomirror autojustify
set xrange [0:140]
set xlabel 'Tempo de Simulação (s)'

# y-axes settings
set ytics nomirror autojustify
set yrange [1000:350000]
set ylabel 'Energia Consumida (J)'

# keys position
set key left

# input file settings
set datafile separator ","

# set line 2 style to dark green
set style line 1 lc rgb 'red' linetype 1 linewidth 1
set style line 2 lc rgb '#09ad00' linetype 1 linewidth 1
set style line 3 lc rgb 'blue' linetype 1 linewidth 1

# ==== WORST CASE ====

set output "images/s1-energy-acc-worst.tex"
plot '../data/consumption-worst-wfreq.csv'\
        using 1:3 with lines ls 1 ti 'Pior Caso',\
    '../data/consumption-worst-v.csv'\
        using 1:3 with lines ls 2 ti 'Valentin',\
    '../data/consumption-worst-m.csv'\
        using 1:3 with lines ls 3 ti 'Proposta'


# ==== MIDDLE CASE ====

set auto y
set output "images/s1-energy-acc-mid.tex"
plot '../data/consumption-mid-wfreq.csv'\
        using 1:3 with lines ls 1 ti 'Pior Caso',\
    '../data/consumption-mid-v.csv'\
        using 1:3 with lines ls 2 ti 'Valentin',\
    '../data/consumption-mid-m.csv'\
        using 1:3 with lines ls 3 ti 'Proposta'


# ==== APPROX BEST CASE ====

set output "images/s1-energy-acc-approx.tex"
plot '../data/consumption-approx-wfreq.csv'\
        using 1:3 with lines ls 1 ti 'Pior Caso',\
    '../data/consumption-approx-v.csv'\
        using 1:3 with lines ls 2 ti 'Valentin',\
    '../data/consumption-approx-m.csv'\
        using 1:3 with lines ls 3 ti 'Proposta'
