#!/bin/bash

for database in InfluxDB PostgreSQL
do
	for size in 1000 10000 100000 1000000 2000000
	do
		echo "database: "$database " size: "$size
		outTemp="avg-time-database-$database-size-$size.dat"

		avgINSERT=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$3; count+=1} END {print sum/count}' \
		../../out_int.txt)

		avgUPDATE=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$4; count+=1} END {print sum/count}' \
		../../out_int.txt)

		avgDELETE=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$5; count+=1} END {print sum/count}' \
		../../out_int.txt)

		echo $avgINSERT $avgUPDATE $avgDELETE > $outTemp
	done
done


for size in 1000 10000 100000 1000000 2000000
do
	allIDB=$(cat avg-time-database-InfluxDB-size-$size.dat)
	allPostgreSQL=$(cat avg-time-database-PostgreSQL-size-$size.dat)

	string=$(echo "$size $allIDB $allPostgreSQL")
	echo $string >> AVG-INT-DB.out

	rm avg-time-database-InfluxDB-size-$size.dat
	rm avg-time-database-PostgreSQL-size-$size.dat
done

printf "%.0e\t%s\t%s\t%s\t%s\t%s\t%s\n" $(cat AVG-INT-DB.out) > AVG-INT-DB.out #format lines
sed -i '1 i\# of Operations IDB-avgINSERT IDB-avgUPDATE IDB-avgDELETE PostgreSQL-avgINSERT PostgreSQL-avgUPDATE PostgreSQL-avgDELETE\' AVG-INT-DB.out
sed -i 's/e+0/E+/' AVG-INT-DB.out