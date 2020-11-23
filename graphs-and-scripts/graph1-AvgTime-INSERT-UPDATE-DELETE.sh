#!/bin/bash

for database in InfluxDB #PostgreSQL
do
	for size in 1000 10000 100000 1000000 2000000
	do
		echo "database: "$database " size: "$size
		outTemp="avg-time-database-$database-size-$size.dat"

		avgINSERT=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$3; count+=1} END {print sum/count}' \
		../out.txt)

		avgUPDATE=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$4; count+=1} END {print sum/count}' \
		../out.txt)

		avgDELETE=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$5; count+=1} END {print sum/count}' \
		../out.txt)

		echo $avgINSERT $avgUPDATE $avgDELETE > $outTemp
	done
done


#string=$(echo "# of Operations IDB-avgINSERT IDB-avgUPDATE IDB-avgDELETE PostgreSQL-avgINSERT PostgreSQL-avgUPDATE PostgreSQL-avgDELETE")
#echo $string >> AVG-DB.out
for size in 1000 10000 100000 1000000 2000000
do
	allIDB=$(cat avg-time-database-InfluxDB-size-$size.dat)
	#allPostgreSQL=$(cat avg-time-database-PostgreSQL-size-$size.dat)

	string=$(printf "%-50s %-20s %-20s\n" "$size $allIDB $allPostgreSQL")
	echo $string >> AVG-DB.out

	rm avg-time-database-InfluxDB-size-$size.dat
	rm avg-time-database-PostgreSQL-size-$size.dat
done

printf "%.0e\t%s\t%s\t%s\n" $(cat AVG-DB.out) > AVG-DB.out #format lines
#awk -i inplace 'BEGINFILE{print "# of Operations IDB-avgINSERT IDB-avgUPDATE IDB-avgDELETE PostgreSQL-avgINSERT PostgreSQL-avgUPDATE PostgreSQL-avgDELETE"}{print}' AVG-DB.out
sed -i '1 i\# of Operations IDB-avgINSERT IDB-avgUPDATE IDB-avgDELETE PostgreSQL-avgINSERT PostgreSQL-avgUPDATE PostgreSQL-avgDELETE\' AVG-DB.out
#sed -i 's/,/./' AVG-DB.out #replace "," for ".", because printf "%e" uses current locale pt_BR.UTF-8
sed -i 's/e+/E/' AVG-DB.out 


