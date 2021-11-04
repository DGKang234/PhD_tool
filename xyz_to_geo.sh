#!/usr/bin/bash

INPUT=$1

n="1"
numb=$(sed -n "$n"p $1)
#echo $numb
dummy="NULL"

for((i=0; i<"$numb"; i++)); do
	n=$(echo "$i+3" | bc -l)
	dummy=$(sed -n "$n"p $1)
	echo $dummy >> tmp.in
done

while read a b c d
do
   echo "atom" $b $c $d $a >> geometry.in
done < tmp.in

rm tmp.in
