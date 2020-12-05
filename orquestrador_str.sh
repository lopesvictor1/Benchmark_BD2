#!/bin/bash

#rm out_string.txt
echo "Executing from 1k insertions to 2m insertions"

for suppliers in 10 100 1000 10000 20000
do
    for((k = 0; k < 30; k+=1)); do
        echo "InfluxDB Execution $k: Suppliers = $suppliers; Parts = 100"
        python3.7 influxdb_queries_string.py --suppliers $suppliers --parts 100 >> out_str.txt
    done
done

for suppliers in 10 100 1000 10000 20000
do
    for((k = 0; k < 30; k+=1)); do
	echo "PostgreSQL Execution $k: Suppliers = $suppliers; Parts = 100"
        python3.7 postgresql_queries_string.py --suppliers $suppliers --parts 100 >> out_str.txt
    done
done

