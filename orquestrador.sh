#!/bin/bash

rm out.txt
echo "Executing from 1k insertions to 2m insertions"

for suppliers in 10 100 1000 10000 20000
do
    for((k = 0; k < 10; k+=1)); do
        echo "Execution $k: Suppliers = $suppliers; Parts = 100"
        python3.7 influxdb_queries.py --suppliers $suppliers --parts 100 >> out.txt
    done
done

for suppliers in 10 100 1000 10000 20000
do
    parts = 100
    for((k = 0; k < 10; k+=1)); do
        python3.7 postgresql_queries.py -s $suppliers -p $parts >> out.txt
    done
done

