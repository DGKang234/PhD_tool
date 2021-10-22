#!/bin/bash

OUT="aims.xyz"          # AIMS OUTPUT RES IN XYZ FORMAT
STRIDE="5"              # STRIDE AIMS OUTPUT ... "geometry.in.next"
TAR=$1                  # TARGET AIMS OUTPUT ... USUALLY "geometry.in.next"

if [ -z $TAR ]; then
        printf "%s\n" "Error, 1st input argument (target aims output file) is empty ..."
        exit 1
#elif [ -f $TAR ]; then
#       printf "%s\n" "Error, target aims output file does not exist ..."
#       exit 1
fi

grep "atom" $TAR > tmp
ATOM_CNT=$( wc -l tmp  | awk '{print $1}' )

declare -a config

echo $ATOM_CNT > $OUT
echo "#src_path:"$PWD"/"$TAR >> $OUT

for (( i=0; i<$ATOM_CNT; i++ )); do

        rln=$( echo "$i +1 " | bc )
        rl=$( sed -n "$rln"p tmp )
        spl=( $rl )

        for (( j=0; j<5; j++ )); do
                config[$i*5+$j]=${spl[$j]}
        done

        printf "%3.2s%12.6lf%12.6lf%12.6lf\n" ${config[$i*$STRIDE+4]} ${config[$i*$STRIDE+1]} ${config[$i*$STRIDE+2]} ${config[$i*$STRIDE+3]} >> $OUT
done

rm tmp
