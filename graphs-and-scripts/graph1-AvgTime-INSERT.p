set encoding iso_8859_1
set terminal postscript eps enhanced color butt "Times-Roman" 36
set output 'graph1-AvgDB_avgINSERT.eps'


set style data histogram
set xlabel '# de Linhas' font "Times-Roman,42" 
set ylabel 'Tempo (ms)' font ",42"
set size 1.5, 1.2
set grid ytics
set style histogram cluster gap 1
set style fill pattern border -1
set key left top
set logscale y 10

set style line 10 lw 3 ps 2.5 lc rgb "#000000"
set style line 9 lw 3 ps 2.5 lc rgb "#000000"
set style line 8 lw 3 ps 2.5 lc rgb "#000000"
set style line 7 lw 3 ps 2.5 lc rgb "#000000"
set style line 6 lw 3 ps 2.5 lc rgb "#000000" 
set style line 5 lw 3 ps 2.5 lc rgb "#000000" 
set style line 4 lw 3 ps 2.5 lc rgb "#000000" 
set style line 3 lw 3 ps 2.5 lc rgb "#000000" 
set style line 2 lw 3 ps 2.5 lc rgb "#000000" 
set style line 16 lw 3 ps 2.5 lc rgb "#000000" 

plot 'AVG-DB.out' using 2:xtic(1) title 'InfluxDB' fs pattern 4 lt -1, \
'' using 5:xtic(1) title 'PostgreSQL' fs pattern 2 lt -1