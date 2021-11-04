#!/bin/bash

OUT="geometry.in"           # OUTPUT FILE NAME

TAR_XYZ=$1                      # SET XYZ INPUT FILE

if [ -z $TAR_XYZ ]; then                                        # CHECK IF TAR XYZ IS SET
        printf "%s\n" "Error, input xyz file is not found"
        exit 1
elif [ ! -f $TAR_XYZ ]; then                                    # CHECK IF TAR XYZ FILE EXISTS
        printf "%s\n" "Errof, input xyz file does not exist"
        exit 1
fi

ATOM_CNT=$( sed -n 1p $TAR_XYZ )        # GET ATOM NUMBER

declare -a config

for (( i=0; i<$ATOM_CNT; i++ )); do

        rln=$( echo "$i +3" | bc )
        rl=$( sed -n "$rln"p $TAR_XYZ )
        spl=( $rl )

        for (( j=0; j<4; j++ )); do
                config[$i*4+$j]=${spl[$j]}
        done
done                                    # END READ INPUT XYZ

if [ -f $OUT ]; then
        rm $OUT
fi

# WRT AIMS INPUT FILE
echo "#src_path:"$PWD"/"$TAR_XYZ > $OUT
for (( i=0; i<$ATOM_CNT; i++ )); do
        printf "%4.4s%15.6lf%12.6lf%12.6lf%5.2s\n" "atom" ${config[$i*4+1]} ${config[$i*4+2]} ${config[$i*4+3]} ${config[$i*4+0]} >> $OUT
done
