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

# fit chart
#set size square

# set line 1 to blue
set style line 1 lc rgb 'blue' linetype 1 linewidth 1 pt 3


# ==== WORST CASE ====

set yrange [50:1250]
set ytics 100,150 nomirror autojustify

set output "./images/s2-partial-worst-wfreq.tex"
plot './../data/consumption-worst-wfreq.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s2-partial-worst-m.tex"
plot './../data/consumption-worst-m.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s2-partial-worst-v.tex"
plot './../data/consumption-worst-v.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''


# ==== MIDDLE CASE ====

set yrange [0:700]
set ytics 50,100 nomirror autojustify

set output "./images/s2-partial-mid-wfreq.tex"
plot './../data/consumption-mid-wfreq.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s2-partial-mid-m.tex"
plot './../data/consumption-mid-m.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s2-partial-mid-v.tex"
plot './../data/consumption-mid-v.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''


# ==== APPROX BEST CASE ====

set yrange [0:185]
set ytics 10,20 nomirror autojustify

set output "./images/s2-partial-approx-wfreq.tex"
plot './../data/consumption-approx-wfreq.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s2-partial-approx-m.tex"
plot './../data/consumption-approx-m.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s2-partial-approx-v.tex"
plot './../data/consumption-approx-v.csv'\
    using 1:(divide($2)) with boxes ti 'Consumo por Intervalo',\
    '' using 1:(divide($3)) with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:(divide($3)):(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:(divide($3)) w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''
