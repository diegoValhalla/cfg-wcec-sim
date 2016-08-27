# refer: http://alvinalexander.com/technology/gnuplot-charts-graphs-examples
# refer: http://www.gnuplotting.org/tag/linespoints/
# refer: http://gnuplot.sourceforge.net/docs_4.2/node184.html
clear
reset

# Remove legend
unset key

set boxwidth 0.4
set style fill solid

# standalone mode when images will not be included in any latex file
#set term epslatex font ",10" color colortext standalone
set term epslatex font ",10" color colortext

# x-axes settings
set xtics nomirror autojustify

# y-axes settings
set ytics nomirror autojustify
set ylabel 'Tempo de Término (s)'

# compute color
computeColor(x) = (x*11244898) + 2851770
mycolor(x) = ((x == 0) ? computeColor(1) : (x == 1) ? computeColor(2) :\
        computeColor(0))

# input file settings
set datafile separator ","


# ==== WORST CASE ====

set yrange [503500:504000] noreverse nowriteback
set ytics 503500,50
set output "images/s2-end-time-worst.tex"
plot\
    '../data/end-time-worst.csv' using 1:3:(mycolor($0)):xtic(2) with boxes\
        lc rgb variable,\
    '' using 1:($3 + 21.5):3 with labels


# ==== MIDDLE CASE ====

set yrange [503700:503750] noreverse nowriteback
set ytics 503700,5
set output "images/s2-end-time-mid.tex"
plot\
    '../data/end-time-mid.csv' using 1:3:(mycolor($0)):xtic(2) with boxes\
        lc rgb variable,\
    '' using 1:($3 + 2.15):3 with labels


# ==== APPROX BEST CASE ====

set ytics 503700,1
set yrange [503700:503710] noreverse nowriteback
set output "images/s2-end-time-approx.tex"
plot\
    '../data/end-time-approx.csv' using 1:3:(mycolor($0)):xtic(2) with boxes\
        lc rgb variable,\
    '' using 1:($3 + 0.5):3 with labels

