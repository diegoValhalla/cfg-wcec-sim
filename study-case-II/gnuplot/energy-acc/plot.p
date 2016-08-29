# refer: http://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# refer: http://www.gnuplotting.org/tag/linespoints/
# refer: http://gnuplot.sourceforge.net/docs_4.2/node184.html
clear
reset

set term epslatex font ",10" color colortext
#set term png

# input file settings
set datafile separator ","

# x-axes settings
set xlabel "Simulation time ($10^3$s)"
set xrange [0:9900]
set xtics 0,1980 nomirror autojustify
#set format x "%.0s"

# y-axes common settings
set ylabel 'Normalized energy consumption'
#set yrange [0:1.0.5]
set ytics 0,0.1 nomirror autojustify

# common function
normalization(i) = ((i - range_min) / (range_max - range_min))
divide(i) = (i / 1000)

# legend position
set key left

# set line 2 style to dark green
set style line 1 lc rgb 'red' linetype 1 linewidth 1
set style line 2 lc rgb '#09ad00' linetype 1 linewidth 1
set style line 3 lc rgb 'blue' linetype 1 linewidth 1

# ==== WORST CASE ====

stats '../../results/consumption-worst-wfreq.csv' using 3 name "range" nooutput
set yrange [0:1.05]
#set output "images/s2-energy-acc-worst.png"
set output "images/s2-energy-acc-worst.tex"
plot '../../results/consumption-worst-wfreq.csv'\
        using (divide($1)):(normalization($3)) with lines ls 1 ti 'Worst Case',\
    '../../results/consumption-worst-v.csv'\
        using (divide($1)):(normalization($3)) with lines ls 2 ti 'Valentin',\
    '../../results/consumption-worst-m.csv'\
        using (divide($1)):(normalization($3)) with lines ls 3 ti 'Proposal'
# due to 'stats' command, yrange must be reinitialize after each plot
set yrange [*:*]


# ==== MIDDLE CASE ====

stats '../../results/consumption-mid-wfreq.csv' using 3 name "range" nooutput
set yrange [0:1.05]
set output "images/s2-energy-acc-mid.tex"
plot '../../results/consumption-mid-wfreq.csv'\
        using (divide($1)):(normalization($3)) with lines ls 1 ti 'Worst Case',\
    '../../results/consumption-mid-v.csv'\
        using (divide($1)):(normalization($3)) with lines ls 2 ti 'Valentin',\
    '../../results/consumption-mid-m.csv'\
        using (divide($1)):(normalization($3)) with lines ls 3 ti 'Proposal'
# due to 'stats' command, yrange must be reinitialize after each plot
set yrange [*:*]


# ==== APPROX BEST CASE ====

stats '../../results/consumption-approx-wfreq.csv' using 3 name "range" nooutput
set yrange [0:1.05]
set output "images/s2-energy-acc-approx.tex"
plot '../../results/consumption-approx-wfreq.csv'\
        using (divide($1)):(normalization($3)) with lines ls 1 ti 'Worst Case',\
    '../../results/consumption-approx-v.csv'\
        using (divide($1)):(normalization($3)) with lines ls 2 ti 'Valentin',\
    '../../results/consumption-approx-m.csv'\
        using (divide($1)):(normalization($3)) with lines ls 3 ti 'Proposal'

