# refer: http://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# refer: http://www.gnuplotting.org/tag/linespoints/
# refer: http://gnuplot.sourceforge.net/docs_4.2/node184.html
clear
reset

set term epslatex font ",10" color colortext

# input file settings
set datafile separator ","

# x-axes settings
set xlabel 'Tempo de Simulação ($10^3$ s)'
set xrange [0:550000]
set xtics 0,50000 nomirror autojustify
set format x "%.0s"

# y-axes common settings
set ylabel 'Energia Consumida ($10^6$ J)'

# since y-values are big
divide(i) = (i / 1000000)

# legend position
set key left

# set line 2 style to dark green
set style line 1 lc rgb 'red' linetype 1 linewidth 1
set style line 2 lc rgb '#09ad00' linetype 1 linewidth 1
set style line 3 lc rgb 'blue' linetype 1 linewidth 1

# ==== WORST CASE ====

set yrange [50:1250]
set ytics 100,150 nomirror autojustify

set output "images/s2-energy-acc-worst.tex"
plot '../../results/consumption-worst-wfreq.csv'\
        using 1:(divide($3)) with lines ls 1 ti 'Pior Caso',\
    '../../results/consumption-worst-v.csv'\
        using 1:(divide($3)) with lines ls 2 ti 'Valentin',\
    '../../results/consumption-worst-m.csv'\
        using 1:(divide($3)) with lines ls 3 ti 'Proposta'


# ==== MIDDLE CASE ====

set yrange [0:700]
set ytics 50,100 nomirror autojustify

set output "images/s2-energy-acc-mid.tex"
plot '../../results/consumption-mid-wfreq.csv'\
        using 1:(divide($3)) with lines ls 1 ti 'Pior Caso',\
    '../../results/consumption-mid-v.csv'\
        using 1:(divide($3)) with lines ls 2 ti 'Valentin',\
    '../../results/consumption-mid-m.csv'\
        using 1:(divide($3)) with lines ls 3 ti 'Proposta'


# ==== APPROX BEST CASE ====

set yrange [0:185]
set ytics 10,20 nomirror autojustify

set output "images/s2-energy-acc-approx.tex"
plot '../../results/consumption-approx-wfreq.csv'\
        using 1:(divide($3)) with lines ls 1 ti 'Pior Caso',\
    '../../results/consumption-approx-v.csv'\
        using 1:(divide($3)) with lines ls 2 ti 'Valentin',\
    '../../results/consumption-approx-m.csv'\
        using 1:(divide($3)) with lines ls 3 ti 'Proposta'
