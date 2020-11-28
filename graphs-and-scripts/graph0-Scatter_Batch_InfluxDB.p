set encoding iso_8859_1
set terminal postscript eps enhanced color butt "Times-Roman" 36
set output 'graph0-Scatter_Batch_InfluxDB.eps'


set xlabel '# de Linhas' font "Times-Roman,42" 
set ylabel 'Tempo (ms)' font ",42"
set size 1.5, 1.2
#set grid ytics
set style fill pattern border -1
set key left top

set style line 1 lw 2 ps 2 lc rgb "#0000FF" #blue
set style line 2 lw 2 ps 2 lc rgb "#FF0000" #red
set style line 3 lw 2 ps 2 lc rgb "#008000" #green


plot 'SCATTER_BATCH_INFLUXDB.out' using 2:xtic(1) title '100' ls 7 ps 2 lc rgb "#0000FF", \
''								  using 3:xtic(1) title '50' ls 7 ps 2 lc rgb "#FF0000", \
''								  using 4:xtic(1) title '25' ls 7 ps 2 lc rgb "#008000"