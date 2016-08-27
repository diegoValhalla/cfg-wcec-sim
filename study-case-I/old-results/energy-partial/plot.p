# refer: http://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# refer: http://www.gnuplotting.org/tag/linespoints/
# refer: http://gnuplot.sourceforge.net/docs_4.2/node184.html
clear
reset

set term epslatex font ",10" color colortext
#set term pngcairo font ",10" color

# x-axes settings
set xlabel 'Tempo de Simulação (s)'
set xrange [0:140]
set xtics nomirror autojustify

# y-axes settings
set ylabel 'Energia Consumida (J)'
set ytics nomirror

# keys position
set key left

# input file settings
set datafile separator ","

set style line 1 lc rgb 'blue' linetype 1 linewidth 1 pt 3

# ==== WORST CASE ====

set yrange [500:355000]
set ytics 25000,50000 nomirror autojustify

set output "./images/s1-partial-worst-wfreq.tex"
plot './../data/consumption-worst-wfreq.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s1-partial-worst-v.tex"
plot './../data/consumption-worst-v.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s1-partial-worst-m.tex"
plot './../data/consumption-worst-m.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''


# ==== MIDDLE CASE ====

set yrange [500:180000]
set ytics 10000,20000 nomirror autojustify

set output "./images/s1-partial-mid-wfreq.tex"
plot './../data/consumption-mid-wfreq.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s1-partial-mid-v.tex"
plot './../data/consumption-mid-v.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s1-partial-mid-m.tex"
plot './../data/consumption-mid-m.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''


# ==== APPROX BEST CASE ====

set yrange [500:50000]
set ytics 5000,5000 nomirror autojustify

set output "./images/s1-partial-approx-wfreq.tex"
plot './../data/consumption-approx-wfreq.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s1-partial-approx-v.tex"
plot './../data/consumption-approx-v.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''

set output "./images/s1-partial-approx-m.tex"
plot './../data/consumption-approx-m.csv'\
    using 1:2 with boxes ti 'Consumo por Intervalo',\
    '' using 1:3 with linespoints ti 'Energia Acumulada' ls 1,\
    '' using 1:3:(0):1 w xerror ps 0 lt 0 lw 0.8 lc rgb "#C0C0C0" ti '',\
    '' using 1:3 w i lt 0 lw 0.8 lc rgb "#C0C0C0" ti ''
